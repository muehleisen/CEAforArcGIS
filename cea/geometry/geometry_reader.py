# -*- coding: utf-8 -*-
"""
===========================
algorithms for manipulation of building geometry
===========================

"""

from __future__ import division
import math
import numpy as np
from geopandas import GeoDataFrame
import pandas as pd
import os

__author__ = "Paul Neitzel"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Paul Neitzel"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


"""
=========================================
Windows
=========================================
"""


def get_facade_area(locator):
    # data for one day to calculate fraction that faces the exterior
    n_shaded_frac_file = locator.get_sen_not_shaded()
    n_shaded_frac = pd.read_csv(n_shaded_frac_file, header=None).T

    # read building sensor id file
    bui_id_df_file = locator.get_bui_id_df()
    bui_id_df = pd.read_csv(bui_id_df_file)

    bui_id_df['ex_frac'] = n_shaded_frac
    bui_id_df['area_frac'] = bui_id_df["sen_area"].multiply(bui_id_df['ex_frac'], axis="index")

    # select vertical surfaces, considered <10% angle
    dir_z_limit = math.sin(10.0 / 180 * math.pi)
    sel_vertical = bui_id_df[bui_id_df['sen_dir_z'] < dir_z_limit]

    area_frac = sel_vertical[["bui", "area_frac"]].groupby(['bui']).sum().reset_index()
    area_frac.columns = ['Name', 'Awall_all']

    return area_frac


def create_windows(locator):
    # read face file
    bui_points_file = locator.get_building_points()
    bui_points = pd.read_csv(bui_points_file, header=None)
    bui_points.columns = ['bui', 'int', 'x', 'y', 'z', 'dir_x', 'dir_y', 'dir_z']

    # read building sensor id file
    bui_id_df_file = locator.get_bui_id_df()
    bui_id_df = pd.read_csv(bui_id_df_file)

    # data for one day to calculate fraction that faces the exterior
    n_shaded_frac_file = locator.get_sen_not_shaded()
    n_shaded_frac = pd.read_csv(n_shaded_frac_file, header=None).T
    bui_id_df['ex_frac'] = n_shaded_frac

    # initialize lists
    window_area = []
    window_height = []
    window_angle = []
    window_orientation = []
    window_bui_name = []

    # builing min level
    bui_min_z = bui_points[["bui", "z"]].groupby("bui").min().reset_index()
    # window to wall ratio
    architecture_path = locator.get_building_architecture()
    prop_architecture = GeoDataFrame.from_file(architecture_path).drop('geometry', axis=1).set_index('Name')

    # fraction facing the exterior
    frac_ex = bui_id_df[["ex_frac", 'bui_fac']].groupby("bui_fac").mean().reset_index()

    for i in range(bui_points['int'].max()):
        # window building name
        bui = bui_points[['bui']][bui_points['int'] == i].reset_index()
        bui = bui['bui'][0]

        # window height
        amin = bui_min_z['z'][bui_min_z['bui'] == bui].tolist()[0]
        height = bui_points[['z']][bui_points['int'] == i].mean().get_value(0)
        window_height.append(height - amin)
        window_bui_name.append(bui)

        # window area
        xyz = bui_points[['x', 'y', 'z']][bui_points['int'] == i].values.tolist()
        a = math.sqrt((xyz[0][0] - xyz[1][0]) ** 2 + (xyz[0][1] - xyz[1][1]) ** 2 + (xyz[0][2] - xyz[1][2]) ** 2)
        b = math.sqrt((xyz[1][0] - xyz[2][0]) ** 2 + (xyz[1][1] - xyz[2][1]) ** 2 + (xyz[1][2] - xyz[2][2]) ** 2)
        c = math.sqrt((xyz[2][0] - xyz[0][0]) ** 2 + (xyz[2][1] - xyz[0][1]) ** 2 + (xyz[2][2] - xyz[0][2]) ** 2)
        s = (a + b + c) / 2
        face_area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        win_wall = prop_architecture.ix[bui]['win_wall']
        win_op = prop_architecture.ix[bui]['win_op']
        frac = frac_ex.ix[i]['ex_frac']
        window_area.append(face_area * win_wall * win_op * frac)

        # window angle
        dir_z = bui_points[['dir_z']][bui_points['int'] == i].mean().get_value(0)
        window_angle.append(math.acos(dir_z) * 180 / math.pi)

        # window orientation
        dir_x = bui_points[['dir_x']][bui_points['int'] == i].mean().get_value(0)
        dir_y = bui_points[['dir_y']][bui_points['int'] == i].mean().get_value(0)
        # orientation = abs(math.copysign(math.acos(dir_y), dir_x) * 180 / math.pi - 180)
        angle = math.copysign(math.acos(dir_y), dir_x) * 180 / math.pi
        if abs(angle) > 135:
            orientation = 0
        elif abs(angle) < 45:
            orientation = 180
        elif angle < 0:
            orientation = 270
        else:
            orientation = 90

        window_orientation.append(orientation)

    df_windows = pd.DataFrame({'name_building': window_bui_name,
                               'area_window': window_area,
                               'height_window_above_ground': window_height,
                               'orientation_window': window_orientation,
                               'angle_window': window_angle,
                               'height_window_in_zone': window_height})

    df_windows = df_windows[df_windows['area_window'] != 0.0]

    # TODO: make it easier group by height and orientation, sum on area, average on angle and height in zone

    return df_windows


def get_ven_props(bui_name, data_path):
    # read building sensor id file
    bui_id_df_file = os.path.join(data_path, 'solar-radiation', 'bui_id_df.csv')
    bui_id_df = pd.read_csv(bui_id_df_file)
    bui_id_df = bui_id_df[bui_id_df['bui'] == bui_name]

    # select vertical surfaces, considered <10% angle
    dir_z_limit = math.sin(10.0 / 180 * math.pi)
    sel_roof = bui_id_df[bui_id_df['sen_dir_z'] > dir_z_limit]

    av_slope = sel_roof[["bui", "sen_dir_z"]].groupby(['bui']).mean().reset_index()
    av_slope['sen_dir_z'] = np.round(np.arccos(av_slope['sen_dir_z']) * 180 / np.pi, 0)

    # select horizontal surfaces
    sel_facade = bui_id_df[bui_id_df['sen_dir_z'] <= dir_z_limit]
    av_slope = sel_roof[["bui", "sen_dir_z"]].groupby(['bui']).mean().reset_index()
    av_slope['sen_dir_z'] = np.round(np.arccos(av_slope['sen_dir_z']) * 180 / np.pi, 0)

    zone_height = bui_id_df['sen_z'].max()-bui_id_df['sen_z'].min()

    return sel_facade['sen_area'].sum(), sel_roof['sen_area'].sum(), zone_height, av_slope['sen_dir_z'].get_value(0)

def get_volume(bui_name, data_path):
    # read building sensor id file
    bui_vol_file = os.path.join(data_path, 'solar-radiation', 'bui_vol.csv')
    bui_vol = pd.read_csv(bui_vol_file)
    return bui_vol[bui_name].get_value(0)



if __name__ == '__main__':
    import cea.inputlocator as il
    bui_name = 'B2368593'
    scenario_path = r'c:\reference-case_HQ\run0'
    locator = il.InputLocator(scenario_path=scenario_path)
    print (get_ven_props(bui_name, os.path.join(scenario_path, 'outputs', 'data')))
    print(get_volume(bui_name, os.path.join(scenario_path, 'outputs', 'data')))

    print (get_facade_area(locator))



    print(create_windows(locator))
