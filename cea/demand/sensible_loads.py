# -*- coding: utf-8 -*-
"""
=========================================
Sensible space heating and space cooling loads
EN-13970
=========================================

"""
from __future__ import division
import os
import numpy as np
import pandas as pd

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"



"""
=========================================
end-use heating or cooling loads
=========================================
"""

def calc_Qhs_Qcs(SystemH, SystemC, tm_t0, te_t, tintH_set, tintC_set, Htr_em, Htr_ms, Htr_is, Htr_1, Htr_2, Htr_3,
                 I_st, Hve, Htr_w, I_ia, I_m, Cm, Af, Losses, tHset_corr, tCset_corr, IC_max, IH_max, Flag):

    def calc_tm(Cm, Htr_3, Htr_em, Im_tot, tm_t0):
        tm_t = (tm_t0 * ((Cm / 3600) - 0.5 * (Htr_3 + Htr_em)) + Im_tot) / ((Cm / 3600) + 0.5 * (Htr_3 + Htr_em))
        tm = (tm_t + tm_t0) / 2
        return tm

    def calc_ts(Htr_1, Htr_ms, Htr_w, Hve, IHC_nd, I_ia, I_st, te_t, tm):
        ts = (Htr_ms * tm + I_st + Htr_w * te_t + Htr_1 * (te_t + (I_ia + IHC_nd) / Hve)) / (Htr_ms + Htr_w + Htr_1)
        return ts

    def calc_ta(Htr_is, Hve, IHC_nd, I_ia, te_t, ts):
        ta = (Htr_is * ts + Hve * te_t + I_ia + IHC_nd) / (Htr_is + Hve)
        return ta

    def calc_top(ta, ts):
        top = 0.31 * ta + 0.69 * ts
        return top

    def Calc_Im_tot(I_m, Htr_em, te_t, Htr_3, I_st, Htr_w, Htr_1, I_ia, IHC_nd, Hve, Htr_2):
        return I_m + Htr_em * te_t + Htr_3 * (I_st + Htr_w * te_t + Htr_1 * (((I_ia + IHC_nd) / Hve) + te_t)) / Htr_2

    if Losses:
        # Losses due to emission and control of systems
        tintH_set = tintH_set + tHset_corr
        tintC_set = tintC_set + tCset_corr

        # measure if this an uncomfortable hour
    uncomfort = 0
    # Case 0 or 1
    IHC_nd = IC_nd_ac = IH_nd_ac = 0
    Im_tot = Calc_Im_tot(I_m, Htr_em, te_t, Htr_3, I_st, Htr_w, Htr_1, I_ia, IHC_nd, Hve, Htr_2)

    tm = calc_tm(Cm, Htr_3, Htr_em, Im_tot, tm_t0)
    ts = calc_ts(Htr_1, Htr_ms, Htr_w, Hve, IHC_nd, I_ia, I_st, te_t, tm)
    tair_case0 = calc_ta(Htr_is, Hve, IHC_nd, I_ia, te_t, ts)
    top_case0 = calc_top(tair_case0, ts)

    if tintH_set <= tair_case0 <= tintC_set:
        ta = tair_case0
        top = top_case0
        IH_nd_ac = 0
        IC_nd_ac = 0
    else:
        if tair_case0 > tintC_set:
            tair_set = tintC_set
        else:
            tair_set = tintH_set
        # Case 2
        IHC_nd = IHC_nd_10 = 10 * Af
        Im_tot = Calc_Im_tot(I_m, Htr_em, te_t, Htr_3, I_st, Htr_w, Htr_1, I_ia, IHC_nd_10, Hve, Htr_2)

        tm = calc_tm(Cm, Htr_3, Htr_em, Im_tot, tm_t0)
        ts = calc_ts(Htr_1, Htr_ms, Htr_w, Hve, IHC_nd_10, I_ia, I_st, te_t, tm)
        tair10 = calc_ta(Htr_is, Hve, IHC_nd_10, I_ia, te_t, ts)

        IHC_nd_un = IHC_nd_10 * (tair_set - tair_case0) / (tair10 - tair_case0)  # - I_TABS
        if IC_max < IHC_nd_un < IH_max:
            ta = tair_set
            top = 0.31 * ta + 0.69 * ts
            IHC_nd_ac = IHC_nd_un
        else:
            if IHC_nd_un > 0:
                IHC_nd_ac = IH_max
            else:
                IHC_nd_ac = IC_max
            # Case 3 when the maxiFmum power is exceeded
            Im_tot = Calc_Im_tot(I_m, Htr_em, te_t, Htr_3, I_st, Htr_w, Htr_1, I_ia, IHC_nd_ac, Hve, Htr_2)

            tm = calc_tm(Cm, Htr_3, Htr_em, Im_tot, tm_t0)
            ts = calc_ts(Htr_1, Htr_ms, Htr_w, Hve, IHC_nd_ac, I_ia, I_st, te_t, tm)
            ta = calc_ta(Htr_is, Hve, IHC_nd_ac, I_ia, te_t, ts)
            top = calc_top(ta, ts)

            uncomfort = 1

        if IHC_nd_un > 0:
            if Flag == True:
                IH_nd_ac = 0
            else:
                IH_nd_ac = IHC_nd_ac
        else:
            if Flag == True:
                IC_nd_ac = IHC_nd_ac
            else:
                IC_nd_ac = 0

    if SystemC == "T0":
        IC_nd_ac = 0
    if SystemH == "T0":
        IH_nd_ac = 0
    return tm, ta, IH_nd_ac, IC_nd_ac, uncomfort, top, Im_tot


