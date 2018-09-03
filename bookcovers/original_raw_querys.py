from django.db import connection


import math

class OriginalRawQuerys:

    def artist_cover_list(artist_id):

        #strArtistSQL = "SELECT artists.cover_filepath, covers.*, AW.year " \
        strArtistSQL = "SELECT covers.book_id, artists.cover_filepath, covers.cover_filename, AW.year " \
                "FROM artists, covers, artworks as AW " \
                "WHERE ((AW.artist_id = %s) OR " \
                "AW.artist_id IN (SELECT AA.artist_aka_id FROM artist_akas as AA WHERE AA.artist_id = %s)) " \
                "AND artists.artist_id = AW.artist_id " \
                "AND covers.artwork_id = AW.artwork_id " \
                "AND covers.flags < 256 " \
                "GROUP BY AW.artwork_id " \
                "ORDER by AW.year ASC, AW.artwork_id"


        with connection.cursor() as cursor:
            cursor.execute(strArtistSQL, [artist_id, artist_id])
            cover_list = cursor.fetchall()

        print (cover_list)
        print ("\n")

        return cover_list

    def author_list():
 
        #strCoverAuthorsSQL = "SELECT A.author_id, A.name, B.book_id, B.author_id, BE.book_id, BE.edition_id " \
        strCoverAuthorsSQL = "SELECT A.author_id, A.name " \
                        "from authors As A, books AS B, editions AS BE " \
                        "WHERE A.author_id = B.author_id AND B.book_id = BE.book_id " \
                        "AND BE.edition_id IN " \
                        "(SELECT BC.edition_id FROM covers as BC " \
                            "WHERE BC.edition_id = BE.edition_id And BC.flags < 256) " \
                        "group by A.name"

        with connection.cursor() as cursor:
            cursor.execute(strCoverAuthorsSQL)
            author_list = cursor.fetchall()

        print (author_list)

        return author_list



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
