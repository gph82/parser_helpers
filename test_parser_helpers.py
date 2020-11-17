import mdtraj as md
from os import path
import numpy as np

import unittest
from mdciao.filenames import filenames

from mdciao.utils import str_and_dict

from tempfile import TemporaryDirectory as _TDir

import pytest

from pandas import \
    DataFrame as _DF,\
    ExcelWriter as _XW

from mdciao import parsers

test_filenames = filenames()

class Test_helpers_just_run(unittest.TestCase):

    def test_list(self):
        parsers_list = parsers._parser_names()
        assert len(parsers_list)>0

    def test_parser2dict(self):
        for name in parsers._parser_names():
            iparser = getattr(parsers,name)()
            dd = parsers._parser2dict(iparser)
            #print(dd)
            print(dd.keys())

if __name__ == '__main__':
    unittest.main()