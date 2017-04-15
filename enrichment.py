"""
enrichment.py
"""

import cPickle
import collections
import numpy as np
import scipy.stats

with open("data.pickle", "r") as data:
    DRUGS_GENERIC, TREATMENTS, FREQUENCIES = cPickle.load(data)

def fisher_wrapper(column):
    """
    Input: a 4d vector
    Output: a 2d vector
    """

    return scipy.stats.fisher_exact(np.reshape(column, (2, 2)))

def main():
    """
    main function
    """

    drugs = ["C0593906", "C0065374", "C0162712", "C0699992"]

    drugs_generic = [
        DRUGS_GENERIC[drug]
        if drug in DRUGS_GENERIC else drug for drug in drugs
    ]

    counter = collections.Counter(
        treatment for drug in drugs_generic for treatment in TREATMENTS[drug]
    )

    observed = np.array(counter.values(), dtype="float")

    background = np.array(
        [FREQUENCIES[key] for key in counter.keys()],
        dtype="float"
    )

    contingencies = np.vstack(
        (
            observed,
            background,
            len(drugs) - observed,
            sum(FREQUENCIES.values()) - background
        )
    )

    tests = zip(
        counter.keys(),
        [fisher_wrapper(column) for column in contingencies.T]
    )

    for row in tests:
        cui, (likelihood, p_value) = row
        print "{}\t{:.2f}\t{:.4f}".format(cui, likelihood, p_value)

if __name__ == "__main__":
    main()
