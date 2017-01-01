#!/bin/sh


PYTHONPATH=../ coverage run -m doctest tests.doctest
coverage html
