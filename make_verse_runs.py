from itertools import count, groupby
import contextlib
import json

import pymysql


SQL_VERSES = """
SELECT `index`
FROM bible_kjv
WHERE `text` LIKE '%wine%'
    OR `text` LIKE '%strong drink%'
    OR `text` LIKE '%drunk%'
"""

SQL_RUNS = """
SELECT books.fullname, bible.chapter, bible.verse, bible.text
FROM bible_books_en books JOIN bible_kjv bible ON books.number = bible.book
WHERE bible.index >= %s AND bible.index <= %s
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
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    # Get the original indexes
    index_set = set()
    with contextlib.closing(connection):
        with connection.cursor() as cursor:
            cursor.execute(SQL_VERSES)
            for result in cursor.fetchall():
                index = result['index']
                # add 3 verses before and 3 verses after for context
                index_set.update(range(index - 3, index + 4))

            verse_runs = []
            for index_start, index_end in make_range_gen(index_set):
                cursor.execute(SQL_RUNS, (index_start, index_end))
                result = cursor.fetchall()

                # Note: I have to be careful with my references because
                # I'm blindly getting the next indexes, which could belong
                # to other books or chapters
                # TODO: make this unneeded
                ref = dict()
                ref['book_start'] = result[0]['fullname']
                ref['book_end'] = result[-1]['fullname']
                ref['chapter_start'] = result[0]['chapter']
                ref['chapter_end'] = result[-1]['chapter']
                ref['verse_start'] = result[0]['verse']
                ref['verse_end'] = result[-1]['verse']
                ref['verses'] = '\n'.join(verse['text'] for verse in result)

                verse_runs.append(ref)

    with open('verse_runs.json', 'w') as output:
        json.dump(verse_runs, output, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
