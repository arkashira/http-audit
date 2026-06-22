# http-audit

A lightweight kernel‑level HTTP interaction collector that filters events by
process name or PID.  It supports dynamic filter changes via `SIGHUP`.

## Features

- CLI flags `--processes` and `--pids` accept comma‑separated values.
- Only events matching the filters are logged.
- Filters can be reloaded at runtime by sending `SIGHUP` to the process.
- Minimal dependency footprint – only the Python standard library.

## Usage
