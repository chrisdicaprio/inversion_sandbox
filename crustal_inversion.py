from pathlib import Path
from enum import Enum
from py4j.java_gateway import JavaGateway, GatewayParameters

OPENSHA_VERSION = 'new'

############################
# JAVA SETUP
############################
jre_path = "/usr/bin/java"
app_jar_path_old = "/home/chrisdc/NSHM/DEV/CALCULATION/opensha-modular/nzshm-opensha/build/libs/nzshm-opensha-all-2024-03-01.jar"
app_jar_path_new = "/home/chrisdc/NSHM/DEV/CALCULATION/opensha-modular/nzshm-opensha/build/libs/nzshm-opensha-all-289-min-bin-one-off.jar"
if OPENSHA_VERSION == 'new':
    app_jar_path = app_jar_path_new
elif 'old' in OPENSHA_VERSION:
    app_jar_path = app_jar_path_old
# /home/chrisdc/Downloads/nzshm-opensha-all-277-polygonizer.jar
jvm_heap_start=3
jvm_heap_max=10
jvm_heap_start_gb = str(jvm_heap_start)
jvm_heap_max_gb = str(jvm_heap_max)

JAVA_CLASSPATH=app_jar_path
CLASSNAME="nz.cri.gns.NZSHM22.opensha.util.NZSHM22_PythonGateway"

initial_gateway_port=25333
java_cmd = f"NZSHM22_APP_PORT={initial_gateway_port} java -Xms{jvm_heap_start_gb}G -Xmx{jvm_heap_max_gb}G -classpath {JAVA_CLASSPATH} {CLASSNAME}"
go = input(f"Start java by runining the following command in a different terminal. Hit enter when ready.\n{java_cmd}\n")


############################
# RUN JAVA WITH PYTHON
############################
initial_gateway_port=25333
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=initial_gateway_port))

ruptureset_filepath = Path("/home/chrisdc/Downloads/NZSHM22_RuptureSet-UnVwdHVyZUdlbmVyYXRpb25UYXNrOjEwMDAzOA==.zip")
solution_filepath = Path('/home/chrisdc/NSHM/DEV/inversion_sandbox/') / f'inversion_solution_{OPENSHA_VERSION}.zip'
print(solution_filepath)



############################
# SOME USEFUL THINGS
############################
class CoolingSchedule(Enum):
    CLASSICAL_SA = "CLASSICAL_SA"
    FAST_SA = "FAST_SA"
    VERYFAST_SA = "VERYFAST_SA"
    LINEAR = "LINEAR"

class NonnegativityConstraint(Enum):
    TRY_ZERO_RATES_OFTEN = "TRY_ZERO_RATES_OFTEN" # sets rate to zero if they are perturbed to negative values (anneals much faster!)
    LIMIT_ZERO_RATES = "LIMIT_ZERO_RATES" # re-perturb rates if they are perturbed to negative values (still might not be accepted)
    PREVENT_ZERO_RATES = "PREVENT_ZERO_RATES" # Any perturbed zero rate MUST accept new value.  100% of rates will be nonnegative if numIterations >> number of Rates.  

class MaxMagType(Enum):
    NONE = "NONE"
    MANIPULATE_MFD = "MANIPULATE_MFD"

class MFDWeightType(Enum):
    EQ_INEQ = "equality inequality"
    UNC = "uncertainty"
    DYN = "dynamic reweighting"

class SlipWeightType(Enum):
    UNC = "uncertainty"
    DYN = "dynamic reweighting"
    ADJ = "uncertainty adjusted"
    RATE = "rate normalized/unnormalized"

class SlipRateWeightWeightingType(Enum):
    NORM = "NORMALIZED"
    UNNORM = "UNNORMALIZED"
    BOTH = "BOTH"
    UNC = "NORMALIZED_BY_UNCERTAINTY"

