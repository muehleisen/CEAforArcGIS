"""
==================================================
photovoltaic
==================================================

"""


from __future__ import division
import numpy as np
import pandas as pd
import arcpy
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
    # select sensor point with sufficient solar radiation
    max_yearly_radiation, min_yearly_production, sensors_rad_clean, sensors_metadata_clean = calc_radiation_sensor_selection_weatherdata(weather_data, radiation_csv, metadata_csv, gv)

    # calculate optimal angle and tilt for panels
    sensors_metadata_cat = optimal_angle_and_tilt(sensors_metadata_clean, latitude, worst_sh, worst_Az, trr_mean, gv.grid_side,
                            gv.module_length_PV, gv.angle_north, min_yearly_production, max_yearly_radiation)

    Number_groups, hourlydata_groups, number_points, prop_observers = calc_groups(sensors_rad_clean, sensors_metadata_cat)

    results, Final = Calc_pv_generation(gv.type_PVpanel, hourlydata_groups, Number_groups, number_points,
                                             prop_observers, weather_data,g, Sz, Az, ha, latitude, gv.misc_losses)

    #Final.to_csv(locator.PV_result(), index=True, float_format='%.2f')
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

    # set value for min yearly production
    max_yearly_radiation = yearly_horizontal_rad
    min_yearly_production = max_yearly_radiation * gv.min_production

    # keep sensors if allow pv installation
    if gv.pvonroof == True:
        sensors_metadata = sensors_metadata
    else:
        sensors_metadata = sensors_metadata[sensors_metadata.fac_type != 'roof']
    if gv.pvonwall == True:
        sensors_metadata = sensors_metadata
    else:
        sensors_metadata = sensors_metadata[sensors_metadata.fac_type != 'wall']

    # join total radiation to sensor_metadata
    sensors_metadata = sensors_metadata.set_index('bui_fac_sen')
    sensors_metadata['total_rad']= sensors_rad.iloc[index_totals]

    # keep sensors above min production in sensors_rad
    # FIXME: change 10000 back to min_yearly_production when yearly data is available
    sensors_metadata_clean = sensors_metadata[sensors_metadata.total_rad > 10000]
    sensors_rad_clean = sensors_rad[sensors_metadata_clean.index.tolist()]

    # eliminate points when hourly production < 50 W/m2
    sensors_rad_clean[sensors_rad_clean[:] <= 50] = 0

    return max_yearly_radiation, min_yearly_production, sensors_rad_clean, sensors_metadata_clean

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
optimal angle and tilt
============================

