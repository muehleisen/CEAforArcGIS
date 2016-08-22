"""
==================================================
photovoltaic
==================================================

"""


from __future__ import division
import numpy as np
import pandas as pd
from math import *
from cea.utilities import epwreader
from cea.utilities import solar_equations
from cea.technologies.solar_collector import optimal_angle_and_tilt, calc_groups, Calc_incidenteangleB

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

"""
============================
PV electricity generation
============================

"""

def calc_PV(locator, radiation_csv, metadata_csv, latitude, longitude, year, gv, weather_path):

    # weather data
    weather_data = epwreader.epw_reader(weather_path)
    # solar properties
    g, Sz, Az, ha, trr_mean, worst_sh, worst_Az = solar_equations.calc_sun_properties(latitude, longitude, weather_data,
                                                                                       gv)
    #
    # select sensor point with sufficient solar radiation
    sensor_names_roof, sensor_names_wall, sensors_rad, sensors_metadata = calc_radiation_sensor_selection_weatherdata(weather_data, radiation_csv, metadata_csv, gv)
    radiation_roof_clean = sensors_rad[sensor_names_roof]
    radiation_wall_clean = sensors_rad[sensor_names_wall]

    # get only datapoints with aminimum 50 W/m2 of radiation for energy production
    radiation_roof_clean[radiation_roof_clean[:] <= 50] = 0
    radiation_wall_clean[radiation_roof_clean[:] <= 50] = 0
    #radiation_clean = radiation_csv.loc[radiation['sensor_id'].isin(metadata_clean.sensor_id)]


    # calculate optimal angle and tilt for panels
    optimal_angle_and_tilt(metadata, latitude, worst_sh, worst_Az, trr_mean, gv.grid_side,
                            gv.module_lenght_PV, gv.angle_north, Min_Isol, Max_Isol)
    #
    #Number_groups, hourlydata_groups, number_points, prop_observers = calc_groups(radiation_clean, metadata_clean)
    #
    #results, Final = Calc_pv_generation(gv.type_PVpanel, hourlydata_groups, Number_groups, number_points,
    #                                         prop_observers, weather_data,g, Sz, Az, ha, latitude, gv.misc_losses)
    #
    # Final.to_csv(locator.PV_result(), index=True, float_format='%.2f')
    return

def calc_radiation_sensor_selection_weatherdata(weather_data, radiation_csv, metadata_csv, gv):
    # get max radiation potential from global horizontal radiation
    yearly_horizontal_rad = weather_data.glohorrad_Whm2.sum()  # [Wh/m2/year]

    # read radiation file
    sensors_rad = pd.read_csv(radiation_csv)
    sensors_metadata = pd.read_csv(metadata_csv)
    # add new row with yearly radiation of each sensor point
    sensors_rad = sensors_rad.append(sensors_rad.sum(0), ignore_index=True)
    index_totals = sensors_rad.shape[0] - 1
    # index_totals = index_totals_0[0] - 1

    # get only data points with production beyond min_production
    max_yearly_radiation = yearly_horizontal_rad.max()  # Maximum solar radiation at each building [Wh/m2/year]

    min_yearly_production_walls = max_yearly_radiation * gv.min_production * 0.5
    min_yearly_production_roofs = max_yearly_radiation * gv.min_production

    # join metadata names and fac_type
    face_type = sensors_metadata[['fac_type', 'bui_fac_sen']].set_index('bui_fac_sen').T
    sensors_rad = sensors_rad.append(face_type, ignore_index=True)

    sensor_names_selection = sensors_rad.ix[index_totals]
    sensor_names_faces_types = sensors_rad.ix[index_totals + 1]

    names_roof = sensor_names_faces_types[sensor_names_faces_types == 'roof'].index.values
    names_walls = sensor_names_faces_types[sensor_names_faces_types == 'wall'].index.values

    sensor_names_roof = sensor_names_selection[names_roof][
        sensor_names_selection[names_roof] > min_yearly_production_roofs].index.values
    sensor_names_wall = sensor_names_selection[names_walls][
        sensor_names_selection[names_walls] > min_yearly_production_walls].index.values

    return sensor_names_roof, sensor_names_wall, sensors_rad, sensors_metadata

