#!/usr/bin/env python3

import math
from operator import itemgetter


def convert_relative_to_presence_absense(df):
    """
    To convert relative abundance profiles into
    presence–absence profiles (1 if a species is present and 0 otherwise),

    relative abundances < min(aij) + 0.01 * (Q95(aij) + min(aij))

    (that is, within 1% of the minimum relative I abundance values
    aij for species i across individuals j; Q95 or 95th percentile
    was used instead of max to improve robustness to outliers) were
    assumed to be due to technical noise.

    Reference: https://doi.org/10.1038/s41559-020-1236-0

    Parameters
    ----------
    df : pd.DataFrame
        a dataframe of relative abundance profile

    Returns
    -------
    pd.DataFrame
        a dataframe of presence-absense profile
    """

    df_ = df.copy()
    for i in range(0, len(df_)):
        abun_tuples = [
            (index, abun) for index, abun in enumerate(df_.iloc[i, 1:].to_list())
        ]
        abun_tuples.sort(key=itemgetter(1))

        abun_min = abun_tuples[0][1]
        Q95 = int(math.floor(len(abun_tuples) * 0.95))
        # Q95 = int(round(len(abun_tuples) * 0.95))

        abun_95 = abun_tuples[Q95 - 1][1]

        for abun in abun_tuples:
            if abun[1] < abun_min + 0.01 * (abun_95 - abun_min):
                df_.iat[i, abun[0] + 1] = 0
            else:
                df_.iat[i, abun[0] + 1] = 1
    return df_
