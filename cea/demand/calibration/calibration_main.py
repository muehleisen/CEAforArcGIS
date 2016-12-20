"""
===========================
Bayesian calibration routine

based on work of (Patil_et_al, 2010 - #http://www.map.ox.ac.uk/media/PDF/Patil_et_al_2010.pdf) in MCMC in pyMC3
and the works of bayesian calibration of (Kennedy and O'Hagan, 2001)
===========================
J. Fonseca  script development          27.10.16


"""

from __future__ import division

import pandas as pd
import pymc3 as pm
import shutil, os
from pymc3.backends import SQLite
import theano.tensor as tt
from theano import as_op
from pymc3.distributions.distribution import Continuous, draw_values, generate_samples
from pymc3.distributions.dist_math import bound
from geopandas import GeoDataFrame as Gdf
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import cea.globalvar
import cea.inputlocator

from cea.demand import demand_main

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def calibration_main(gv, locator, weather_path, building_name, variables, building_load, retrieve_results, scenario_path,
                     method, niter):

    # create function of demand calculation and send to theano
    @as_op(itypes=[tt.dscalar, tt.dscalar, tt.dscalar, tt.dscalar, tt.dscalar, tt.dscalar, tt.dscalar], otypes=[tt.dvector])
    def demand_calculation(phi, err, var1, var2, var3, var4, var5):
        out = np.empty(1)
        samples = [var1, var2, var3, var4, var5]

        # create an overides file which contains changes in the input variables.
        prop_thermal = Gdf.from_file(loc.get_building_thermal()).set_index('Name')
        prop_overrides = pd.DataFrame(index=prop_thermal.index)
        for i, key in enumerate(vars):
            prop_overrides[key] = samples[i]
        prop_overrides.to_csv(loc.get_building_overrides())

        # call CEA demand calculation
        gv.multiprocessing = False
        demand_main.demand_calculation(loc, weather_path, gv)  # simulation
        result = pd.read_csv(loc.get_demand_results_file(building_name), usecols=[building_load]) * (1 + phi + err)

        if method is 'cvremse':
            out[0] = calc_CVrmse(result[building_load].values, obs_data)
        else:
            out = result[building_load].values[gv.seasonhours[0]:-gv.seasonhours[1]]

        print out, phi, err, var1, var2, var3, var4, var5
        return out

    # copy scenario folder to do overides only there
    simulation_path = locator.get_temporary_folder()+'//'+'test'
    if os.path.exists(simulation_path):
        shutil.rmtree(simulation_path)
    shutil.copytree(scenario_path, simulation_path)
    loc = cea.inputlocator.InputLocator(scenario_path=simulation_path)

    # import arguments of probability density functions (PDF) of variables and create priors:
    pdf = pd.concat([pd.read_excel(locator.get_uncertainty_db(), group, axis=1) for group in
                     ['THERMAL', 'ARCHITECTURE', 'INDOOR_COMFORT', 'INTERNAL_LOADS']]).set_index('name')

    # import measured data for building and building load:
    obs_data = pd.read_csv(locator.get_demand_measured_file(building_name))[building_load].values[gv.seasonhours[0]:-gv.seasonhours[1]]

    # create bayesian calibration model in PYMC3
    with pm.Model() as basic_model:

        # add all priors of selected varialbles to the model and assign a triangular distribution
        # for this we create a global variable out of the strings included in the list variables
        vars = []
        for i, variable in enumerate(variables):
            lower = pdf.loc[variable, 'min']
            upper = pdf.loc[variable, 'max']
            globals()['var'+str(i+1)] = pm.Uniform('var'+str(i+1), lower=lower, upper=upper)
            vars.append('var'+str(i+1))

        # get priors for the model inaquacy and the measurement errors.
        phi = pm.Uniform('phi', lower=0, upper=0.01)
        err = pm.Uniform('err', lower=0, upper=0.02)

        # expected value of outcome
        mu = pm.Deterministic('mu', demand_calculation(phi, err, var1, var2, var3, var4, var5))

        # Likelihood (sampling distribution) of observations
        if method is 'cvrmse':
            sigma = pm.HalfNormal('sigma', sd=0.1)
            y_obs = pm.Normal('y_obs', mu=mu, sd=sigma, observed = 0.0)
        else:
            y_obs = pm.ZeroInflatedPoisson('y_obs', theta=mu, psi=0.5,  observed=obs_data)

    if retrieve_results:
        with basic_model:

            # plot posteriors
            trace = pm.backends.text.load(locator.get_calibration_folder(niter))
            pm.traceplot(trace)
            plt.show()

        # plot comparison to mean values
        ppc = pm.sample_ppc(trace, samples=500, model=basic_model, size=100)
        ax = plt.subplot()
        sns.distplot([x.mean() for x in ppc['var1']], kde=False, ax=ax)
        ax.axvline(obs_data.mean())
        ax.set(title='Posterior predictive of the mean', xlabel='mean(x)', ylabel='Frequency')
        plt.show()
    else:

        with basic_model:
            step = pm.Metropolis()
            trace = pm.sample(niter, step=step)
            pm.backends.text.dump(locator.get_calibration_folder(niter), trace)
    return


