from rankfm.rankfm import RankFM
from typing import List


def get_rankfm_pred(model: RankFM, user: int, k: int = 10) -> List[int]:
    """
    Возвращает список рекомендуемых песен для заданного пользователя на основе модели rankfm.
    
    :param model: Модель rankfm.
    :param user: Идентификатор пользователя.
    :param k: Количество рекомендаций, которые нужно сделать (по умолчанию 10).
    :return: Список идентификаторов песен.
    """
    # Используем модель rankfm для получения рекомендаций
    recommendations = model.recommend([user], n_items=k, filter_previous=True)
    
    # Преобразуем результат в список идентификаторов песен
    song_ids = recommendations.to_numpy().tolist()[0]
    
    # Возвращаем список идентификаторов песен
    return song_ids