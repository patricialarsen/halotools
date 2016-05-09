#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np 
import pytest 
import multiprocessing 

from ..mock_observables_helpers import enforce_pbcs, get_num_threads

__all__ = ('test_enforce_pbcs', )

fixed_seed = 43

def test_enforce_pbcs():
    npts = 10
    x = np.linspace(0, 1, npts)
    y = np.linspace(0, 1, npts)
    z = np.linspace(0, 1, npts)

    enforce_pbcs(x, y, z, [1, 1, 1])

    with pytest.raises(ValueError) as err:
        enforce_pbcs(x, y, z, [0.9, 1, 1])
    substr = "You set xperiod = "
    assert substr in err.value.args[0]

    with pytest.raises(ValueError) as err:
        enforce_pbcs(x, y, z, [1, 0.9, 1])
    substr = "You set yperiod = "
    assert substr in err.value.args[0]

    with pytest.raises(ValueError) as err:
        enforce_pbcs(x, y, z, [1, 1, 0.9])
    substr = "You set zperiod = "
    assert substr in err.value.args[0]

    x = np.linspace(-1, 1, npts)
    with pytest.raises(ValueError) as err:
        enforce_pbcs(x, y, z, [1, 1, 1])
    substr = "your input data has negative values"
    assert substr in err.value.args[0]

def test_get_num_threads():

    input_num_threads = 1
    result = get_num_threads(input_num_threads, enforce_max_cores = False)
    assert result == 1

    input_num_threads = 'max'
    result = get_num_threads(input_num_threads, enforce_max_cores = False)
    assert result == multiprocessing.cpu_count()

    max_cores = multiprocessing.cpu_count()

    input_num_threads = max_cores + 1
    result = get_num_threads(input_num_threads, enforce_max_cores = False)
    assert result == input_num_threads

    input_num_threads = max_cores + 1
    result = get_num_threads(input_num_threads, enforce_max_cores = True)
    assert result == max_cores

    input_num_threads = '$'
    with pytest.raises(ValueError) as err:
        result = get_num_threads(input_num_threads, enforce_max_cores = True)
    substr = "Input ``num_threads`` must be an integer"
    assert err.value.args[0] in substr