def calc_radiation_sensor_selection(weather_data, radiation_csv, metadata_csv, gv):
    # read radiation file
    sensors_rad = pd.read_csv(radiation_csv)
    sensors_metadata = pd.read_csv(metadata_csv)
    # add new row with yearly radiation of each sensor point
    sensors_rad = sensors_rad.append(sensors_rad.sum(0), ignore_index=True)
    index_totals = sensors_rad.shape[0] - 1
    # index_totals = index_totals_0[0] - 1

    # get only data points with production beyond min_production
    max_yearly_radiation = sensors_rad.ix[index_totals].max()  # Maximum solar radiation at each building [Wh/m2/year]

    min_yearly_production_walls = max_yearly_radiation * gv.min_production * 0.5
    min_yearly_production_roofs = max_yearly_radiation * gv.min_production

    # join metadata names and fac_type
    face_type = sensors_metadata[['fac_type', 'bui_fac_sen']].set_index('bui_fac_sen').T
    sensors_rad = sensors_rad.append(face_type, ignore_index=True)

    sensor_names_selection = sensors_rad.ix[index_totals]
    sensor_names_faces_types = sensors_rad.ix[index_totals + 1]

    names_roof = sensor_names_faces_types[sensor_names_faces_types == 'roof'].index.values
    names_walls = sensor_names_faces_types[sensor_names_faces_types == 'wall'].index.values

    sensor_names_roof = sensor_names_selection[names_roof][
        sensor_names_selection[names_roof] > min_yearly_production_roofs].index.values
    sensor_names_wall = sensor_names_selection[names_walls][
        sensor_names_selection[names_walls] > min_yearly_production_walls].index.values
    return sensor_names_roof, sensor_names_wall


def Calc_pv_generation(type_panel, hourly_radiation, Number_groups, number_points, prop_observers, weather_data,
                       g, Sz, Az, ha, latitude, misc_losses):


    lat = radians(latitude)
    g_vector = np.radians(g)
    ha_vector = np.radians(ha)
    Sz_vector = np.radians(Sz)
    Az_vector = np.radians(Az)
    result = list(range(Number_groups))
    areagroups = list(range(Number_groups))
    Sum_PV = np.zeros(8760)

    n = 1.526 #refractive index of galss
    Pg = 0.2 # ground reflectance
    K = 0.4 # extinction coefficien
    eff_nom,NOCT,Bref,a0,a1,a2,a3,a4,L  = calc_properties_PV(type_panel)

    for group in range(Number_groups):
        teta_z = prop_observers.loc[group,'aspect'] #azimuth of paneles of group
        areagroup = prop_observers.loc[group,'area_netpv']*number_points[group]
        tilt_angle = prop_observers.loc[group,'slope'] #tilt angle of panels
        radiation = pd.DataFrame({'I_sol':hourly_radiation[group]}) #choose vector with all values of Isol
        radiation['I_diffuse'] = weather_data.ratio_diffhout*radiation.I_sol #calculate diffuse radiation
        radiation['I_direct'] = radiation['I_sol'] - radiation['I_diffuse']  #direct radaition

        #to radians of properties - solar position and tilt angle
        tilt = radians(tilt_angle) #slope of panel
        teta_z = radians(teta_z) #azimuth of panel

        #calculate effective indicent angles necesary
        teta_vector = np.vectorize(Calc_incidenteangleB)(g_vector, lat, ha_vector, tilt, teta_z)
        teta_ed, teta_eg  = Calc_diffuseground_comp(tilt)

        results = np.vectorize(Calc_Sm_PV)(weather_data.drybulb_C,radiation.I_sol, radiation.I_direct, radiation.I_diffuse, tilt,
                                              Sz_vector, teta_vector, teta_ed, teta_eg,
                                              n, Pg, K,NOCT,a0,a1,a2,a3,a4,L)


        result[group] = np.vectorize(Calc_PV_power)(results[0], results[1], eff_nom, areagroup, Bref,misc_losses)
        areagroups[group] = areagroup

        Sum_PV = Sum_PV + result[group]

    Final = pd.DataFrame({'PV_kWh':Sum_PV,'Area':sum(areagroups)})
    return result, Final


