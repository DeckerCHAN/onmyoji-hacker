# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Factory method for easily getting imdbs by name."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__sets = {}
from lib.datasets.derek_set import derek_set


def get_imdb(name):
    """Get an imdb (image database) by name."""
    if name not in __sets:
        raise KeyError('Unknown dataset: {}'.format(name))
    return __sets[name]()

__sets['derek_set_train'] = (lambda split='train': derek_set(split))
__sets['derek_set_val'] = (lambda split='val': derek_set(split))

def list_imdbs():
    """List all registered imdbs."""
    return list(__sets.keys())