class PaleoProbabilityModel(Enum):
    NZSHM22_C_41 = "NZSHM22_C_41" 
    NZSHM22_C_42 = "NZSHM22_C_42"
    NZSHM22_C_43 = "NZSHM22_C_43"
    UCERF3 = "UCERF3"
    UCERF3_PLUS_PT25 = "UCERF3_PLUS_PT25"
    UCERF3_PLUS_PT5 = "UCERF3_PLUS_PT5"

class PaleoConstraint(Enum):
    GEODETIC_SLIP_PRIOR_NO_TVZ = "GEODETIC_SLIP_PRIOR_NO_TVZ"
    GEODETIC_SLIP_NO_TVZ = "GEODETIC_SLIP_NO_TVZ"
    GEOLOGIC_SLIP_NO_TVZ = "GEOLOGIC_SLIP_NO_TVZ"
    GEODETIC_SLIP_PRIOR_22FEB = "GEODETIC_SLIP_PRIOR_22FEB"
    GEODETIC_SLIP_22FEB = "GEODETIC_SLIP_22FEB"
    GEOLOGIC_SLIP_22FEB = "GEOLOGIC_SLIP_22FEB"
    GEODETIC_SLIP_PRIOR_4FEB = "GEODETIC_SLIP_PRIOR_4FEB"
    GEODETIC_SLIP_4FEB = "GEODETIC_SLIP_4FEB"
    GEOLOGIC_SLIP_4FEB = "GEOLOGIC_SLIP_4FEB"
    GEOLOGIC_SLIP_1_0 = "GEOLOGIC_SLIP_1_0"
    GEODETIC_SLIP_1_0 = "GEODETIC_SLIP_1_0"
    PALEO_RI_GEOLOGIC_MAY24 = "PALEO_RI_GEOLOGIC_MAY24"
    PALEO_RI_GEODETIC_MAY24 = "PALEO_RI_GEODETIC_MAY24"
    PALEO_RI_GEODETICGEOLOGICPRIOR_MAY24 = "PALEO_RI_GEODETICGEOLOGICPRIOR_MAY24"
    
class SpatialSeisPDF(Enum):
    NZSHM22_1246 = "NZSHM22_1246"
    NZSHM22_1246R = "NZSHM22_1246R"
    NZSHM22_1456 = "NZSHM22_1456"
    NZSHM22_1456R = "NZSHM22_1456R"
    NZSHM22_1346 = "NZSHM22_1346"
    FLOOR_ADDOPTIEEPASCOMB_CRU = "FLOOR_ADDOPTIEEPASCOMB_CRU"

# there are many more, but I've put just a few useful ones in
class DeformationModel(Enum):
    SBD_0_1_PUY_30_0PT7 = "SBD_0_1_PUY_30_0PT7"
    GEOD_NO_PRIOR_2022_RmlsZToxMDAwODc_ = "GEOD_NO_PRIOR_2022_RmlsZToxMDAwODc_"
    FAULT_MODEL = "FAULT_MODEL"
    SBD_0_2A_HKR_MMIN7PT5_EXP_LTP1A = "SBD_0_2A_HKR_MMIN7PT5_EXP_LTP1A"

class PertubationFunction(Enum):
    EXPONENTIAL_SCALE = "EXPONENTIAL_SCALE"
    VARIABLE_EXPONENTIAL_SCALE = "VARIABLE_EXPONENTIAL_SCALE"

class PlotLevel(Enum):
    LIGHT = "LIGHT"
    DEFAULT = "DEFAULT"
    FULL = "FULL"
    REVIEW = "REVIEW"




############################
# INVERSION PARAMETERS
############################
# initial_solution_filepath = Path("/home/chrisdc/Downloads/NZSHM22_InversionSolution-QXV0b21hdGlvblRhc2s6MTA3MDA2.zip")
report_level = PlotLevel.DEFAULT
non_negativity_function = NonnegativityConstraint.TRY_ZERO_RATES_OFTEN
cooling_schedule = CoolingSchedule.FAST_SA
perturbation_function = PertubationFunction.EXPONENTIAL_SCALE
inversion_seconds = 5*60
selection_interval_secs = 1
threads_per_selector = 4
averaging_threads = 4
averaging_interval_secs = 30
completion_energy = 0.0

