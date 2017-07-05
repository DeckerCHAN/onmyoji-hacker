#!/usr/bin/env bash

DATASET_DIR=/home/deckerchan/Workspace/Python/models-master/slim/data/flower
TRAIN_DIR=/home/deckerchan/Workspace/Python/models-master/slim/data/train_logs
python train_image_classifier.py \
    --train_dir=${TRAIN_DIR} \
    --dataset_name=flowers \
    --dataset_split_name=train \
    --dataset_dir=${DATASET_DIR} \
    --model_name=vgg_16