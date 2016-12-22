# -*- coding: utf-8 -*-


from __future__ import division
import numpy as np



__author__ = "Gabriel Happle"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

'''
RC model calculations according to sia 2044

Merkblatt 2044 Kilimatisierte Gebauede - Standard-Berechnungsverfahren fuer den Leistungs-und Energiebedarf
'''

# SIA 2044 constants
h_cv_i = 2.5 # (W/m2K) (4) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011
h_r_i = 5.5 # (W/m2K) (5) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011
h_ic = 9.1 # (W/m2K) (6) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011
f_sa = 0.1 # (-) section 2.1.4 in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011
f_r_l = 0.7 # (-) section 2.1.4 in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011
f_r_p = 0.5 # (-) section 2.1.4 in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011
f_r_a = 0.2 # (-) section 2.1.4 in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 2.1.3
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def calc_h_mc(bpr):

    # get properties from bpr # TODO: to be addressed in issue #443
    a_m = bpr.rc_model['Am']

    # (7) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    h_mc = h_ic * a_m

    return h_mc


def calc_h_ac(bpr):

    # get properties from bpr # TODO: to be addressed in issue #443
    a_t = bpr.rc_model['Atot']

    # (8) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    h_ac = a_t / (1/h_cv_i - 1/h_ic)

    return h_ac


def calc_h_op_m(bpr):

    # work around # TODO: to be addressed in issue #443
    # get h_op from ISO model (with basement factor)
    h_op_m = bpr.rc_model['Htr_op']
    # TODO: This formula should be adjusted to be compatible with SIA2044

    # (9) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # h_op_m = a_j_m * u_j  # summation
    # TODO: this formula in the future should take specific properties of the location of the building into account
    # e.g. adiabatic building elements with U = 0

    return h_op_m


def calc_h_em(bpr):

    # calculate values
    h_op_m = calc_h_op_m(bpr)
    h_mc = calc_h_mc(bpr)

    # (10) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    h_em = 1 / (1 / h_op_m - 1 / h_mc)

    return h_em


def calc_h_j_em():

    # TODO: to be addressed in issue #443

    # (11) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    #h_j_em = (h_em * a_j_m * u_j) / h_op_m

    # TODO: this formula in the future should take specific properties of the location of the building into account
    # e.g. adiabatic building elements with U = 0

    return None


def calc_h_ec(bpr):

    # (12) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # h_ec = a_j_l * u_j
    # TODO: this formula in the future should take specific properties of the location of the building into account
    # e.g. adiabatic building elements with U = 0
    # TODO: can incorporate point or linear thermal bridges

    h_ec = bpr.rc_model['Htr_w']  # h_ec is Htr_w of ISO13790 RC model

    return h_ec


def calc_h_ea(tsd, t):

    cp = 1.005 / 3.6  # (Wh/kg/K)
    # TODO: check units of air flow

    # get values
    m_v_sys = tsd['m_ve_mech'][t]  # mass flow rate mechanical ventilation
    m_v_w = tsd['m_ve_window'][t]  # mass flow rate window ventilation
    m_v_inf = tsd['m_ve_inf_simple'][t]  # mass flow rate infiltration

    # (13) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # adapted for mass flows instead of volume flows
    h_ea = (m_v_sys + m_v_w + m_v_inf) * cp

    return h_ea


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 2.1.4
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def calc_phi_a(phi_hc_cv, bpr, tsd, t):

    # (14) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get internal loads
    phi_i_l = 0.9 * tsd['Elf'][
        t]  # internal gains from lighting, factor of 0.9 taken from old method calc_Qgain_sen() #TODO make function and dynamic, check factor
    phi_i_a = 0.9 * tsd['Eaf'][t] + tsd['Qcdataf'][t] - tsd['Qcref'][
        t]  # internal gains from appliances, factor of 0.9 taken from old method calc_Qgain_sen() #TODO make function and dynamic, check factor
    phi_i_p = tsd['people'][t] * bpr.internal_loads['Qs_Wp']  # internal gains from people

    # solar gains
    phi_s = tsd['I_sol'][t]  # solar gains

    # standard assumptions
    #f_sa = 0.1
    #f_r_l = 0.7
    #f_r_p = 0.5
    #f_r_a = 0.2

    phi_a = f_sa * phi_s + (1-f_r_l)*phi_i_l + (1-f_r_p) * phi_i_p +(1-f_r_a)*phi_i_a + phi_hc_cv

    return phi_a


