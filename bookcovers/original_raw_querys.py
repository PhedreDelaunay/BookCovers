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
        """
        lists covers for this artist
        :param artist_id:
        :param return_dict:
        :return:
        """

        #strArtistSQL = "SELECT artists.cover_filepath, covers.*, AW.year " \

        # Original query is displaying correct order by happy accident.
        # Added "AND covers.is_variant = false " to force correct order
        # this is a new column added to get correct order in django query
        # needed here to match order in test
        strArtistSQL = "SELECT covers.book_id, artists.cover_filepath, covers.cover_filename, AW.artwork_id, AW.year " \
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
    def artist_set_list(artist_id, return_dict=False):
        print (f"artist_set_list: artist_id={artist_id}")
        strArtistSetList = ("SELECT sets.*, artists.name FROM sets, artists, authors "
                "WHERE sets.artist_id = %s AND sets.artist_id = artists.artist_id "
                "and sets.author_id = authors.author_id "
                "ORDER BY authors.name")

        #print(f"strArtistSetList is\n{strArtistSetList}\n")
        with connection.cursor() as cursor:
            cursor.execute(strArtistSetList, [artist_id])
            if return_dict:
                set_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                set_list = cursor.fetchall()
            #print(f"Original artist set list is\n{set_list}\n")

        return set_list

    @staticmethod
    def artist_set_cover_list(artist_id, return_dict=False):
        """
        gets all covers in all sets for this artist, ordered by author and volume
        :param artist_id:
        :param return_dict:
        :return:
        """
        #print (f"artist_cover_set_list: artist_id={artist_id}")

        # get all books for sets for an artist, ordered by author and volume
        strArtistSetCovers = ("SELECT artists.cover_filepath, authors.name, BC.*, BSL.volume, sets.author_id "
                              "FROM artists, covers as BC, series as BS, books_series as BSL, sets, artworks as AW, authors "
                              "WHERE (sets.artist_id = %s)"
                              "AND BS.series_id = sets.series_id AND BSL.series_id = BS.series_id "
                              "AND BC.flags < 256  AND BC.is_variant = False AND BC.book_id = BSL.book_id "
                              "AND sets.artist_id = AW.artist_id AND AW.artist_id = artists.artist_id "
                              "AND BC.artwork_id = AW.artwork_id "
                              "AND authors.author_id = sets.author_id "
                              "AND BC.cover_id NOT IN (SELECT BSE.cover_id FROM set_exceptions as BSE WHERE BSE.set_id = sets.set_id) "
                              "ORDER BY authors.name, BSL.volume")

        #print(f"strAASetCovers is\n{strAASetCovers}\n")
        with connection.cursor() as cursor:
            cursor.execute(strArtistSetCovers, [artist_id])
            if return_dict:
                set_cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                set_cover_list = cursor.fetchall()
            #print(f"Original artist set cover list is\n{set_cover_list}\n")

        return set_cover_list

    @staticmethod
    def author_list(return_dict=False):
        """
        list all authors with a book cover to display
        """
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


    @staticmethod
    def author_cover_list(author_id, return_dict=False):
        """
        get all covers of all books by this author
        :param: id of author to fetch book list for
        :param return_dict: True = return results in a dictionary
        :return:
        """

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
    def author_book_list(author_id, return_dict=False):
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

        strAuthorSQL = strAuthorBooksSQL

        print (f"strAuthorBooksSQL is\n{strAuthorBooksSQL}\n")
        with connection.cursor() as cursor:
            cursor.execute(strAuthorSQL, [author_id, author_id])
            if return_dict:
                cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                cover_list = cursor.fetchall()
            print(f"Original author book list is\n{cover_list}\n")

        return cover_list

    @staticmethod
    def author_covers_for_title(book_id, return_dict=False):
        """
        list all covers for this title
        :param book_id:
        :return:
        """
        strAuthorCoverSQL = ("SELECT artists.cover_filepath, AW.artwork_id, BC.*, BE.print_year, C.country_id, C.display_order "
                            "FROM artists, artworks as AW, covers AS BC, editions AS BE, countries AS C "
                            "WHERE BC.flags < 256 AND BC.book_id = %s AND BC.book_id = BE.book_id "
                            "AND BC.edition_id = BE.edition_id "
                            "AND AW.artwork_id = BC.artwork_id AND artists.artist_id = AW.artist_id "
                            "AND C.country_id = BE.country_id "
                            "ORDER BY C.display_order, BE.print_year")

        #print(f"strAuthorCoverSQL is\n{strAuthorCoverSQL}\n")
        with connection.cursor() as cursor:
            cursor.execute(strAuthorCoverSQL, [book_id])
            if return_dict:
                cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                cover_list = cursor.fetchall()
            # print(f"Original book title cover list is\n{cover_list}\n")

        return cover_list

    @staticmethod
    def artwork_cover_list(book_id, artist_id, return_dict=False):
        print (f"artwork_cover_list: book_id={book_id} artist_id={artist_id}")
        strArtworkCoverSQL = ("SELECT artists.cover_filepath, covers. *, artworks.artist_id "
                    "FROM artists, covers, artworks "
                    "WHERE covers.flags < 256 "
                       "AND covers.artwork_id IN (SELECT DISTINCT artwork_id FROM covers WHERE covers.book_id = %s) "
                       "AND ((artworks.artist_id = %s) OR artworks.artist_id IN ("
                            "SELECT AA.artist_aka_id FROM artist_akas AS AA WHERE AA.artist_id = %s)) "
                       "AND artists.artist_id = artworks.artist_id "
                       "AND covers.artwork_id = artworks.artwork_id")

        #print(f"strArtworkCoverSQL is\n{strArtworkCoverSQL}\n")
        with connection.cursor() as cursor:
            cursor.execute(strArtworkCoverSQL, [book_id, artist_id, artist_id])
            if return_dict:
                cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                cover_list = cursor.fetchall()
            print(f"Original artwork cover list is\n{cover_list}\n")

        return cover_list

    @staticmethod
    def author_set_list(author_id, return_dict=False):
        #print (f"author_set_list: author_id={author_id}")
        strAuthorSetList = ("SELECT sets.*, authors.name FROM sets, authors "
                "WHERE sets.author_id = %s AND sets.author_id = authors.author_id")

        #print(f"strAuthorSetList is\n{strAuthorSetList}\n")
        with connection.cursor() as cursor:
            cursor.execute(strAuthorSetList, [author_id])
            if return_dict:
                set_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                set_list = cursor.fetchall()
            #print(f"Original author set list is\n{set_list}\n")

        return set_list

    @staticmethod
    def author_set_cover_list(author_id, return_dict=False):
        """
        gets all covers in all sets for this author, ordered by artist and volume
        :param author_id:
        :param return_dict:
        :return:
        """
        #print (f"author_cover_set_list: author_id={author_id}")

        # get all books for sets for an author, ordered by artist and volume
        strAuthorSetCovers = ("SELECT artists.cover_filepath, BC.*, BSL.volume, sets.artist_id "
                        "FROM artists, covers as BC, series as BS, books_series as BSL, sets, artworks as AW "
                        "WHERE (sets.author_id = %s)"
                        "AND BS.series_id = sets.series_id AND BSL.series_id = BS.series_id "
                        "AND BC.flags < 256  AND BC.is_variant = False AND BC.book_id = BSL.book_id "
                        "AND sets.artist_id = AW.artist_id AND AW.artist_id = artists.artist_id "
                        "AND BC.artwork_id = AW.artwork_id "
                        "AND BC.cover_id NOT IN (SELECT BSE.cover_id FROM set_exceptions as BSE WHERE BSE.set_id = sets.set_id) "
                        "ORDER BY sets.artist_id, BSL.volume")

        #print(f"strAASetCovers is\n{strAASetCovers}\n")
        with connection.cursor() as cursor:
            cursor.execute(strAuthorSetCovers, [author_id])
            if return_dict:
                set_cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                set_cover_list = cursor.fetchall()
            #print(f"Original author/artist set cover list is\n{set_cover_list}\n")

        return set_cover_list

    @staticmethod
    def author_artist_set_cover_list(author_id, artist_id, return_dict=True):
        """
        gets covers from sets for this author and artist
        assumes only 1 set will meet this criteria - which is probably true now but may not always be the case
        :param author_id:
        :param artist_id:
        :param return_dict:
        :return:
        """
        strAASetCovers = ("SELECT artists.cover_filepath, BC.*, BSL.volume, sets.artist_id "
                            "FROM artists, covers as BC, series as BS, books_series as BSL, sets, artworks as AW "
                            "WHERE (sets.author_id = %s) "
                            "AND BS.series_id = sets.series_id AND BSL.series_id = BS.series_id "
                            "AND BC.flags < 256 AND BC.is_variant = false "
                            "AND BC.book_id = BSL.book_id AND AW.artist_id = %s "
                            "AND sets.artist_id = AW.artist_id AND AW.artist_id = artists.artist_id "
                            "AND BC.artwork_id = AW.artwork_id "
                            "AND BC.cover_id NOT IN (SELECT BSE.cover_id FROM set_exceptions as BSE WHERE BSE.set_id = sets.set_id) "
                            "GROUP BY AW.artwork_id "
                            "ORDER BY BSL.volume")

        #print(f"strAASetCovers is\n{strAASetCovers}\n")
        with connection.cursor() as cursor:
            cursor.execute(strAASetCovers, [author_id, artist_id])
            if return_dict:
                set_cover_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                set_cover_list = cursor.fetchall()
            #print(f"Original author/artist set cover list is\n{set_cover_list}\n")

        return set_cover_list

    @staticmethod
    def print_history(print_run_id, return_dict=True):
        """
        gets the print runs for the given print_run_id
        :param print_run_id:
        :param return_dict:
        :return:
        """

        #print (f"print_history: print_run_id={print_run_id}")

        strPrintHistory = ("SELECT BPR.*, BC.cover_filename, artists.cover_filepath "
                            "FROM print_runs AS BPR "
                            "LEFT JOIN covers AS BC ON BPR.cover_id = BC.cover_id "
                            "LEFT JOIN artworks ON BC.artwork_id = artworks.artwork_id "
                            "LEFT JOIN artists on artworks.artist_id = artists.artist_id "
                            "WHERE BPR.print_run_id = %s")

        #print(f"strPrintHistory is\n{strPrintHistory}\n")
        with connection.cursor() as cursor:
            cursor.execute(strPrintHistory, [print_run_id])
            if return_dict:
                print_history = OriginalRawQuerys.dictfetchall(cursor)
            else:
                print_history = cursor.fetchall()
        return print_history

    @staticmethod
    def panorama_list(return_dict=True):
        """
        gets the panoramas
        :param return_dict:
        :return:
        """

        # strPanoramaList = ('SELECT BP.*, '
        #                    'artists.name as artist_name, artists.cover_filepath, authors.name as author_name '
        #                    'FROM panoramas as BP, artists, authors '
        #                    'WHERE BP.artist_id = artists.artist_id AND BP.author_id = authors.author_id '
        #                    'ORDER BY "BP.order"')
        # without quotes around BP.order we get the error
        # "django.db.utils.OperationalError: near "order": syntax error"
        # without quotes around BP.order the results are not ordered - presumably being interpreted as a literal

        strPanoramaList = ('SELECT *, '
                           'artists.name as artist_name, artists.cover_filepath, authors.name as author_name '
                           'FROM panoramas, artists, authors '
                           'WHERE panoramas.artist_id = artists.artist_id AND panoramas.author_id = authors.author_id '
                           'ORDER BY "order"')

        with connection.cursor() as cursor:
            cursor.execute(strPanoramaList)
            if return_dict:
                panoramas = OriginalRawQuerys.dictfetchall(cursor)
            else:
                panoramas = cursor.fetchall()
        return panoramas

    @staticmethod
    def panorama(current_entry, total_entrys, return_dict=True):
        strSQL = ("SELECT *, artists.name, artists.cover_filepath, authors.name "
                "FROM panoramas, artists, authors "
                "WHERE panoramas.artist_id = artists.artist_id AND panoramas.author_id = authors.author_id "
                "ORDER BY \"order\"")

        strPSQL = strSQL + f"LIMIT {current_entry}, {total_entrys}"
        print (f"strPSQL is {strPSQL}")

        with connection.cursor() as cursor:
            cursor.execute(strPSQL)
            if return_dict:
                panorama = OriginalRawQuerys.dictfetchall(cursor)
            else:
                panorama = cursor.fetchall()
        return panorama

    @staticmethod
    def adhoc_query(sql_query, return_dict=False):
        """
        runs an adhoc query without parameters
        :param sql_query:
        :param return_dict:
        :return:
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            if return_dict:
                book_list = OriginalRawQuerys.dictfetchall(cursor)
            else:
                book_list = cursor.fetchall()
            # print(f"Original book title cover list is\n{cover_list}\n")

        return book_list


    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

