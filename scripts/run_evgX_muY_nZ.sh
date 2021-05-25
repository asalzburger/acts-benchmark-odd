#!/bin/bash

echo "Setting up the environment variables ..."

export EVG=${1}
export MU=${2}
export N_EVENTS=${3}
export EVG_NAME=`echo ${EVG} | tr := _`

export ODD_DIR=${GITHUB_WORKSPACE}/acts/thirdparty/OpenDataDetector

export EVGEN_CONFIG="--gen-npileup ${MU} --gen-hard-process=${EVG}"
export MATERIAL_CONFIG="--mat-input-type=file --mat-input-file=${GITHUB_WORKSPACE}/data/odd-material-map.root"
export BFIELD_CONFIG="--bf-constant-tesla=0.:0.:2."
export DIGI_CONFIG="--digi-config-file=${ODD_DIR}/config/odd-digi-smearing-config.json"
export FATRAS_CONFIG=""
export TRUTH_FITTING_CONFIG="--fit-initial-variance-inflation=100"
export CKF_CONFIG="--ckf-selection-chi2max=10 --ckf-initial-variance-inflation=100"
export SEEDING_CONFIG="--geo-selection-config-file=${ODD_DIR}/config/odd-seeding-config.json"

source ${GITHUB_WORKSPACE}/scripts/fatras_reco_chain.sh

echo "Running ACTS fast simulation chain test ..."
echo "- Processing ${N_EVENTS} event of generated process ${EVG} at <mu> = ${MU}"

export OUT_DIR=${RUN_DIR}/${EVG_NAME}-n${N_EVENTS}-mu${MU}
mkdir ${OUT_DIR} 
echo "--events=${N_EVENTS} ${EVGEN_CONFIG}" > ${OUT_DIR}/evgen.response
echo "--output-dir=${OUT_DIR} --output-csv" >> ${OUT_DIR}/evgen.response   
${INSTALL_DIR}/bin/ActsExamplePythia8 --response-file=${OUT_DIR}/evgen.response > ${OUT_DIR}/evgen.log

# Running Fatras-Reco chain 
fatras_reco_chain