scaling_c_dip_slip = scaling_c_strike_slip = 4.2
scaling_recalc_mag = True
deformation_model = DeformationModel.FAULT_MODEL
spatial_seis_pdf = SpatialSeisPDF.FLOOR_ADDOPTIEEPASCOMB_CRU
enable_tvz = False

# ====== Constraint Values ======
# MFD
mfd = dict(
    N=3.4,
    b=0.959,
    transition_mag=7.85,
    min_mag=6.799,  # this is to get around the MFD binning bug
    max_mag=10.0,
)
if (OPENSHA_VERSION == 'new') or (OPENSHA_VERSION == 'old_6.8'):
    mfd['min_mag'] = 6.8
max_mag_type = MaxMagType.MANIPULATE_MFD

# Slip Rate
slip_rate_factor = dict(
    sans=0.9,
    tvz=0.7,
)

# Paleo
paleo_rate_constraint = PaleoConstraint.PALEO_RI_GEODETIC_MAY24
paleo_probability_model = PaleoProbabilityModel.NZSHM22_C_42


# ======== Weighting ======== 
reweighting = True

mfd_weight_type = MFDWeightType.UNC # only used if no re-weighting
# see the options below for other valid key:value pairs dependint on the MFD weighting type
mfd_weights = dict(
    uncertainty_power=0.001,
    uncertainty_scalar=0.1,
    uncertainty_weight=0, # used for some weight types (not re-weighting)
    mfd_equality_weight=0, # used for some weight types (not re-weighting)
    mfd_inequality_weight=0, # used for some weight types (not re-weighting)
)

# ======== Slip Weights ======== 
slip_weight_type = SlipWeightType.UNC # weight types are ignored if reweighting is True
# Dictates how slip rates are used to scale the slip misfits. Only used if slip_weight_type is UNC
slip_rate_weighting_type = SlipRateWeightWeightingType.BOTH  
slip_weights = dict(
    uncertainty_scaling_factor=0.0,
    uncertainty_weight=0,
    rate_weight=0,
    rate_normalized_weight=0,
    rate_unnormalized_weight=0,
)
unmodified_sliprate_std = True

# ======== Paleo Weights ======== 
use_paleo = True
paleo_weights = dict(
    smoothness=1.0e5,
    paleo_weight=1.0e2,  # only used if there is no re-weighting
)


############################
# RUN INVERSION
############################
inversion_runner = gateway.entry_point.getCrustalInversionRunner()

inversion_runner.setInversionAveraging(
                int(averaging_threads),
                int(averaging_interval_secs)
)
inversion_runner.setCoolingSchedule(cooling_schedule.value)

inversion_runner.setSpatialSeisPDF(spatial_seis_pdf.value)
inversion_runner.setDeformationModel(deformation_model.value)
inversion_runner.setSlipRateFactor(float(slip_rate_factor["sans"]), float(slip_rate_factor["tvz"]))
sr = gateway.jvm.nz.cri.gns.NZSHM22.opensha.calc.SimplifiedScalingRelationship()
sr.setupCrustal(
    float(scaling_c_dip_slip),
    float(scaling_c_strike_slip)
)
inversion_runner.setScalingRelationship(sr, bool(scaling_recalc_mag))
inversion_runner\
    .setInversionSeconds(int(inversion_seconds))\
    .setEnergyChangeCompletionCriteria(float(0), float(completion_energy), float(1))\
    .setSelectionInterval(int(selection_interval_secs))\
    .setNumThreadsPerSelector(int(threads_per_selector))\
    .setNonnegativityConstraintType(non_negativity_function.value)\
    .setPerturbationFunction(perturbation_function.value)
inversion_runner.setRuptureSetFile(str(ruptureset_filepath))
inversion_runner.setInversionAveraging(
                int(averaging_threads),
                int(averaging_interval_secs))

