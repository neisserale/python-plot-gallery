"""Command-line entry point: `uv run gallery <command>`."""

import argparse
import sys
from collections.abc import Sequence

from plot_gallery import __version__

# (name, help, accepts plot ids) for every subcommand defined in docs/specs/02 §5.1
COMMANDS = [
    ('new', 'scaffold a new plot folder from the templates', False),
    ('sync', 'pin dependencies in plot.py and sync the notebook data/final cells', True),
    ('render', 'run plot.py in a sandbox and save the images', True),
    ('execute', 'run the notebook in a sandbox and store its outputs', True),
    ('build', 'validate everything and compile the catalog, schemas and bundles', False),
    ('update', 'sync, render, execute and build in one go (the everyday command)', True),
    ('check', 'run every validation and drift check without writing (used by CI)', False),
]


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser with one subparser per command."""
    parser = argparse.ArgumentParser(
        prog='gallery',
        description='Validate Plot Gallery content and generate the files the website reads.',
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(dest='command', metavar='<command>')

    for name, help_text, accepts_ids in COMMANDS:
        subparser = subparsers.add_parser(name, help=help_text, description=help_text)
        if name == 'new':
            subparser.add_argument('plot_id', help='kebab-case id, e.g. box-penguin-body-mass')
        elif accepts_ids:
            subparser.add_argument('plot_ids', nargs='*', help='plot ids (default: all plots)')
        if name == 'check':
            subparser.add_argument(
                '--skip-notebooks', action='store_true', help='skip notebook execution'
            )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse the arguments and run the selected command; returns the process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 2

    print(f'gallery {args.command}: not implemented yet (Phase 2).', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
