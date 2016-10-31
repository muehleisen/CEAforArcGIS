# Table of contents
- [run_as_script](#run_as_script)
   - [demand_calculation](#demand_calculation)
      - [get_prop_solar](#get_prop_solar)
      - [get_temperatures](#get_temperatures)
      - [get_envelope_properties](#get_envelope_properties)
         - [schedule_maker](#schedule_maker)
            - [read_schedules](#read_schedules)
         - [thermal_loads_all_buildings](#thermal_loads_all_buildings)
            - [calc_thermal_loads](#calc_thermal_loads)
               - [initialize_timestep_data](#initialize_timestep_data)
               - [calc_occ](#calc_occ)
                  - [calc_occ_schedule](#calc_occ_schedule)
               - [calc_Eint](#calc_eint)
                  - [average_appliances_lighting_schedule](#average_appliances_lighting_schedule)
               - [calc_Qgain_lat](#calc_qgain_lat)
               - [get_properties_natural_ventilation](#get_properties_natural_ventilation)
                  - [calc_qv_delta_p_ref](#calc_qv_delta_p_ref)
                  - [get_building_geometry_ventilation](#get_building_geometry_ventilation)
                  - [calc_coeff_lea_zone](#calc_coeff_lea_zone)
                  - [allocate_default_leakage_paths](#allocate_default_leakage_paths)
                  - [lookup_coeff_wind_pressure](#lookup_coeff_wind_pressure)
                  - [calc_coeff_vent_zone](#calc_coeff_vent_zone)
                  - [allocate_default_ventilation_openings](#allocate_default_ventilation_openings)
               - [calc_Qgain_sen](#calc_qgain_sen)
                  - [calc_I_sol](#calc_i_sol)
                     - [calc_Asol](#calc_asol)
                     - [calc_I_rad](#calc_i_rad)
                        - [calc_hr](#calc_hr)
               - [calc_thermal_load_hvac](#calc_thermal_load_hvac)
                  - [setpoint_correction_for_space_emission_systems](#setpoint_correction_for_space_emission_systems)
                  - [calc_Qhs_Qcs_sys_max](#calc_qhs_qcs_sys_max)
                  - [calc_hex](#calc_hex)
                     - [calc_w](#calc_w)
                  - [calc_h_ve_adj](#calc_h_ve_adj)
                  - [calc_Htr](#calc_htr)
                  - [calc_Qhs_Qcs](#calc_qhs_qcs)
                  - [calc_hvac](#calc_hvac)
                     - [calc_h](#calc_h)
                     - [calc_t_from_h](#calc_t_from_h)
                     - [calc_w3_cooling_case](#calc_w3_cooling_case)
               - [calc_thermal_load_mechanical_and_natural_ventilation_timestep](#calc_thermal_load_mechanical_and_natural_ventilation_timestep)
                  - [calc_Qhs_Qcs_dis_ls](#calc_qhs_qcs_dis_ls)
               - [calc_temperatures_emission_systems](#calc_temperatures_emission_systems)
                  - [calc_radiator](#calc_radiator)
                     - [newton](#newton)
               - [calc_Qwwf](#calc_qwwf)
                  - [calc_Qww_schedule](#calc_qww_schedule)
                     - [calc_mww](#calc_mww)
                     - [calc_Qww](#calc_qww)
                     - [calc_Qww_dis_ls_r](#calc_qww_dis_ls_r)
                        - [calc_disls](#calc_disls)
                     - [calc_Qww_dis_ls_nr](#calc_qww_dis_ls_nr)
                  - [calc_Qww_st_ls](#calc_qww_st_ls)
               - [calc_Eauxf](#calc_eauxf)
                  - [calc_Eauxf_ww](#calc_eauxf_ww)
                  - [calc_Eauxf_hs_dis](#calc_eauxf_hs_dis)
                  - [calc_Eauxf_cs_dis](#calc_eauxf_cs_dis)
                     - [calc_Eauxf_fw](#calc_eauxf_fw)
                  - [calc_Eauxf_ve](#calc_eauxf_ve)
         - [write_totals_csv](#write_totals_csv)

# allocate_default_leakage_paths
- number of invocations: 1
- max duration: 0.028 s
- avg duration: 0.028 s
- min duration: 0.028 s
- total duration: 0.028 s

### Input
- **coeff_lea_zone** `['float64']`: *2299.5191401150646*
- **area_facade_zone** `['float64']`: *2500.0*
- **area_roof_zone** `['float64']`: *625.0*
- **height_zone** `['float64']`: *25.0*


### Output
- `['tuple']`: (array([ 459.90382802,  459.90382802,  459.90382802,  459.90382802,
        459.90382802]), array([  6.25,   6.25,  18.75,  18.75,  25.  ]), [0, 1, 0, 1, 2])

### Docstring template

```
PARAMETERS
----------

:param coeff_lea_zone:
:type coeff_lea_zone: float64

:param area_facade_zone:
:type area_facade_zone: float64

:param area_roof_zone:
:type area_roof_zone: float64

:param height_zone:
:type height_zone: float64

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# allocate_default_ventilation_openings
- number of invocations: 1
- max duration: 0.028 s
- avg duration: 0.028 s
- min duration: 0.028 s
- total duration: 0.028 s

### Input
- **coeff_vent_zone** `['float']`: *0.0*
- **height_zone** `['float64']`: *25.0*


### Output
- `['tuple']`: (array([ 0.,  0.,  0.,  0.]), array([  6.25,   6.25,  18.75,  18.75]), [0, 1, 0, 1])

### Docstring template

```
PARAMETERS
----------

:param coeff_vent_zone:
:type coeff_vent_zone: float

:param height_zone:
:type height_zone: float64

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# average_appliances_lighting_schedule
- number of invocations: 1
- max duration: 0.455 s
- avg duration: 0.455 s
- min duration: 0.455 s
- total duration: 0.455 s

### Input
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*
- **schedules** `['list']`: *[([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, *
- **building_uses** `['dict']`: *{u'PFloor': 1.0, u'OFFICE': 1.0, u'PARKING': 0.0}*


### Output
- `['ndarray']`: array([ 0.08,  0.08,  0.08, ...,  0.06,  0.06,  0.06])

### Docstring template

```
PARAMETERS
----------

:param list_uses:
:type list_uses: list

:param schedules:
:type schedules: list

:param building_uses:
:type building_uses: dict

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# calc_Asol
- number of invocations: 1
- max duration: 0.041 s
- avg duration: 0.041 s
- min duration: 0.041 s
- total duration: 0.041 s

### Input
- **t** `['int']`: *5472*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x1458C3F0>*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x068BE230>*


### Output
- `['tuple']`: (17.0, 2.5, 600.0)

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int

:param bpr:
:type bpr: BuildingPropertiesRow

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Eauxf
- number of invocations: 1
- max duration: 0.355 s
- avg duration: 0.355 s
- min duration: 0.355 s
- total duration: 0.355 s

### Input
- **Ll** `['float64']`: *25.0*
- **Lw** `['float64']`: *25.0*
- **Mww** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **Qcsf** `['ndarray']`: *array([-0., -0., -0., ..., -0., -0., -0.])*
- **Qcsf_0** `['float64']`: *-613906.75789570482*
- **Qhsf** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **Qhsf_0** `['float64']`: *280780.73423655302*
- **Qww** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **Qwwf** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **Qwwf_0** `['float64']`: *26898.154839815834*
- **Tcs_re** `['ndarray']`: *array([0, 0, 0, ..., 0, 0, 0])*
- **Tcs_sup** `['ndarray']`: *array([0, 0, 0, ..., 0, 0, 0])*
- **Ths_re** `['ndarray']`: *array([0, 0, 0, ..., 0, 0, 0])*
- **Ths_sup** `['ndarray']`: *array([0, 0, 0, ..., 0, 0, 0])*
- **Vw** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **Year** `['int64']`: *2016*
- **fforma** `['float64']`: *1.0*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x141B7E10>*
- **nf_ag** `['float64']`: *7.0*
- **nfp** `['float64']`: *1.0*
- **qv_req** `['ndarray']`: *array([ 0.80791366,  0.80791366,  0.80791366, ...,  0.80791366,
        0.80791366,  0.80791366])*
- **sys_e_cooling** `['unicode']`: *u'T3'*
- **sys_e_heating** `['unicode']`: *u'T2'*
- **Ehs_lat_aux** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*


### Output
- `['tuple']`: (array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]))

### Docstring template

```
PARAMETERS
----------

:param Ll:
:type Ll: float64

:param Lw:
:type Lw: float64

:param Mww:
:type Mww: ndarray

:param Qcsf:
:type Qcsf: ndarray

:param Qcsf_0:
:type Qcsf_0: float64

:param Qhsf:
:type Qhsf: ndarray

:param Qhsf_0:
:type Qhsf_0: float64

:param Qww:
:type Qww: ndarray

:param Qwwf:
:type Qwwf: ndarray

:param Qwwf_0:
:type Qwwf_0: float64

:param Tcs_re:
:type Tcs_re: ndarray

:param Tcs_sup:
:type Tcs_sup: ndarray

:param Ths_re:
:type Ths_re: ndarray

:param Ths_sup:
:type Ths_sup: ndarray

:param Vw:
:type Vw: ndarray

:param Year:
:type Year: int64

:param fforma:
:type fforma: float64

:param gv:
:type gv: GlobalVariables

:param nf_ag:
:type nf_ag: float64

:param nfp:
:type nfp: float64

:param qv_req:
:type qv_req: ndarray

:param sys_e_cooling:
:type sys_e_cooling: unicode

:param sys_e_heating:
:type sys_e_heating: unicode

:param Ehs_lat_aux:
:type Ehs_lat_aux: ndarray

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Eauxf_cs_dis
- number of invocations: 1
- max duration: 0.033 s
- avg duration: 0.033 s
- min duration: 0.033 s
- total duration: 0.033 s

### Input
- **Qcsf** `['float64']`: *-0.0*
- **Qcsf0** `['float64']`: *-613906.75789570482*
- **Imax** `['float64']`: *115.0*
- **deltaP_des** `['float64']`: *14.950000000000001*
- **b** `['int32']`: *1*
- **ts** `['int32']`: *0*
- **tr** `['int32']`: *0*
- **cpw** `['float64']`: *4.1840000000000002*


### Output
- `['float']`: 0.0

### Docstring template

```
PARAMETERS
----------

:param Qcsf:
:type Qcsf: float64

:param Qcsf0:
:type Qcsf0: float64

:param Imax:
:type Imax: float64

:param deltaP_des:
:type deltaP_des: float64

:param b:
:type b: int32

:param ts:
:type ts: int32

:param tr:
:type tr: int32

:param cpw:
:type cpw: float64

RETURNS
-------

:returns:
:rtype: float

```

[TOC](#table-of-contents)
---

# calc_Eauxf_fw
- number of invocations: 1
- max duration: 0.036 s
- avg duration: 0.036 s
- min duration: 0.036 s
- total duration: 0.036 s

### Input
- **freshw** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **nf** `['float64']`: *7.0*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x141D7B50>*


### Output
- `['ndarray']`: array([ 0.,  0.,  0., ...,  0.,  0.,  0.])

### Docstring template

```
PARAMETERS
----------

:param freshw:
:type freshw: ndarray

:param nf:
:type nf: float64

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# calc_Eauxf_hs_dis
- number of invocations: 1
- max duration: 0.029 s
- avg duration: 0.029 s
- min duration: 0.029 s
- total duration: 0.029 s

### Input
- **Qhsf** `['float64']`: *0.0*
- **Qhsf0** `['float64']`: *280780.73423655302*
- **Imax** `['float64']`: *115.0*
- **deltaP_des** `['float64']`: *14.950000000000001*
- **b** `['int32']`: *1*
- **ts** `['int32']`: *0*
- **tr** `['int32']`: *0*
- **cpw** `['float64']`: *4.1840000000000002*


### Output
- `['float']`: 0.0

### Docstring template

```
PARAMETERS
----------

:param Qhsf:
:type Qhsf: float64

:param Qhsf0:
:type Qhsf0: float64

:param Imax:
:type Imax: float64

:param deltaP_des:
:type deltaP_des: float64

:param b:
:type b: int32

:param ts:
:type ts: int32

:param tr:
:type tr: int32

:param cpw:
:type cpw: float64

RETURNS
-------

:returns:
:rtype: float

```

[TOC](#table-of-contents)
---

# calc_Eauxf_ve
- number of invocations: 1
- max duration: 0.031 s
- avg duration: 0.031 s
- min duration: 0.031 s
- total duration: 0.031 s

### Input
- **Qhsf** `['float64']`: *0.0*
- **Qcsf** `['float64']`: *-0.0*
- **P_ve** `['float64']`: *0.55000000000000004*
- **qve** `['float64']`: *0.80791365509236346*
- **SystemH** `['unicode_']`: *u'T2'*
- **SystemC** `['unicode_']`: *u'T3'*


### Output
- `['float']`: 0.0

### Docstring template

```
PARAMETERS
----------

:param Qhsf:
:type Qhsf: float64

:param Qcsf:
:type Qcsf: float64

:param P_ve:
:type P_ve: float64

:param qve:
:type qve: float64

:param SystemH:
:type SystemH: unicode_

:param SystemC:
:type SystemC: unicode_

RETURNS
-------

:returns:
:rtype: float

```

[TOC](#table-of-contents)
---

# calc_Eauxf_ww
- number of invocations: 1
- max duration: 0.028 s
- avg duration: 0.028 s
- min duration: 0.028 s
- total duration: 0.028 s

### Input
- **Qww** `['float64']`: *0.0*
- **Qwwf** `['float64']`: *0.0*
- **Qwwf0** `['float64']`: *26898.154839815834*
- **Imax** `['float64']`: *115.0*
- **deltaP_des** `['float64']`: *14.950000000000001*
- **b** `['int32']`: *1*
- **qV_des** `['float64']`: *0.0*


### Output
- `['float']`: 0.0

### Docstring template

```
PARAMETERS
----------

:param Qww:
:type Qww: float64

:param Qwwf:
:type Qwwf: float64

:param Qwwf0:
:type Qwwf0: float64

:param Imax:
:type Imax: float64

:param deltaP_des:
:type deltaP_des: float64

:param b:
:type b: int32

:param qV_des:
:type qV_des: float64

RETURNS
-------

:returns:
:rtype: float

```

[TOC](#table-of-contents)
---

# calc_Eint
- number of invocations: 1
- max duration: 1.05 s
- avg duration: 1.05 s
- min duration: 1.05 s
- total duration: 1.05 s

### Input
- **tsd** `['dict']`: *{'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'qm_ve_mech': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'T_sky': array([ 34.64474108,  34.64474108,  34.46468985, ...,  34.20457916,
        34.24561453,  34.21825944]), 'Twwf_sup': 60, 'Qcs_sen_incl_em_ls': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta': array([ nan,  nan,  nan,*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x14168190>*
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*
- **schedules** `['list']`: *[([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, *


### Output
- `['dict']`: {'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  6183.,  6183.]), 'T_sky': array([ 34.64474108,  34.64474108,  34.46468985, ...,  34.20457916,
        34.

### Docstring template

```
PARAMETERS
----------

:param tsd:
:type tsd: dict

:param bpr:
:type bpr: BuildingPropertiesRow

:param list_uses:
:type list_uses: list

:param schedules:
:type schedules: list

RETURNS
-------

:returns:
:rtype: dict

```

[TOC](#table-of-contents)
---

# calc_Htr
- number of invocations: 1
- max duration: 0.029 s
- avg duration: 0.029 s
- min duration: 0.029 s
- total duration: 0.029 s

### Input
- **Hve** `['float64']`: *1270.4280643596396*
- **Htr_is** `['float64']`: *29263.392857143353*
- **Htr_ms** `['float64']`: *131040.0*
- **Htr_w** `['float64']`: *1300.0*


### Output
- `['tuple']`: (1217.5690569376122, 2517.569056937612, 2470.1127128217076)

### Docstring template

```
PARAMETERS
----------

:param Hve:
:type Hve: float64

:param Htr_is:
:type Htr_is: float64

:param Htr_ms:
:type Htr_ms: float64

:param Htr_w:
:type Htr_w: float64

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_I_rad
- number of invocations: 1
- max duration: 0.163 s
- avg duration: 0.163 s
- min duration: 0.163 s
- total duration: 0.163 s

### Input
- **t** `['int']`: *5472*
- **tsd** `['dict']`: *{'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x1456E530>*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x1456E530>*


### Output
- `['float64']`: 9240.9396390576476

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int

:param tsd:
:type tsd: dict

:param bpr:
:type bpr: BuildingPropertiesRow

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_I_sol
- number of invocations: 1
- max duration: 0.363 s
- avg duration: 0.363 s
- min duration: 0.363 s
- total duration: 0.363 s

### Input
- **t** `['int']`: *5472*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x1401F5B0>*
- **tsd** `['dict']`: *{'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x146074F0>*


### Output
- `['tuple']`: (-9240.9396390576476, 9240.9396390576476)

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int

:param bpr:
:type bpr: BuildingPropertiesRow

:param tsd:
:type tsd: dict

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Qgain_lat
- number of invocations: 1
- max duration: 0.038 s
- avg duration: 0.038 s
- min duration: 0.038 s
- total duration: 0.038 s

### Input
- **people** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **X_ghp** `['float64']`: *80.0*
- **sys_e_cooling** `['unicode']`: *u'T3'*
- **sys_e_heating** `['unicode']`: *u'T2'*


### Output
- `['ndarray']`: array([ 0.,  0.,  0., ...,  0.,  0.,  0.])

### Docstring template

```
PARAMETERS
----------

:param people:
:type people: ndarray

:param X_ghp:
:type X_ghp: float64

:param sys_e_cooling:
:type sys_e_cooling: unicode

:param sys_e_heating:
:type sys_e_heating: unicode

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# calc_Qgain_sen
- number of invocations: 1
- max duration: 0.484 s
- avg duration: 0.484 s
- min duration: 0.484 s
- total duration: 0.484 s

### Input
- **t** `['int']`: *5472*
- **tsd** `['dict']`: *{'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x068B1370>*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x068B1370>*


### Output
- `['dict']`: {'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int

:param tsd:
:type tsd: dict

:param bpr:
:type bpr: BuildingPropertiesRow

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: dict

```

[TOC](#table-of-contents)
---

# calc_Qhs_Qcs
- number of invocations: 1
- max duration: 0.033 s
- avg duration: 0.033 s
- min duration: 0.033 s
- total duration: 0.033 s

### Input
- **SystemH** `['unicode']`: *u'T2'*
- **SystemC** `['unicode']`: *u'T3'*
- **tm_t0** `['float64']`: *13.699999999999999*
- **te_t** `['float64']`: *13.699999999999999*
- **tintH_set** `['float64']`: *-30.0*
- **tintC_set** `['int32']`: *28*
- **Htr_em** `['float64']`: *620.42362322454858*
- **Htr_ms** `['float64']`: *131040.0*
- **Htr_is** `['float64']`: *29263.392857143353*
- **Htr_1** `['float64']`: *1217.5690569376122*
- **Htr_2** `['float64']`: *2517.569056937612*
- **Htr_3** `['float64']`: *2470.1127128217076*
- **I_st** `['float64']`: *4614.8322599917401*
- **Hve** `['float64']`: *1270.4280643596396*
- **Htr_w** `['float64']`: *1300.0*
- **I_ia** `['float64']`: *2782.3499999999999*
- **I_m** `['float64']`: *-10964.64565249684*
- **Cm** `['float64']`: *1350000000.0*
- **Af** `['float64']`: *4500.0*
- **Losses** `['bool']`: *False*
- **tHset_corr** `['float']`: *1.0999999999999999*
- **tCset_corr** `['float']`: *-0.7*
- **IC_max** `['float64']`: *-2250000.0*
- **IH_max** `['float64']`: *2250000.0*
- **Flag** `['bool_']`: *True*


### Output
- `['tuple']`: (13.689853850767667, 13.838603747816054, 13.749541487617034, 0, 0, 0, 13.777150788278728, 38519.86332027304)

### Docstring template

```
PARAMETERS
----------

:param SystemH:
:type SystemH: unicode

:param SystemC:
:type SystemC: unicode

:param tm_t0:
:type tm_t0: float64

:param te_t:
:type te_t: float64

:param tintH_set:
:type tintH_set: float64

:param tintC_set:
:type tintC_set: int32

:param Htr_em:
:type Htr_em: float64

:param Htr_ms:
:type Htr_ms: float64

:param Htr_is:
:type Htr_is: float64

:param Htr_1:
:type Htr_1: float64

:param Htr_2:
:type Htr_2: float64

:param Htr_3:
:type Htr_3: float64

:param I_st:
:type I_st: float64

:param Hve:
:type Hve: float64

:param Htr_w:
:type Htr_w: float64

:param I_ia:
:type I_ia: float64

:param I_m:
:type I_m: float64

:param Cm:
:type Cm: float64

:param Af:
:type Af: float64

:param Losses:
:type Losses: bool

:param tHset_corr:
:type tHset_corr: float

:param tCset_corr:
:type tCset_corr: float

:param IC_max:
:type IC_max: float64

:param IH_max:
:type IH_max: float64

:param Flag:
:type Flag: bool_

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Qhs_Qcs_dis_ls
- number of invocations: 1
- max duration: 0.033 s
- avg duration: 0.033 s
- min duration: 0.033 s
- total duration: 0.033 s

### Input
- **tair** `['float64']`: *18.09775109867255*
- **text** `['float64']`: *1.1000000000000001*
- **Qhs** `['float64']`: *0.0*
- **Qcs** `['float64']`: *0.0*
- **tsh** `['float64']`: *70.0*
- **trh** `['float64']`: *55.0*
- **tsc** `['int64']`: *7*
- **trc** `['int64']`: *15*
- **Qhs_max** `['float64']`: *279838.73423655302*
- **Qcs_max** `['float64']`: *-203788.88452871342*
- **D** `['int32']`: *20*
- **Y** `['float64']`: *0.20000000000000001*
- **SystemH** `['unicode_']`: *u'T2'*
- **SystemC** `['unicode_']`: *u'T3'*
- **Bf** `['float64']`: *0.69999999999999996*
- **Lv** `['float64']`: *76.3125*


### Output
- `['tuple']`: (0, 0)

### Docstring template

```
PARAMETERS
----------

:param tair:
:type tair: float64

:param text:
:type text: float64

:param Qhs:
:type Qhs: float64

:param Qcs:
:type Qcs: float64

:param tsh:
:type tsh: float64

:param trh:
:type trh: float64

:param tsc:
:type tsc: int64

:param trc:
:type trc: int64

:param Qhs_max:
:type Qhs_max: float64

:param Qcs_max:
:type Qcs_max: float64

:param D:
:type D: int32

:param Y:
:type Y: float64

:param SystemH:
:type SystemH: unicode_

:param SystemC:
:type SystemC: unicode_

:param Bf:
:type Bf: float64

:param Lv:
:type Lv: float64

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Qhs_Qcs_sys_max
- number of invocations: 1
- max duration: 0.03 s
- avg duration: 0.03 s
- min duration: 0.03 s
- total duration: 0.03 s

### Input
- **Af** `['float64']`: *4500.0*
- **prop_HVAC** `['dict']`: *{u'Qcsmax_Wm2': 500, u'dTcs0_C': 8, u'type_ctrl': u'T2', u'type_cs': u'T3', u'dThs0_C': 15, u'Qhsmax_Wm2': 500, u'Tscs0_C': 7, u'type_hs': u'T2', u'Tsww0_C': 60, u'Qwwmax_Wm2': 500, u'dTww0_C': 50, u'Tshs0_C': 70, u'type_dhw': u'T1'}*


### Output
- `['tuple']`: (-2250000.0, 2250000.0)

### Docstring template

```
PARAMETERS
----------

:param Af:
:type Af: float64

:param prop_HVAC:
:type prop_HVAC: dict

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Qww
- number of invocations: 1
- max duration: 0.027 s
- avg duration: 0.027 s
- min duration: 0.027 s
- total duration: 0.027 s

### Input
- **mww** `['float64']`: *0.0*
- **Tww_sup_0** `['int64']`: *60*
- **Tww_re** `['float64']`: *10.0*
- **Cpw** `['float64']`: *4.1840000000000002*


### Output
- `['float64']`: 0.0

### Docstring template

```
PARAMETERS
----------

:param mww:
:type mww: float64

:param Tww_sup_0:
:type Tww_sup_0: int64

:param Tww_re:
:type Tww_re: float64

:param Cpw:
:type Cpw: float64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_Qww_dis_ls_nr
- number of invocations: 1
- max duration: 0.032 s
- avg duration: 0.032 s
- min duration: 0.032 s
- total duration: 0.032 s

### Input
- **tair** `['float64']`: *18.09775109867255*
- **Qww** `['float64']`: *0.0*
- **Lvww_dis** `['float64']`: *64.0625*
- **Lvww_c** `['float64']`: *57.8125*
- **Y** `['float64']`: *0.20000000000000001*
- **Qww_0** `['float64']`: *24854.952380952382*
- **V** `['float64']`: *221.5887865406485*
- **Flowtap** `['float64']`: *0.035999999999999997*
- **twws** `['int64']`: *60*
- **Cpw** `['float64']`: *4.1840000000000002*
- **Pwater** `['int32']`: *998*
- **Bf** `['float64']`: *0.69999999999999996*
- **te** `['float64']`: *1.1000000000000001*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x1401F5B0>*


### Output
- `['int']`: 0

### Docstring template

```
PARAMETERS
----------

:param tair:
:type tair: float64

:param Qww:
:type Qww: float64

:param Lvww_dis:
:type Lvww_dis: float64

:param Lvww_c:
:type Lvww_c: float64

:param Y:
:type Y: float64

:param Qww_0:
:type Qww_0: float64

:param V:
:type V: float64

:param Flowtap:
:type Flowtap: float64

:param twws:
:type twws: int64

:param Cpw:
:type Cpw: float64

:param Pwater:
:type Pwater: int32

:param Bf:
:type Bf: float64

:param te:
:type te: float64

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: int

```

[TOC](#table-of-contents)
---

# calc_Qww_dis_ls_r
- number of invocations: 1
- max duration: 0.034 s
- avg duration: 0.034 s
- min duration: 0.034 s
- total duration: 0.034 s

### Input
- **Tair** `['float64']`: *18.09775109867255*
- **Qww** `['float64']`: *0.0*
- **lsww_dis** `['float64']`: *498.75*
- **lcww_dis** `['float64']`: *97.0*
- **Y** `['float64']`: *0.29999999999999999*
- **Qww_0** `['float64']`: *24854.952380952382*
- **V** `['float64']`: *221.5887865406485*
- **Flowtap** `['float64']`: *0.035999999999999997*
- **twws** `['int64']`: *60*
- **Cpw** `['float64']`: *4.1840000000000002*
- **Pwater** `['int32']`: *998*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x1404C470>*


### Output
- `['int']`: 0

### Docstring template

```
PARAMETERS
----------

:param Tair:
:type Tair: float64

:param Qww:
:type Qww: float64

:param lsww_dis:
:type lsww_dis: float64

:param lcww_dis:
:type lcww_dis: float64

:param Y:
:type Y: float64

:param Qww_0:
:type Qww_0: float64

:param V:
:type V: float64

:param Flowtap:
:type Flowtap: float64

:param twws:
:type twws: int64

:param Cpw:
:type Cpw: float64

:param Pwater:
:type Pwater: int32

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: int

```

[TOC](#table-of-contents)
---

# calc_Qww_schedule
- number of invocations: 1
- max duration: 0.511 s
- avg duration: 0.511 s
- min duration: 0.511 s
- total duration: 0.511 s

### Input
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*
- **schedules** `['list']`: *[([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, *
- **building_uses** `['dict']`: *{u'PFloor': 1.0, u'OFFICE': 1.0, u'PARKING': 0.0}*


### Output
- `['ndarray']`: array([ 0.,  0.,  0., ...,  0.,  0.,  0.])

### Docstring template

```
PARAMETERS
----------

:param list_uses:
:type list_uses: list

:param schedules:
:type schedules: list

:param building_uses:
:type building_uses: dict

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# calc_Qww_st_ls
- number of invocations: 1
- max duration: 0.267 s
- avg duration: 0.267 s
- min duration: 0.267 s
- total duration: 0.267 s

### Input
- **Vww** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*
- **Tww_setpoint** `['int']`: *60*
- **Ta** `['ndarray']`: *array([ 18.0977511 ,  17.98130007,  17.86025781, ...,  18.43915293,
        18.31809641,  18.19779079])*
- **Bf** `['float']`: *0.7*
- **Pwater** `['int']`: *998*
- **Cpw** `['float']`: *4.184*
- **Qww_dis_ls_r** `['ndarray']`: *array([0, 0, 0, ..., 0, 0, 0])*
- **Qww_dis_ls_nr** `['ndarray']`: *array([0, 0, 0, ..., 0, 0, 0])*
- **U_dhwtank** `['float']`: *0.225*
- **AR** `['float']`: *3.3*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x141D7630>*
- **T_ext** `['ndarray']`: *array([ 1.1,  1.1,  1. , ...,  1.4,  1.4,  1.4])*
- **Qww** `['ndarray']`: *array([ 0.,  0.,  0., ...,  0.,  0.,  0.])*


### Output
- `['tuple']`: (array([ 43.53614507,  43.54472871,  43.61106789, ...,  43.21721942,
        43.22706533,  43.23672449]), array([ 59.9756721 ,  59.95133941,  59.92696965, ...,  59.89415203,
        59.86999685,  59.84583627]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]))

### Docstring template

```
PARAMETERS
----------

:param Vww:
:type Vww: ndarray

:param Tww_setpoint:
:type Tww_setpoint: int

:param Ta:
:type Ta: ndarray

:param Bf:
:type Bf: float

:param Pwater:
:type Pwater: int

:param Cpw:
:type Cpw: float

:param Qww_dis_ls_r:
:type Qww_dis_ls_r: ndarray

:param Qww_dis_ls_nr:
:type Qww_dis_ls_nr: ndarray

:param U_dhwtank:
:type U_dhwtank: float

:param AR:
:type AR: float

:param gv:
:type gv: GlobalVariables

:param T_ext:
:type T_ext: ndarray

:param Qww:
:type Qww: ndarray

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_Qwwf
- number of invocations: 1
- max duration: 1.634 s
- avg duration: 1.634 s
- min duration: 1.634 s
- total duration: 1.634 s

### Input
- **Af** `['float64']`: *4500.0*
- **Lcww_dis** `['float64']`: *97.0*
- **Lsww_dis** `['float64']`: *498.75*
- **Lvww_c** `['float64']`: *57.8125*
- **Lvww_dis** `['float64']`: *64.0625*
- **T_ext** `['ndarray']`: *array([ 1.1,  1.1,  1. , ...,  1.4,  1.4,  1.4])*
- **Ta** `['ndarray']`: *array([ 18.0977511 ,  17.98130007,  17.86025781, ...,  18.43915293,
        18.31809641,  18.19779079])*
- **Tww_re** `['ndarray']`: *array([ 10.,  10.,  10., ...,  10.,  10.,  10.])*
- **Tww_sup_0** `['int64']`: *60*
- **Y** `['list']`: *[0.2, 0.3, 0.3]*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x1458C3F0>*
- **Vww_lpd** `['float64']`: *10.0*
- **Vw_lpd** `['float64']`: *20.0*
- **Occ_m2p** `['float64']`: *14.0*
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*
- **schedules** `['list']`: *[([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, *
- **building_uses** `['dict']`: *{u'PFloor': 1.0, u'OFFICE': 1.0, u'PARKING': 0.0}*


### Output
- `['tuple']`: (array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 43.53614507,  43.54472871,  43.61106789, ...,  43.21721942,
        43.22706533,  43.23672449]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 26898.154839815834, array([ 59.9756721 ,  59.95133941,  59.92696965, ...,  59.89415203,
        59.86999685,  59.84583627]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), array([ 0.,  0.,  0., ...,  0.,  0.,  0.]))

### Docstring template

```
PARAMETERS
----------

:param Af:
:type Af: float64

:param Lcww_dis:
:type Lcww_dis: float64

:param Lsww_dis:
:type Lsww_dis: float64

:param Lvww_c:
:type Lvww_c: float64

:param Lvww_dis:
:type Lvww_dis: float64

:param T_ext:
:type T_ext: ndarray

:param Ta:
:type Ta: ndarray

:param Tww_re:
:type Tww_re: ndarray

:param Tww_sup_0:
:type Tww_sup_0: int64

:param Y:
:type Y: list

:param gv:
:type gv: GlobalVariables

:param Vww_lpd:
:type Vww_lpd: float64

:param Vw_lpd:
:type Vw_lpd: float64

:param Occ_m2p:
:type Occ_m2p: float64

:param list_uses:
:type list_uses: list

:param schedules:
:type schedules: list

:param building_uses:
:type building_uses: dict

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_coeff_lea_zone
- number of invocations: 1
- max duration: 0.029 s
- avg duration: 0.029 s
- min duration: 0.029 s
- total duration: 0.029 s

### Input
- **qv_delta_p_lea_ref** `['float64']`: *31250.0*


### Output
- `['float64']`: 2299.5191401150646

### Docstring template

```
PARAMETERS
----------

:param qv_delta_p_lea_ref:
:type qv_delta_p_lea_ref: float64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_coeff_vent_zone
- number of invocations: 1
- max duration: 0.036 s
- avg duration: 0.036 s
- min duration: 0.036 s
- total duration: 0.036 s

### Input
- **area_vent_zone** `['int']`: *0*


### Output
- `['float']`: 0.0

### Docstring template

```
PARAMETERS
----------

:param area_vent_zone:
:type area_vent_zone: int

RETURNS
-------

:returns:
:rtype: float

```

[TOC](#table-of-contents)
---

# calc_disls
- number of invocations: 1
- max duration: 0.033 s
- avg duration: 0.033 s
- min duration: 0.033 s
- total duration: 0.033 s

### Input
- **tamb** `['float']`: *22.0*
- **hotw** `['float']`: *4970.990476190476*
- **Flowtap** `['float']`: *0.036*
- **V** `['float']`: *221.5887865406485*
- **twws** `['long']`: *60L*
- **Lsww_dis** `['float']`: *498.75*
- **p** `['int']`: *998*
- **cpw** `['float']`: *4.184*
- **Y** `['float']`: *0.3*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x14168230>*


### Output
- `['float64']`: 41.209155148741452

### Docstring template

```
PARAMETERS
----------

:param tamb:
:type tamb: float

:param hotw:
:type hotw: float

:param Flowtap:
:type Flowtap: float

:param V:
:type V: float

:param twws:
:type twws: long

:param Lsww_dis:
:type Lsww_dis: float

:param p:
:type p: int

:param cpw:
:type cpw: float

:param Y:
:type Y: float

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_h
- number of invocations: 1
- max duration: 0.028 s
- avg duration: 0.028 s
- min duration: 0.028 s
- total duration: 0.028 s

### Input
- **t** `['int32']`: *24*
- **w** `['float64']`: *0.011593980099780365*


### Output
- `['float64']`: 53.650534390756988

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int32

:param w:
:type w: float64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_h_ve_adj
- number of invocations: 1
- max duration: 0.032 s
- avg duration: 0.032 s
- min duration: 0.032 s
- total duration: 0.032 s

### Input
- **q_m_mech** `['float64']`: *1.2603453019440871*
- **q_m_nat** `['int']`: *0*
- **temp_ext** `['float64']`: *13.699999999999999*
- **temp_sup** `['float64']`: *13.699999999999999*
- **temp_zone_set** `['float64']`: *13.699999999999999*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x1419C890>*


### Output
- `['float64']`: 1270.4280643596396

### Docstring template

```
PARAMETERS
----------

:param q_m_mech:
:type q_m_mech: float64

:param q_m_nat:
:type q_m_nat: int

:param temp_ext:
:type temp_ext: float64

:param temp_sup:
:type temp_sup: float64

:param temp_zone_set:
:type temp_zone_set: float64

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_hex
- number of invocations: 1
- max duration: 0.088 s
- avg duration: 0.088 s
- min duration: 0.088 s
- total duration: 0.088 s

### Input
- **rel_humidity_ext** `['int64']`: *93*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x14168B10>*
- **temp_ext** `['float64']`: *13.699999999999999*
- **temp_zone_prev** `['float64']`: *13.699999999999999*
- **timestep** `['int']`: *5472*


### Output
- `['tuple']`: (13.699999999999999, 0.0091380190832960652)

### Docstring template

```
PARAMETERS
----------

:param rel_humidity_ext:
:type rel_humidity_ext: int64

:param gv:
:type gv: GlobalVariables

:param temp_ext:
:type temp_ext: float64

:param temp_zone_prev:
:type temp_zone_prev: float64

:param timestep:
:type timestep: int

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_hr
- number of invocations: 1
- max duration: 0.032 s
- avg duration: 0.032 s
- min duration: 0.032 s
- total duration: 0.032 s

### Input
- **emisivity** `['float64']`: *0.89000000000000001*
- **theta_ss** `['float64']`: *36.761822102218716*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x14607CB0>*


### Output
- `['float64']`: 5.9995230702280633

### Docstring template

```
PARAMETERS
----------

:param emisivity:
:type emisivity: float64

:param theta_ss:
:type theta_ss: float64

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_hvac
- number of invocations: 1
- max duration: 0.039 s
- avg duration: 0.039 s
- min duration: 0.039 s
- total duration: 0.039 s

### Input
- **rhum_1** `['int64']`: *93*
- **temp_1** `['float64']`: *13.699999999999999*
- **temp_zone_set** `['float']`: *13.838603747816054*
- **qv_req** `['float64']`: *1.0502877516200726*
- **qe_sen** `['int']`: *0*
- **temp_5_prev** `['float64']`: *13.699999999999999*
- **wint** `['float64']`: *0.0*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x14167870>*
- **timestep** `['int']`: *5472*


### Output
- `['tuple']`: (0, 0, 0, 0, 0, 0, 0, nan, nan, 13.699999999999999, 13.699999999999999, 0, 0, 13.838603747816054)

### Docstring template

```
PARAMETERS
----------

:param rhum_1:
:type rhum_1: int64

:param temp_1:
:type temp_1: float64

:param temp_zone_set:
:type temp_zone_set: float

:param qv_req:
:type qv_req: float64

:param qe_sen:
:type qe_sen: int

:param temp_5_prev:
:type temp_5_prev: float64

:param wint:
:type wint: float64

:param gv:
:type gv: GlobalVariables

:param timestep:
:type timestep: int

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_mww
- number of invocations: 1
- max duration: 0.036 s
- avg duration: 0.036 s
- min duration: 0.036 s
- total duration: 0.036 s

### Input
- **schedule** `['float64']`: *0.0*
- **Vww_lpd** `['float64']`: *10.0*
- **Occ_m2p** `['float64']`: *14.0*
- **Af** `['float64']`: *4500.0*
- **Pwater** `['int32']`: *998*


### Output
- `['tuple']`: (0.0, 0.0)

### Docstring template

```
PARAMETERS
----------

:param schedule:
:type schedule: float64

:param Vww_lpd:
:type Vww_lpd: float64

:param Occ_m2p:
:type Occ_m2p: float64

:param Af:
:type Af: float64

:param Pwater:
:type Pwater: int32

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_occ
- number of invocations: 1
- max duration: 0.996 s
- avg duration: 0.996 s
- min duration: 0.996 s
- total duration: 0.996 s

### Input
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*
- **schedules** `['list']`: *[([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, *
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x068BE230>*


### Output
- `['ndarray']`: array([ 0.,  0.,  0., ...,  0.,  0.,  0.])

### Docstring template

```
PARAMETERS
----------

:param list_uses:
:type list_uses: list

:param schedules:
:type schedules: list

:param bpr:
:type bpr: BuildingPropertiesRow

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# calc_occ_schedule
- number of invocations: 1
- max duration: 0.462 s
- avg duration: 0.462 s
- min duration: 0.462 s
- total duration: 0.462 s

### Input
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*
- **schedules** `['list']`: *[([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, *
- **building_uses** `['dict']`: *{u'PFloor': 1.0, u'OFFICE': 1.0, u'PARKING': 0.0}*


### Output
- `['ndarray']`: array([ 0.,  0.,  0., ...,  0.,  0.,  0.])

### Docstring template

```
PARAMETERS
----------

:param list_uses:
:type list_uses: list

:param schedules:
:type schedules: list

:param building_uses:
:type building_uses: dict

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# calc_qv_delta_p_ref
- number of invocations: 1
- max duration: 0.029 s
- avg duration: 0.029 s
- min duration: 0.029 s
- total duration: 0.029 s

### Input
- **n_delta_p_ref** `['float64']`: *2.0*
- **vol_building** `['float64']`: *15625.0*


### Output
- `['float64']`: 31250.0

### Docstring template

```
PARAMETERS
----------

:param n_delta_p_ref:
:type n_delta_p_ref: float64

:param vol_building:
:type vol_building: float64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_radiator
- number of invocations: 1
- max duration: 0.03 s
- avg duration: 0.03 s
- min duration: 0.03 s
- total duration: 0.03 s

### Input
- **Qh** `['float64']`: *0.0*
- **tair** `['float64']`: *18.09775109867255*
- **Qh0** `['float64']`: *280780.73423655302*
- **tair0** `['float64']`: *22.0*
- **tsh0** `['float64']`: *70.0*
- **trh0** `['float64']`: *55.0*


### Output
- `['tuple']`: (0, 0, 0)

### Docstring template

```
PARAMETERS
----------

:param Qh:
:type Qh: float64

:param tair:
:type tair: float64

:param Qh0:
:type Qh0: float64

:param tair0:
:type tair0: float64

:param tsh0:
:type tsh0: float64

:param trh0:
:type trh0: float64

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_t_from_h
- number of invocations: 1
- max duration: 0.031 s
- avg duration: 0.031 s
- min duration: 0.031 s
- total duration: 0.031 s

### Input
- **h** `['float64']`: *-2.5782916214161133*
- **w** `['float64']`: *0.011593980099780365*


### Output
- `['float64']`: -30.764459852313106

### Docstring template

```
PARAMETERS
----------

:param h:
:type h: float64

:param w:
:type w: float64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_temperatures_emission_systems
- number of invocations: 1
- max duration: 0.43 s
- avg duration: 0.43 s
- min duration: 0.43 s
- total duration: 0.43 s

### Input
- **tsd** `['dict']`: *{'Im_tot': array([ 7086.42209963,  7056.77191846,  6788.11207801, ...,  6320.89192022,
        6282.20158332,  6259.31405999]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Qhsf': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 18.40194999,  18.28281563,  18.1612885 , ...,  18.76617412,
        18.64232814,  18.519250*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x141D7630>*
- **Qcsf_0** `['float64']`: *-613906.75789570482*
- **Qhsf_0** `['float64']`: *280780.73423655302*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x14514570>*


### Output
- `['tuple']`: (array([0, 0, 0, ..., 0, 0, 0]), array([0, 0, 0, ..., 0, 0, 0]), array([0, 0, 0, ..., 0, 0, 0]), array([0, 0, 0, ..., 0, 0, 0]), array([0, 0, 0, ..., 0, 0, 0]), array([0, 0, 0, ..., 0, 0, 0]))

### Docstring template

```
PARAMETERS
----------

:param tsd:
:type tsd: dict

:param bpr:
:type bpr: BuildingPropertiesRow

:param Qcsf_0:
:type Qcsf_0: float64

:param Qhsf_0:
:type Qhsf_0: float64

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# calc_thermal_load_hvac
- number of invocations: 1
- max duration: 0.555 s
- avg duration: 0.555 s
- min duration: 0.555 s
- total duration: 0.555 s

### Input
- **t** `['int']`: *5472*
- **tsd** `['dict']`: *{'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x141B7470>*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x145855F0>*


### Output
- `['dict']`: {'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int

:param tsd:
:type tsd: dict

:param bpr:
:type bpr: BuildingPropertiesRow

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: dict

```

[TOC](#table-of-contents)
---

# calc_thermal_load_mechanical_and_natural_ventilation_timestep
- number of invocations: 1
- max duration: 0.111 s
- avg duration: 0.111 s
- min duration: 0.111 s
- total duration: 0.111 s

### Input
- **t** `['int']`: *6192*
- **tsd** `['dict']`: *{'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x1401FCD0>*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x1401FCD0>*


### Output
- `['dict']`: {'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'w_int': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 've': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'people': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta_sup_cs': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Elf': array([ 5724.,  5724.,  5724., ...,  4293.,  4293.,  4293.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ealf': array([ 8244.,  8244.,  8244., ...,  6183.,  61

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: int

:param tsd:
:type tsd: dict

:param bpr:
:type bpr: BuildingPropertiesRow

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: dict

```

[TOC](#table-of-contents)
---

# calc_thermal_loads
- number of invocations: 1
- max duration: 10.682 s
- avg duration: 10.682 s
- min duration: 10.682 s
- total duration: 10.682 s

### Input
- **building_name** `['str']`: *'B01'*
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x145148F0>*
- **weather_data** `['DataFrame']`: *(8760, 4)*
- **usage_schedules** `['dict']`: *{'list_uses': [u'OFFICE', u'PARKING'], 'schedules': [([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0*
- **date** `['DatetimeIndex']`: *DatetimeIndex(['2016-01-01 00:00:00', '2016-01-01 01:00:00',
               '2016-01-01 02:00:00', '2016-01-01 03:00:00',
               '2016-01-01 04:00:00', '2016-01-01 05:00:00',
               '2016-01-01 06:00:00', '2016-01-01 07:00:00',
               '2016-01-01 08:00:00', '2016-01-01 09:00:00',
               ...
               '2016-12-30 14:00:00', '2016-12-30 15:00:00',
               '2016-12-30 16:00:00', '2016-12-30 17:00:00',
               '2016-12-30 18:00:00', '2016-12-30 19:0*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x068B1370>*
- **locator** `['LocatorDecorator']`: *???*

#### weather_data:
```
         drybulb_C  relhum_percent   windspd_ms    skytemp_C
count  8760.000000     8760.000000  8760.000000  8760.000000
mean     10.150000       73.861644     1.838094    44.884267
std       8.022269       15.889964     1.847214     9.589083
min     -10.300000       28.000000     0.000000    20.330004
25%       3.700000       62.000000     0.500000    36.956793
50%      10.400000       77.000000     1.300000    45.147171
75%      16.100000       86.000000     2.500000    52.211059
max      32.300000      100.000000    15.300000    70.460600
```

### Output
- `['NoneType']`: None

### Docstring template

```
PARAMETERS
----------

:param building_name:
:type building_name: str

:param bpr:
:type bpr: BuildingPropertiesRow

:param weather_data:
:type weather_data: DataFrame

:param usage_schedules:
:type usage_schedules: dict

:param date:
:type date: DatetimeIndex

:param gv:
:type gv: GlobalVariables

:param locator:
:type locator: LocatorDecorator

RETURNS
-------

:returns:
:rtype: NoneType

INPUT / OUTPUT FILES
--------------------

- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B01.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B01T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
```

[TOC](#table-of-contents)
---

# calc_w
- number of invocations: 1
- max duration: 0.03 s
- avg duration: 0.03 s
- min duration: 0.03 s
- total duration: 0.03 s

### Input
- **t** `['float64']`: *13.699999999999999*
- **RH** `['int64']`: *93*


### Output
- `['float64']`: 0.0091380190832960652

### Docstring template

```
PARAMETERS
----------

:param t:
:type t: float64

:param RH:
:type RH: int64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# calc_w3_cooling_case
- number of invocations: 1
- max duration: 0.029 s
- avg duration: 0.029 s
- min duration: 0.029 s
- total duration: 0.029 s

### Input
- **t5** `['int32']`: *24*
- **w2** `['float64']`: *0.011593980099780365*
- **t3** `['float64']`: *16.0*
- **w5** `['float64']`: *0.011723331676612525*


### Output
- `['float64']`: 0.011431278978344625

### Docstring template

```
PARAMETERS
----------

:param t5:
:type t5: int32

:param w2:
:type w2: float64

:param t3:
:type t3: float64

:param w5:
:type w5: float64

RETURNS
-------

:returns:
:rtype: float64

```

[TOC](#table-of-contents)
---

# demand_calculation
- number of invocations: 1
- max duration: 42.053 s
- avg duration: 42.053 s
- min duration: 42.053 s
- total duration: 42.053 s

### Input
- **locator** `['InputLocator']`: *<cea.inputlocator.InputLocator object at 0x141673F0>*
- **weather_path** `['str']`: *'C:\\Users\\darthoma\\Documents\\GitHub\\CEAforArcGIS\\cea\\databases\\CH\\Weather\\Zug-2010.epw'*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x141673F0>*


### Output
- `['DataFrame']`: (9, 61)

### Docstring template

```
PARAMETERS
----------

:param locator:
:type locator: InputLocator

:param weather_path:
:type weather_path: str

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: DataFrame

INPUT / OUTPUT FILES
--------------------

- get_surface_properties: c:\reference-case-open\baseline\outputs\data\solar-radiation\properties_surfaces.csv
- get_building_geometry: c:\reference-case-open\baseline\inputs\building-geometry\zone.shp
- get_building_hvac: c:\reference-case-open\baseline\inputs\building-properties\technical_systems.shp
- get_building_thermal: c:\reference-case-open\baseline\inputs\building-properties\thermal_properties.shp
- get_building_occupancy: c:\reference-case-open\baseline\inputs\building-properties\occupancy.shp
- get_building_architecture: c:\reference-case-open\baseline\inputs\building-properties\architecture.shp
- get_building_age: c:\reference-case-open\baseline\inputs\building-properties\age.shp
- get_building_comfort: c:\reference-case-open\baseline\inputs\building-properties\indoor_comfort.shp
- get_building_internal: c:\reference-case-open\baseline\inputs\building-properties\internal_loads.shp
```

[TOC](#table-of-contents)
---

# get_building_geometry_ventilation
- number of invocations: 1
- max duration: 0.033 s
- avg duration: 0.033 s
- min duration: 0.033 s
- total duration: 0.033 s

### Input
- **gdf_building_geometry** `['dict']`: *{'perimeter': 100.0, u'Blength': 25.0, u'height_bg': 3.5714285714299998, u'floors_bg': 1.0, u'height_ag': 25.0, u'floors_ag': 7.0, u'Bwidth': 25.0, 'footprint': 625.0}*


### Output
- `['tuple']`: (2500.0, 625.0, 25.0, 0)

### Docstring template

```
PARAMETERS
----------

:param gdf_building_geometry:
:type gdf_building_geometry: dict

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# get_envelope_properties
- number of invocations: 1
- max duration: 0.197 s
- avg duration: 0.197 s
- min duration: 0.197 s
- total duration: 0.197 s

### Input
- **locator** `['LocatorDecorator']`: *???*
- **prop** `['GeoDataFrame']`: *(9, 10)*

#### prop:
```
         Occ_m2p  f_cros  n50  win_op  win_wall
count   9.000000       9    9     9.0  9.000000
mean   12.444444       0    2     0.5  0.366667
std     4.666667       0    0     0.0  0.100000
min     0.000000       0    2     0.5  0.100000
25%    14.000000       0    2     0.5  0.400000
50%    14.000000       0    2     0.5  0.400000
75%    14.000000       0    2     0.5  0.400000
max    14.000000       0    2     0.5  0.400000
```

### Output
- `['DataFrame']`: (9, 14)

### Docstring template

```
PARAMETERS
----------

:param locator:
:type locator: LocatorDecorator

:param prop:
:type prop: GeoDataFrame

RETURNS
-------

:returns:
:rtype: DataFrame

INPUT / OUTPUT FILES
--------------------

- get_envelope_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\envelope_systems.xls
- get_envelope_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\envelope_systems.xls
- get_envelope_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\envelope_systems.xls
- get_envelope_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\envelope_systems.xls
```

[TOC](#table-of-contents)
---

# get_prop_solar
- number of invocations: 1
- max duration: 0.297 s
- avg duration: 0.297 s
- min duration: 0.297 s
- total duration: 0.297 s

### Input
- **locator** `['LocatorDecorator']`: *???*


### Output
- `['DataFrame']`: (9, 4)

### Docstring template

```
PARAMETERS
----------

:param locator:
:type locator: LocatorDecorator

RETURNS
-------

:returns:
:rtype: DataFrame

INPUT / OUTPUT FILES
--------------------

- get_radiation: c:\reference-case-open\baseline\outputs\data\solar-radiation\radiation.csv
- get_surface_properties: c:\reference-case-open\baseline\outputs\data\solar-radiation\properties_surfaces.csv
```

[TOC](#table-of-contents)
---

# get_properties_natural_ventilation
- number of invocations: 1
- max duration: 0.413 s
- avg duration: 0.413 s
- min duration: 0.413 s
- total duration: 0.413 s

### Input
- **gdf_geometry_building** `['dict']`: *{'perimeter': 100.0, u'Blength': 25.0, u'height_bg': 3.5714285714299998, u'floors_bg': 1.0, u'height_ag': 25.0, u'floors_ag': 7.0, u'Bwidth': 25.0, 'footprint': 625.0}*
- **gdf_architecture_building** `['dict']`: *{u'Occ_m2p': 14.0, u'a_roof': 0.5, u'f_cros': 0.0, u'n50': 2.0, u'win_op': 0.5, u'win_wall': 0.40000000000000002, u'a_wall': 0.84999999999999998, u'rf_sh': 0.080000000000000002, u'e_wall': 0.93999999999999995, u'e_roof': 0.94999999999999996, u'G_win': 0.75, u'e_win': 0.89000000000000001}*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x144FAFB0>*


### Output
- `['dict']`: {'coeff_wind_pressure_path_vent': array([ 0.05, -0.05,  0.05, -0.05]), 'coeff_vent_path': array([ 0.,  0.,  0.,  0.]), 'height_vent_path': array([  6.25,   6.25,  18.75,  18.75]), 'coeff_lea_path': array([ 459.90382802,  459.90382802,  459.90382802,  459.90382802,
        459.90382802]), 'factor_cros': 0.0, 'height_lea_path': array([  6.25,   6.25,  18.75,  18.75,  25.  ]), 'coeff_wind_pressure_path_lea': array([ 0.05, -0.05,  0.05, -0.05,  0.  ])}

### Docstring template

```
PARAMETERS
----------

:param gdf_geometry_building:
:type gdf_geometry_building: dict

:param gdf_architecture_building:
:type gdf_architecture_building: dict

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: dict

```

[TOC](#table-of-contents)
---

# get_temperatures
- number of invocations: 1
- max duration: 0.147 s
- avg duration: 0.147 s
- min duration: 0.147 s
- total duration: 0.147 s

### Input
- **locator** `['LocatorDecorator']`: *???*
- **prop_HVAC** `['GeoDataFrame']`: *(9, 5)*

#### prop_HVAC:
```
       Name type_cs type_ctrl type_dhw type_hs
count     9       9         9        9       9
unique    9       2         2        2       2
top     B08      T3        T2       T1      T2
freq      1       8         8        8       8
```

### Output
- `['DataFrame']`: (9, 14)

### Docstring template

```
PARAMETERS
----------

:param locator:
:type locator: LocatorDecorator

:param prop_HVAC:
:type prop_HVAC: GeoDataFrame

RETURNS
-------

:returns:
:rtype: DataFrame

INPUT / OUTPUT FILES
--------------------

- get_technical_emission_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\emission_systems.xls
- get_technical_emission_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\emission_systems.xls
- get_technical_emission_systems: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Systems\emission_systems.xls
```

[TOC](#table-of-contents)
---

# initialize_timestep_data
- number of invocations: 1
- max duration: 0.041 s
- avg duration: 0.041 s
- min duration: 0.041 s
- total duration: 0.041 s

### Input
- **bpr** `['BuildingPropertiesRow']`: *<cea.demand.thermal_loads.BuildingPropertiesRow object at 0x14167090>*
- **weather_data** `['DataFrame']`: *(8760, 4)*

#### weather_data:
```
         drybulb_C  relhum_percent   windspd_ms    skytemp_C
count  8760.000000     8760.000000  8760.000000  8760.000000
mean     10.150000       73.861644     1.838094    44.884267
std       8.022269       15.889964     1.847214     9.589083
min     -10.300000       28.000000     0.000000    20.330004
25%       3.700000       62.000000     0.500000    36.956793
50%      10.400000       77.000000     1.300000    45.147171
75%      16.100000       86.000000     2.500000    52.211059
max      32.300000      100.000000    15.300000    70.460600
```

### Output
- `['dict']`: {'Im_tot': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'qm_ve_mech': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Top': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ts': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'T_sky': array([ 34.64474108,  34.64474108,  34.46468985, ...,  34.20457916,
        34.24561453,  34.21825944]), 'Twwf_sup': 60, 'Qcs_sen_incl_em_ls': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]), 'Ta': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]), 'Ta_re_cs': array([ 0.,  0.,

### Docstring template

```
PARAMETERS
----------

:param bpr:
:type bpr: BuildingPropertiesRow

:param weather_data:
:type weather_data: DataFrame

RETURNS
-------

:returns:
:rtype: dict

```

[TOC](#table-of-contents)
---

# lookup_coeff_wind_pressure
- number of invocations: 1
- max duration: 0.027 s
- avg duration: 0.027 s
- min duration: 0.027 s
- total duration: 0.027 s

### Input
- **height_path** `['ndarray']`: *array([  6.25,   6.25,  18.75,  18.75,  25.  ])*
- **class_shielding** `['int']`: *2*
- **orientation_path** `['list']`: *[0, 1, 0, 1, 2]*
- **slope_roof** `['int']`: *0*
- **factor_cros** `['float64']`: *0.0*


### Output
- `['ndarray']`: array([ 0.05, -0.05,  0.05, -0.05,  0.  ])

### Docstring template

```
PARAMETERS
----------

:param height_path:
:type height_path: ndarray

:param class_shielding:
:type class_shielding: int

:param orientation_path:
:type orientation_path: list

:param slope_roof:
:type slope_roof: int

:param factor_cros:
:type factor_cros: float64

RETURNS
-------

:returns:
:rtype: ndarray

```

[TOC](#table-of-contents)
---

# newton
- number of invocations: 1
- max duration: 0.03 s
- avg duration: 0.03 s
- min duration: 0.03 s
- total duration: 0.03 s

### Input
- **func** `['builtin_function_or_method']`: *???*
- **x0** `['float']`: *328.0*
- **args** `['tuple']`: *(18718.7156157702, 6.186839050924459, 280780.734236553, 295.0, 40.03272547828592, 0.3)*
- **tol** `['float']`: *0.01*
- **maxiter** `['int']`: *100*


### Output
- `['float']`: 312.3197184209625

### Docstring template

```
PARAMETERS
----------

:param func:
:type func: builtin_function_or_method

:param x0:
:type x0: float

:param args:
:type args: tuple

:param tol:
:type tol: float

:param maxiter:
:type maxiter: int

RETURNS
-------

:returns:
:rtype: float

```

[TOC](#table-of-contents)
---

# read_schedules
- number of invocations: 1
- max duration: 0.034 s
- avg duration: 0.034 s
- min duration: 0.034 s
- total duration: 0.034 s

### Input
- **use** `['unicode']`: *u'OFFICE'*
- **x** `['DataFrame']`: *(24, 40)*

#### x:
```
        NaN  Weekday_1  Saturday_1  Sunday_1  NaN  \
count    24         24          24        24    0   
unique   24          5           1         1    0   
top      24          0           0         0  NaN   
freq      1         13          24        24  NaN   

                                                      NaN  NaN  Weekday_2  \
count                                                   1   24       24.0   
unique                                                  1   24        4.0   
top     Probability of use of lighting and appliances ...   24        0.1   
freq                                                    1    1       14.0   

        Saturday_2  Sunday_2  ...   NaN  NaN  NaN    NaN  NaN  NaN   NaN  NaN  \
count         24.0      24.0  ...     0    0    0      1    0    0     1    0   
unique         1.0       1.0  ...     0    0    0      1    0    0     1    0   
top            0.1       0.1  ...   NaN  NaN  NaN  month  NaN  NaN  data  NaN   
freq          24.0      24.0  ...   NaN  NaN  NaN      1  NaN  NaN     1  NaN   

        NaN   NaN  
count     0     1  
unique    0     1  
top     NaN  data  
freq    NaN     1  

[4 rows x 40 columns]
```

### Output
- `['tuple']`: ([array([0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.4, 0.6,
       0.8, 0.8, 0.4, 0.2, 0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=object), array([0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=object), array([0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=object)], [array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.4, 0.8, 0

### Docstring template

```
PARAMETERS
----------

:param use:
:type use: unicode

:param x:
:type x: DataFrame

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# run_as_script
- number of invocations: 1
- max duration: 42.165 s
- avg duration: 42.165 s
- min duration: 42.165 s
- total duration: 42.165 s

### Input


### Output
- `['NoneType']`: None

### Docstring template

```
PARAMETERS
----------

RETURNS
-------

:returns:
:rtype: NoneType

```

[TOC](#table-of-contents)
---

# schedule_maker
- number of invocations: 1
- max duration: 0.367 s
- avg duration: 0.367 s
- min duration: 0.367 s
- total duration: 0.367 s

### Input
- **dates** `['DatetimeIndex']`: *DatetimeIndex(['2016-01-01 00:00:00', '2016-01-01 01:00:00',
               '2016-01-01 02:00:00', '2016-01-01 03:00:00',
               '2016-01-01 04:00:00', '2016-01-01 05:00:00',
               '2016-01-01 06:00:00', '2016-01-01 07:00:00',
               '2016-01-01 08:00:00', '2016-01-01 09:00:00',
               ...
               '2016-12-30 14:00:00', '2016-12-30 15:00:00',
               '2016-12-30 16:00:00', '2016-12-30 17:00:00',
               '2016-12-30 18:00:00', '2016-12-30 19:0*
- **locator** `['LocatorDecorator']`: *???*
- **list_uses** `['list']`: *[u'OFFICE', u'PARKING']*


### Output
- `['list']`: [([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 

### Docstring template

```
PARAMETERS
----------

:param dates:
:type dates: DatetimeIndex

:param locator:
:type locator: LocatorDecorator

:param list_uses:
:type list_uses: list

RETURNS
-------

:returns:
:rtype: list

INPUT / OUTPUT FILES
--------------------

- get_archetypes_schedules: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Archetypes\Archetypes_schedules.xlsx
- get_archetypes_schedules: C:\Users\darthoma\Documents\GitHub\CEAforArcGIS\cea\databases\CH\Archetypes\Archetypes_schedules.xlsx
```

[TOC](#table-of-contents)
---

# setpoint_correction_for_space_emission_systems
- number of invocations: 1
- max duration: 0.027 s
- avg duration: 0.027 s
- min duration: 0.027 s
- total duration: 0.027 s

### Input
- **heating_system** `['unicode']`: *u'T2'*
- **cooling_system** `['unicode']`: *u'T3'*
- **control_system** `['unicode']`: *u'T2'*


### Output
- `['tuple']`: (1.0999999999999999, -0.7)

### Docstring template

```
PARAMETERS
----------

:param heating_system:
:type heating_system: unicode

:param cooling_system:
:type cooling_system: unicode

:param control_system:
:type control_system: unicode

RETURNS
-------

:returns:
:rtype: tuple

```

[TOC](#table-of-contents)
---

# thermal_loads_all_buildings
- number of invocations: 1
- max duration: 39.361 s
- avg duration: 39.361 s
- min duration: 39.361 s
- total duration: 39.361 s

### Input
- **building_properties** `['BuildingProperties']`: *<cea.demand.thermal_loads.BuildingProperties object at 0x14607BF0>*
- **date** `['DatetimeIndex']`: *DatetimeIndex(['2016-01-01 00:00:00', '2016-01-01 01:00:00',
               '2016-01-01 02:00:00', '2016-01-01 03:00:00',
               '2016-01-01 04:00:00', '2016-01-01 05:00:00',
               '2016-01-01 06:00:00', '2016-01-01 07:00:00',
               '2016-01-01 08:00:00', '2016-01-01 09:00:00',
               ...
               '2016-12-30 14:00:00', '2016-12-30 15:00:00',
               '2016-12-30 16:00:00', '2016-12-30 17:00:00',
               '2016-12-30 18:00:00', '2016-12-30 19:0*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x141B7AD0>*
- **locator** `['LocatorDecorator']`: *???*
- **num_buildings** `['int']`: *9*
- **usage_schedules** `['dict']`: *{'list_uses': [u'OFFICE', u'PARKING'], 'schedules': [([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16000000000000003, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.48, 0.6400000000000001, 0.6400000000000001, 0.32000000000000006, 0.16000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0*
- **weather_data** `['DataFrame']`: *(8760, 4)*

#### weather_data:
```
         drybulb_C  relhum_percent   windspd_ms    skytemp_C
count  8760.000000     8760.000000  8760.000000  8760.000000
mean     10.150000       73.861644     1.838094    44.884267
std       8.022269       15.889964     1.847214     9.589083
min     -10.300000       28.000000     0.000000    20.330004
25%       3.700000       62.000000     0.500000    36.956793
50%      10.400000       77.000000     1.300000    45.147171
75%      16.100000       86.000000     2.500000    52.211059
max      32.300000      100.000000    15.300000    70.460600
```

### Output
- `['NoneType']`: None

### Docstring template

```
PARAMETERS
----------

:param building_properties:
:type building_properties: BuildingProperties

:param date:
:type date: DatetimeIndex

:param gv:
:type gv: GlobalVariables

:param locator:
:type locator: LocatorDecorator

:param num_buildings:
:type num_buildings: int

:param usage_schedules:
:type usage_schedules: dict

:param weather_data:
:type weather_data: DataFrame

RETURNS
-------

:returns:
:rtype: NoneType

INPUT / OUTPUT FILES
--------------------

- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B02.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B02T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B03.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B03T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B04.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B04T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B05.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B05T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B07.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B07T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B08.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B08T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B09.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B09T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
- get_demand_results_file: c:\reference-case-open\baseline\outputs\data\demand\B06.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B06T.csv
- get_demand_results_folder: c:\reference-case-open\baseline\outputs\data\demand
```

[TOC](#table-of-contents)
---

# write_totals_csv
- number of invocations: 1
- max duration: 0.652 s
- avg duration: 0.652 s
- min duration: 0.652 s
- total duration: 0.652 s

### Input
- **building_properties** `['BuildingProperties']`: *<cea.demand.thermal_loads.BuildingProperties object at 0x1401FEB0>*
- **locator** `['LocatorDecorator']`: *???*
- **gv** `['GlobalVariables']`: *<cea.globalvar.GlobalVariables object at 0x142C5590>*


### Output
- `['DataFrame']`: (9, 61)

### Docstring template

```
PARAMETERS
----------

:param building_properties:
:type building_properties: BuildingProperties

:param locator:
:type locator: LocatorDecorator

:param gv:
:type gv: GlobalVariables

RETURNS
-------

:returns:
:rtype: DataFrame

INPUT / OUTPUT FILES
--------------------

- get_temporary_file: c:\users\darthoma\appdata\local\temp\B01T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B02T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B03T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B04T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B05T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B07T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B08T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B09T.csv
- get_temporary_file: c:\users\darthoma\appdata\local\temp\B06T.csv
- get_total_demand: c:\reference-case-open\baseline\outputs\data\demand\Total_demand.csv
```

[TOC](#table-of-contents)
---

