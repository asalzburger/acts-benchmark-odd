echo "Setting up local environment variables, mimicking github runner system ..."

export GITHUB_WORKSPACE=${1}
export RUN_DIR=${GITHUB_WORKSPACE}/run
mkdir -p $RUN_DIR