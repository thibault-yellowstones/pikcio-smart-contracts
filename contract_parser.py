import sys
import logging
from os import path
from argparse import ArgumentParser

from mypy.build import parse, Options
from mypy.errors import CompileError
from mypy.nodes import FuncDef, AssignmentStmt, NameExpr, Expression, \
    FloatExpr, IntExpr, StrExpr


def _extract_storage_vars(compiled):
    """

    :param compiled:
    :type compiled: MypyFile
    :return:
    """
    assignments = [
        (lvalue, def_.rvalue)
        for def_ in compiled.defs
        if isinstance(def_, AssignmentStmt)
        for lvalue in def_.lvalues
        if isinstance(lvalue, NameExpr)
        if not lvalue.name.startswith('_')
    ]

    return [
        (
            lvalue.name,
            rvalue.value if hasattr(rvalue, 'value') else
            rvalue.name if hasattr(rvalue, 'name') else
            str(rvalue)
        )
        for (lvalue, rvalue) in assignments
    ]


def _extract_endpoints(compiled):
    return [
        def_ for def_ in compiled.defs
        if isinstance(def_, FuncDef)
        if not def_.name().startswith('_')
    ]


def _parse_contract_from_source_insecure(source_code, filename):

    logging.debug('Compiling source_code...')
    compiled = parse(
        source=source_code, fnam=filename,
        options=Options(), module='__main__', errors=None

    )
    logging.debug('Done.')

    variable_constants = _extract_storage_vars(compiled)
    endpoints = _extract_endpoints(compiled)
    return {
        'is_success': True,
        'storage': [
            str(def_) for def_ in variable_constants
        ],
        'endpoints': {
            def_.name(): def_.type for def_ in endpoints
        }
    }


def parse_contract_from_source(source_code, filename='script.py'):
    try:
        return _parse_contract_from_source_insecure(source_code, filename)
    except (CompileError, ValueError) as e:
        logging.error(e)
        return {
            'is_success': False,
            'error': str(e)
        }


def parse_contract_from_file(source_path):
    with open(source_path) as fd:
        code = fd.read()
    return parse_contract_from_source(code, path.basename(source_path))


def _parse_args():
    """Loads the arguments from the command line."""
    parser = ArgumentParser(
        description='Parses Pikcio contract to generate  JSON interfaces.'
    )
    parser.add_argument("file", type=str, help='input file')
    args, _ = parser.parse_known_args()
    return args.file


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    args_file = _parse_args()
    parse_result = parse_contract_from_file(args_file)
    print(parse_result)
