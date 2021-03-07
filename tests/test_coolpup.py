#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 13:24:55 2019

@author: Ilya Flyamer
"""

from coolpuppy import *
import numpy as np
import pandas as pd
from scipy import sparse
import cooler
import pytest
import subprocess
import os

amap = load_array_with_header("tests/loop_ref.np.txt")['data']
amapTAD = load_array_with_header("tests/tad_ref.np.txt")['data']


def test_corner_cv():
    assert np.isclose(corner_cv(amap), 0.06402256144363466)
    assert np.isclose(corner_cv(amap, 3), 0.06687246748037583)


def test_get_enrichment():
    assert np.isclose(get_enrichment(amap, 1), 1.7988016831397438)
    assert np.isclose(get_enrichment(amap, 3), 1.4364442129281982)


bed = pd.read_csv("tests/test.bed", sep="\t", names=["chr", "start", "end"])

# def test_filter_bed():
#    assert filter_bed(bed, 1000, 2000, ['chr1']).shape == (1, 3)

# bedpe = pd.read_csv(
#    "tests/test.bedpe",
#    sep="\t",
#    names=["chr1", "start1", "end1", "chr2", "start2", "end2"],
# )

# def test_filter_bedpe():
#    assert filter_bedpe(bedpe, 100000, 1000000, ['chr3']).shape == (1, 6)


# def test_auto_read_bed():
#    assert np.all(auto_read_bed('tests/test.bed') == bed)
#    assert np.all(auto_read_bed('tests/test.bedpe') == bedpe)
#
# def test_get_mids():
#    bed_mids = get_mids(bed, 1000, kind='bed')
#    assert np.all(bed_mids['Bin'] == [1, 12, 2, 1])
#    assert np.all(bed_mids['Pad'] == [500, 10000, 1000, 500])
#
#    bedpe_mids = get_mids(bedpe, 1000, kind='bedpe')
#    assert np.all(bedpe_mids['Bin1'] == [1, 21, 1, 101])
#    assert np.all(bedpe_mids['Bin2'] == [3, 51, 1, 201])
#    assert np.all(bedpe_mids['Pad1'] == [100, 1000, 150, 1000])
#    assert np.all(bedpe_mids['Pad2'] == [100, 1000, 50, 1000])

amapbed2 = load_array_with_header("tests/bed2_ref.np.txt")['data']


def test___main__():
    # Loops

    for f in (
        "tests/testing_loop.txt",
        "tests/testing_tad.txt",
        "tests/testing_bed2.txt",
        "tests/testing_loop_numeric.txt",
        "tests/testing_loop_numeric_noX.txt",
    ):
        try:
            os.remove(f)
        except:
            print(f, "doesn't exist")

    subprocess.run(
        """coolpup.py tests/Scc1-control.10000.cool
                      tests/CH12_loops_Rao.bed --basetype bedpe --mindist 0
                      --unbalanced --coverage_norm --outdir tests
                      --outname testing_loop.txt --ignore_diags 0 --n_proc 2
                      --seed 0""".split()
    )
    testamap = load_array_with_header("tests/testing_loop.txt")['data']
    assert np.isclose(get_enrichment(amap, 3), get_enrichment(testamap, 3), 0.1)

    # Bed2
    # subprocess.run(
    #     """coolpup.py tests/Scc1-control.10000.cool
    #                   tests/Bonev_CTCF+.bed --bed2 tests/Bonev_CTCF-.bed
    #                   --mindist 0 --subset 1000
    #                   --unbalanced --coverage_norm --outdir tests
    #                   --outname testing_bed2.txt --n_proc 2
    #                   --seed 0""".split()
    # )
    # assert np.isclose(
    #     get_enrichment(amapbed2, 3),
    #     get_enrichment(np.loadtxt("tests/testing_bed2.txt"), 3),
    #     0.1,
    # )

    # TADs
    subprocess.run(
        """coolpup.py tests/Scc1-control.10000.cool
                      tests/CH12_TADs_Rao.bed --basetype bed --local --rescale
                      --unbalanced --coverage_norm --outdir tests
                      --outname testing_tad.txt --n_proc 2
                      --seed 0""".split()
    )

    assert np.isclose(
        get_local_enrichment(amapTAD),
        get_local_enrichment(np.loadtxt("tests/testing_tad.txt")),
        0.01,
    )

    # Numeric chroms
    subprocess.run(
        """coolpup.py tests/Scc1-control.10000.numeric_chroms.cool
                      tests/CH12_loops_Rao_numeric_chroms.bed
                      --basetype bedpe
                      --mindist 0
                      --unbalanced --coverage_norm --outdir tests
                      --outname testing_loop_numeric.txt --n_proc 2
                      --seed 0""".split()
    )
    testamap = load_array_with_header("tests/testing_loop_numeric.txt")['data']
    assert np.isclose(get_enrichment(amap, 3), get_enrichment(testamap, 3), 0.1)
    
    subprocess.run(
        """coolpup.py tests/Scc1-control.10000.numeric_chroms.cool
                      tests/CH12_loops_Rao_numeric_chroms_noX.bed
                      --mindist 0
                      --unbalanced --coverage_norm --outdir tests
                      --outname testing_loop_numeric_noX.txt --n_proc 2
                      --seed 0""".split()
    )
    testamap = load_array_with_header("tests/testing_loop_numeric_noX.txt")['data']
    assert np.isclose(get_enrichment(amap, 3), get_enrichment(testamap, 3), 0.1)


