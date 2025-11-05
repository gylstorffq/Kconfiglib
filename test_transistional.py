import difflib
import errno
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from kconfiglib import Kconfig, Symbol, Choice, COMMENT, MENU, MenuNode, \
                       BOOL, TRISTATE, HEX, \
                       TRI_TO_STR, \
                       escape, unescape, \
                       expr_str, expr_items, split_expr, \
                       _ordered_unique, \
                       OR, AND, \
                       KconfigError



def verify_value(c, sym_name, val):
        # Verifies that a symbol has a particular value.

        if isinstance(val, int):
            val = TRI_TO_STR[val]

        sym = c.syms[sym_name]
        assert sym.str_value == val


def test_transitional():
    c = Kconfig("tests/Ktransitional", warn=False)
    verify_value(c, "MODULES", "y")
    verify_value(c, "NEW_BOOL", "n")
    c.load_config("tests/config_set_transitional")
    verify_value(c, "MODULES", "y")
    verify_value(c, "NEW_BOOL", "y")


KCONFIG_TRANSITIONAL_EXPECTED_CONTENT = """\
config transitional
CONFIG_MODULES=y
CONFIG_NEW_BOOL=y
CONFIG_NEW_TRISTATE=m
CONFIG_NEW_STRING="test string"
CONFIG_NEW_HEX=0x1234
CONFIG_NEW_INT=42
# CONFIG_NEW_BOOL_PRECEDENCE is not set
CONFIG_NEW_STRING_PRECEDENCE="user value"
CONFIG_NEW_TRISTATE_PRECEDENCE=y
CONFIG_NEW_HEX_PRECEDENCE=0xABCD
CONFIG_NEW_INT_PRECEDENCE=100
# CONFIG_NEW_DISABLED is not set
# CONFIG_DEPENDENCY_TEST is not set
# CONFIG_NEW_CONDITIONAL_DEFAULT is not set
# CONFIG_REGULAR_OPTION is not set
"""

def test_transitional_file_content():
    config_test_file = "tests/config_test"
    c = Kconfig("tests/Ktransitional", warn=False)
    c.load_config("tests/config_set_transitional")
    c.write_config(config_test_file, header="config transitional\n")
    with open(config_test_file, "r") as config:
        assert config.read() == KCONFIG_TRANSITIONAL_EXPECTED_CONTENT