def calc_Htr(Hve, Htr_is, Htr_ms, Htr_w):
    Htr_1 = 1 / (1 / Hve + 1 / Htr_is)
    Htr_2 = Htr_1 + Htr_w
    Htr_3 = 1 / (1 / Htr_2 + 1 / Htr_ms)
    return Htr_1, Htr_2, Htr_3


def calc_qv_req(ve, people, Af, gv, hour_day, hour_year, limit_inf_season, limit_sup_season):
    infiltration_occupied = gv.hf * gv.NACH_inf_occ  # m3/h.m2
    infiltration_non_occupied = gv.hf * gv.NACH_inf_non_occ  # m3/h.m2
    if people > 0:
        q_req = (ve + (infiltration_occupied * Af)) / 3600  # m3/s
    else:
        if (21 < hour_day or hour_day < 7) and (limit_inf_season < hour_year < limit_sup_season):
            q_req = (ve * 1.3 + (infiltration_non_occupied * Af)) / 3600  # free cooling
        else:
            q_req = (ve + (infiltration_non_occupied * Af)) / 3600  #
    return q_req  # m3/s


"""
=========================================
capacity of emission/control system
=========================================
"""


def calc_Qhs_Qcs_sys_max(Af, prop_HVAC):
    # TODO: Documentation
    # Refactored from CalcThermalLoads

    IC_max = -prop_HVAC['Qcsmax_Wm2'] * Af
    IH_max = prop_HVAC['Qhsmax_Wm2'] * Af
    return IC_max, IH_max



"""
=========================================
solar and heat gains
=========================================
"""

def calc_Qgain_sen(people, Qs_Wp, Eal_nove, Eprof, Qcdata, Qcrefri, tsd, Am, Atot, Htr_w, bpr, gv):

    # itnernal loads
    tsd['I_sol']= calc_I_sol(bpr, gv)
    tsd['I_int_sen'] = people * Qs_Wp + 0.9 * (Eal_nove + Eprof) + Qcdata - Qcrefri  # here 0.9 is assumed

    # divide into components for RC model
    tsd['I_ia'] = 0.5 * tsd['I_int_sen']
    tsd['I_m'] = (Am / Atot) * (tsd['I_ia'] + tsd['I_sol'])
    tsd['I_st'] = (1 - (Am / Atot) - (Htr_w / (9.1 * Atot))) * (tsd['I_ia'] + tsd['I_sol'])

    return tsd


def calc_Qgain_lat(people, X_ghp, sys_e_cooling, sys_e_heating):
    # TODO: Documentation
    # Refactored from CalcThermalLoads
    if sys_e_heating == 'T3' or sys_e_cooling == 'T3':
        w_int = people * X_ghp / (1000 * 3600)  # kg/kg.s
    else:
        w_int = 0

    return w_int


def calc_I_sol(bpr, gv):
    from cea.tech import blinds
    solar_specific = bpr.solar / bpr.rc_model['Awall_all']  # array in W/m2
    blinds_reflection = np.vectorize(blinds.calc_blinds_reflection)(solar_specific, bpr.architecture['type_shade'], gv.g_gl)
    solar_effective_area = blinds_reflection * (1 - gv.F_f) * bpr.rc_model['Aw']  # Calculation of solar effective area per hour in m2
    net_solar_gains = solar_effective_area * solar_specific  # how much are the net solar gains in Wh per hour of the year.
    return net_solar_gains.values


"""
=========================================
temperature of emission/control system
=========================================
"""


