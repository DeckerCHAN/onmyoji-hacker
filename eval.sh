#!/usr/bin/env bash
python3 slim/eval_image_classifier.py --checkpoint_path=slim/data/models --eval_dir=slim/data/eval	  --dataset_name=customer  --dataset_split_name=validation   --dataset_dir=slim/data/customer    --model_name=vgg_16