if enable_tvz:
    inversion_runner.setGutenbergRichterMFD(
            float(mfd["N_sans"]),
            float(mfd["N_tvz"]),
            float(mfd["b_sans"]),
            float(mfd["b_tvz"]),
            float(mfd["transition_mag"]),
    )
    inversion_runner.setEnableTvzMFDs(True)
    inversion_runner.setMinMags(max_mag_type.value, float(mfd["min_mag_sans"]), float(mfd["min_mag_tvz"]))
else:
    inversion_runner.setGutenbergRichterMFD(
            float(mfd["N"]),
            float(1.0), 
            float(mfd["b"]),
            float(1.0),
            float(mfd["transition_mag"]),
    )
    inversion_runner.setEnableTvzMFDs(False)
    inversion_runner.setMinMags(float(mfd["min_mag"]), float(mfd["min_mag"]))
    inversion_runner.setMaxMags(max_mag_type.value, float(mfd["max_mag"]), float(mfd["max_mag"]))

if reweighting:
    inversion_runner.setUncertaintyWeightedMFDWeights(
        float(1.0),
        float(mfd_weights["uncertainty_power"]),
        float(mfd_weights["uncertainty_scalar"]),
    )
    inversion_runner.setReweightTargetQuantity("MAD")
    
    inversion_runner.setSlipRateUncertaintyConstraint(
        1.0,
        float(slip_weights["uncertainty_scaling_factor"]),
    )
    inversion_runner.setUnmodifiedSlipRateStdvs(unmodified_sliprate_std)
    
    inversion_runner.setPaleoRateConstraints(
        1.0,
        float(paleo_weights["smoothness"]),
        paleo_rate_constraint.value,
        paleo_probability_model.value,
    )
else:
    if mfd_weight_type is MFDWeightType.UNC:
        inversion_runner.setUncertaintyWeightedMFDWeights(
            float(mfd_weights["uncertainty_weight"]),
            float(mfd_weights["uncertainty_power"]),
            float(mfd_weights["uncertainty_scalar"]),
        )
    elif mfd_weight_type is MFDWeightType.EQ_INEQ:
        inversion_runner.setUncertaintyWeightedMFDWeights(
            float(mfd_weights["mfd_equality_weight"]),
            float(mfd_weights["mfd_inequality_weight"]),
        )

    if slip_weight_type is SlipWeightType.UNC:
        inversion_runner.setSlipRateUncertaintyConstraint(
            float(slip_weights["uncertainty_weight"]),
            float(slip_weights["uncertainty_scaling_factor"]),
        )
        inversion_runner.setUnmodifiedSlipRateStdvs(unmodified_sliprate_std)
    elif slip_weight_type is SlipWeightType.ADJ:
        inversion_runner.setSlipRateUncertaintyConstraint(
            float(slip_weights["rate_weight"]),
            float(slip_weights["uncertainty_scaling_factor"]),
        )
    elif slip_weight_type is SlipWeightType.RATE:
        inversion_runner.setSlipRateConstraint(slip_rate_weighting_type,
            float(slip_weights["rate_normalized_weight"]),
            float(slip_weights["rate_unnormalized_weight"]),
        )
    
    inversion_runner.setPaleoRateConstraints(
        float(paleo_weights["weight"]), 
        float(paleo_weights["smoothness"]),
        paleo_rate_constraint.value,
        paleo_probability_model.value,
    )


# inversion_runner.setInitialSolution(str(initial_solution_filepath))
inversion_runner.runInversion()
inversion_runner.writeSolution(str(solution_filepath))

############################
# RUN INVERISION REPORT 
############################
report_folder = solution_filepath.parent / 'reports' / OPENSHA_VERSION

report_name = f"inversion diagnostics. OpenSHA {OPENSHA_VERSION}"
report_generator = gateway.entry_point.getReportPageGen()
report_generator\
            .setName(report_name)\
            .setSolution(str(solution_filepath))\
            .setOutputPath(str(report_folder))\
            .setPlotLevel(report_level.value)\
            .setFillSurfaces(True)\
            .generatePage()
