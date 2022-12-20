from sklearn.metrics import ndcg_score
import numpy as np


def MAP_k(true, pred, k):
    m = 0
    num = min(len(true), len(pred))
    for tr, pr in zip(true, pred):
        if not tr:
            continue
        tr_in_pr = np.isin(pr[:k], tr)
        m += (tr_in_pr / np.arange(1, k + 1)).sum() / (1 / np.arange(1, len(tr) + 1)).sum()
    m = m / num
    return m


def AR_k(true, pred, k):
 
    if not true:
        return 0.0
    
    if len(pred)>k:
        pred = pred[:k]

    score = 0.0
    hits = 0.0

    for i, p in enumerate(pred):
        if p in true and p not in pred[:i]:
            hits += 1.0
            score += hits / (i+1.0)

    return score / len(true)

def MAR_k(true, pred, k):
    
    return np.mean([AR_k(a,p,k) for a,p in zip(true, pred)])


