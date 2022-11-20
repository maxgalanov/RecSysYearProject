# Описание raw_data
Данные находятся в репозитории в [hse_rec_sys/data/raw/](https://github.com/maxgalanov/RecSysYearProject/blob/main/hse_rec_sys/data/raw/raw_data_links.txt). Все датасеты получены из [The Million Song Dataset](http://millionsongdataset.com/) - это открытый набор данных для миллиона современных популярных музыкальных треков.

### Датасет train_triplets.txt
Датасет получен из [Taste Profile dataset](http://millionsongdataset.com/tasteprofile/). Набор данных содержит реальное количество прослушиваний (count_play) пользователями (user_id), все песни сопоставляются с датасетом MSD по song_id.

Данные представлены в формате триплетов user_id, song_id, count_play.
| user_id | song_id | count_play |
| ------ | ------ | ------ |
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOAKIMP12A8C130995|	1 |
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOAPDEY12A81C210A9|	1 |
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOBBMDR12A8C13253B|	2 |
| b80344d063b5ccb3212f76538f3d9e43d87dca9e|	SOBFNSP12AF72A0E22|	1 |

Цифры:
- 1 019 318 уникальных пользователей (user_id)
- 384 546 уникальных песен The Echo Nest Datset (song_id)
- 48 373 586 триплетов: user_id - song_id - count_play


### Датасет unique_tracks.txt
Датасет получен из [The Million Song Dataset](http://millionsongdataset.com/sites/default/files/AdditionalFiles/unique_tracks.txt). Набор данных содержит информацию о песнях:
- track_id - идентификатор песни из The Million Song Dataset
- song_id - идентификатор песни из The Echo Nest Datset
- artist_name - имя исполнителя
- song_title - название трека

| track_id | song_id | artist_name | artist_name |
| ------ | ------ | ------ | ------ |
| TRMMMYQ128F932D901 | SOQMMHC12AB0180CB8 | Faster Pussy cat | Silent Night |
| TRMMMKD128F425225D | SOVFVAK12A8C1350D9 | Karkkiautomaatti | Tanssi vaan |
| TRMMMRX128F93187D9 | SOGTUKN12AB017F4F1 | Hudson Mohawke | No One Could Ever |

Цифры:
- 1 000 000 уникальных track_id
- 999 056 уникальных song_id


### Датасет sid_mismatches.txt
Данные получены из [The Million Song Dataset](http://millionsongdataset.com/sites/default/files/tasteprofile/sid_mismatches.txt). Набор данных содержит информацию о неверно объединенных парах song_id и track_id :
- track_id - идентификатор песни из The Million Song Dataset
- song_id - идентификатор песни из The Echo Nest Datset

Цифры:
- 19 093 неверно объединенных пар track_id - song_id


### Датасет song_data.csv
Данные получены из [The Million Song Dataset](http://millionsongdataset.com/sites/default/files/tasteprofile/sid_mismatches.txt). Набор данных содержит информацию о треках:
- song_id - идентификатор песни из The Echo Nest Datset
- title - название песни
- release - название альбома
- artist_name - имя исполнителя
- year - год выхода песни (0 - нет информации о годе)

| song_id | title | release | artist_name | year |
| ------ | ------ | ------ | ------ | ------ |
| SOQMMHC12AB0180CB8 | Silent Night | Monster Ballads X-Mas | Faster Pussy cat | 2003 |
| SOVFVAK12A8C1350D9 | Tanssi vaan | Karkuteill | Karkkiautomaatti | 1995 |
| SOGTUKN12AB017F4F1 | No One Could Ever | Butter | Hudson Mohawke | 2006 |

Цифры:
- 999 056 уникальных песен
- 69 991 уникальных исполнителей
- 503 890 уникальных песен, для которых определен год
- 1922 - минимальный год выхода трека
- 2011 - максимальный год выхода трека


### Датасет msd_beatunes_map.txt
Данные получены из [The Last.fm Dataset](http://millionsongdataset.com/lastfm/). Набор данных содержит информацию о жанрах треков:
- track_id - идентификатор песни из MSD
- seed_genre - поджанр песни
- numberOfUserLabels
- [label, strength]

| track_id | seed_genre | numberOfUserLabels | [label, strength] |
| ------ | ------ | ------ | ------ |
| TRAAAAK128F9318786 | Rock | 201 | Rock	0.6766169	Metal	0.09950249	Hard Rock	0.04477612	Alternative	0.03482587	Alt. Rock	0.029850746 ... |
| TRAAAAV128F421A322 | Rock | 8 | Rock	0.5	Punk	0.5 |
| TRAAAAW128F429D538 | Hip-Hop | 133 | Hip-Hop	0.48872182	Hip-Hop/Rap	0.2706767	Rap	0.09022556 ... |

Цифры:
- 6 151 уникальный поджанр
- 677 038 уникальных трека, для которых определен поджанр

### Датасет msd-MAGD-genreAssignment.txt
Данные получены из [Million Song Dataset Benchmarks](http://www.ifs.tuwien.ac.at/mir/msd/partitions/msd-MAGD-genreAssignment.cls). Набор данных содержит информацию о жанрах треков:
- track_id - идентификатор песни из MSD
- genre - жанр песни

| track_id | genre |
| ------ | ------ |
| TRAAAAK128F9318786 | Pop_Rock |
| TRAAAAV128F421A322 | Pop_Rock |
| TRAAAAW128F429D538 | Rap |

Цифры:
- 21 уникальный жанр
- 422 714 уникальных трека, для которых определен жанр
  

### Датасет msd_lastfm_map.txt
Данные получены из [The Last.fm Dataset](http://millionsongdataset.com/lastfm/). Набор данных содержит информацию о стилях треков:
- track_id - идентификатор песни из MSD
- seed_genre - поджанр песни
- [tag, strength]

| track_id | seed_genre | [tag, strength] |
| ------ | ------ | ------ |
| TRAAAAK128F9318786 | rock | alternativerock	100	rock	60	hardrock	60	heavymetal	20... |
| TRAAAAW128F429D538 | bayarea | bayarea	100	hieroglyiphics	100	classic	50... |
| TRAAABD128F429CF47 | oldies | 60s	100	soul	52	pop	41	rock	35	malevocalists	35... |

Цифры:
- 35 048 уникальных поджанров
- 505 216 уникальных трека, для которых определен поджанр

### Датасет data10000.csv
Это 1% от основного датасета, полученного из [The Million Song Dataset](http://www.millionsongdataset.com/pages/getting-dataset/#subset) с помощью написанного нами парсера [Parser_for_10k.ipynb](https://github.com/maxgalanov/RecSysYearProject/blob/main/hse_rec_sys/notebooks/Parser_for_10k.ipynb). Набор данных содержит информацию о 10 000 треках:
- artist_name - имя исполнителя
- artist_familarity - популярность исполнителя
- artist_hotttnesss -  алгоритмическая оценка 🔥 исполнителя
- artist_id - идентификатор исполнителя
- artist_location - место рождения исполнителя
- danceability - танцевальность трека
- duration - продолжительность трека в секундах
- energy - энергичность трека (0 - если не оценивалась)
- loudness - громкость трека
- mode - настроение песни (мажорное или минорное)
- mode_confidence - показатель достоверности настроения песни
- song_hotttnesss -  алгоритмическая оценка 🔥 трека
- song_id - идентификатор песни из The Echo Nest Datset
- tempo - темп в ударах в минуту
- time_signature - оценка количества ударов в такте
- time_signature_confidence - показатель достоверности оценки количества ударов в такте
- title - название трека
- track_id - идентификатор песни из MSD
- year - год выхода песни

Основной датасет имеет такую же структуру и содержит информацию о 1 000 000 треков.
