from sklearn.metrics import ndcg_score
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def precision_k(true, pred, k):
    """
    Calculates the precision of the predicted ranking at position k.

    Parameters
    ----------
    true : list of lists
        The actual relevance scores of the items in the ranking, in descending order.
    pred : list of lists
        The predicted relevance scores of the items in the ranking, in descending order.
    k : int, optional
        The position at which to calculate the precision. The default is to consider all items.

    Returns
    -------
    float
        The precision of the predicted ranking at position k.
    """
    p = 0
    num = min(len(true), len(pred))
    
    for tr, pr in zip(true, pred):
        if not tr:
            continue
        
        p += len(set(tr) & set(pr[:k])) / min(float(k), len(tr))
        
    p = p / num
    return p


def recall_k(true, pred, k):
    """
    Calculates the recall of the predicted ranking at position k.

    Parameters
    ----------
    true : list of lists
        The actual relevance scores of the items in the ranking, in descending order.
    pred : list of lists
        The predicted relevance scores of the items in the ranking, in descending order.
    k : int, optional
        The position at which to calculate the precision. The default is to consider all items.

    Returns
    -------
    float
        The precision of the predicted ranking at position k.
    """
    r = 0
    num = min(len(true), len(pred))
    
    for tr, pr in zip(true, pred):
        if not tr:
            continue
        
        r += len(set(tr) & set(pr[:k])) / len(tr)
        
    r = r / num
    return r


def MAP_k(true, pred, k):
    """
    Computes the mean average precision (MAP) for the top k items recommended to each user.

    Parameters:
    true (list of lists): List of lists where each sublist represents the true items of a user.
    pred (list of lists): List of lists where each sublist represents the predicted items of a user.
    k (int): Number of items to be considered for computing MAP.

    Returns:
    m (float): Mean average precision (MAP) for the top k items recommended to each user.
    """
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
    """
    Computes the average recall (AR) for the top k items recommended to a single user.

    Parameters:
    true (list): List of true items of a user.
    pred (list): List of predicted items of a user.
    k (int): Number of items to be considered for computing AR.

    Returns:
    score (float): Average recall (AR) for the top k items recommended to a single user.
    """
    if not true:
        return 0.0
    
    if len(pred) > k:
        pred = pred[:k]

    score = 0.0
    hits = 0.0

    for i, p in enumerate(pred):
        if p in true and p not in pred[:i]:
            hits += 1.0
            score += hits / (i+1.0)
    
    score = score / len(true)

    return score


def MAR_k(true, pred, k):
    """
    Computes the mean average recall (MAR) for the top k items recommended to multiple users.

    Parameters:
    true (list of lists): List of lists where each sublist represents the true items of a user.
    pred (list of lists): List of lists where each sublist represents the predicted items of a user.
    k (int): Number of items to be considered for computing MAR.

    Returns:
    score (float): Mean average recall (MAR) for the top k items recommended to multiple users.
    """
    score = np.mean([AR_k(a, p, k) for a, p in zip(true, pred)])
    
    return score


def nDCG_k(y_true, y_pred, k=None):
    """
    Calculates the Normalized Discounted Cumulative Gain (NDCG) score.

    Parameters
    ----------
    y_true : list of lists
        List of lists with the true items for each user.
    y_pred : list of lists
        List of lists with the predicted items for each user.
    k : int, optional
        The number of items to consider for the NDCG calculation. If not
        specified, all items will be considered.

    Returns
    -------
    ndcg : float
        The NDCG score.
    """
    ndcg = 0.0
    for i in range(len(y_true)):
        idcg = 0.0
        dcg = 0.0
        if k:
            tr = y_true[i]
            pr = list(y_pred[i][:k])
        for j, item in enumerate(pr):
            if item in tr:
                idcg += 1.0 / np.log2(j + 2)
                dcg += 1.0 / np.log2(pr.index(item) + 2)
        if idcg == 0.0:
            continue
        ndcg += dcg / idcg
        
    ndcg = ndcg / len(y_true)
    return ndcg


def calculate_coverage(pred, num_songs):
    """
    Computes the fraction of unique songs recommended to all users.

    Parameters:
    pred (np.array): 2D array where each row represents the songs recommended to a user.
    num_songs (int): Total number of songs.

    Returns:
    cov (float): Fraction of unique songs recommended to all users, with a range from 0 to 1, where 0 indicates no songs were recommended 
                 and 1 indicates that all songs were recommended to at least one user.
    """
    unique_songs = np.unique(pred)
    cov = len(unique_songs) / num_songs
    
    return cov


def calculate_personalization(pred, num_users, num_songs):
    """
    Computes the average similarity between all pairs of songs recommended to different users.

    Parameters:
    pred (np.array): 2D array where each row represents the songs recommended to a user.
    num_users (int): Number of users.
    num_songs (int): Number of songs.

    Returns:
    avg_sim (float): Average similarity between all pairs of songs recommended to different users, 
                     with a range from 0 to 1, where 0 indicates no similarity and 1 indicates perfect similarity.
    """
    matrix_ohe = np.zeros((num_users, num_songs), dtype=np.float32)
    matrix_ohe[np.arange(num_users), pred.T] = 1.
    sim_matrix = cosine_similarity(matrix_ohe)
    avg_sim = 1 - (sim_matrix.sum() - num_users) / (num_users * (num_users - 1))
    
    return avg_sim


def calculate_novelty(predicted_items, item_frequencies):
    """
    Calculate the novelty score of a set of predicted items.

    Parameters:
    - predicted_items (list of lists): A list of lists of predicted item IDs for each user.
    - item_frequencies (dict): A dictionary mapping item IDs to their frequency of occurrence in the dataset.

    Returns:
    - novelty_score (float): The novelty score of the predicted items.
    """
    all_unique_items = set(item for user_items in predicted_items for item in user_items)
    item_distribution = np.array([item_frequencies.get(item, 1e-6) for item in all_unique_items])
    item_distribution = item_distribution / item_distribution.sum()
    novelty_score = -np.sum(item_distribution * np.log2(item_distribution))
    
    return novelty_score