#!/usr/bin/env bash

MINICONDA_INSTALLER_BASE_URL='http://repo.continuum.io/miniconda/'
INSTALLER=''

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    case "${TOXENV}" in
        py27)
            # Install some custom Python 2 requirements on OS X
            INSTALLER='Miniconda2-4.2.15-MacOSX-x86_64.sh'
            ;;

        *)
            # Install some custom Python 3 requirements on OS X
            INSTALLER='Miniconda3-4.2.12-MacOSX-x86_64.sh'
            ;;
    esac

elif [[ $TRAVIS_OS_NAME == 'linux' ]]; then

    case "${TOXENV}" in
        py27)
            # Install some custom Python 2 requirements on Linux 64
            INSTALLER='Miniconda2-4.2.12-Linux-x86_64.sh'
            ;;
        *)
            # Install some custom Python 3 requirements on Linux 64
            INSTALLER='Miniconda3-4.2.12-Linux-x86_64.sh'
            ;;
    esac

else
    echo "Unknown Travis OS name: ${TRAVIS_OS_NAME}"
fi

MINICONDA_INSTALLER_URL="${MINICONDA_INSTALLER_BASE_URL}${INSTALLER}"

echo $MINICONDA_INSTALLER_URL

travis_retry wget $MINICONDA_INSTALLER_URL
chmod +x miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH=/home/travis/miniconda/bin:$PATH
conda update --yes conda
python -V
pip -V
