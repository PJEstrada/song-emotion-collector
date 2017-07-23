# -*- coding: utf-8 -*-
from music.models import Song, SongClassification, Participant
import operator

results = []
results_classified = []
for song in Song.objects.all():

    classifications = song.classifications.all()
    if len(classifications) < 3:
        results.append(song.pk)
    else:
        # Get major classification
        emotion_counts = {'alegria': 0, 'tristeza': 0, 'enojo': 0, 'miedo': 0, 'neutral': 0}
        for c in classifications:
            try:
                emotion_counts[c.mood_label] += 1
            except:
                print "Cannot find emotion: "+c.mood_label


        max_element_key = max(emotion_counts.iteritems(), key=operator.itemgetter(1))[0]
        if max_element_key == 'neutral':
            results.append(song.pk)
        results_classified.append({'song': song, 'emotion': max_element_key})

print "PENDING SONGS"
print len(results)
print "CLASSIFIED SONGS"
for x in results_classified:
    print x
    x['song'].mood = x['emotion']
    x['song'].save()

participants = [
    1,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    15,
    16,
    17,
    18,
    20,
    21,
    24,
    23,
    25,
    26,
    27,
    28,
    29,
    22,
    31,
    32,
    33,
    35,
    36,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    89,
    88,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    1252,
    1258,
    1259,
    1322,
    1323,
    1326,
    1325,
    1327,
    1349,
    1350,
    1391,
    1394,
    1393,
    1396,
    1395,
    1392,
    1397,
    1401,
    1390,
    1398,
    1404,
    1389,
    1403,
    1400,
    1407,
    1406,
    1408,
    1402,
    1624,
    1861,
    1862,
    1864,
    1863,
    1866,
    1865,
    1867,
    1868,
    1869,
    1870,
    1871,
    1872,
    1873,
    1874,
    1878,
    1876,
    1877,
    1879,
    1882,
    1881,
    1885,
    1886,
    1888,
    1889,
    1890,
    1891,
    1892,
    1893,
    1894,
    1898,
    1901,
    1902,
    1903,
    1904,
    1905,
    1906,
    1907,
    1908,
    1909,
    1910,
    1911,
    1913,
    1914,
    1915,
    1916,
    1917,
    1918,
    1920,
    1923,
    1924,
    1925,
    1926,
    1927,
    1928,
    1930,
    1931,
    1946,
    1952,
    1954,
    1956,
    1957,
    1958,
    1959,
    1960,
    1961,
    1962,
    1963,
    1966,
    1967,
    1968,
    1969,
    1970,
    1971,
    1972,
    1990,
    1999,
    2019,
    2024,
    2025,
    2026,
    2027,
    2028,
    2029,
    2031,
    2032,
    2033,
    2034,
    2035,
    2036,
    2037,
    2038,
    2046,
    2047,
    2048,
    2049,
    2050,
    2051,
    2052,
    2059,
    2068,
    2071,
    2072,
    2073,
    2074,
    2079,
    2080,
    2081,
    2091,
]

for clf in SongClassification.objects.all():
    if clf.participant not in participants:
        participants.append(clf.participant)
