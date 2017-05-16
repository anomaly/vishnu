#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    brew update
    brew install pyenv-virtualenv

    case "${TOXENV}" in
        py27)
            brew install python
            ;;
    esac
fi

pip install -U virtualenv
virtualenv vishnu
vishnu/bin/activate

pip install -U tox
pip install -U coveralls