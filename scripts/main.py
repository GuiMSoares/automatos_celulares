"""Main entry point for the WireWorld cellular automaton application."""

import sys
from app import WireWorldApp


def main():
    """Main entry point."""
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    app = WireWorldApp(initial_file)
    app.run()


if __name__ == '__main__':
    main()
