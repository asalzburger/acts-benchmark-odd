#!/bin/bash

echo "Setting up the environment variables ..."

export PDG_PARTICLE=${1}
export N_PARTICLES=${2}
export N_EVENTS=${3}
export PT_VALS=${4} 

export ODD_DIR=${GITHUB_WORKSPACE}/acts/thirdparty/OpenDataDetector

export MATERIAL_CONFIG="--mat-input-type=file --mat-input-file=${GITHUB_WORKSPACE}/data/odd-material-map.root"
export BFIELD_CONFIG="--bf-constant-tesla=0.:0.:2."
export DIGI_CONFIG="--digi-config-file=${ODD_DIR}/config/odd-digi-smearing-config.json"
export FATRAS_CONFIG=""
export TRUTH_FITTING_CONFIG="--fit-initial-variance-inflation=100.:100.:100.:100.:100.:100."
export CKF_CONFIG="--ckf-selection-chi2max=10 --ckf-initial-variance-inflation=100.:100.:100.:100.:100.:100."
export SEEDING_CONFIG="--geo-selection-config-file=${ODD_DIR}/config/odd-seeding-config.json"

source ${GITHUB_WORKSPACE}/scripts/fatras_reco_chain.sh

#pt_vals= (1 5 100)

echo "Running ACTS fast simulation chain test ..."
echo "- Processing ${N_EVENTS} events with ${N_PARTICLES} particles (PDG: ${PDG_PARTICLE}) each"
for pt in ${PT_VALS}; do
   echo "-- Running chain for pT ${pt}"
   # Runnig Generation
   echo "-- Generation ..." 
   export OUT_DIR=${RUN_DIR}/pdg${PDG_PARTICLE}-n${N_EVENTS}-mp${N_PARTICLES}-pT${pt}
   mkdir ${OUT_DIR}
   echo "--events=${N_EVENTS} --gen-mom-gev ${pt}:${pt} --gen-randomize-charge --gen-mom-transverse --gen-nparticles=${N_PARTICLES}" > ${OUT_DIR}/evgen.response
   echo "--output-dir=${OUT_DIR} --output-csv" >> ${OUT_DIR}/evgen.response   
   ${INSTALL_DIR}/bin/ActsExampleParticleGun --response-file=${OUT_DIR}/evgen.response > ${OUT_DIR}/evgen.log
   # Running Fatras-Reco chain 
   fatras_reco_chain
done


echo "... done."