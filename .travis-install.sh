#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    sudo brew update
    sudo brew install python2
    sudo brew install pyenv-virtualenv

    case "${TOXENV}" in
        py27)
            # Install some custom Python 2.7 requirements on OS X
            ;;
    esac
else
    # Install some custom requirements on Linux
fi

pip install virtualenv

pip install -U tox
pip install -U coveralls