# -*- coding: utf-8 -*-
# @Time     : 2025/4/1
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


class InputType:
    CSV = 'csv'


class RawDataName:
    STD_FORM_DF = 'std_form_df'


class DataName:
    CONSTR_DICT = 'constr_dict'
    OBJ = 'obj'
    RHS_LIST = 'rhs_list'
    VAR_COLUMNS_DICT = 'var_columns_dict'
    VAR_NAME = 'var_name'

    LP_STD_FORM = 'lp_std_form'                                 # dataframe, the standard form of the lp

    CURRENT_LP_SIMPLEX_TABLEAU = 'current_lp_simplex_tableau'   # dataframe, the current simplex tableau of the LP
    CURRENT_ENTERING_VAR_LIST = 'current_entering_var_list'     # list, the list of current entering var(s)
    CURRENT_PIVOT_ROW_DICT = 'current_pivot_row_dict'           # dict, the pivot rows of corresponding entering var, e.g. {var_name1: row_index_1, ...}

    OPTIMAL_LABEL = 'opt_label'                                 # integer value. 1: optimal solution is found; 0: solving; -1: unbounded
    ITER_NUMBER = 'iter_num'                                    # integer, the number of iterations has been implemented

    RECORD_LP_SIMPLEX_TABLEAU = 'record_lp_simplex_tableau'     # dict, the simplex tableau of each iteration
    RECORD_ENTERING_VAR_LIST = 'record_entering_var_list'       # dict, the entering var list of each iteration
    RECORD_PIVOT_ROW_DICT = 'record_pivot_row_dict'             # dict, the pivot row of each iteration


class ResultName:
    OBJ_VALUE = 'obj_value'                                     # float, the objective value of the lp
    FINAL_SIMPLEX_TABLEAU = 'final_simplex_tableau'             # dataframe, the final simplex tableau of the solved LP


class ConstantName:
    OBJ_ROW = 'OBJ_ROW'
    RHS_COL = 'RHS'

    LP_STATUS_OPT = 1
    LP_STATUS_UNBOUNDED = -1
    LP_STATUS_SOLVING = 0


class PrefixName:
    CONSTR_PREFIX = 'cons_'