def calc_phi_c(phi_hc_r, bpr, tsd, t):

    # (15) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get internal loads
    phi_i_l = 0.9 * tsd['Elf'][t]  # internal gains from lighting, factor of 0.9 taken from old method calc_Qgain_sen() #TODO make function and dynamic, check factor
    phi_i_a = 0.9 * tsd['Eaf'][t] + tsd['Qcdataf'][t] - tsd['Qcref'][t]  # internal gains from appliances, factor of 0.9 taken from old method calc_Qgain_sen() #TODO make function and dynamic, check factor
    phi_i_p = tsd['people'][t] * bpr.internal_loads['Qs_Wp'] # internal gains from people

    # solar gains
    phi_s = tsd['I_sol'][t] # solar gains

    # call functions for factor
    f_ic = calc_f_ic(bpr)
    f_sc = calc_f_sc(bpr)

    # standard assumptions
    #f_sa = 0.1
    #f_r_l = 0.7
    #f_r_p = 0.5
    #f_r_a = 0.2

    phi_c = f_ic * (f_r_l*phi_i_l+f_r_p*phi_i_p+f_r_a*phi_i_a + phi_hc_r) + (1-f_sa)*f_sc*phi_s

    return phi_c


def calc_phi_m(phi_hc_r, bpr, tsd, t):

    # (16) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get internal loads
    phi_i_l = 0.9 * tsd['Elf'][
        t]  # internal gains from lighting, factor of 0.9 taken from old method calc_Qgain_sen() #TODO make function and dynamic, check factor
    phi_i_a = 0.9 * tsd['Eaf'][t] + tsd['Qcdataf'][t] - tsd['Qcref'][
        t]  # internal gains from appliances, factor of 0.9 taken from old method calc_Qgain_sen() #TODO make function and dynamic, check factor
    phi_i_p = tsd['people'][t] * bpr.internal_loads['Qs_Wp']  # internal gains from people

    # solar gains
    phi_s = tsd['I_sol'][t]  # solar gains

    # call functions for factors
    f_im = calc_f_im(bpr)
    f_sm = calc_f_sm(bpr)

    # standard assumption
    #f_sa = 0.1
    #f_r_l = 0.7
    #f_r_p = 0.5
    #f_r_a = 0.2
    phi_m = f_im * (f_r_l*phi_i_l+f_r_p*phi_i_p+f_r_a*phi_i_a + phi_hc_r) + (1-f_sa)*f_sm*phi_s

    return phi_m


def calc_f_ic(bpr):

    # (17) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get values from bpr
    a_t = bpr.rc_model['Atot']
    a_m = bpr.rc_model['Am']
    h_ec = calc_h_ec(bpr)
    #h_ic = 9.1  # in (W/m2K) from (8) in SIA 2044

    f_ic = (a_t - a_m - h_ec / h_ic) / a_t

    return f_ic


def calc_f_sc(bpr):

    # (18) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get values from bpr
    a_t = bpr.rc_model['Atot']
    a_m = bpr.rc_model['Am']
    a_w = bpr.rc_model['Aw']
    h_ec = bpr.rc_model['Htr_w']
    #h_ic = 9.1  # in (W/m2K) from (8) in SIA 2044

    f_sc = (a_t-a_m-a_w-h_ec/h_ic) / (a_t - a_w)

    return f_sc


def calc_f_im(bpr):

    # (19) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get values from bpr
    a_t = bpr.rc_model['Atot']
    a_m = bpr.rc_model['Am']

    f_im = a_m / a_t

    return f_im


def calc_f_sm(bpr):

    # (20) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # Gabriel Happle 01.12.2016

    # get values from bpr
    a_t = bpr.rc_model['Atot']
    a_m = bpr.rc_model['Am']
    a_w = bpr.rc_model['Aw']

    f_sm = a_m / (a_t - a_w)

    return f_sm

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 2.1.5
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def calc_theta_ea(tsd, t):

    # get values
    m_v_sys = tsd['m_ve_mech'][t]  # mass flow rate mechanical ventilation
    m_v_w = tsd['m_ve_window'][t]  # mass flow rate window ventilation
    m_v_inf = tsd['m_ve_inf_simple'][t]  # mass flow rate infiltration
    theta_v_sys = tsd['theta_ve_mech'][t]  # supply air temperature of mechanical ventilation (i.e. after HEX)
    theta_e = tsd['T_ext'][t]  # outdoor air temperature

    # (21) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # adjusted for mass flows instead of volume flows and simplified by (rho*cp)/(rho*cp) = 1
    # Gabriel Happle 01.12.2016

    theta_ea = (m_v_sys * theta_v_sys + (m_v_w + m_v_inf) * theta_e) / (m_v_sys + m_v_w + m_v_inf)

    return theta_ea


