"""Main entry point for the gitunify package."""

from __future__ import annotations

if __name__ == "__main__":
    from gitunify.utils.log import setup_logger

    setup_logger(print_version=True)
