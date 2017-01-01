#!/bin/sh


PYTHONPATH=../ coverage run -m doctest tests.doctest
coverage html
rm -rf ./.coverage
