#!/usr/bin/env python
"""CLI tool to get economically growing areas by state.

Usage:
    python get_growth_areas.py <STATE_CODE>
    python get_growth_areas.py --list

Examples:
    python get_growth_areas.py VA
    python get_growth_areas.py TX
    python get_growth_areas.py --list
"""

import sys
from pathlib import Path

# Add vrm_crawl to path
sys.path.insert(0, str(Path(__file__).parent))

from vrm_crawl.growth_areas import format_growth_areas, get_all_supported_states  # noqa: E402


def main():
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        print("Usage: python get_growth_areas.py <STATE_CODE>")
        print("       python get_growth_areas.py --list")
        print("\nExamples:")
        print("  python get_growth_areas.py VA")
        print("  python get_growth_areas.py TX")
        sys.exit(1)

    arg = sys.argv[1]

    if arg in ("--list", "-l"):
        states = get_all_supported_states()
        print("\nSupported states with growth area data:")
        print(", ".join(states))
        print("\nUse: python get_growth_areas.py <STATE_CODE> to see growth areas")
        return

    state = arg.upper()
    output = format_growth_areas(state)
    print(output)


if __name__ == "__main__":
    main()