def Calc_diffuseground_comp(tilt_radians):
    """

    Parameters
    ----------
    tilt_radians

    Returns
    -------
    teta_ed: groups-reflected radiation
    teta_eg: diffuse radiation

    References
    ----------
    Duffie, J. A. and Beckman, W. A. (2013) Radiation Transmission through Glazing: Absorbed Radiation, in
    Solar Engineering of Thermal Processes, Fourth Edition, John Wiley & Sons, Inc., Hoboken, NJ, USA.
    doi: 10.1002/9781118671603.ch5

    """
    tilt = degrees(tilt_radians)
    teta_ed = 59.68 - 0.1388 * tilt + 0.001497 * tilt ** 2  # angle in degrees
    teta_eG = 90 - 0.5788 * tilt + 0.002693 * tilt ** 2  # angle in degrees
    return radians(teta_ed), radians(teta_eG)

def Calc_Sm_PV(te, I_sol, I_direct, I_diffuse, tilt, Sz, teta, tetaed, tetaeg,
               n, Pg, K, NOCT, a0, a1, a2, a3, a4, L):
    """
    To calculate the absorbed solar radiation on tilted surface.

    Parameters
    ----------
    te
    I_sol
    I_direct
    I_diffuse
    tilt
    Sz
    teta
    tetaed
    tetaeg
    n
    Pg
    K
    NOCT
    a0
    a1
    a2
    a3
    a4
    L

    Returns
    -------

    References
    ----------
    Duffie, J. A. and Beckman, W. A. (2013) Radiation Transmission through Glazing: Absorbed Radiation, in
    Solar Engineering of Thermal Processes, Fourth Edition, John Wiley & Sons, Inc., Hoboken, NJ, USA.
    doi: 10.1002/9781118671603.ch5

    """
    # ha is local solar time


    # calcualte ratio of beam radiation on a tilted plane
    # to avoid inconvergence when I_sol = 0
    lim1 = radians(0)
    lim2 = radians(90)
    lim3 = radians(89.999)

    if teta < lim1:
        teta = min(lim3, abs(teta))
    if teta >= lim2:
        teta = lim3

    if Sz < lim1:
        Sz = min(lim3, abs(Sz))
    if Sz >= lim2:
        Sz = lim3
    # Rb: ratio of beam radiation of tilted surface to that on horizontal surface
    Rb = cos(teta) / cos(Sz)  # Sz is Zenith angle

    # calculate the specific air mass, m
    m = 1 / cos(Sz)
    M = a0 + a1 * m + a2 * m ** 2 + a3 * m ** 3 + a4 * m ** 4

    # angle refractive  (aproximation accrding to Soteris A.)
    teta_r = asin(sin(teta) / n)  # in radians
    Ta_n = exp(-K * L) * (1 - ((n - 1) / (n + 1)) ** 2)
    # calculate parameters of anlge modifier #first for the direct radiation
    if teta < 1.5707:  # 90 degrees in radians
        part1 = teta_r + teta
        part2 = teta_r - teta
        Ta_B = exp((-K * L) / cos(teta_r)) * (
        1 - 0.5 * ((sin(part2) ** 2) / (sin(part1) ** 2) + (tan(part2) ** 2) / (tan(part1) ** 2)))
        kteta_B = Ta_B / Ta_n
    else:
        kteta_B = 0

    # angle refractive for diffuse radiation
    teta_r = asin(sin(tetaed) / n)  # in radians
    part1 = teta_r + tetaed
    part2 = teta_r - tetaed
    Ta_D = exp((-K * L) / cos(teta_r)) * (
    1 - 0.5 * ((sin(part2) ** 2) / (sin(part1) ** 2) + (tan(part2) ** 2) / (tan(part1) ** 2)))
    kteta_D = Ta_D / Ta_n

    # angle refractive for global radiatoon
    teta_r = asin(sin(tetaeg) / n)  # in radians
    part1 = teta_r + tetaeg
    part2 = teta_r - tetaeg
    Ta_eG = exp((-K * L) / cos(teta_r)) * (
    1 - 0.5 * ((sin(part2) ** 2) / (sin(part1) ** 2) + (tan(part2) ** 2) / (tan(part1) ** 2)))
    kteta_eG = Ta_eG / Ta_n

    # absorbed solar radiation
    S = M * Ta_n * (kteta_B * I_direct * Rb + kteta_D * I_diffuse * (1 + cos(tilt)) / 2 + kteta_eG * I_sol * Pg * (
    1 - cos(tilt)) / 2)  # in W/m2
    if S <= 0:  # when points are 0 and too much losses
        S = 0
    # temperature of cell
    Tcell = te + S * (NOCT - 20) / (800)

    return S, Tcell

