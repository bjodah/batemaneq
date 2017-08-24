#!/bin/bash -xeu
PKG_NAME=${1:-${CI_REPO##*/}}
if [[ "$CI_BRANCH" =~ ^v[0-9]+.[0-9]?* ]]; then
    eval export ${PKG_NAME^^}_RELEASE_VERSION=\$CI_BRANCH
    echo ${CI_BRANCH} | tail -c +2 > __conda_version__.txt
fi
python2.7 setup.py sdist
(cd ./dist/; python2.7 -m pip install *.tar.gz)
(cd /; python2.7 -m pytest --pyargs $PKG_NAME)
(cd ./dist/; python3 -m pip install *.tar.gz)
(cd /; python3 -m pytest --pyargs $PKG_NAME)
python2.7 setup.py build_ext -i
python3 setup.py build_ext -i
PYTHONPATH=$(pwd) ./scripts/run_tests.sh --cov $PKG_NAME --cov-report html
./scripts/coverage_badge.py htmlcov/ htmlcov/coverage.svg
! grep "DO-NOT-MERGE!" -R . --exclude ci.sh
