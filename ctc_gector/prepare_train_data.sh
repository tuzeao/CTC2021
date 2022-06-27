#!/bin/bash

# train
#INPUT=inputs/questions.xlsx
#SOURCE=inputs/source
#TARGET=inputs/target
#OUTPUT=inputs/train_data

# train 2
#INPUT=inputs/questions.xlsx
#SOURCE=inputs/source_v2
#TARGET=inputs/target_v2
#OUTPUT=inputs/train_data_v2

# train 3
INPUT=inputs/questions.xlsx
SOURCE=inputs/source_v3
TARGET=inputs/target_v3
OUTPUT=inputs/train_data_v3
# Dev
#INPUT=inputs/questions_dev.xlsx
#SOURCE=inputs/dev_source
#TARGET=inputs/dev_target
#OUTPUT=inputs/dev_data
rm -f $OUTPUT
python my_read_data.py -i $INPUT -s $SOURCE -t $TARGET
python token_data.py -s $SOURCE -t $TARGET -so $SOURCE.tok -to $TARGET.tok
python utils/preprocess_data.py -s $SOURCE.tok -t $TARGET.tok -o $OUTPUT