def calc_theta_ec(tsd, t):

    # WORKAROUND
    theta_ec = tsd['T_ext'][t]  # TODO: adjust to actual calculation

    # (22) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    # theta_ec = a_j_l * u_j * theta_e_j / h_ec

    # TODO: this formula in the future should take specific properties of the location of the building into account
    # e.g. adiabatic building elements with U = 0

    # TODO: theta_e_j is depending on adjacent space to surface (outdoor, adiabatic, ground, etc.)

    return theta_ec


def calc_theta_em(tsd, t):

    # WORKAROUND
    theta_em = tsd['T_ext'][t]  # TODO: adjust to actual calculation

    # (23) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    # theta_em = h_j_em * theta_e_j / h_em

    # TODO: this formula in the future should take specific properties of the location of the building into account
    # e.g. adiabatic building elements with U = 0

    # TODO: theta_e_j is depending on adjacent space to surface (outdoor, adiabatic, ground, etc.)

    return theta_em


def calc_theta_e_star():

    # TODO: To be addressed in issue #446

    # (24) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    #

    # standard values for calculation
    h_e_load_and_temp = 13.5  # (W/m2K) for load and temperature calculation
    h_e_energy = 23  # (W/m2K) for energy demand calculation

    f_r_roof = 1  # (-)
    f_r_wall = 0.5  # (-)
    h_r = 5.5  # (-)
    delta_t_er = 11  # (K)

    # if is_roof(surface):
        #f_r = f_r_roof
    #elif is_wall(surface):
        #f_r = f_r_wall
    #else:
        #raise()

    #if is_energy_calculation(calculation):
       # h_e = h_e_energy
    #elif is_load_or_temp_calculation(calculation):
       # h_e = h_e_load_and_temp
    #else:
        #raise()


    #theta_e_star = theta_e + (alpha_s * i_s_i) / h_e - (f_r * h_r * epsilon_0 * delta_t_er) / h_e

    #return theta_e_star

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 2.1.6
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def calc_theta_m_t(phi_hc_cv, phi_hc_r, bpr, tsd, t):

    # get values
    theta_m_t_1 = tsd['theta_m'][t-1] if not np.isnan(tsd['theta_m'][t - 1]) else tsd['T_ext'][t - 1]
    c_m = bpr.rc_model['Cm']
    h_3 = calc_h_3(bpr, tsd, t)
    h_em = calc_h_em(bpr)
    phi_m_tot = calc_phi_m_tot(phi_hc_cv, phi_hc_r, bpr, tsd, t)

    # (25) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    theta_m_t = (theta_m_t_1 * (c_m - 0.5 * (h_3 + h_em)) + phi_m_tot) / (c_m + 0.5 * (h_3 + h_em))

    return theta_m_t


def calc_h_1(bpr, tsd, t):

    # get values
    h_ea = calc_h_ea(tsd, t)
    h_ac = calc_h_ac(bpr)

    # (26) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    h_1 = 1 / (1 / h_ea + 1 / h_ac)

    return h_1


def calc_h_2(bpr, tsd, t):

    # get values
    h_1 = calc_h_1(bpr, tsd, t)
    h_ec = calc_h_ec(bpr)

    # (27) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    h_2 = h_1 + h_ec

    return h_2


def calc_h_3(bpr, tsd, t):

    # get values
    h_2 = calc_h_2(bpr, tsd, t)
    h_mc = calc_h_mc(bpr)

    # (28) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    h_3 = 1 / (1 / h_2 + 1 / h_mc)

    return h_3


