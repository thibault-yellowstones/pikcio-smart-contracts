import sys
import logging
from argparse import ArgumentParser


def parse(source_code):
    logging.debug('Compiling source_code...')
    module = compile(source_code, 'submitted_code', 'exec')
    logging.debug('Done.')

    module.

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

    source_file = _parse_args()
    with open(source_file, 'r') as fd:
        code = fd.read()

    parse(code)