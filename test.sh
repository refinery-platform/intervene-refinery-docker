#!/usr/bin/env bash
set -o errexit

# xtrace turned on only within the travis folds
start() { echo travis_fold':'start:$1; echo $1; set -v; }
end() { set +v; echo travis_fold':'end:$1; echo; echo; }
retry() {
    TRIES=1
    until curl --silent --fail http://localhost:$PORT/ > /tmp/response.txt; do
        echo "$TRIES: not up yet"
        if (( $TRIES > 10 )); then
            $OPT_SUDO docker logs $CONTAINER_NAME
            die "HTTP requests to app never succeeded"
        fi
        (( TRIES++ ))
        sleep 1
    done
    echo 'Container responded with:'
    head -n50 /tmp/response.txt
}
source shared.sh


start doctest
python -m doctest context/python/*.py -v
end doctest


start format
flake8 context || die "Run 'autopep8 --in-place -r context'"
end format


start isort
isort --recursive context --check-only || die "Run 'isort --recursive context'"
end isort


start docker_build
./docker_build.sh
end docker_build


start docker_run
./docker_run.sh
retry
echo "docker is responsive"
ACTUAL_TEXT=`curl http://localhost:8888/`
grep 'Intervene - an interactive Shiny app for UpSet plots' <(echo "$ACTUAL_TEXT") || die "No match: $ACTUAL_TEXT"

BASE='docker exec intervene-container cat /srv/shiny-server/sample-apps/intervene/data'
ACTUAL_COLUMNS=`$BASE/columns.txt`
diff context/fixtures/food/output-columns.txt <(echo "$ACTUAL_COLUMNS") || die "Unexpected columns; Actual: $ACTUAL_COLUMNS"
ACTUAL_MATRIX=`$BASE/ratio_matrix.txt`
diff context/fixtures/food/output-matrix.txt <(echo "$ACTUAL_MATRIX") || die "Unexpected matrix; Actual: $ACTUAL_MATRIX"

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
echo "container cleaned up"
end docker_run