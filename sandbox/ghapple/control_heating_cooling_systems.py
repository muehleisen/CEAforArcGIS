# -*- coding: utf-8 -*-


from __future__ import division
from sandbox.ghapple import rc_model_SIA_with_TABS

import numpy as np
from sandbox.ghapple import helpers

__author__ = "Gabriel Happle"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


def has_heating_system(bpr):
    """
    determines whether a building has a heating system installed or not

    Parameters
    ----------
    bpr : building properties row object

    Returns
    -------
    bool

    """

    if bpr.hvac['type_hs'] in {'T1', 'T2', 'T3', 'T4'}:
        return True
    elif bpr.hvac['type_hs'] in {'T0'}:
        return False
    else:
        raise


def has_cooling_system(bpr):
    """
    determines whether a building has a cooling system installed or not

    Parameters
    ----------
    bpr : building properties row object

    Returns
    -------
    bool

    """

    if bpr.hvac['type_cs'] in {'T1', 'T2', 'T3'}:
        return True
    elif bpr.hvac['type_cs'] in {'T0'}:
        return False
    else:
        raise


def is_active_heating_system(bpr, tsd, t):

    # check for heating system in building
    # check for heating season
    # check for heating demand
    if has_heating_system(bpr) \
            and helpers.is_heatingseason_hoy(t) \
            and rc_model_SIA_with_TABS.has_heating_demand(bpr, tsd, t):

        return True
    else:
        return False


def is_active_cooling_system(bpr, tsd, t):

    # check for cooling system in building
    # check for cooling season
    # check for cooling demand
    if has_cooling_system(bpr) \
            and helpers.is_coolingseason_hoy(t) \
            and rc_model_SIA_with_TABS.has_cooling_demand(bpr, tsd, t):

        return True
    else:
        return False