#!/bin/sh

export PYTHONPATH=../
python -m doctest ./tests.doctest
python -m doctest ../Readme.md

