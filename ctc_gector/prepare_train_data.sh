#!/bin/bash

INPUT=inputs/questions.xlsx
SOURCE=inputs/source
TARGET=inputs/target
OUTPUT=inputs/train_data

python my_read_data.py -i $INPUT -s $SOURCE -t $TARGET

python token_data.py -i $SOURCE -o $SOURCE.tok
python token_data.py -i $TARGET -o $TARGET.tok

python utils/preprocess_data.py -s $SOURCE.tok -t $TARGET.tok -o $OUTPUT

