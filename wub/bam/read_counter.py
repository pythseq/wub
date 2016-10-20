# -*- coding: utf-8 -*-
"""Count reads per reference in BAM/SAM file."""

import pysam
from collections import defaultdict


def count_reads(alignment_file, in_format='BAM', min_aln_qual=0):
    """Count reads mapping to references in a BAM file.

    :param alignment_file: BAM file.
    :param min_aln_qual: Minimum mapping quality.
    :returns: Dictionary with read counts per reference.
    :rtype: dict
    """
    counts = defaultdict(int)
    if in_format == 'BAM':
        mode = "rb"
    elif in_format == 'SAM':
        mode = "r"
    else:
        raise Exception("Invalid format: {}".format(in_format))
    
    aln_iter = pysam.AlignmentFile(alignment_file, mode)


    for segment in aln_iter:
        if segment.is_unmapped:
            continue
        if segment.mapping_quality >= min_aln_qual:
            counts[segment.reference_name] += 1

    aln_iter.close()

    return dict(counts)
