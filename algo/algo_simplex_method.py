# -*- coding: utf-8 -*-
# @Time     : 2025/07/01
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com

import logging

import pandas as pd
import numpy as np

from util.names import *
from util.headers import *


logger = logging.getLogger(__name__)


class AlgoSimplexMethod:

    def __init__(self, processed_data):
        self.data = processed_data
        self.data[DataName.ITER_NUMBER] = 0
        self.result = {}


    def SolveLPBasic(self):
        logger.info('Start solving LP')

        while self.data[DataName.OPTIMAL_LABEL] == ConstantName.LP_STATUS_SOLVING:
            logger.info(f'Iteration {self.data[DataName.ITER_NUMBER]}')

            self.OptimalityTest()
            if self.data[DataName.OPTIMAL_LABEL] != ConstantName.LP_STATUS_SOLVING:
                continue

            self.SelectEnteringVar()

            self.UnBTest()
            if self.data[DataName.OPTIMAL_LABEL] != ConstantName.LP_STATUS_SOLVING:
                continue

            self.SelectLeavingVar()

            self.PivotOperation()

            if self.data[DataName.OPTIMAL_LABEL] == ConstantName.LP_STATUS_SOLVING:
                self.RecordSolvingProcess()
                self.data[DataName.ITER_NUMBER] += 1

        logger.info('End solving LP')

        self.GetResult()


    def PivotOperation(self):

        logger.info('Start Pivot Operation')
        logger.info(f'var: {self.data[DataName.CURRENT_ENTERING_VAR_LIST]}')
        logger.info(f'row: {self.data[DataName.CURRENT_PIVOT_ROW_DICT]}')

        # take a copy for updating the tableau
        current_simplex_tableau = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()

        # implement the pivot operation regarding every entering variables
        for entering_var in self.data[DataName.CURRENT_ENTERING_VAR_LIST]:

            # read the pivot row of the entering variable
            pivoting_row_index = self.data[DataName.CURRENT_PIVOT_ROW_DICT][entering_var]

            # check the correctness of the coefficient in the tableau
            pivot_value = current_simplex_tableau[entering_var][pivoting_row_index]
            if pivot_value == 0:
                raise ValueError(f'Error: 0 should not be at row {pivoting_row_index }, column {entering_var}')

            # process the pivot operation
            pivot_row = current_simplex_tableau.loc[pivoting_row_index] / pivot_value

            for row_idx in current_simplex_tableau.index:
                if row_idx != pivoting_row_index:
                    entry_to_erase = current_simplex_tableau.loc[row_idx][entering_var]
                    current_simplex_tableau.loc[row_idx] = current_simplex_tableau.loc[row_idx] - pivot_row * entry_to_erase

            current_simplex_tableau.loc[pivoting_row_index] = pivot_row

        # update the simplex tableau stored in data
        self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU] = current_simplex_tableau
        logger.info('End Pivot Operation')

    def OptimalityTest(self):
        current_simplex_tableau = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()

        first_row = current_simplex_tableau.loc[ConstantName.OBJ_ROW]
        obj_coefficient_row = first_row[self.data[DataName.VAR_NAME]]

        max_price = obj_coefficient_row.max()

        # If all the entries in the objective row are less than or equal to 0, then no choice of entering variable can be made and the solution is in fact optimal.
        if max_price <= 0:
            logger.info('No choice of entering variables due to non-positive min_price')
            self.data[DataName.OPTIMAL_LABEL] = ConstantName.LP_STATUS_OPT
        else:
            self.data[DataName.OPTIMAL_LABEL] = ConstantName.LP_STATUS_SOLVING

    def SelectEnteringVar(self):
        logger.info('Start Select Entering Variable')
        current_simplex_tableau = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()

        first_row = current_simplex_tableau.loc[SimplexTableauHeader.OBJ_ROW]
        obj_coefficient_row = first_row[self.data[DataName.VAR_NAME]]

        # ===================================
        # select entering variable, assuming that the optimal solution is not reached
        # ===================================
        min_price_var_name = obj_coefficient_row.idxmax()

        next_entering_var_name = [min_price_var_name]
        self.data[DataName.CURRENT_ENTERING_VAR_LIST] = next_entering_var_name
        logger.info(f'End Selecting Entering Var. Updated Entering Var: {next_entering_var_name}')

    def UnBTest(self):
        logger.info('Start Unsoundness Test')

        # Assume that the one and the only entering var is chosen
        entering_var = self.data[DataName.CURRENT_ENTERING_VAR_LIST][0]
        current_simplex_tableau = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()

        pivot_column = current_simplex_tableau[entering_var]

        # check if there is any positive entries in the pivot column
        max_coefficient = pivot_column.max()

        # if there are no positive entries, then the LP should be unbounded
        if max_coefficient <= 0:
            logger.info('No positive entries in pivot column. LP is unbounded.')
            self.data[DataName.OPTIMAL_LABEL] = ConstantName.LP_STATUS_UNBOUNDED
        else:
            self.data[DataName.OPTIMAL_LABEL] = ConstantName.LP_STATUS_SOLVING

    def SelectLeavingVar(self):
        logger.info('Start Select Leaving Variable')

        # Assume that the one and the only entering var is chosen, and the LP is not unbounded.
        entering_var = self.data[DataName.CURRENT_ENTERING_VAR_LIST][0]
        current_simplex_tableau = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()

        pivot_column = current_simplex_tableau[entering_var]

        # ratio test
        potential_rows_df = current_simplex_tableau[pivot_column > 0].drop(ConstantName.OBJ_ROW)
        potential_rows_df['ratio'] = potential_rows_df[SimplexTableauHeader.RHS_COL] / potential_rows_df[entering_var]

        pivot_row_idx = potential_rows_df['ratio'].idxmin()

        # update the pivot row index in data
        self.data[DataName.CURRENT_PIVOT_ROW_DICT] = {entering_var: pivot_row_idx}

    def RecordSolvingProcess(self):
        iter_num = self.data[DataName.ITER_NUMBER]
        self.data[DataName.RECORD_LP_SIMPLEX_TABLEAU][iter_num] = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()
        self.data[DataName.RECORD_ENTERING_VAR_LIST][iter_num] = self.data[DataName.CURRENT_ENTERING_VAR_LIST]
        self.data[DataName.RECORD_PIVOT_ROW_DICT][iter_num] = self.data[DataName.CURRENT_PIVOT_ROW_DICT]

    def GetResult(self):

        logger.info('Start process result')

        if self.data[DataName.OPTIMAL_LABEL] == ConstantName.LP_STATUS_OPT:
            self.result[ResultName.FINAL_SIMPLEX_TABLEAU] = self.data[DataName.CURRENT_LP_SIMPLEX_TABLEAU].copy()
            self.result[ResultName.OBJ_VALUE] = self.result[ResultName.FINAL_SIMPLEX_TABLEAU][SimplexTableauHeader.RHS_COL][SimplexTableauHeader.OBJ_ROW]

        logger.info('End process result')