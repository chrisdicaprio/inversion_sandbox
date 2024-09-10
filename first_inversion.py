from pathlib import Path

from py4j.java_gateway import JavaGateway, GatewayParameters



############################
# JAVA SETUP
############################
jre_path = "/usr/bin/java"
app_jar_path = "/home/chrisdc/NSHM/DEV/CALCULATION/opensha-modular/nzshm-opensha/build/libs/nzshm-opensha-all.jar"
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

ruptureset_filepath = Path("/home/chrisdc/Downloads/RupSet_Sub_FM(SBD_0_2_PUY_15)_mnSbS(2)_mnSSPP(2)_mxSSL(0.5)_ddAsRa(2.0,5.0,5)_ddMnFl(0.1)_ddPsCo(0.0)_ddSzCo(0.0)_thFc(0.0).zip")
solution_filepath = Path('/home/chrisdc/NSHM/DEV/inversion_sandbox/test.zip')
deformation_model = "SBD_0_1_PUY_30_0PT7"
inversion_seconds = 10
mfd_equality_weight = 1.0e4
slip_rate_weighting_type = "BOTH"
mfd_inequality_weight = 0.0
slip_rate_normalized_weight = 1.033
scaling_c_val = 4.0
scaling_recalc_mag = True
slip_rate_unnormalized_weight = 1.0e5
mfd_mag_gt_5 = 4.6
mfd_b_value = 0.902
mfd_transition_mag = 9.15
completion_energy = 0.0
selection_interval_secs = 1
threads_per_selector = 4
non_negativity_function = "TRY_ZERO_RATES_OFTEN"
perturbation_function = "EXPONENTIAL_SCALE"
averaging_threads = 4
averaging_interval_secs = 30
mfd_min_mag = 7.0

inversion_runner = gateway.entry_point.getSubductionInversionRunner()
sr = gateway.jvm.nz.cri.gns.NZSHM22.opensha.calc.SimplifiedScalingRelationship()
sr.setupSubduction(float(scaling_c_val))
inversion_runner.setScalingRelationship(sr, bool(scaling_recalc_mag))

inversion_runner.setGutenbergRichterMFDWeights(float(mfd_equality_weight), float(mfd_inequality_weight))
inversion_runner.setSlipRateConstraint(slip_rate_weighting_type, float(slip_rate_normalized_weight),float(slip_rate_unnormalized_weight))
inversion_runner.setGutenbergRichterMFD(
                    float(mfd_mag_gt_5),
                    float(mfd_b_value),
                    float(mfd_transition_mag),
                    float(mfd_min_mag),
)
inversion_runner.setDeformationModel(deformation_model)
inversion_runner\
    .setInversionSeconds(int(inversion_seconds))\
    .setEnergyChangeCompletionCriteria(float(0), float(completion_energy), float(1))\
    .setSelectionInterval(int(selection_interval_secs))\
    .setNumThreadsPerSelector(int(threads_per_selector))\
    .setNonnegativityConstraintType(non_negativity_function)\
    .setPerturbationFunction(perturbation_function)
inversion_runner.setRuptureSetFile(str(ruptureset_filepath))
inversion_runner.setInversionAveraging(
                int(averaging_threads),
                int(averaging_interval_secs))
inversion_runner.runInversion()
inversion_runner.writeSolution(str(solution_filepath))


############################
# RUN INVERISION REPORT 
############################
report_folder = solution_filepath.parent / 'reports'
report_name = "inversion diagnostics"
report_level = "FULL"
report_generator = gateway.entry_point.getReportPageGen()
report_generator\
            .setName(report_name)\
            .setSolution(str(solution_filepath))\
            .setOutputPath(str(report_folder))\
            .setPlotLevel(report_level)\
            .setFillSurfaces(True)\
            .generatePage()
