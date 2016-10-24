import unittest

import tempfile
import os

from wub.bam import compare


class TestBamCompare(unittest.TestCase):

    """Test BAM comparison test."""

    def _generate_test_data(self):
        """Generate test data for dnadiff test."""
        fh_sam_one = tempfile.NamedTemporaryFile(suffix=".sam", delete=False)
        self.sam_one = fh_sam_one.name

        data = """@SQ	SN:chr0	LN:827
@SQ	SN:chr1	LN:6379
@PG	ID:bwa	PN:bwa	VN:0.7.15-r1142-dirty	CL:bwa mem genome.fas reads.fq
r0_chr1_4118_4168_+/q17/s0/d0/i1	0	chr1	4119	60	8M1I42M	*	0	0	CATTTGGTACCATTGTGATCCGCTCTTAGAAACTTTTGGCACTTTATCGCG	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:1	MD:Z:50	AS:i:43	XS:i:0
r1_chr1_72_122_+/q12/s0/d2/i1	4	*	0	0	*	*	0	0	AGCGCAGTGGTCGACTTAGCTTATTCACGAGAGCCTTCCAACTGGCCAG	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	AS:i:0	XS:i:0
r2_chr0_279_329_-/q17/s0/d1/i0	16	chr0	280	60	16M1D33M	*	0	0	AGAACTTGCAAGCGCGGCTCCAGCCTTTCAGGACGAGACCCTCCAAGAC	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:1	MD:Z:16^C33	AS:i:42	XS:i:0
r3_chr1_60_110_+/q14/s1/d1/i0	0	chr1	61	51	36M1D13M	*	0	0	GGTGTTTTATATAGCGCAGTGTCGACTTAGCTTATTGCGACGAGCCTTC	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:2	MD:Z:36^C0A12	AS:i:37	XS:i:0
r4_chr1_1268_1318_+/q12/s1/d2/i0	0	chr1	1269	28	19M1D23M1D6M	*	0	0	GTATTCCATCGAGCTGGATCAGTTTAGGAGTGTGCCTAGGTATATCCC	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:3	MD:Z:19^G5G17^C6	AS:i:30	XS:i:0
r5_chr0_576_626_-/q12/s1/d2/i0	4	*	0	0	*	*	0	0	GCAAATTTTACAGATGATAAAACACCGAATATTCAGACCGTGTAAATA	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	AS:i:0	XS:i:0
r6_chr0_509_559_-/q12/s0/d3/i0	16	chr0	510	60	20M1D27M	*	0	0	TGTGGTAGGAGCGGAGCGGGCCCACACCCCCATCCCCCGCGAAATAA	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:1	MD:Z:20^A27	AS:i:40	XS:i:0
r7_chr1_2417_2467_-/q12/s1/d1/i1	16	chr1	2418	41	6M1D37M1I6M	*	0	0	AGCCGATCATCCCGTCCCTGTTCACTCCTACGTCTTGGCTTGGAAAGTGT	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:3	MD:Z:6^G27G15	AS:i:34	XS:i:0
r8_chr0_661_711_-/q11/s0/d3/i1	4	*	0	0	*	*	0	0	GTCTGAGGCGCCATATTAGGCGGGCAAAATGGACTATGACTGTGGCAG	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	AS:i:0	XS:i:0
r9_chr0_523_573_-/q14/s0/d1/i1	16	chr0	524	59	3M1I25M1D21M	*	0	0	AGCGGGGACCCACACCCCCATCCCCCGCGAATAATTCAACGTTCGCATTA	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:2	MD:Z:28^A21	AS:i:39	XS:i:0
"""

        fh_sam_one.write(data)
        fh_sam_one.flush()
        fh_sam_one.close()

        data = """@SQ	SN:chr0	LN:827
@SQ	SN:chr1	LN:6379
@PG	ID:bwa	PN:bwa	VN:0.7.15-r1142-dirty	CL:bwa mem genome.fas reads.fq
r0_chr1_4118_4168_+/q17/s0/d0/i1	0	chr1	4119	60	8M1I42M	*	0	0	CATTTGGTACCATTGTGATCCGCTCTTAGAAACTTTTGGCACTTTATCGCG	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:1	MD:Z:50	AS:i:43	XS:i:0
r1_chr1_72_122_+/q12/s0/d2/i1	4	*	0	0	*	*	0	0	AGCGCAGTGGTCGACTTAGCTTATTCACGAGAGCCTTCCAACTGGCCAG	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	AS:i:0	XS:i:0
r2_chr0_279_329_-/q17/s0/d1/i0	16	chr0	280	60	16M1D33M	*	0	0	AGAACTTGCAAGCGCGGCTCCAGCCTTTCAGGACGAGACCCTCCAAGAC	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:1	MD:Z:16^C33	AS:i:42	XS:i:0
r3_chr1_60_110_+/q14/s1/d1/i0	0	chr1	61	51	36M1D13M	*	0	0	GGTGTTTTATATAGCGCAGTGTCGACTTAGCTTATTGCGACGAGCCTTC	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:2	MD:Z:36^C0A12	AS:i:37	XS:i:0
r4_chr1_1268_1318_+/q12/s1/d2/i0	0	chr1	1269	28	19M1D23M1D6M	*	0	0	GTATTCCATCGAGCTGGATCAGTTTAGGAGTGTGCCTAGGTATATCCC	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:3	MD:Z:19^G5G17^C6	AS:i:30	XS:i:0
r5_chr0_576_626_-/q12/s1/d2/i0	4	*	0	0	*	*	0	0	GCAAATTTTACAGATGATAAAACACCGAATATTCAGACCGTGTAAATA	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	AS:i:0	XS:i:0
r6_chr0_509_559_-/q12/s0/d3/i0	16	chr0	510	60	20M1D27M	*	0	0	TGTGGTAGGAGCGGAGCGGGCCCACACCCCCATCCCCCGCGAAATAA	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:1	MD:Z:20^A27	AS:i:40	XS:i:0
r7_chr1_2417_2467_-/q12/s1/d1/i1	16	chr1	2418	41	6M1D37M1I6M	*	0	0	AGCCGATCATCCCGTCCCTGTTCACTCCTACGTCTTGGCTTGGAAAGTGT	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:3	MD:Z:6^G27G15	AS:i:34	XS:i:0
r8_chr0_661_711_-/q11/s0/d3/i1	4	*	0	0	*	*	0	0	GTCTGAGGCGCCATATTAGGCGGGCAAAATGGACTATGACTGTGGCAG	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	AS:i:0	XS:i:0
r9_chr0_523_573_-/q14/s0/d1/i1	16	chr0	726	59	4M25M1D21M	*	0	0	AGCGGGGACCCACACCCCCATCCCCCGCGAATAATTCAACGTTCGCATTA	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII	NM:i:2	MD:Z:28^A21	AS:i:39	XS:i:0
"""
        fh_sam_two = tempfile.NamedTemporaryFile(suffix=".sam", delete=False)
        self.sam_two = fh_sam_two.name

        fh_sam_two.write(data)
        fh_sam_two.flush()
        fh_sam_two.close()

    def _cleanup_test_data(self):
        """Cleanup test dataset."""
        os.unlink(self.sam_one)
        os.unlink(self.sam_two)

    def test_bam_read_counter(self):
        """Test read_counter wrapper."""
        self._generate_test_data()
        res = compare.bam_compare(self.sam_one, self.sam_two, in_format='SAM')
        self.assertAlmostEqual(res['AlignedSimilarity'], 0.8546, places=3)
        self._cleanup_test_data()
