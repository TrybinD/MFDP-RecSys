import numpy as np

def average_precision(actual, recommended):
    ap_sum = 0
    hits = 0
    for i, product_id in enumerate(recommended):
        if product_id in actual:
            hits += 1
            ap_sum += hits / (i + 1)
    return ap_sum / len(recommended)


def average_single_precision(actual, recommended):
    idx = np.where(recommended == actual)[0] + 1

    if idx:
        return 1/((idx.item())*len(recommended))
    return 0