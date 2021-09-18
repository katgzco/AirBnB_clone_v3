#!/bin/bash

rm -r __pycache__

cd models
rm -r __pycache__

cd engine
rm -r __pycache__

cd ../../tests
rm -r __pycache__

cd test_models
rm -r __pycache__

cd test_engine
rm -r __pycache__