"""

def optimal_angle_and_tilt(sensors_metadata_clean, latitude, worst_sh, worst_Az, transmissivity,
                           grid_side, module_length, angle_north, Min_Isol, Max_Isol):

    def Calc_optimal_angle(teta_z, latitude, transmissivity):
        """

        Parameters
        ----------
        teta_z: surface azimuth, 0 degree south (east negative, west positive)
        latitude
        transmissivity

        Returns
        -------
        S.W.Quinn, B.Lehman.A simple formula for estimating the optimum tilt angles of photovoltaic panels.
        2013 IEEE 14th Work Control Model Electron, Jun, 2013, pp.1-8
        """
        if transmissivity <= 0.15:
            gKt = 0.977
        elif 0.15 < transmissivity <= 0.7:
            gKt = 1.237 - 1.361 * transmissivity
        else:
            gKt = 0.273
        Tad = 0.98
        Tar = 0.97
        Pg = 0.2  # ground reflectance of 0.2
        l = radians(latitude)
        a = radians(teta_z)  # this is surface azimuth
        b = atan((cos(a) * tan(l)) * (1 / (1 + ((Tad * gKt - Tar * Pg) / (2 * (1 - gKt))))))
        return b  #radians

    def Calc_optimal_spacing(Sh, Az, tilt_angle, module_length):
        h = module_length * sin(radians(tilt_angle))
        D1 = h / tan(radians(Sh))
        D = max(D1 * cos(radians(180 - Az)), D1 * cos(radians(Az - 180)))
        return D

    def Calc_categoriesroof(teta_z, B, GB, Max_Isol):
        B = degrees(B)
        if -122.5 < teta_z <= -67:
            CATteta_z = 1
        elif -67 < teta_z <= -22.5:
            CATteta_z = 3
        elif -22.5 < teta_z <= 22.5:
            CATteta_z = 5
        elif 22.5 < teta_z <= 67:
            CATteta_z = 4
        elif 67 <= teta_z <= 122.5:
            CATteta_z = 2
        else:
            CATteta_z = None
            print('teta_z not in expected range')

        if 0 < B <= 5:
            CATB = 1  # flat roof
        elif 5 < B <= 15:
            CATB = 2  # tilted 25 degrees
        elif 15 < B <= 25:
            CATB = 3  # tilted 25 degrees
        elif 25 < B <= 40:
            CATB = 4  # tilted 25 degrees
        elif 40 < B <= 60:
            CATB = 5  # tilted 25 degrees
        elif B > 60:
            CATB = 6  # tilted 25 degrees
        else:
            CATB = None
            print('B not in expected range')

        GB_percent = GB / Max_Isol
        if 0 < GB_percent <= 0.25:
            CATGB = 1
        elif 0.25 < GB_percent <= 0.50:
            CATGB = 2
        elif 0.50 < GB_percent <= 0.75:
            CATGB = 3
        elif 0.75 < GB_percent <= 0.90:
            CATGB = 4
        elif 0.90 < GB_percent <= 1:
            CATGB = 5
        else:
            CATGB = None
            print('GB not in expected range')

        return CATteta_z, CATB, CATGB

        # calculate values for flat roofs Slope < 5 degrees.
    optimal_angle_flat = Calc_optimal_angle(0, latitude, transmissivity)
    optimal_spacing_flat = Calc_optimal_spacing(worst_sh, worst_Az, optimal_angle_flat, module_length)
    sensors_metadata_clean['B'] = np.where(sensors_metadata_clean['slope'] >= 5, sensors_metadata_clean['slope'], optimal_angle_flat)
    sensors_metadata_clean['array_s'] = np.where(sensors_metadata_clean['slope'] >= 5, 0, optimal_spacing_flat)
    sensors_metadata_clean['teta_z'] = np.where(sensors_metadata_clean['slope'] >= 5, sensors_metadata_clean['teta_z'], 0)
    #sensors_metadata_clean['area_netpv'] = (grid_side - sensors_metadata_clean.array_s) / [cos(x) for x in sensors_metadata_clean.B] * grid_side
    sensors_metadata_clean['area_netpv'] = module_length**2*(sensors_metadata_clean.sen_area / module_length*(sensors_metadata_clean.array_s/2 + module_length*[cos(x) for x in sensors_metadata_clean.B]))

    # categorize the sensors by
    result = np.vectorize(Calc_categoriesroof)(sensors_metadata_clean.teta_z, sensors_metadata_clean.B,
                                               sensors_metadata_clean.total_rad, Max_Isol)
    sensors_metadata_clean['CATteta_z'] = result[0]
    sensors_metadata_clean['CATB'] = result[1]
    sensors_metadata_clean['CATGB'] = result[2]
    return sensors_metadata_clean

def calc_groups(sensors_rad_clean, sensors_metadata_cat):
    # add categories to sensors_rad
    #sensors_rad_clean = sensors_rad_clean.append(sensors_metadata_cat['CATB'])
    #sensors_rad_clean = sensors_rad_clean.append(sensors_metadata_cat['CATGB'])
    #sensors_rad_clean = sensors_rad_clean.append(sensors_metadata_cat['CATteta_z'])

    # calculate number of optima groups as number of optimal combiantions.
    groups_ob = sensors_metadata_cat.groupby(['CATB', 'CATGB', 'CATteta_z'])
    prop_observers = groups_ob.mean().reset_index()
    prop_observers = pd.DataFrame(prop_observers)
    number_groups = groups_ob.size().count()
    list = groups_ob.groups.values()
    for x in range(0,number_groups):
        sensors_group = sensors_rad_clean[list[x]]
    groups_ob = sensors_rad_clean.groupby(['CATB', 'CATGB', 'CATteta_z'])
    hourlydata_groups = groups_ob.mean().reset_index()
    hourlydata_groups = pd.DataFrame(hourlydata_groups)
    Number_pointsgroup = groups_ob.size().reset_index()
    number_points = Number_pointsgroup[0]    # number of sensors in each group

    hourlydata_groups = hourlydata_groups.drop({'ID', 'GB', 'grid_code', 'pointid', 'array_s', 'area_netpv', 'aspect',
                                                'slope', 'CATB', 'CATGB', 'CATteta_z'}, axis=1).transpose().reindex(
        axis=1)  # vector with radiation points of group
    hourlydata_groups['newindex'] = hourlydata_groups.index
    hourlydata_groups['newindex'] = hourlydata_groups.newindex.apply(lambda x: re.findall('\d+', x))
    hourlydata_groups.index = range(8760)
    for hour in range(8760):
        hourlydata_groups.loc[hour, 'newindex'] = int(hourlydata_groups.loc[hour, 'newindex'][0])

    hourlydata_groups.set_index('newindex', inplace=True)
    hourlydata_groups.sort_index(inplace=True)
    hourlydata_groups.index = range(8760)

    return Number_groups, hourlydata_groups, number_points, prop_observers

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