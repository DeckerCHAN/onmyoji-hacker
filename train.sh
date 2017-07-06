#!/usr/bin/env bash
python3 slim/train_image_classifier.py --dataset_dir=slim/data/customer --train_dir=slim/data/models --dataset_name=customer --dataset_split_name=train --model_name=vgg_16