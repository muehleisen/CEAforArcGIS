import numpy as np
import functions as f
import pandas as pd


def CalcThermalLoads_tcorr_factor(Name, prop_occupancy, prop_architecture, prop_thermal, prop_geometry, prop_HVAC, prop_RC_model,
                     prop_age, Solar, locationFinal, Profiles, Profiles_names, T_ext, T_ext_max, RH_ext, T_ext_min,
                     path_temporary_folder, gv, servers, coolingroom):


    Af = prop_RC_model.Af
    Aef = prop_RC_model.Aef
    sys_e_heating = prop_HVAC.type_hs
    sys_e_cooling = prop_HVAC.type_cs
    sys_e_ctrl = prop_HVAC.type_ctrl  #room temperature control types

    # calculate schedule and variables
    ta_hs_set, ta_cs_set, people, ve, q_int, Eal_nove, Eprof, Edataf, Qcdataf, Qcrefrif, vww, vw, X_int, hour_day = f.calc_mixed_schedule(Profiles, Profiles_names, prop_occupancy)

    if Af > 0:
        # extract properties of building
        # Geometry
        Am, Atot, Aw, Awall_all, Cm, Ll, Lw, Retrofit, Sh_typ, Year, footprint, nf_ag, nfp = f.get_properties_building_envelope( prop_RC_model, prop_age, prop_architecture, prop_geometry, prop_occupancy)

        Lcww_dis, Lsww_dis, Lv, Lvww_c, Lvww_dis, Tcs_re_0, Tcs_sup_0, Ths_re_0, Ths_sup_0, Tww_re_0, Tww_sup_0, Y, fforma = f.get_properties_building_systems(
        Ll, Lw, Retrofit, Year, footprint, gv, nf_ag, nfp, prop_HVAC)

        # we define limtis of season.
        limit_inf_season = gv.seasonhours[0] + 1
        limit_sup_season = gv.seasonhours[1]

        # data and refrigeration loads
        Qcdata = Qcdataf * Af
        Qcrefri = Qcrefrif * Af

        # 2. Transmission coefficients in W/K
        qv_req = np.vectorize(f.calc_qv_req)(ve, people, Af, gv, hour_day, range(8760), limit_inf_season,
                                       limit_sup_season)  # in m3/s
        Hve = (gv.PaCa * qv_req)
        Htr_is = prop_RC_model.Htr_is
        Htr_ms = prop_RC_model.Htr_ms
        Htr_w = prop_RC_model.Htr_w
        Htr_em = prop_RC_model.Htr_em
        Htr_1, Htr_2, Htr_3 = np.vectorize(f.calc_Htr)(Hve, Htr_is, Htr_ms, Htr_w)

        # 3. Heat flows in W
        # . Solar heat gains
        I_sol = f.calc_heat_gains_solar(Aw, Awall_all, Sh_typ, Solar, gv)

        #  Sensible heat gains
        I_int_sen = f.calc_heat_gains_internal_sensible(Af, q_int)

        #  Calculate latent internal loads in terms of added moisture:
        w_int = f.calc_heat_gains_internal_latent(Af, X_int, sys_e_cooling, sys_e_heating)

        #  Components of Sensible heat gains
        I_ia, I_m, I_st = f.calc_comp_heat_gains_sensible(Am, Atot, Htr_w, I_int_sen, I_sol)  # TODO: rename function according to ISO standard

        # 4. Heating and cooling loads
        IC_max, IH_max = f.calc_capacity_heating_cooling_system(Af, prop_HVAC)  # TODO: check name of function

        # define empty arrrays
        uncomfort = np.zeros(8760)
        Ta = np.zeros(8760)
        Tm = np.zeros(8760)
        Qhs_sen = np.zeros(8760)
        Qcs_sen = np.zeros(8760)
        Qhs_lat = np.zeros(8760)
        Qcs_lat = np.zeros(8760)
        Qhs_em_ls = np.zeros(8760)
        Qcs_em_ls = np.zeros(8760)
        QHC_sen = np.zeros(8760)
        ma_sup_hs = np.zeros(8760)
        Ta_sup_hs = np.zeros(8760)
        Ta_re_hs = np.zeros(8760)
        ma_sup_cs = np.zeros(8760)
        Ta_sup_cs = np.zeros(8760)
        Ta_re_cs = np.zeros(8760)
        w_sup = np.zeros(8760)
        w_re = np.zeros(8760)
        Ehs_lat_aux = np.zeros(8760)
        Qhs_sen_incl_em_ls = np.zeros(8760)
        Qcs_sen_incl_em_ls = np.zeros(8760)
        t5 = np.zeros(8760)
        Tww_re = np.zeros(8760)
        Top = np.zeros(8760)
        Im_tot = np.zeros(8760)

        # model of losses in the emission and control system for space heating and cooling
        tHset_corr, tCset_corr = f.calc_tHC_corr(sys_e_heating,sys_e_cooling,sys_e_ctrl)

        # we give a seed high enough to avoid doing a iteration for 2 years.
        tm_t0 = tm_t1 = 16
        # end-use demand calculation
        t5_1 = 21  # definition of first temperature to start calculation of air conditioning system
        for k in range(8760):
            # if it is in the season
            if limit_inf_season <= k < limit_sup_season:
                # take advantage of this loop to fill the values of cold water
                Flag_season = True
                Tww_re[k] = 14
            else:
                # take advantage of this loop to fill the values of cold water
                Tww_re[k] = Tww_re_0
                Flag_season = False
            # Calc of Qhs/Qcs - net/useful heating and cooling deamnd in W
            Losses = False  # 0 is false and 1 is true
            Tm[k], Ta[k], Qhs_sen[k], Qcs_sen[k], uncomfort[k], Top[k], Im_tot[k] = f.calc_TL(sys_e_heating, sys_e_cooling,
                                                                                        tm_t0,
                                                                                        T_ext[k], ta_hs_set[k],
                                                                                        ta_cs_set[k], Htr_em, Htr_ms,
                                                                                        Htr_is, Htr_1[k],
                                                                                        Htr_2[k], Htr_3[k], I_st[k],
                                                                                        Hve[k], Htr_w, I_ia[k], I_m[k],
                                                                                        Cm, Af, Losses,
                                                                                        tHset_corr, tCset_corr, IC_max,
                                                                                        IH_max, Flag_season)


            # losses in the emission/control system
            Qhs_em_ls[k], Qcs_em_ls[k] = f.calc_Qem_ls_f(tHset_corr, tCset_corr, ta_hs_set[k], ta_cs_set[k], Qhs_sen[k],
                                                     Qcs_sen[k], T_ext[k], Flag_season)
            if Qcs_em_ls[k] > 0:
                Qcs_em_ls[k] = 0
            if Qhs_em_ls[k] < 0:
                Qhs_em_ls[k] = 0

            tm_t0 = Tm[k]

            # Calculate new sensible loads with HVAC systems incl. recovery.
            Qhs_sen_incl_em_ls[k] = Qhs_em_ls[k] + Qhs_sen[k]
            Qcs_sen_incl_em_ls[k] = Qcs_em_ls[k] + Qcs_sen[k]
            if sys_e_cooling == 'T0':
                Qcs_sen[k] = 0
            if sys_e_heating == 'T3' or sys_e_cooling == 'T3':
                QHC_sen[k] = Qhs_sen[k] + Qcs_sen[k] + Qhs_em_ls[k] + Qcs_em_ls[k]
                temporal_Qhs, temporal_Qcs, Qhs_lat[k], Qcs_lat[k], Ehs_lat_aux[k], ma_sup_hs[k], ma_sup_cs[k], Ta_sup_hs[k], Ta_sup_cs[k], Ta_re_hs[k], Ta_re_cs[k], w_re[k], w_sup[k], t5[k] = f.calc_HVAC(sys_e_heating,
                                                                                                 sys_e_cooling,
                                                                                                 people[k], RH_ext[k],
                                                                                                 T_ext[k], Ta[k],
                                                                                                 qv_req[k], Flag_season,
                                                                                                 QHC_sen[k], t5_1, w_int[k], gv)
                t5_1 = t5[k]
                if sys_e_heating == 'T3':
                    Qhs_sen_incl_em_ls[k] = temporal_Qhs
                    Qhs_sen[k] = temporal_Qhs - Qhs_em_ls[k]
                if sys_e_cooling == 'T3':
                    Qcs_sen_incl_em_ls[k] = temporal_Qcs


        # Calc of Qhs_dis_ls/Qcs_dis_ls - losses due to distribution of heating/cooling coils
        # erase possible disruptions from dehumidification days
        #Qhs_sen_incl_em_ls = Qhs_sen + Qhs_em_ls
        #Qcs_sen_incl_em_ls = Qcs_sen + Qcs_em_ls
        #Qhs_sen_incl_em_ls[Qhs_sen_incl_em_ls < 0] = 0
        #Qcs_sen_incl_em_ls[Qcs_sen_incl_em_ls > 0] = 0
        Qhs_sen_incl_em_ls_0 = Qhs_sen_incl_em_ls.max()
        Qcs_sen_incl_em_ls_0 = Qcs_sen_incl_em_ls.min()  # cooling loads up to here in negative values
        Qhs_d_ls, Qcs_d_ls = np.vectorize(f.calc_Qdis_ls)(Ta, T_ext, Qhs_sen_incl_em_ls, Qcs_sen_incl_em_ls, Ths_sup_0,
                                                    Ths_re_0, Tcs_sup_0, Tcs_re_0, Qhs_sen_incl_em_ls_0,
                                                    Qcs_sen_incl_em_ls_0,
                                                    gv.D, Y[0], sys_e_heating, sys_e_cooling, gv.Bf, Lv)

        # Calc requirements of generation systems (both cooling and heating do not have a storage):
        Qhsf = Qhs_sen_incl_em_ls + Qhs_d_ls   # no latent is considered because it is already added as electricity from the adiabatic system.
        Qcs = (Qcs_sen_incl_em_ls - Qcs_em_ls) + Qcs_lat
        Qcsf = Qcs + Qcs_em_ls + Qcs_d_ls
        Qcsf = -abs(Qcsf)
        Qcs = -abs(Qcs)

        # Calc nominal temperatures of systems
        Qhsf_0 = np.nanmax(Qhsf)  # in W
        Qcsf_0 = np.nanmin(Qcsf)  # in W negative

        #print(np.nanmax(Qhsf))
        #print(Qhs_sen_incl_em_ls)
        #print(Qhs_d_ls)
        #print(Qhsf.max())
        #print (tHset_corr, tCset_corr)
        #print (np.where(Qhsf == Qhsf_0))
        #DATE = pd.date_range('1/1/2010', periods=8760, freq='H')
        #pd.DataFrame(
        #    {'Qcsf': Qcsf, 'Qcsf_0': Qcsf_0, 'Qhsf': Qhsf, 'Qhsf_0': Qhsf_0, 'Qcs_em_ls': Qcs_em_ls,
        #     'Qhs_em_ls': Qhs_em_ls, 'Qhs_sen':Qhs_sen, 'Qcs_sen':Qcs_sen, 'Qhs_sen_incl_em_ls':Qhs_sen_incl_em_ls,'Qcs_sen_incl_em_ls':Qcs_sen_incl_em_ls }).to_csv(locationFinal + '\\' + Name + 'test.csv', index=False, float_format='%.2f')

        # Cal temperatures of all systems
        Tcs_re, Tcs_sup, Ths_re, Ths_sup, mcpcs, mcphs = f.calc_temperatures_emission_systems(Qcsf, Qcsf_0, Qhsf, Qhsf_0,
                                                                                        Ta, Ta_re_cs, Ta_re_hs,
                                                                                        Ta_sup_cs, Ta_sup_hs,
                                                                                        Tcs_re_0, Tcs_sup_0,
                                                                                        Ths_re_0, Ths_sup_0, gv,
                                                                                        ma_sup_cs, ma_sup_hs,
                                                                                        sys_e_cooling,
                                                                                        sys_e_heating, ta_hs_set,
                                                                                        w_re, w_sup)
        # Cal dhw heating demand
        Mww, Qww, Qww_ls_st, Qwwf, Qwwf_0, Tww_st, Vw, Vww, mcpww = f.calc_dhw_heating_demand(Af, Lcww_dis, Lsww_dis,
                                                                                        Lvww_c, Lvww_dis, T_ext, Ta,
                                                                                        Tww_re, Tww_sup_0, Y, gv,
                                                                                        vw, vww)

        # clac auxiliary loads of pumping systems
        Eaux_cs, Eaux_fw, Eaux_hs, Eaux_ve, Eaux_ww = f.calc_pumping_systems_aux_loads(Af, Ll, Lw, Mww, Qcsf, Qcsf_0,
                                                                                 Qhsf, Qhsf_0, Qww, Qwwf, Qwwf_0,
                                                                                 Tcs_re, Tcs_sup, Ths_re, Ths_sup,
                                                                                 Vw, Year, fforma, gv, nf_ag, nfp,
                                                                                 qv_req, sys_e_cooling,
                                                                                 sys_e_heating)

        # Calc total auxiliary loads
        Eauxf = (Eaux_ww + Eaux_fw + Eaux_hs + Eaux_cs + Ehs_lat_aux + Eaux_ve)

        # calculate other quantities
        Occupancy = np.floor(people * Af)
        Occupants = Occupancy.max()
        Waterconsumption = Vww + Vw  # volume of water consumed in m3/h
        waterpeak = Waterconsumption.max()

        # Af = 0: no conditioned floor area
    else:
        # scalars
        waterpeak = Occupants = 0
        Qwwf_0 = Ealf_0 = Qhsf_0 = Qcsf_0 = 0
        Ths_sup_0 = Ths_re_0 = Tcs_re_0 = Tcs_sup_0 = Tww_sup_0 = 0
        # arrays
        Occupancy = Eauxf = Waterconsumption = np.zeros(8760)
        Qwwf = Qww = Qhs_sen = Qhsf = Qcs_sen = Qcs = Qhs_em_ls = Qcs_em_ls = Qcsf = Qcdata = Qcrefri = Qd = Qc = Qww_ls_st = np.zeros(8760)
        Ths_sup = Ths_re = Tcs_re = Tcs_sup = mcphs = mcpcs = mcpww = Vww = Tww_re = Tww_st = uncomfort = np.zeros(
        8760)  # in C

    # calc electrical loads
    Ealf, Ealf_0, Ealf_tot, Eauxf_tot, Edata, Edata_tot, Epro, Epro_tot = f.calc_loads_electrical(Aef, Eal_nove,
                                                                                            Eauxf, Edataf, Eprof)

    # write results to csv
    f.results_to_csv(Af, Ealf, Ealf_0, Ealf_tot, Eauxf, Eauxf_tot, Edata, Edata_tot, Epro, Epro_tot, Name, Occupancy,
                     Occupants, Qcdata, Qcrefri, Qcs, Qcsf, Qcsf_0, Qhs_sen, Qhs_em_ls, Qcs_em_ls, Qhsf, Qhsf_0, Qww,
                     Qww_ls_st, Qwwf, Qwwf_0,
                     Tcs_re, Tcs_re_0, Tcs_sup, Tcs_sup_0, Ths_re, Ths_re_0, Ths_sup, Ths_sup_0, Tww_re, Tww_st,
                     Tww_sup_0, Waterconsumption, locationFinal, mcpcs, mcphs, mcpww, path_temporary_folder,
                     sys_e_cooling, sys_e_heating, waterpeak)

    return



