#!/bin/bash

TARBALL=${1}
TMPDIR=${2:-/tmp/__octave}
CATEGORIES='main extra language'

CURRENTDIR=$(pwd)
RELEASE=$(sed -e 's/^.*\([0-9]\{8\}\).*$/\1/' <<< ${TARBALL})

mkdir -p ${TMPDIR}
tar -xvzf ${TARBALL} -C ${TMPDIR}

cd ${TMPDIR}/octave-forge*

for cat in ${CATEGORIES}; do
    mkdir -p ${TMPDIR}/{src,db}/${cat}
    for pkg in $(ls ${cat}); do
        mypkg=${pkg%.tar.gz}
        tar -xvzf ${cat}/${pkg} -C ${TMPDIR}/src/${cat}
        mkdir ${TMPDIR}/db/${cat}/${mypkg}
        cp ${TMPDIR}/{src,db}/${cat}/${mypkg}/DESCRIPTION
    done
done

mkdir ${TMPDIR}/octave-forge-${RELEASE}
cp -r ${TMPDIR}/db/* ${TMPDIR}/octave-forge-${RELEASE}/

cd ${TMPDIR} && tar -cvzf "${CURRENTDIR}/octave-forge-${RELEASE}.db.tar.gz" \
    octave-forge-${RELEASE}

rm -rf ${TMPDIR}
