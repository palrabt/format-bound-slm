#!/usr/bin/env python3
"""Player server entry point. Delegates to player.server.

Usage:
    python3 player.py <config.json> [--log-level err|info|debug]
"""
import argparse
from game.player.server import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bohnanza player server")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["err", "info", "debug"],
        help="logging verbosity: err, info (default), debug",
    )
    args = parser.parse_args()
    run(args.config, log_level=args.log_level)