def calc_CVrmse(prediction, target):
    CVrmse = np.sqrt(((prediction - target) ** 2).mean()) / prediction.mean()
    return CVrmse


# Create Triangular distributions
# class Triangular(Continuous):
#     R"""
#     Continuous Triangular log-likelihood.
#
#     Parameters
#     ----------
#     lower : float
#         Lower limit.
#     c: float
#         mode
#     upper : float
#         Upper limit.
#     """
#
#     def __init__(self, lower=0, upper=1, c=0.5, transform='interval',
#                  *args, **kwargs):
#         super(Triangular, self).__init__(*args, **kwargs)
#
#         self.c = c
#         self.lower = lower
#         self.upper = upper
#         self.mean = c
#         self.median = self.mean
#
#     def random(self, point=None, size=None, repeat=None):
#         lower, c, upper = draw_values([self.lower, self.c, self.upper],
#                                       point=point)
#         return generate_samples(stats.triang.rvs, c=c, loc=lower, scale=upper - lower,
#                                 size=size, random_state=None)
#
#
#     def logp(self, value):
#         c = self.c
#         lower = self.lower
#         upper = self.upper
#         #f1 = -tt.log(2 * (value - lower) / ((upper - lower) * (c - lower)))
#         #f2 = -tt.log(2 / (upper - lower))
#         #f3 = -tt.log(2 * (upper - value) / ((upper - lower) * (upper - c)))
#         #return bound(lower <= value < c, f1, bound(value == c, f2, bound(c < value <= upper, f3)))
#
#         return triang_logp(lower, upper, c, value)
#
# @as_op(itypes=[tt.dscalar, tt.dscalar, tt.dscalar, tt.dscalar], otypes=[tt.dscalar])
# def triang_logp(lower, upper, c, value):
#     if lower <= value < c:
#         return -tt.log(2 * (value - lower) / ((upper - lower) * (c - lower)))
#     elif value is c:
#         return -tt.log(2 / (upper - lower))
#     elif c < value <= upper:
#         return -tt.log(2 * (upper - value) / ((upper - lower) * (upper - c)))
#     else:
#         return -np.inf


def run_as_script():
    import cea.inputlocator as inputlocator
    gv = cea.globalvar.GlobalVariables()
    scenario_path = gv.scenario_reference
    locator = inputlocator.InputLocator(scenario_path=scenario_path)
    weather_path = locator.get_default_weather()

    # based on the variables listed in the uncertainty database and selected
    # through a screeing process. they need to be 5.
    variables = ['U_win', 'U_wall', 'Ths_setb_C', 'Ths_set_C', 'Cm']
    building_name = 'B01'
    building_load = 'Qhsf_kWh'
    retrieve_results = False  # flag to retrieve and analyze results from calibration
    method = 'poisson' # cvrmse and normal distribution or 'zero_poisson' with an entire timeseries
    calibration_main(gv, locator, weather_path, building_name, variables, building_load, retrieve_results, scenario_path,
                     method, niter=1000)

if __name__ == '__main__':
    run_as_script()
