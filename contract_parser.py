import sys
import logging
from argparse import ArgumentParser

from mypy import build
from mypy.errors import CompileError
from mypy.nodes import FuncDef


def parse(source_path):
    with open(source_path) as fd:
        code = fd.read()

    logging.debug('Compiling source_code...')
    try:
        mypy_file = build.parse(
            source=code,
            fnam="smart_contract.py",
            module='__main__',
            errors=None,
            options=build.Options()
        )
        for def_ in mypy_file.defs:
            if isinstance(def_, FuncDef):
                print(def_.type)
                print(def_.name())
    except CompileError as e:
        print(e)
    logging.debug('Done.')


def _parse_args():
    """Loads the arguments from the command line."""
    parser = ArgumentParser(
        description='Parses Pikcio contract to generate '
                    'JSON interfaces.')
    parser.add_argument("file", type=str, help='input file')
    args, _ = parser.parse_known_args()
    return args.file


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    args_file = _parse_args()
    parse(args_file)