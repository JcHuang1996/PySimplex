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

        self.data = {}


    def LPInputDecomp(self):

        standard_form = self.raw_data[RawDataName.STD_FORM_DF]

        # Ensure 'RHS' column exists
        if 'RHS' not in standard_form.columns:
            raise ValueError("The input DataFrame must contain a column named 'RHS'.")

        # Extract variable names
        variable_name = [col for col in standard_form.columns if col != 'RHS']
        self.data[DataName.VAR_NAME] = variable_name

        # Objective row (first row, excluding RHS), as a list
        obj = standard_form.loc[0, variable_name].tolist()
        self.data[DataName.OBJ] = obj

        # Constraints dictionary (rows 1 to end)
        df_constraints = standard_form.loc[1:, variable_name]
        constr_dict, rhs_dict = {}, {}
        for i, row in enumerate(df_constraints.itertuples(index=False)):
            constr_dict[PrefixName.CONSTR_PREFIX + str(i)] = list(row)

        self.data[DataName.CONSTR_DICT] = constr_dict

        # Column-wise dictionary (excluding RHS)
        column_dict = {col: standard_form[col].tolist() for col in variable_name}
        self.data[DataName.VAR_COLUMNS_DICT] = column_dict

        # RHS column
        rhs_list = standard_form['RHS'].tolist()
        self.data[DataName.RHS_LIST] = rhs_list



