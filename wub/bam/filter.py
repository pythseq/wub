# -*- coding: utf-8 -*-
"""Filter SAM/BAM records by various criteria."""

import itertools


def get_alignment_score(segement):
    """Get alignment score from pysam segment.

    :param segment: Pysam aligned segment.
    :returns: Alignment score.
    :rtype: int
    """

    score = 0
    try:
        score = segement.get_tag('AS')
    except:
        pass
    return score


def filter_top_per_query(records_iter):
    """Filter pysam records keeping top scoring per query. Assumes
    records are sorted by name.

    :param records_iter: Iterator of pysam aligned segments.
    :returns: Generator of filtered records.
    :rtype: generator
    """
    buff = []
    for rec in itertools.chain(records_iter, [None]):
        if len(buff) == 0:
            buff.append(rec)
        elif rec is None or buff[-1].query_name != rec.query_name:
            sorted_buff = sorted(buff, key=get_alignment_score, reverse=True)
            buff = [rec]
            yield sorted_buff[0]
        else:
            buff.append(rec)
