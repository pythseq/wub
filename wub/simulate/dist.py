# -*- coding: utf-8 -*-

import numpy as np

"""Sample from various distributions."""


def sample_truncated_gamma(mean, shape, low=None, high=None):
    """A naive rejection approach to sample from truncated gamma distribution.
    Note that truncation points ae included in the sample.

    :param mean: Mean of the distribution.
    :param shape: Shape parameter.
    :param low: Lower truncation point.
    :param high: Upper truncation point.
    :returns: Random sample from the specified distribution.
    :rtype: float

    """

    scale = float(mean) / shape
    while True:
        sample = np.random.gamma(scale=scale, shape=shape, size=1)
        if low is not None and sample < low:
            continue
        if high is not None and sample > high:
            continue
        return float(sample)
