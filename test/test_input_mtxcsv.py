# -*- coding: utf-8 -*-
# @Time     : 2025/4/1
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


import logging
import pandas as pd

from dao import DataReader
from dao.data_process.data_processor import DataProcessor
from util.names import InputType, RawDataName
from util.project_logger import init_logger


logger = logging.getLogger(__name__)


def test_csv_standard_form():

    test_read_method = 'local'
    test_file_type = 'csv'
    test_file_path = '/Users/huangjiacheng/PySimplex/test/test_data/ex_1.csv'

    lp_input_reader = DataReader(
        read_method=test_read_method,
        local_file_type=test_file_type,
        local_file_path=test_file_path
    )
    lp_input_reader.read()

    lp_standard_form = lp_input_reader.raw_data
    logger.info('input finish')

    input_processor = DataProcessor(lp_standard_form)
    input_processor.LPInputDecomp()
    logger.info('standard form process finish')


if __name__ == '__main__':
    init_logger()
    test_csv_standard_form()