def Calc_PV_power(S, Tcell, eff_nom, areagroup, Bref,misc_losses):
    """

    Parameters
    ----------
    S: absorbed radiation [W/m2]
    Tcell: cell temperature [degree]
    eff_nom
    areagroup: panel area [m2]
    Bref
    misc_losses: expected system loss

    Returns
    -------
    P: Power production [kWh]

    """
    P = eff_nom*areagroup*S*(1-Bref*(Tcell-25))*(1-misc_losses)/1000 # Osterwald, 1986) in kWatts
    return P

"""
============================
properties of module
============================

"""

def calc_properties_PV(type_PVpanel):
    if type_PVpanel == 1:#     # assuming only monocrystalline panels.
        eff_nom = 0.16 # GTM 2014
        NOCT = 43.5 # Fanney et al.,
        Bref = 0.0035  # Fuentes et al.,Luque and Hegedus, 2003).
        a0 = 0.935823
        a1 = 0.054289
        a2 = -0.008677
        a3 = 0.000527
        a4 = -0.000011
        L = 0.002 # glazing tickness
    if type_PVpanel == 2:#     # polycristalline
        eff_nom = 0.15 # GTM 2014
        NOCT = 43.9 # Fanney et al.,
        Bref = 0.0044
        a0 = 0.918093
        a1 = 0.086257
        a2 = -0.024459
        a3 = 0.002816
        a4 = -0.000126
        L = 0.002 # glazing tickness
    if type_PVpanel == 3:#     # amorphous
        eff_nom = 0.08  # GTM 2014
        NOCT = 38.1 # Fanney et al.,
        Bref = 0.0026
        a0 = 1.10044085
        a1 = -0.06142323
        a2 = -0.00442732
        a3 = 0.000631504
        a4 = -0.000019184
        L = 0.0002 # glazing tickness

    return eff_nom,NOCT,Bref,a0,a1,a2,a3,a4,L


"""
============================
investment and maintenance costs
============================

"""



def calc_Cinv_PV(P_peak):
    """
    P_peak in kW
    result in CHF
    Lifetime 20 y
    """
    if P_peak < 10:
        InvCa = 3500.07 * P_peak /20
    else:
        InvCa = 2500.07 * P_peak /20

    return InvCa # [CHF/y]

"""
============================
test
============================

"""

def test_photovoltaic():
    import cea.inputlocator
    import cea.globalvar

    locator = cea.inputlocator.InputLocator(r'C:\reference-case-zug\baseline')
    # for the interface, the user should pick a file out of of those in ...DB/Weather/...
    weather_path = locator.get_default_weather()
    radiation = locator.get_radiation(building_name='B2368593')
    radiation_metadata = locator.get_radiation_metadata(building_name='B2368593')
    gv = cea.globalvar.GlobalVariables()

    calc_PV(locator=locator, radiation_csv= radiation, metadata_csv= radiation_metadata, latitude=46.95240555555556, longitude=7.439583333333333, year=2014, gv=gv,
            weather_path=weather_path)


if __name__ == '__main__':
    test_photovoltaic()