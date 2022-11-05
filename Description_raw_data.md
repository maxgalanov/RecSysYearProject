# Описание raw_data
Все датасеты получены из [The Million Song Dataset](http://millionsongdataset.com/) - это открытый набор данных для миллиона современных популярных музыкальных треков.

#### Датасет train_triplets.txt
Датасет получен из [Taste Profile dataset](http://millionsongdataset.com/tasteprofile/). Набор данных содержит реальное количество прослушиваний (count_play) пользователями (user_id), все песни сопоставляются с датасетом MSD по song_id.

Данные представлены в формате триплетов user_id, song_id, count_play.
| user_id | song_id | count_play |
| ------ | ------ | ------ |
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOAKIMP12A8C130995|	1|
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOAPDEY12A81C210A9|	1|
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOBBMDR12A8C13253B|	2|
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOBFNSP12AF72A0E22|	1|

Цифры:
- 1 019 318 уникальных пользователей (user_id)
- 384 546 уникальных песен The Echo Nest (song_id)
- 48 373 586 триплетов: user_id - song_id - count_play


#### Датасет unique_tracks.txt
Датасет получен из [The Million Song Dataset](http://millionsongdataset.com/sites/default/files/AdditionalFiles/unique_tracks.txt). Набор данных содержит информацию о песнях:
- track_id - идентификатор песни из The Million Song Dataset
- song_id - идентификатор песни из The Echo Nest
- artist_name - имя исполнителя
- song_title - название трека

Цифры:
- 1 000 000 уникальных track_id
- 999 056 уникальных song_id


#### Датасет sid_mismatches.txt
Данные получены из [The Million Song Dataset](http://millionsongdataset.com/sites/default/files/tasteprofile/sid_mismatches.txt). Набор данных содержит информацию о неверно объединенных парах song_id и track_id :
- track_id - идентификатор песни из The Million Song Dataset
- song_id - идентификатор песни из The Echo Nest

Цифры:
- 19 093 неверно объединенных пар track_id - song_id


#### Датасет song_data.csv
Данные получены из [The Million Song Dataset](http://millionsongdataset.com/sites/default/files/tasteprofile/sid_mismatches.txt). Набор данных содержит информацию о треках:
- song_id - идентификатор песни из The Echo Nest
- title - название песни
- release - название альбома
- artist_name - имя исполнителя
- year - год выхода песни (0 - нет информации о годе)

Цифры:
- 999 056 уникальных песен
- 69 991 уникальных исполнителей
- 503 890 уникальных песен, для которых определен год
- 1922 - минимальный год выхода трека
- 2011 - максимальный год выхода трека


#### Датасет msd_beatunes_map.txt
Данные получены из [The Last.fm Dataset](http://millionsongdataset.com/lastfm/). Набор данных содержит информацию о жанрах треков:
- track_id - идентификатор песни из MSD
- seed_genre - жанр песни

Цифры:
- 6 151 уникальных жанров
- 677 038 уникальных трека, для которых определен жанр

#### Датасет msd-MAGD-genreAssignment.txt
Данные получены из [Million Song Dataset Benchmarks](http://www.ifs.tuwien.ac.at/mir/msd/partitions/msd-MAGD-genreAssignment.cls). Набор данных содержит информацию о жанрах треков:
- track_id - идентификатор песни из MSD
- genre - жанр песни

Цифры:
- 21 уникальных жанров
- 422 714 уникальных трека, для которых определен жанр
  
  

#### Датасет msd-MASD-styleAssignment.txt
Данные получены из [Million Song Dataset Benchmarks](http://www.ifs.tuwien.ac.at/mir/msd/partitions/msd-MASD-styleAssignment.cls). Набор данных содержит информацию о стилях треков:
- track_id - идентификатор песни из MSD
- style - жанр песни

Цифры:
- 25 уникальных стилей
- 273 936 уникальных трека, для которых определен стиль