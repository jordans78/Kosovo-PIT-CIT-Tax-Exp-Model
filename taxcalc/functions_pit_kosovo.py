"""
Functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


'''
-------------------------------------------------------------------------------------
I. PERSONAL INCOME TAX CALCULATION
-------------------------------------------------------------------------------------
'''

'''
Income
'''

# D19	Total Income (add 8 to 18)
@iterate_jit(nopython=True)
def total_inc_fun(gross_wage,net_income_business,net_income_partnership,gross_rents,gross_i_interest_pen_pay,gross_i_interest,gross_i_inta_prop,capital_gain,foreign_s_inc,other_inc_gifts,calc_total_inc):
    calc_total_inc =  gross_wage+net_income_business+net_income_partnership+gross_rents+gross_i_interest_pen_pay+gross_i_interest+gross_i_inta_prop+capital_gain+foreign_s_inc+other_inc_gifts
    return calc_total_inc

'''New'''
# Deductions for expenses related to intangible property income
@iterate_jit(nopython=True)
def ded_exp_int_prop_fun(ded_exp_int_prop, toggle_ded_exp_int_prop,calc_ded_exp_int_prop):
    calc_ded_exp_int_prop = ded_exp_int_prop * toggle_ded_exp_int_prop
    return calc_ded_exp_int_prop

'''New'''
@iterate_jit(nopython=True)
def other_allowed_ded_fun(other_allowed_ded, toggle_other_allowed_ded,calc_other_allowed_ded):
    calc_other_allowed_ded = other_allowed_ded * toggle_other_allowed_ded
    return calc_other_allowed_ded


"New"
'''Deduction for rents expenses, actual or 10% of gross rents'''
''' This calculated variable is not connects with others'''
@iterate_jit(nopython=True)
def total_ded_rents_expen_rents_fun(ded_rents_expen_rents10pct, rate_ded_rents,calc_ded_rents_expen_rents):
    tax_base_rents=ded_rents_expen_rents10pct/0.1   
    if ded_rents_expen_rents10pct > 0:
        calc_ded_rents_expen_rents=tax_base_rents*rate_ded_rents
        return calc_ded_rents_expen_rents
    else:
        calc_ded_rents_expen_rents=0
        return calc_ded_rents_expen_rents



"New"
''' Deduction for Charitable Contributions (max 5% of taxable amount).not claimed on FS'''
@iterate_jit(nopython=True)
def tax_charity_contribution_fun(dis_charity_contribution, rate_charitable_contribution,calc_dis_charity_contribution):
    tax_charity_contribution=dis_charity_contribution/0.05   
    if dis_charity_contribution > 0:
        calc_dis_charity_contribution=tax_charity_contribution*rate_charitable_contribution
        return calc_dis_charity_contribution
    else:
        calc_dis_charity_contribution=0
        return calc_dis_charity_contribution



'''Deductions'''
# D24	Total deductions (add 20 to 23)
@iterate_jit(nopython=True)
def total_ded_fun(calc_ded_rents_expen_rents,ded_pen_cont,calc_ded_exp_int_prop,calc_other_allowed_ded,calc_total_ded):
    calc_total_ded =  calc_ded_rents_expen_rents+ded_pen_cont+calc_ded_exp_int_prop+calc_other_allowed_ded
    return calc_total_ded


# D25	Taxable amount (19-24)
@iterate_jit(nopython=True)
def taxable_amount_fun(calc_total_inc,calc_total_ded,calc_taxable_amount):
    calc_taxable_amount =  calc_total_inc-calc_total_ded
    return calc_taxable_amount


# D27 Deduction for Charitable Contributions (max 5% of taxable amount).not claimed on FS
@iterate_jit(nopython=True)
def charity_contribution_fun(calc_dis_charity_contribution, toggle_charitable,calc_charity_contribution):
    calc_charity_contribution = calc_dis_charity_contribution * toggle_charitable
    return calc_charity_contribution


# D28	Total Additional Deductions (26+27)
@iterate_jit(nopython=True)
def tot_additional_ded_fun(calc_charity_contribution,loss_carried_for,calc_tot_additional_ded):
    calc_tot_additional_ded =  calc_charity_contribution+loss_carried_for
    return calc_tot_additional_ded


# @iterate_jit(nopython=True)
# def total_tax_fun(calc_total_tax_payable,pitax):
#     pitax=calc_total_tax_payable
#     return (pitax)

# PIT
# D29 Taxable Income before tax [25]-[28] (if negative put the amount in brackets)
@iterate_jit(nopython=True)
def taxable_inc_before_tax_fun(calc_taxable_amount,calc_tot_additional_ded,calc_taxable_inc_before_tax):
    calc_taxable_inc_before_tax =  calc_taxable_amount-calc_tot_additional_ded
    return calc_taxable_inc_before_tax


# D30 Tax on Taxable Income as per tax brackets 
@iterate_jit(nopython=True)
def total_tax_fun(calc_taxable_inc_before_tax, rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3,pitax):
    pitax = (rate1 * min(calc_taxable_inc_before_tax, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., calc_taxable_inc_before_tax - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., calc_taxable_inc_before_tax - tbrk2)) +
                    rate4 * max(0., calc_taxable_inc_before_tax - tbrk3))
    return (pitax)




# '''Tax Withheld during the Year'''

# # D36	Total tax withheld and Credit (add 31 to 35)
# @iterate_jit(nopython=True)
# def total_witheld_credit_fun(tax_withheld_wage_employer,tax_withheld_wage_interest,tax_withheld_rents,tax_witheld_lottery_gains,foreign_tax_credit,calc_total_witheld_credit):
#     calc_total_witheld_credit =  tax_withheld_wage_employer+tax_withheld_wage_interest+tax_withheld_rents+tax_witheld_lottery_gains+foreign_tax_credit
#     return calc_total_witheld_credit

# # D37 Subtract: Line [30] - Line [36] to determine total tax payable
# @iterate_jit(nopython=True)
# def total_pay_for_fun(calc_tax_on_tax_inc_bracket,calc_total_witheld_credit,calc_total_pay_for):
#     calc_total_pay_for =  calc_tax_on_tax_inc_bracket-calc_total_witheld_credit
#     return calc_total_pay_for


# # D40 Total advance payments [38] + [39]
# @iterate_jit(nopython=True)
# def total_advance_payment_fun(q_advance_business_inc,q_payment_ren_inc_int_prop,calc_total_advance_payment):
#     calc_total_advance_payment =  q_advance_business_inc+q_payment_ren_inc_int_prop
#     return calc_total_advance_payment


# # D41	Total Tax Payable [37] - [40]
# @iterate_jit(nopython=True)
# def total_tax_payable_fun(calc_total_pay_for, calc_total_advance_payment,calc_total_tax_payable):
#     calc_total_tax_payable = (calc_total_pay_for - calc_total_advance_payment)
#     if calc_total_tax_payable < 0:
#         calc_total_tax_payable=0
#         return calc_total_tax_payable
#     else:
#         calc_total_tax_payable=calc_total_tax_payable
#         return calc_total_tax_payable


# Total tax

# Warninig ! Check this out once again 

# @iterate_jit(nopython=True)
# def total_tax_fun(calc_total_tax_payable,pitax):
#     pitax=calc_total_tax_payable
#     return (pitax)




