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
            for result in cursor.fetchall():
                index_set.add(*result)

    # get all verses 3 before and one after for context
    context_set = set()
    for index in index_set:
        context_set.update(range(index - 3, index + 2))

    # now sort that into a list of "runs" of verses
    for index in sorted(context_set):
        print(index, end='')
        if index in index_set:
            print(' *', end='')
        print()

    # Now get the starts and ends of those
    # https://stackoverflow.com/a/10420670/2958070
    def make_inclusive_range(g):
        l = list(g)
        return l[0], l[-1]

    context_list = sorted(context_set)
    index_range_gen = (make_inclusive_range(g) for _, g in
                       groupby(context_list, key=lambda n, c=count(): n - next(c)))

    for index_start, index_end in index_range_gen:
        print(index_start, index_end)


if __name__ == "__main__":
    main()
