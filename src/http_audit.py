#!/usr/bin/env python3
"""
Simple kernel-level HTTP interaction collector with process/PID filtering.
"""

import argparse
import json
import os
import signal
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict, Any


@dataclass
class Config:
    processes: Set[str] = field(default_factory=set)
    pids: Set[int] = field(default_factory=set)
    log_file: str = "http_audit.log"


class EventFilter:
    """Filter events based on process names or PIDs."""

    def __init__(self, config: Config):
        self.config = config

    def matches(self, event: Dict[str, Any]) -> bool:
        """
        Return True if the event matches the current filter criteria.
        Event must contain 'process_name' and 'pid'.
        """
        pname = event.get("process_name")
        pid = event.get("pid")
        if pname is None or pid is None:
            return False
        if self.config.processes and pname not in self.config.processes:
            return False
        if self.config.pids and pid not in self.config.pids:
            return False
        return True


class Logger:
    """Simple logger that writes JSON lines to a file."""

    def __init__(self, path: str):
        self.path = path
        # Ensure directory exists
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def log(self, event: Dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")


class Collector:
    """Collects events, applies filters, and logs them."""

    def __init__(self, config: Config):
        self.config = config
        self.filter = EventFilter(config)
        self.logger = Logger(config.log_file)

    def process_event(self, event: Dict[str, Any]) -> None:
        if self.filter.matches(event):
            self.logger.log(event)

    def reload_config(self, signum, frame) -> None:
        """Signal handler to reload filters from command line args."""
        # In a real daemon we would re-read args or a config file.
        # For this demo, we simply toggle a flag to indicate reload.
        self.config.processes = set()
        self.config.pids = set()


def parse_args(argv: Optional[List[str]] = None) -> Config:
    parser = argparse.ArgumentParser(description="Kernel-Level HTTP Interaction Collector")
    parser.add_argument(
        "--processes",
        type=str,
        default="",
        help="Comma-separated list of binary names to filter",
    )
    parser.add_argument(
        "--pids",
        type=str,
        default="",
        help="Comma-separated list of PIDs to filter",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="http_audit.log",
        help="Path to the log file",
    )
    args = parser.parse_args(argv)

    processes = {p.strip() for p in args.processes.split(",") if p.strip()}
    pids = {int(p.strip()) for p in args.pids.split(",") if p.strip()}
    return Config(processes=processes, pids=pids, log_file=args.log_file)


def main(argv: Optional[List[str]] = None) -> None:
    config = parse_args(argv)
    collector = Collector(config)

    # Register SIGHUP to reload config
    signal.signal(signal.SIGHUP, collector.reload_config)

    # In a real implementation, this would hook into kernel events.
    # Here we just read JSON lines from stdin for demonstration.
    for line in sys.stdin:
        try:
            event = json.loads(line)
            collector.process_event(event)
        except json.JSONDecodeError:
            continue


if __name__ == "__main__":
    main()