def calc_phi_m_tot(phi_hc_cv, phi_hc_r, bpr, tsd, t):

    # get values
    phi_m = calc_phi_m(phi_hc_r, bpr, tsd, t)
    h_em = calc_h_em(bpr)
    theta_em = calc_theta_em(tsd, t)
    h_3 = calc_h_3(bpr, tsd, t)
    phi_c = calc_phi_c(phi_hc_r, bpr, tsd, t)
    h_ec = calc_h_ec(bpr)
    theta_ec = calc_theta_ec(tsd, t)
    h_1 = calc_h_1(bpr, tsd, t)
    phi_a = calc_phi_a(phi_hc_cv, bpr, tsd, t)
    h_ea = calc_h_ea(tsd, t)
    theta_ea = calc_theta_ea(tsd, t)
    h_2 = calc_h_2(bpr, tsd, t)

    # (29) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    phi_m_tot = phi_m + h_em * theta_em + (h_3 * (phi_c + h_ec * theta_ec + h_1 * (phi_a / h_ea + theta_ea))) / h_2

    return phi_m_tot


def calc_theta_m(phi_hc_cv, phi_hc_r, bpr, tsd, t):

    # get values
    theta_m_t = calc_theta_m_t(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    theta_m_t_1 = tsd['theta_m'][t-1] if not np.isnan(tsd['theta_m'][t - 1]) else tsd['T_ext'][t - 1]

    # (30) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    theta_m = (theta_m_t + theta_m_t_1) / 2

    return theta_m


def calc_theta_c(phi_hc_cv, phi_hc_r, bpr, tsd, t):

    # get values
    h_mc = calc_h_mc(bpr)
    theta_m = calc_theta_m(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    phi_c = calc_phi_c(phi_hc_r, bpr, tsd, t)
    h_ec = calc_h_ec(bpr)
    theta_ec = calc_theta_ec(tsd, t)
    h_1 = calc_h_1(bpr, tsd, t)
    phi_a = calc_phi_a(phi_hc_cv, bpr, tsd, t)
    h_ea = calc_h_ea(tsd, t)
    theta_ea = calc_theta_ea(tsd, t)

    # (31) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    theta_c = (h_mc * theta_m + phi_c + h_ec * theta_ec + h_1 * (phi_a / h_ea + theta_ea)) / (h_mc + h_ec + h_1)

    return theta_c


def calc_theta_a(phi_hc_cv, phi_hc_r, bpr, tsd, t):

    # get values
    h_ac = calc_h_ac(bpr)
    theta_c = calc_theta_c(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    h_ea = calc_h_ea(tsd, t)
    theta_ea = calc_theta_ea(tsd, t)
    phi_a = calc_phi_a(phi_hc_cv, bpr, tsd, t)

    # (32) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    theta_a = (h_ac * theta_c + h_ea * theta_ea + phi_a) / (h_ac + h_ea)

    return theta_a


def calc_theta_o(phi_hc_cv, phi_hc_r, bpr, tsd, t):

    # get values
    theta_a = calc_theta_a(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    theta_c = calc_theta_c(phi_hc_cv, phi_hc_r, bpr, tsd, t)

    # (33) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    theta_o = theta_a * 0.31 + theta_c * 0.69

    return theta_o

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 2.2.7
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def calc_phi_hc_cv(phi_hc, f_hc_cv):

    # (58) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    phi_hc_cv = f_hc_cv * phi_hc

    return phi_hc_cv


def calc_phi_hc_r(phi_hc, f_hc_cv):

    # (59) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    phi_hc_r = (1 - f_hc_cv) * phi_hc

    return phi_hc_r


def calc_theta_tabs_su():

    # TODO: to be addressed in issue #444

    # (60) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # theta_tabs_su = theta_tabs_su_max - (theta_tabs_su_max - theta_tabs_su_min) * (theta_e -  theta_e_min)/(theta_e_max - theta_e_min)

    return None


def calc_phi_tabs():

    # TODO: to be addressed in issue #444

    # (61) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011
    # phi_tabs = h_tabs * (theta_tabs_su - theta_m_t_1)

    return None


def calc_h_tabs():

    # TODO: to be addressed in issue #444

    # (62) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    # typical values
    # a_tabs = 0.8 * a_ngf
    # r_tabs = 0.08  # (m2K/W)

    # h_tabs = a_tabs / r_tabs

    return None


def calc_phi_m_tot_tabs():

    # TODO: to be addressed in issue #444

    # (63) in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    # phi_m_tot = calc_phi_m_tot() + phi_tabs

    return None


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 2.3.2
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def calc_rc_model_temperatures_no_heating_cooling(bpr, tsd, t):

    # no heating or cooling
    phi_hc_cv = 0
    phi_hc_r = 0

    rc_model_temp = calc_rc_model_temperatures(phi_hc_cv, phi_hc_r, bpr, tsd, t)

    return rc_model_temp


def calc_rc_model_temperatures(phi_hc_cv, phi_hc_r, bpr, tsd, t):
    # calculate node temperatures of RC model
    theta_m = calc_theta_m(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    theta_c = calc_theta_c(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    theta_a = calc_theta_a(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    theta_o = calc_theta_o(phi_hc_cv, phi_hc_r, bpr, tsd, t)
    rc_model_temp = {'theta_m': theta_m, 'theta_c': theta_c, 'theta_a': theta_a, 'theta_o': theta_o}
    return rc_model_temp


def calc_rc_model_temperatures_heating(phi_hc, bpr, tsd, t):

    # lookup convection factor for heating/cooling system
    f_hc_cv = lookup_f_hc_cv_heating(bpr)

    # convective and radiative fractions of heating system
    phi_hc_cv = calc_phi_hc_cv(phi_hc, f_hc_cv)
    phi_hc_r = calc_phi_hc_r(phi_hc, f_hc_cv)

    rc_model_temp = calc_rc_model_temperatures(phi_hc_cv, phi_hc_r, bpr, tsd, t)

    return rc_model_temp


def calc_rc_model_temperatures_cooling(phi_hc, bpr, tsd, t):
    # lookup convection factor for heating/cooling system
    f_hc_cv = lookup_f_hc_cv_cooling(bpr)

    # convective and radiative fractions of heating system
    phi_hc_cv = calc_phi_hc_cv(phi_hc, f_hc_cv)
    phi_hc_r = calc_phi_hc_r(phi_hc, f_hc_cv)

    rc_model_temp = calc_rc_model_temperatures(phi_hc_cv, phi_hc_r, bpr, tsd, t)

    return rc_model_temp


def has_heating_demand(bpr, tsd, t):

    if np.isnan(tsd['ta_hs_set'][t]):
        # no set point = system off
        return False

    elif not np.isnan(tsd['ta_hs_set'][t]):

        # calculate temperatures
        rc_model_temp = calc_rc_model_temperatures_no_heating_cooling(bpr, tsd, t)

        # check temperatures
        if rc_model_temp['theta_a'] >= tsd['ta_hs_set'][t]:
            # if temperature w/o conditioning is higher
            return False
        elif rc_model_temp['theta_a'] < tsd['ta_hs_set'][t]:
            # if temperature w/o conditioning is lower than heating temperature set point
            return True
        else:
            raise ValueError(rc_model_temp['theta_a'], tsd['ta_hs_set'][t])


def has_cooling_demand(bpr, tsd, t):

    if np.isnan(tsd['ta_cs_set'][t]):
        # no set point = system off
        return False

    elif not np.isnan(tsd['ta_cs_set'][t]):

        # calculate temperatures
        rc_model_temp = calc_rc_model_temperatures_no_heating_cooling(bpr, tsd, t)

        # calculate temperatures
        if rc_model_temp['theta_a'] <= tsd['ta_cs_set'][t]:
            # if temperature w/o conditioning is lower than cooling set point temperature
            return False
        elif rc_model_temp['theta_a'] > tsd['ta_cs_set'][t]:
            # if temperature w/o conditioning is higher than cooling set point temperature
            return True
        else:
            raise


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3.8.1
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

f_hc_cv_heating_system = {'T1' : 1, 'T2' : 1, 'T3' : 1, 'T4' : 0.5}  # T1 = radiator, T2 = radiator, T3 = AC, T4 = floor heating #TODO: add heating ceiling
f_hc_cv_cooling_system = {'T1' : 0.5, 'T2' : 1, 'T3' : 1}  # T1 = ceiling cooling, T2 mini-split AC, T3 = AC #TODO: add floor cooling


def lookup_f_hc_cv_heating(bpr):

    # 3.1.8.1 in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    # look up factor
    f_hc_cv = f_hc_cv_heating_system[bpr.hvac['type_hs']]

    return f_hc_cv


def lookup_f_hc_cv_cooling(bpr):

    # 3.1.8.1 in SIA 2044 / Korrigenda C1 zum Merkblatt SIA 2044:2011 / Korrigenda C2 zum Mekblatt SIA 2044:2011

    # look up factor
    f_hc_cv = f_hc_cv_cooling_system[bpr.hvac['type_cs']]

    return f_hc_cv