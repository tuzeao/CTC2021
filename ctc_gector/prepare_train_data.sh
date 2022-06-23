#!/bin/bash

INPUT=inputs/questions.xlsx
SOURCE=inputs/source
TARGET=inputs/target
OUTPUT=inputs/train_data

# Dev
#INPUT=inputs/questions_dev.xlsx
#SOURCE=inputs/dev_source
#TARGET=inputs/dev_target
#OUTPUT=inputs/dev_data

python my_read_data.py -i $INPUT -s $SOURCE -t $TARGET
python token_data.py -s $SOURCE -t $TARGET -so $SOURCE.tok -to $TARGET.tok
python utils/preprocess_data.py -s $SOURCE.tok -t $TARGET.tok -o $OUTPUT

