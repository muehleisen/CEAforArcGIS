"""
===========================
Analytical energy demand model algorithm
===========================

"""
from __future__ import division

import multiprocessing as mp
import os

import pandas as pd
import time

import cea.globalvar
import cea.inputlocator
from cea.demand import occupancy_model
from cea.demand import thermal_loads
from cea.demand.thermal_loads import BuildingProperties
from cea.utilities import epwreader

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Daren Thomas", "Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

"""
=========================================
demand calculation
=========================================
"""


def demand_calculation(locator, weather_path, gv):
    """
    Algorithm to calculate the hourly demand of energy services in buildings
    using the integrated model of Fonseca et al. 2015. Applied energy.
    (http://dx.doi.org/10.1016/j.apenergy.2014.12.068)

    PARAMETERS
    ----------
    :param locator: An InputLocator to locate input files
    :type locator: cea.inputlocator.InputLocator

    :param weather_path: A path to the EnergyPlus weather data file (.epw)
    :type weather_path: str

    :param gv: A GlobalVariable (context) instance
    :type gv: cea.globalvar.GlobalVariable


    RETURNS
    -------

    :returns: None
    :rtype: NoneType


    INPUT / OUTPUT FILES
    --------------------

    - get_radiation: c:\reference-case\baseline\outputs\data\solar-radiation\radiation.csv
    - get_surface_properties: c:\reference-case\baseline\outputs\data\solar-radiation\properties_surfaces.csv
    - get_building_geometry: c:\reference-case\baseline\inputs\building-geometry\zone.shp
    - get_building_hvac: c:\reference-case\baseline\inputs\building-properties\technical_systems.shp
    - get_building_thermal: c:\reference-case\baseline\inputs\building-properties\thermal_properties.shp
    - get_building_occupancy: c:\reference-case\baseline\inputs\building-properties\occupancy.shp
    - get_building_architecture: c:\reference-case\baseline\inputs\building-properties\architecture.shp
    - get_building_age: c:\reference-case\baseline\inputs\building-properties\age.shp
    - get_building_comfort: c:\reference-case\baseline\inputs\building-properties\indoor_comfort.shp
    - get_building_internal: c:\reference-case\baseline\inputs\building-properties\internal_loads.shp


    SIDE EFFECTS
    ------------

    Produces a demand file per building and a total demand file for the whole zone of interest.

    B153767T.csv: csv file for every building with hourly demand data
    Total_demand.csv: csv file of yearly demand data per buidling.
    """
    if not os.path.exists(locator.get_radiation()) or not os.path.exists(locator.get_surface_properties()):
        raise ValueError("No radiation file found in scenario. Consider running radiation script first.")

    t0 = time.clock()

    date = pd.date_range(gv.date_start, periods=8760, freq='H')

    # weather model
    weather_data = epwreader.epw_reader(weather_path)[['drybulb_C', 'relhum_percent', 'windspd_ms', 'skytemp_C']]

    # building properties model
    building_properties = BuildingProperties(locator, gv)

    # schedules model
    list_uses = list(building_properties._prop_occupancy.drop('PFloor', axis=1).columns)
    schedules = occupancy_model.schedule_maker(date, locator, list_uses)
    schedules_dict = {'list_uses': list_uses, 'schedules': schedules}

    # in case gv passes a list of specific buildings to simulate.
    if gv.simulate_building_list:
        list_building_names = gv.simulate_building_list
    else:
        list_building_names = building_properties.list_building_names()

    # demand
    if gv.multiprocessing and mp.cpu_count() > 1:
        thermal_loads_all_buildings_multiprocessing(building_properties, date, gv, locator, list_building_names,
                                                    schedules_dict, weather_data)
    else:
        thermal_loads_all_buildings(building_properties, date, gv, locator, list_building_names, schedules_dict,
                                    weather_data)

    if gv.print_totals:
        totals, time_series = gv.demand_writer.write_totals_csv(building_properties, locator)
        gv.log('done - time elapsed: %(time_elapsed).2f seconds', time_elapsed=time.clock() - t0)
        return totals, time_series

#=========================================
#multiple or single core calculation
#=========================================


def thermal_loads_all_buildings(building_properties, date, gv, locator, list_building_names, usage_schedules,
                                weather_data):
    num_buildings = len(list_building_names)
    for i, building in enumerate(list_building_names):
        bpr = building_properties[building]
        thermal_loads.calc_thermal_loads(
            building, bpr, weather_data, usage_schedules, date, gv, locator)
        gv.log('Building No. %(bno)i completed out of %(num_buildings)i: %(building)s', bno=i + 1,
               num_buildings=num_buildings, building=building)


def thermal_loads_all_buildings_multiprocessing(building_properties, date, gv, locator, list_building_names, usage_schedules,
                                                weather_data):
    pool = mp.Pool()
    gv.log("Using %i CPU's" % mp.cpu_count())
    joblist = []
    num_buildings = len(list_building_names)
    for building in list_building_names:
        bpr = building_properties[building]
        job = pool.apply_async(thermal_loads.calc_thermal_loads,
                               [building, bpr, weather_data, usage_schedules, date, gv, locator])
        joblist.append(job)
    for i, job in enumerate(joblist):
        job.get(240)
        gv.log('Building No. %(bno)i completed out of %(num_buildings)i', bno=i + 1, num_buildings=num_buildings)
    pool.close()


#=========================================
#test
#=========================================


def run_as_script(scenario_path=None, weather_path=None):
    gv = cea.globalvar.GlobalVariables()
    if scenario_path is None:
        scenario_path = gv.scenario_reference
    locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)
    # for the interface, the user should pick a file out of of those in ...DB/Weather/...
    if weather_path is None:
        weather_path = locator.get_default_weather()

    gv.log('Running demand calculation for scenario %(scenario)s', scenario=scenario_path)
    gv.log('Running demand calculation with weather file %(weather)s', weather=weather_path)
    demand_calculation(locator=locator, weather_path=weather_path, gv=gv)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario', help='Path to the scenario folder')
    parser.add_argument('-w', '--weather', help='Path to the weather file')
    args = parser.parse_args()

    run_as_script(scenario_path=args.scenario, weather_path=args.weather)
