from itertools import count, groupby
import contextlib
# import json

import pymysql


SQL_VERSES = """
SELECT `index`
FROM bible_kjv
WHERE `text` LIKE '%wine%'
    OR `text` LIKE '%strong drink%'
    OR `text` LIKE '%drunk%'
"""


def make_range_gen(iterable):
    l = sorted(iterable)

    # Now get the starts and ends of those
    # https://stackoverflow.com/a/10420670/2958070
    def make_inclusive_range(g):
        l = list(g)
        return l[0], l[-1]

    index_range_gen = (make_inclusive_range(g) for _, g in
                       groupby(l, key=lambda n, c=count(): n - next(c)))
    return index_range_gen


def main():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 # password='passwd',
                                 db='bible_kjv',
                                 charset='utf8mb4')

    # Get the original indexes
    index_set = set()
    with contextlib.closing(connection):
        with connection.cursor() as cursor:
            cursor.execute(SQL_VERSES)
            for (index, ) in cursor.fetchall():
                index_set.update(range(index - 3, index + 2))

    for index_start, index_end in make_range_gen(index_set):
        print(index_start, index_end)


if __name__ == "__main__":
    main()
