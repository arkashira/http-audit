import os
import json
import signal
import tempfile
import pytest

from http_audit import Config, EventFilter, Logger, Collector, parse_args


def test_event_filter_matches_process_and_pid():
    cfg = Config(processes={"nginx"}, pids={1234})
    filt = EventFilter(cfg)
    event = {"process_name": "nginx", "pid": 1234, "data": "test"}
    assert filt.matches(event) is True


def test_event_filter_excludes_unmatched_process():
    cfg = Config(processes={"nginx"}, pids={1234})
    filt = EventFilter(cfg)
    event = {"process_name": "apache", "pid": 1234, "data": "test"}
    assert filt.matches(event) is False


def test_event_filter_excludes_unmatched_pid():
    cfg = Config(processes={"nginx"}, pids={1234})
    filt = EventFilter(cfg)
    event = {"process_name": "nginx", "pid": 5678, "data": "test"}
    assert filt.matches(event) is False


def test_event_filter_no_filters_passes_all():
    cfg = Config()
    filt = EventFilter(cfg)
    event = {"process_name": "any", "pid": 9999}
    assert filt.matches(event) is True


def test_logger_writes_json_line(tmp_path):
    log_path = tmp_path / "log.jsonl"
    logger = Logger(str(log_path))
    event = {"foo": "bar"}
    logger.log(event)
    with open(log_path, "r", encoding="utf-8") as f:
        line = f.readline()
    assert json.loads(line) == event


def test_collector_logs_only_matching_events(tmp_path):
    log_path = str(tmp_path / "log.jsonl")
    cfg = Config(processes={"nginx"}, pids={1234}, log_file=log_path)
    collector = Collector(cfg)

    events = [
        {"process_name": "nginx", "pid": 1234, "msg": "ok"},
        {"process_name": "apache", "pid": 1234, "msg": "bad"},
        {"process_name": "nginx", "pid": 5678, "msg": "bad"},
    ]

    for e in events:
        collector.process_event(e)

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    logged_event = json.loads(lines[0])
    assert logged_event["msg"] == "ok"


def test_parse_args_defaults():
    cfg = parse_args([])
    assert cfg.processes == set()
    assert cfg.pids == set()
    assert cfg.log_file == "http_audit.log"


def test_parse_args_with_values():
    cfg = parse_args(["--processes", "nginx,apache", "--pids", "1234,5678", "--log-file", "out.log"])
    assert cfg.processes == {"nginx", "apache"}
    assert cfg.pids == {1234, 5678}
    assert cfg.log_file == "out.log"


def test_signal_reload_config(tmp_path):
    log_path = str(tmp_path / "log.jsonl")
    cfg = Config(processes={"nginx"}, pids={1234}, log_file=log_path)
    collector = Collector(cfg)

    # Simulate SIGHUP
    collector.reload_config(signal.SIGHUP, None)

    # After reload, filters should be empty
    assert collector.filter.config.processes == set()
    assert collector.filter.config.pids == set()

    # Now any event should be logged
    event = {"process_name": "any", "pid": 9999, "msg": "hello"}
    collector.process_event(event)

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    logged_event = json.loads(lines[0])
    assert logged_event["msg"] == "hello"
