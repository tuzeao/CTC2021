#!/bin/bash

set -e
set -v

BASE_DIR=.
TRAIN_PATH=inputs/train_data
VALID_PATH=inputs/dev_data
#BASE_MODEL=ctc2021_baseline
BASE_MODEL=bert_wwm
VOCAB_PATH=$BASE_DIR/data/output_vocabulary/
SAVE_MODEL=save_dir
NUM_EPOCH=10
UPDATE_PER_EPOCH=1000

CUDA_VISIBLE_DEVICES=1 python train.py \
	--train_set $TRAIN_PATH \
	--dev_set $VALID_PATH \
	--model_dir $SAVE_MODEL \
        --vocab_path $VOCAB_PATH \
	--n_epoch $NUM_EPOCH \
	--cold_steps_count 1 \
	--accumulation_size 2 \
	--updates_per_epoch $UPDATE_PER_EPOCH  \
	--tn_prob 0 \
	--tp_prob 1 \
	--transformer_model $BASE_MODEL \
	--special_tokens_fix 0 \
	--batch_size 64 \
	--pretrain_folder $BASE_MODEL \
	--patience 10 \
