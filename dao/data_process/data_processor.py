# -*- coding: utf-8 -*-
# @Time     : 2025/04/21
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


import pandas as pd
import numpy as np

from util.names import *
from util.headers import *


class DataProcessor(object):


    def __init__(self, input_data):

        self.raw_data = input_data

        self.processed_data = {}

    def LPDecomp(self):
        pass

