import pytest
import json
from http_audit import load_config, run_profiler, Config

def test_load_config():
    config_file = 'example_config.json'
    with open(config_file, 'w') as f:
        json.dump({'process_filter': 'test_filter', 'alert_sinks': ['sink1', 'sink2']}, f)
    config = load_config(config_file)
    assert config.process_filter == 'test_filter'
    assert config.alert_sinks == ['sink1', 'sink2']

def test_run_profiler():
    config = Config('test_filter', ['sink1', 'sink2'])
    run_profiler(config)

def test_load_config_invalid_file():
    with pytest.raises(FileNotFoundError):
        load_config('non_existent_file.json')

def test_load_config_invalid_json():
    config_file = 'example_config.json'
    with open(config_file, 'w') as f:
        f.write('Invalid JSON')
    with pytest.raises(json.JSONDecodeError):
        load_config(config_file)
