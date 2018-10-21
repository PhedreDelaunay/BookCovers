from django.db import connection

# https://docs.djangoproject.com/en/2.1/topics/db/sql/

class OriginalRawQuerys:

    @staticmethod
    def artist_list(return_dict=False):
        strCoverArtistsSQL = "SELECT A.artist_id, A.name, AW.artist_id from artists as A, artworks as AW " \
        "WHERE A.artist_id = AW.artist_id " \
        "AND AW.artwork_id IN " \
        "(SELECT BC.artwork_id FROM covers as BC " \
        "WHERE BC.artwork_id = AW.artwork_id AND BC.flags < 256) " \
        "group by A.name"

        with connection.cursor() as cursor:
            cursor.execute(strCoverArtistsSQL)
            if return_dict:
                artist_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                artist_list = cursor.fetchall()

        # print (artist_list)

        return artist_list

    @staticmethod
    def artist_cover_list(artist_id, return_dict=False):

        #strArtistSQL = "SELECT artists.cover_filepath, covers.*, AW.year " \

        # Original query is displaying correct order by happy accident.
        # Added "AND covers.is_variant = false " to force correct order
        # this is a new column added to get correct order in django query
        # needed here to match order in test
        strArtistSQL = "SELECT covers.book_id, artists.cover_filepath, covers.cover_filename, AW.year " \
                "FROM artists, covers, artworks as AW " \
                "WHERE ((AW.artist_id = %s) OR " \
                "AW.artist_id IN (SELECT AA.artist_aka_id FROM artist_akas as AA WHERE AA.artist_id = %s)) " \
                "AND artists.artist_id = AW.artist_id " \
                "AND covers.artwork_id = AW.artwork_id " \
                "AND covers.flags < 256 " \
                "AND covers.is_variant = false " \
                "GROUP BY AW.artwork_id " \
                "ORDER by AW.year ASC, AW.artwork_id"


        print (strArtistSQL)
        print ("\n")
        with connection.cursor() as cursor:
            cursor.execute(strArtistSQL, [artist_id, artist_id])
            if return_dict:
                cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                cover_list = cursor.fetchall()
            print(f"Original artist cover list is\n{cover_list}\n")

        return cover_list

    @staticmethod
    def author_list(return_dict=False):
 
        strCoverAuthorsSQL = "SELECT A.author_id, A.name, B.book_id, B.author_id, BE.book_id, BE.edition_id " \
                        "FROM authors As A, books AS B, editions AS BE " \
                        "WHERE A.author_id = B.author_id AND B.book_id = BE.book_id " \
                        "AND BE.edition_id IN " \
                        "(SELECT BC.edition_id FROM covers as BC " \
                            "WHERE BC.edition_id = BE.edition_id And BC.flags < 256) " \
                        "group by A.name"

        with connection.cursor() as cursor:
            cursor.execute(strCoverAuthorsSQL)
            if return_dict:
                author_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                author_list = cursor.fetchall()

        print (author_list)

        return author_list



    def author_cover_list(author_id, return_dict=False):
        """
        get all books by this author
        :param: id of author to fetch book list for
        :param return_dict: True = return results in a dictionary
        :return:
        """

        # get all books by this author
        strAuthorBooksSQL = ("SELECT artists.cover_filepath, BC.*, books.book_id, books.author_id, books.copyright_year,"
                             "authors.author_id, BE.edition_id, AW.artist_id, AW.year "
                "FROM artists, covers as BC, books, authors, editions as BE, artworks as AW "
                "WHERE ((authors.author_id = %s) OR "
                    "authors.author_id IN "
                    "(SELECT AA.author_aka_id FROM author_akas as AA WHERE AA.author_id = %s)) "
                "AND books.author_id = authors.author_id AND BC.book_id = books.book_id "
                "AND BE.edition_id = BC.edition_id "
                "AND AW.artwork_id = BC.artwork_id "
                "AND artists.artist_id = AW.artist_id "
                "AND BC.flags < 256 "
                "GROUP BY books.book_id "
                "ORDER BY books.copyright_year, books.book_id, AW.year")

        # get all covers of all books by this author
        strAuthorCoversSQL = ("SELECT artists.cover_filepath, BC.*, books.book_id, books.author_id, books.copyright_year, "
                            "authors.name, BE.edition_id, AW.artwork_id, AW.year "
                        "FROM artists, covers as BC, books, authors, editions as BE, artworks as AW "
                        "WHERE ((authors.author_id = %s) OR "
                                "authors.author_id IN "
                                "(SELECT AA.author_aka_id FROM author_akas as AA WHERE AA.author_id = %s)) "
                        "AND books.author_id = authors.author_id AND BC.book_id = books.book_id "
                        "AND BE.edition_id = BC.edition_id "
                        "AND AW.artwork_id = BC.artwork_id "
                        "AND artists.artist_id = AW.artist_id "
                        "AND BC.flags < 256 "
                        "ORDER BY books.copyright_year, books.book_id, AW.year")

        strAuthorSQL = strAuthorCoversSQL


        print (f"strAuthorSQL is\n{strAuthorSQL}\n")
        with connection.cursor() as cursor:
            cursor.execute(strAuthorSQL, [author_id, author_id])
            if return_dict:
                cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                cover_list = cursor.fetchall()
            # print(f"Original author cover list is\n{cover_list}\n")

        return cover_list

    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
