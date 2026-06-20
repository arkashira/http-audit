import argparse
import json
from dataclasses import dataclass

@dataclass
class Config:
    process_filter: str
    alert_sinks: list

def load_config(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Config(data['process_filter'], data['alert_sinks'])

def run_profiler(config):
    # Simulate profiler run
    print(f"Running profiler with process filter: {config.process_filter}")
    print(f"Alert sinks: {config.alert_sinks}")

def main():
    parser = argparse.ArgumentParser(description='HTTP Audit Profiler')
    parser.add_argument('--config', help='Path to config file')
    args = parser.parse_args()
    config = load_config(args.config)
    run_profiler(config)

if __name__ == '__main__':
    main()
