# -*- coding: utf-8 -*-
# @Time     : 2025/4/1
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


import logging


logger = logging.getLogger(__name__)


class DataReader(object):

    def __init__(self, read_method, local_file_type, local_file_path):
        self.read_method = read_method
        self.local_file_type = local_file_type
        self.local_file_path = local_file_path

        self.lp_problem = {}

    def read(self):

        if self.read_method == 'local':
            pass

        elif self.read_method == 'remote':
            pass