def CalcThermalLoads_tcorr(Name, prop_occupancy, prop_architecture, prop_thermal, prop_geometry, prop_HVAC, prop_RC_model,
                         prop_age, Solar, locationFinal, Profiles, Profiles_names, T_ext, T_ext_max, RH_ext, T_ext_min,
                         path_temporary_folder, gv, servers, coolingroom):


    Af = prop_RC_model.Af
    Aef = prop_RC_model.Aef
    sys_e_heating = prop_HVAC.type_hs
    sys_e_cooling = prop_HVAC.type_cs
    sys_e_ctrl = prop_HVAC.type_ctrl  # room temperature control types

    # calculate schedule and variables
    ta_hs_set, ta_cs_set, people, ve, q_int, Eal_nove, Eprof, Edataf, Qcdataf, Qcrefrif, vww, vw, X_int, hour_day = f.calc_mixed_schedule(Profiles, Profiles_names, prop_occupancy)

    if Af > 0:
        # extract properties of building
        # Geometry
        Am, Atot, Aw, Awall_all, Cm, Ll, Lw, Retrofit, Sh_typ, Year, footprint, nf_ag, nfp = f.get_properties_building_envelope(
        prop_RC_model, prop_age, prop_architecture, prop_geometry, prop_occupancy)

        Lcww_dis, Lsww_dis, Lv, Lvww_c, Lvww_dis, Tcs_re_0, Tcs_sup_0, Ths_re_0, Ths_sup_0, Tww_re_0, Tww_sup_0, Y, fforma = f.get_properties_building_systems(
        Ll, Lw, Retrofit, Year, footprint, gv, nf_ag, nfp, prop_HVAC)

        # we define limtis of season.
        limit_inf_season = gv.seasonhours[0] + 1
        limit_sup_season = gv.seasonhours[1]

        # data and refrigeration loads
        Qcdata = Qcdataf * Af
        Qcrefri = Qcrefrif * Af

        # 2. Transmission coefficients in W/K
        qv_req = np.vectorize(f.calc_qv_req)(ve, people, Af, gv, hour_day, range(8760), limit_inf_season,
                                       limit_sup_season)  # in m3/s
        Hve = (gv.PaCa * qv_req)
        Htr_is = prop_RC_model.Htr_is
        Htr_ms = prop_RC_model.Htr_ms
        Htr_w = prop_RC_model.Htr_w
        Htr_em = prop_RC_model.Htr_em
        Htr_1, Htr_2, Htr_3 = np.vectorize(f.calc_Htr)(Hve, Htr_is, Htr_ms, Htr_w)

        # 3. Heat flows in W
        # . Solar heat gains
        I_sol = f.calc_heat_gains_solar(Aw, Awall_all, Sh_typ, Solar, gv)

        #  Sensible heat gains
        I_int_sen = f.calc_heat_gains_internal_sensible(Af, q_int)

        #  Calculate latent internal loads in terms of added moisture:
        w_int = f.calc_heat_gains_internal_latent(Af, X_int, sys_e_cooling, sys_e_heating)

        #  Components of Sensible heat gains
        I_ia, I_m, I_st = f.calc_comp_heat_gains_sensible(Am, Atot, Htr_w, I_int_sen,
                                                    I_sol)  # TODO: rename function according to ISO standard

        # 4. Heating and cooling loads
        IC_max, IH_max = f.calc_capacity_heating_cooling_system(Af, prop_HVAC)  # TODO: check name of function

        # define empty arrrays
        uncomfort = np.zeros(8760)
        Ta = np.zeros(8760)
        Tm = np.zeros(8760)
        Qhs_sen = np.zeros(8760)
        Qcs_sen = np.zeros(8760)
        Qhs_lat = np.zeros(8760)
        Qcs_lat = np.zeros(8760)
        Qhs_em_ls = np.zeros(8760)
        Qcs_em_ls = np.zeros(8760)
        QHC_sen = np.zeros(8760)
        ma_sup_hs = np.zeros(8760)
        Ta_sup_hs = np.zeros(8760)
        Ta_re_hs = np.zeros(8760)
        ma_sup_cs = np.zeros(8760)
        Ta_sup_cs = np.zeros(8760)
        Ta_re_cs = np.zeros(8760)
        w_sup = np.zeros(8760)
        w_re = np.zeros(8760)
        Ehs_lat_aux = np.zeros(8760)
        Qhs_sen_incl_em_ls = np.zeros(8760)
        Qcs_sen_incl_em_ls = np.zeros(8760)
        t5 = np.zeros(8760)
        Tww_re = np.zeros(8760)
        Top = np.zeros(8760)
        Im_tot = np.zeros(8760)

        # model of losses in the emission and control system for space heating and cooling
        tHset_corr, tCset_corr = f.calc_tHC_corr(sys_e_heating, sys_e_cooling, sys_e_ctrl)

        # we give a seed high enough to avoid doing a iteration for 2 years.
        tm_t0 = tm_t1 = 16
        # end-use demand calculation
        t5_1 = 21  # definition of first temperature to start calculation of air conditioning system
        for k in range(8760):
            # if it is in the season
            if limit_inf_season <= k < limit_sup_season:
                # take advantage of this loop to fill the values of cold water
                Flag_season = True
                Tww_re[k] = 14
            else:
                # take advantage of this loop to fill the values of cold water
                Tww_re[k] = Tww_re_0
                Flag_season = False
            # Calc of Qhs/Qcs - net/useful heating and cooling deamnd in W
            Losses = False  # 0 is false and 1 is true
            Tm[k], Ta[k], Qhs_sen[k], Qcs_sen[k], uncomfort[k], Top[k], Im_tot[k] = f.calc_TL(sys_e_heating, sys_e_cooling,
                                                                                        tm_t0,
                                                                                        T_ext[k], ta_hs_set[k],
                                                                                        ta_cs_set[k], Htr_em, Htr_ms,
                                                                                        Htr_is, Htr_1[k],
                                                                                        Htr_2[k], Htr_3[k], I_st[k],
                                                                                        Hve[k], Htr_w, I_ia[k], I_m[k],
                                                                                        Cm, Af, Losses,
                                                                                        tHset_corr, tCset_corr, IC_max,
                                                                                        IH_max, Flag_season)

            #  Calc of Qhs_em_ls/Qcs_em_ls - losses due to emission systems in W
            Losses = True
            Results1 = f.calc_TL(sys_e_heating, sys_e_cooling, tm_t1, T_ext[k], ta_hs_set[k], ta_cs_set[k],
                           Htr_em, Htr_ms, Htr_is, Htr_1[k], Htr_2[k], Htr_3[k], I_st[k], Hve[k], Htr_w, I_ia[k],
                           I_m[k],
                           Cm, Af, Losses, tHset_corr, tCset_corr, IC_max, IH_max, Flag_season)

            # losses in the emission/control system
            Qhs_em_ls[k] = Results1[2] - Qhs_sen[k]
            Qcs_em_ls[k] = Results1[3] - Qcs_sen[k]
            if Qcs_em_ls[k] > 0:
                Qcs_em_ls[k] = 0
            if Qhs_em_ls[k] < 0:
                Qhs_em_ls[k] = 0

            tm_t0 = Tm[k]
            tm_t1 = Results1[0]

            # calc comfort hours:
            uncomfort[k] = Results1[4]
            Top[k] = Results1[5]
            Im_tot[k] = Results1[6]

            # Calculate new sensible loads with HVAC systems incl. recovery.
            if sys_e_heating != 'T3':
                Qhs_sen_incl_em_ls[k] = Results1[2]
            if sys_e_cooling == 'T0':
                Qcs_sen_incl_em_ls[k] = 0
            if sys_e_heating == 'T3' or sys_e_cooling == 'T3':
                QHC_sen[k] = Qhs_sen[k] + Qcs_sen[k] + Qhs_em_ls[k] + Qcs_em_ls[k]
                temporal_Qhs, temporal_Qcs, Qhs_lat[k], Qcs_lat[k], Ehs_lat_aux[k], ma_sup_hs[k], ma_sup_cs[k], Ta_sup_hs[
                k], Ta_sup_cs[k], Ta_re_hs[k], Ta_re_cs[k], w_re[k], w_sup[k], t5[k] = f.calc_HVAC(sys_e_heating,
                                                                                                 sys_e_cooling,
                                                                                                 people[k], RH_ext[k],
                                                                                                 T_ext[k], Ta[k],
                                                                                                 qv_req[k], Flag_season,
                                                                                                 QHC_sen[k], t5_1,
                                                                                                 w_int[k], gv)
                t5_1 = t5[k]
                if sys_e_heating == 'T3':
                    Qhs_sen_incl_em_ls[k] = temporal_Qhs
                    Qhs_sen[k] = temporal_Qhs - Qhs_em_ls[k]
                if sys_e_cooling == 'T3':
                    Qcs_sen_incl_em_ls[k] = temporal_Qcs

        # Calc of Qhs_dis_ls/Qcs_dis_ls - losses due to distribution of heating/cooling coils
        # erase possible disruptions from dehumidification days
        # Qhs_sen_incl_em_ls[Qhs_sen_incl_em_ls < 0] = 0
        # Qcs_sen_incl_em_ls[Qcs_sen_incl_em_ls > 0] = 0
        Qhs_sen_incl_em_ls_0 = Qhs_sen_incl_em_ls.max()
        Qcs_sen_incl_em_ls_0 = Qcs_sen_incl_em_ls.min()  # cooling loads up to here in negative values
        Qhs_d_ls, Qcs_d_ls = np.vectorize(f.calc_Qdis_ls)(Ta, T_ext, Qhs_sen_incl_em_ls, Qcs_sen_incl_em_ls, Ths_sup_0,
                                                    Ths_re_0, Tcs_sup_0, Tcs_re_0, Qhs_sen_incl_em_ls_0,
                                                    Qcs_sen_incl_em_ls_0,
                                                    gv.D, Y[0], sys_e_heating, sys_e_cooling, gv.Bf, Lv)

        # Calc requirements of generation systems (both cooling and heating do not have a storage):
        Qhsf = Qhs_sen_incl_em_ls + Qhs_d_ls  # no latent is considered because it is already added as electricity from the adiabatic system.
        Qcs = (Qcs_sen_incl_em_ls - Qcs_em_ls) + Qcs_lat
        Qcsf = Qcs + Qcs_em_ls + Qcs_d_ls
        Qcsf = -abs(Qcsf)
        Qcs = -abs(Qcs)

        # Calc nomincal temperatures of systems
        Qhsf_0 = Qhsf.max()  # in W
        Qcsf_0 = Qcsf.min()  # in W negative

        # Cal temperatures of all systems
        Tcs_re, Tcs_sup, Ths_re, Ths_sup, mcpcs, mcphs = f.calc_temperatures_emission_systems(Qcsf, Qcsf_0, Qhsf, Qhsf_0,
                                                                                        Ta, Ta_re_cs, Ta_re_hs,
                                                                                        Ta_sup_cs, Ta_sup_hs,
                                                                                        Tcs_re_0, Tcs_sup_0,
                                                                                        Ths_re_0, Ths_sup_0, gv,
                                                                                        ma_sup_cs, ma_sup_hs,
                                                                                        sys_e_cooling,
                                                                                        sys_e_heating, ta_hs_set,
                                                                                        w_re, w_sup)
        Mww, Qww, Qww_ls_st, Qwwf, Qwwf_0, Tww_st, Vw, Vww, mcpww = f.calc_dhw_heating_demand(Af, Lcww_dis, Lsww_dis,
                                                                                        Lvww_c, Lvww_dis, T_ext, Ta,
                                                                                        Tww_re, Tww_sup_0, Y, gv,
                                                                                        vw, vww)

        # clac auxiliary loads of pumping systems
        Eaux_cs, Eaux_fw, Eaux_hs, Eaux_ve, Eaux_ww = f.calc_pumping_systems_aux_loads(Af, Ll, Lw, Mww, Qcsf, Qcsf_0,
                                                                                 Qhsf, Qhsf_0, Qww, Qwwf, Qwwf_0,
                                                                                 Tcs_re, Tcs_sup, Ths_re, Ths_sup,
                                                                                 Vw, Year, fforma, gv, nf_ag, nfp,
                                                                                 qv_req, sys_e_cooling,
                                                                                 sys_e_heating)

        # Calc total auxiliary loads
        Eauxf = (Eaux_ww + Eaux_fw + Eaux_hs + Eaux_cs + Ehs_lat_aux + Eaux_ve)

        # calculate other quantities
        Occupancy = np.floor(people * Af)
        Occupants = Occupancy.max()
        Waterconsumption = Vww + Vw  # volume of water consumed in m3/h
        waterpeak = Waterconsumption.max()

    # Af = 0: no conditioned floor area
    else:
        # scalars
        waterpeak = Occupants = 0
        Qwwf_0 = Ealf_0 = Qhsf_0 = Qcsf_0 = 0
        Ths_sup_0 = Ths_re_0 = Tcs_re_0 = Tcs_sup_0 = Tww_sup_0 = 0
        # arrays
        Occupancy = Eauxf = Waterconsumption = np.zeros(8760)
        Qwwf = Qww = Qhs_sen = Qhsf = Qcs_sen = Qcs = Qhs_em_ls = Qcs_em_ls = Qcsf = Qcdata = Qcrefri = Qd = Qc = Qww_ls_st = np.zeros(8760)
        Ths_sup = Ths_re = Tcs_re = Tcs_sup = mcphs = mcpcs = mcpww = Vww = Tww_re = Tww_st = uncomfort = np.zeros(
        8760)  # in C

    # calc electrical loads
    Ealf, Ealf_0, Ealf_tot, Eauxf_tot, Edata, Edata_tot, Epro, Epro_tot = f.calc_loads_electrical(Aef, Eal_nove,
                                                                                            Eauxf, Edataf, Eprof)

    # write results to csv
    f.results_to_csv(Af, Ealf, Ealf_0, Ealf_tot, Eauxf, Eauxf_tot, Edata, Edata_tot, Epro, Epro_tot, Name, Occupancy,
               Occupants, Qcdata, Qcrefri, Qcs, Qcsf, Qcsf_0, Qhs_sen, Qhs_em_ls, Qcs_em_ls, Qhsf, Qhsf_0, Qww,
               Qww_ls_st, Qwwf, Qwwf_0,
               Tcs_re, Tcs_re_0, Tcs_sup, Tcs_sup_0, Ths_re, Ths_re_0, Ths_sup, Ths_sup_0, Tww_re, Tww_st,
               Tww_sup_0, Waterconsumption, locationFinal, mcpcs, mcphs, mcpww, path_temporary_folder,
               sys_e_cooling, sys_e_heating, waterpeak)

    return