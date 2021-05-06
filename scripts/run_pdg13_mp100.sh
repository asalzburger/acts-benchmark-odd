#!/bin/bash

echo "Setting up the environment variables ..."

export N_EVENTS=1000
export N_PARTICLES=100
export PDG_PARTICLE=13

export ODD_DIR=${GITHUB_WORKSPACE}/acts/thirdparty/OpenDataDetector

export MATERIAL_CONFIG="--mat-input-type=file --mat-input-file=${GITHUB_WORKSPACE}/data/odd-material-map.root"
export BFIELD_CONFIG="--bf-constant-tesla=0.:0.:2."
export DIGI_CONFIG="--digi-config-file=${ODD_DIR}/config/odd-digi-smearing-config.json"
export FATRAS_CONFIG=""
export FITTING_CONFIG=""

pt_vals=(1 5 100)

echo "Running ACTS fast simulation chain test ..."
echo "- Processing ${N_EVENTS} with ${N_PARTICLES} particles (PDG: ${PDG_PARTICLE}) each"
for pt in ${pt_vals}; do
   echo "-- Running chain for pT ${pt}"
   # Runnig Generation
   echo "-- Generation ..." 
   export OUT_DIR=${RUN_DIR}/pdg${PDG_PARTICLE}-n${N_EVENTS}-mp${N_PARTICLES}-pT${pt}
   mkdir ${OUT_DIR}
   echo "--events=${N_EVENTS} --gen-mom-gev ${pt}:${pt} --gen-randomize-charge --gen-mom-transverse --gen-nparticles=${N_PARTICLES}" > ${OUT_DIR}/evgen.response
   echo "--output-dir=${OUT_DIR} --output-csv" >> ${OUT_DIR}/evgen.response   
   ${INSTALL_DIR}/bin/ActsExampleParticleGun --response-file=${OUT_DIR}/evgen.response > ${OUT_DIR}/evgen.log
   # Runnig Fatras
   echo "-- Fatras ... " 
   echo "--events=${N_EVENTS} --dd4hep-input=${ODD_DIR}/xml/OpenDataDetector.xml" > ${OUT_DIR}/fatras.response
   echo "${FATRAS_CONFIG} ${BFIELD_CONFIG} ${MATERIAL_CONFIG}" >> ${OUT_DIR}/fatras.response
   echo "--input-dir=${OUT_DIR}   --output-dir=${OUT_DIR} --output-csv" >> ${OUT_DIR}/fatras.response
   ${INSTALL_DIR}/bin/ActsExampleFatrasDD4hep --response-file=${OUT_DIR}/fatras.response > ${OUT_DIR}/fatras.log
   # Runnint Truth Fitting
   echo "-- Truth Fitting with smeared digitization ... " 
   echo "--events=${N_EVENTS} --dd4hep-input=${ODD_DIR}/xml/OpenDataDetector.xml" > ${OUT_DIR}/fitting.response
   echo "${FITTING_CONFIG}  ${BFIELD_CONFIG} ${MATERIAL_CONFIG} ${DIGI_CONFIG}" >> ${OUT_DIR}/fitting.response
   echo "--input-dir=${OUT_DIR} --output-dir=${OUT_DIR}" >> ${OUT_DIR}/fitting.response
   ${INSTALL_DIR}/bin/ActsExampleTruthTracksDD4hep  --response-file=${OUT_DIR}/fitting.response > ${OUT_DIR}/fitting.log
done

echo "... done."