# def test_by_window():
#    try:
#        clr = cooler.Cooler("GSE93431_UNTR.10kb.cool.HDF5")
#    except OSError:
#        import wget
#
#        wget.download(
#            "ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE93nnn/GSE93431/suppl/GSE93431_UNTR.10kb.cool.HDF5.gz",
#            out="tests/",
#        )
#        subprocess.run("gzip -d tests/GSE93431_UNTR.10kb.cool.HDF5.gz".split())
#        clr = cooler.Cooler("tests/GSE93431_UNTR.10kb.cool.HDF5")
#    assert clr.binsize == 10000


# def test_pileupsWithControl():
#    loops = auto_read_bed('tests/CH12_loops_Rao.bed')
#    loopmids = get_mids(loops, resolution=10000, kind='bedpe')
#    pup = pileupsWithControl(loopmids, 'tests/Scc1-control.10000.cool',
#                             mindist=210000, balance=False, cov_norm=True,
#                             kind='bedpe', pad=10, seed=0)
#    assert np.allclose(pup, amap)
#
#    np.random.seed(0)
#    ctcf_left = auto_read_bed('tests/Bonev_CTCF+.bed').sample(1000)
#    ctcf_right = auto_read_bed('tests/Bonev_CTCF-.bed').sample(1000)
#
#    leftmids = get_mids(ctcf_left, resolution=10000, kind='bed')
#    rightmids = get_mids(ctcf_right, resolution=10000, kind='bed')
#
#    pup = pileupsWithControl(leftmids, 'tests/Scc1-control.10000.cool',
#                             mids2=rightmids, ordered_mids=True,
#                             mindist=210000, balance=False, cov_norm=True,
#                             kind='bed', pad=10, seed=0)
#    assert np.allclose(pup, amapbed2)
#
#    np.random.seed(0)
#    loops = auto_read_bed('tests/CH12_loops_Rao_numeric_chroms.bed')
#    loopmids = get_mids(loops, resolution=10000, kind='bedpe')
#    pup = pileupsWithControl(loopmids, 'tests/Scc1-control.10000.numeric_chroms.cool',
#                             mindist=210000, balance=False, cov_norm=True,
#                             kind='bedpe', pad=10, seed=0)
#    assert np.allclose(pup, amap)