def calc_temperatures_emission_systems(Qcsf, Qcsf_0, Qhsf, Qhsf_0, Ta, Ta_re_cs, Ta_re_hs, Ta_sup_cs, Ta_sup_hs,
                                       Tcs_re_0, Tcs_sup_0, Ths_re_0, Ths_sup_0, gv, ma_sup_cs, ma_sup_hs,
                                       sys_e_cooling, sys_e_heating, ta_hs_set):

    from cea.tech import  radiators, heating_coils, tabs
    # local variables
    Ta_0 = ta_hs_set.max()
    if sys_e_heating == 'T0':
        Ths_sup = np.zeros(8760)  # in C
        Ths_re = np.zeros(8760)  # in C
        mcphs = np.zeros(8760)  # in KW/C

    if sys_e_cooling == 'T0':
        Tcs_re = np.zeros(8760)  # in C
        Tcs_sup = np.zeros(8760)  # in C
        mcpcs = np.zeros(8760)  # in KW/C

    if sys_e_heating == 'T1' or sys_e_heating == 'T2':  # radiators

        Ths_sup, Ths_re, mcphs = np.vectorize(radiators.calc_radiator)(Qhsf, Ta, Qhsf_0, Ta_0, Ths_sup_0, Ths_re_0)

    if sys_e_heating == 'T3':  # air conditioning
        index = np.where(Qhsf == Qhsf_0)
        ma_sup_0 = ma_sup_hs[index[0][0]]
        Ta_sup_0 = Ta_sup_hs[index[0][0]] + 273
        Ta_re_0 = Ta_re_hs[index[0][0]] + 273
        Ths_sup, Ths_re, mcphs = np.vectorize(heating_coils.calc_heating_coil)(Qhsf, Qhsf_0, Ta_sup_hs, Ta_re_hs,
                                                                               Ths_sup_0, Ths_re_0, ma_sup_hs,ma_sup_0,
                                                                               Ta_sup_0, Ta_re_0, gv.Cpa)

    if sys_e_cooling == 'T3':  # air conditioning

        index = np.where(Qcsf == Qcsf_0)
        ma_sup_0 = ma_sup_cs[index[0][0]] + 273
        Ta_sup_0 = Ta_sup_cs[index[0][0]] + 273
        Ta_re_0 = Ta_re_cs[index[0][0]] + 273
        Tcs_sup, Tcs_re, mcpcs = np.vectorize(heating_coils.calc_cooling_coil)(Qcsf, Qcsf_0, Ta_sup_cs, Ta_re_cs,
                                                                               Tcs_sup_0, Tcs_re_0, ma_sup_cs, ma_sup_0,
                                                                               Ta_sup_0, Ta_re_0, gv.Cpa)

    if sys_e_heating == 'T4':  # floor heating

        Ths_sup, Ths_re, mcphs = np.vectorize(tabs.calc_floorheating)(Qhsf, Ta, Qhsf_0, Ta_0, Ths_sup_0, Ths_re_0)

    return Tcs_re, Tcs_sup, Ths_re, Ths_sup, mcpcs, mcphs

"""
=========================================
space heating/cooling losses
=========================================
"""

def calc_Qhs_Qcs_dis_ls(tair, text, Qhs, Qcs, tsh, trh, tsc, trc, Qhs_max, Qcs_max, D, Y, SystemH, SystemC, Bf, Lv):
    """calculates distribution losses based on ISO 15316"""
    # Calculate tamb in basement according to EN
    tamb = tair - Bf * (tair - text)
    if SystemH != 'T0' and Qhs > 0:
        Qhs_d_ls = ((tsh + trh) / 2 - tamb) * (Qhs / Qhs_max) * (Lv * Y)
    else:
        Qhs_d_ls = 0
    if SystemC != 'T0' and Qcs < 0:
        Qcs_d_ls = ((tsc + trc) / 2 - tamb) * (Qcs / Qcs_max) * (Lv * Y)
    else:
        Qcs_d_ls = 0

    return Qhs_d_ls, Qcs_d_ls


def calc_Qhs_Qcs_em_ls(SystemH, SystemC):
    """model of losses in the emission and control system for space heating and cooling.
    correction factor for the heating and cooling setpoints. extracted from SIA 2044 (replacing EN 15243)"""
    tHC_corr = [0, 0]
    # values extracted from SIA 2044 - national standard replacing values suggested in EN 15243
    if SystemH == 'T4' or 'T1':
        tHC_corr[0] = 0.5 + 1.2
    elif SystemH == 'T2':
        tHC_corr[0] = 0 + 1.2
    elif SystemH == 'T3':  # no emission losses but emissions for ventilation
        tHC_corr[0] = 0.5 + 1  # regulation is not taking into account here
    else:
        tHC_corr[0] = 0.5 + 1.2

    if SystemC == 'T4':
        tHC_corr[1] = 0 - 1.2
    elif SystemC == 'T5':
        tHC_corr[1] = - 0.4 - 1.2
    elif SystemC == 'T3':  # no emission losses but emissions for ventilation
        tHC_corr[1] = 0 - 1  # regulation is not taking into account here
    else:
        tHC_corr[1] = 0 + - 1.2

    return list(tHC_corr)

