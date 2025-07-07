# -*- coding: utf-8 -*-
# @Time     : 2025/04/21
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


import logging

import pandas as pd
import numpy as np

from util.names import *
from util.headers import *


logger = logging.getLogger(__name__)


class DataProcessor(object):


    def __init__(self, input_data):

        self.raw_data = input_data

        self.data = {}


    def SolvingDataInitialize(self):

        logger.info('The solving status is set to solving.')
        self.data[DataName.OPTIMAL_LABEL] = ConstantName.LP_STATUS_SOLVING


    def STDFormInitialize(self):

        standard_form = self.raw_data[RawDataName.STD_FORM_DF].copy()

        # ====================================
        # Ensure the df has necessary elements
        # ====================================

        # check the size
        (form_row_num, form_col_num) = standard_form.shape
        if form_row_num < 2:
            raise ValueError('Missing necessary rows')
        if form_col_num < 2:
            raise ValueError('Missing necessary columns')

        # Ensure 'RHS' column exists
        if 'RHS' not in standard_form.columns:
            raise ValueError("The input DataFrame must contain a column named 'RHS'.")

        # ====================================
        # Name the necessary elements
        # ====================================
        constr_num, var_num = form_row_num - 1, form_col_num - 1

        variable_name = [col for col in standard_form.columns if col != SimplexTableauHeader.RHS_COL]
        self.data[DataName.VAR_NAME] = variable_name

        constr_name = [PrefixName.CONSTR_PREFIX + str(i) for i in range(1, constr_num+1)]
        standard_form.index = [SimplexTableauHeader.OBJ_ROW] + constr_name

        # ====================================
        # Save the renamed dataframe as the LP's standard form
        # ====================================
        self.data[DataName.LP_STD_FORM] = standard_form.copy()

        # ====================================
        # multiply first row of the standard form by -1
        # ====================================
        standard_form.loc[SimplexTableauHeader.OBJ_ROW] = -1 * standard_form.loc[SimplexTableauHeader.OBJ_ROW]

        # ====================================
        # Save the simplex tableau
        # ====================================
        self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU] = standard_form.copy()

        logger.info('LP standard form initialized')

        #
        # # Objective row (first row, excluding RHS), as a list
        # obj = standard_form.loc[0, variable_name].tolist()
        # self.data[DataName.OBJ] = obj
        #
        # # Constraints dictionary (rows 1 to end)
        # df_constraints = standard_form.loc[1:, variable_name]
        # constr_dict, rhs_dict = {}, {}
        # for i, row in enumerate(df_constraints.itertuples(index=False)):
        #     constr_dict[PrefixName.CONSTR_PREFIX + str(i)] = list(row)
        #
        # self.data[DataName.CONSTR_DICT] = constr_dict
        #
        # # Column-wise dictionary (excluding RHS)
        # column_dict = {col: standard_form[col].tolist() for col in variable_name}
        # self.data[DataName.VAR_COLUMNS_DICT] = column_dict
        #
        # # RHS column
        # rhs_list = standard_form['RHS'].tolist()
        # self.data[DataName.RHS_LIST] = rhs_list



