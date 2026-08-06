"""Pytest plugin: record every warning to JSONL for the dep-watcher.

The suite normally runs with ``-p no:warnings`` (see pytest.ini), which
discards every warning — including ``RemovedInDjangoXXWarning`` and other
deprecation signals we want to act on during the deprecation window. This
plugin is loaded only in the dedicated *inventory* run (see
``.github/workflows/dep-warnings.yml``), where ``-p no:warnings`` is dropped
via an ``-o addopts=...`` override and warnings are set to ``default::`` so
they record without failing.

Lives in ``tests/plugins/`` (a tracked location) rather than
``internal_tools/`` (which is gitignored / dev-only) so a fresh Gitea checkout
contains it and CI can load it with ``-p warn_collector``. It matches none of
pytest's ``python_files`` patterns, so a normal run never collects it.

Each recorded warning becomes one JSONL line:
``{category, filename, lineno, message, when, nodeid}`` — exactly the shape
the refinery classifier (``service/dep_warnings.py``) consumes.

One file per xdist worker (keyed on ``PYTEST_XDIST_WORKER``, default
``warns_main.jsonl``) so parallel workers never interleave appends; a
``threading.Lock`` guards the append within a worker. The refinery globs
``warns_*.jsonl`` and de-dupes.

Output directory is overridable via ``WARN_COLLECTOR_DIR`` (default: cwd).
"""

import json
import os
import threading

_OUT_DIR = os.environ.get("WARN_COLLECTOR_DIR") or os.getcwd()
_WORKER = os.environ.get("PYTEST_XDIST_WORKER", "main")
_PATH = os.path.join(_OUT_DIR, f"warns_{_WORKER}.jsonl")
_LOCK = threading.Lock()


def pytest_warning_recorded(warning_message, when, nodeid, location):
    """Append one JSONL record per warning pytest surfaces."""
    try:
        category = warning_message.category.__name__
    except Exception:
        category = str(getattr(warning_message, "category", "Unknown"))
    record = {
        "category": category,
        "filename": warning_message.filename,
        "lineno": warning_message.lineno,
        "message": str(warning_message.message)[:400],
        "when": when,  # "config" | "collect" | "runtest"
        "nodeid": (nodeid or "")[:200],
    }
    line = json.dumps(record) + "\n"
    with _LOCK, open(_PATH, "a") as fh:
        fh.write(line)
