#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    brew update
    brew install pyenv-virtualenv

    brew install memcached
    brew install libmemcached
    brew install redis

    brew tap homebrew/services
    brew services start memcached
    brew services start redis

    case "${TOXENV}" in
        py27)
            brew install python
            ;;
    esac
elif [[ $TRAVIS_OS_NAME == 'linux' ]]; then
    apt install libmemcached-dev
fi

pip install -U virtualenv
virtualenv vishnu
vishnu/bin/activate

pip install -U tox
pip install -U coveralls