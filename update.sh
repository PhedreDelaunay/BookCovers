#!/bin/bash
# Remember to collectstatic if changing style.css

# 27-Jul-2020
# display titles in details page in purple
cp bookcovers/static/bookcovers/style.css ~/djabbic/bookcovers/static/bookcovers/
cp bookcovers/templates/bookcovers/book_detail.html ~/djabbic/bookcovers/templates/bookcovers/
cp bookcovers/templates/bookcovers/cover_detail.html ~/djabbic/bookcovers/templates/bookcovers/
cp bookcovers/templates/bookcovers/author_books.html ~/djabbic/bookcovers/templates/bookcovers/
~/init/djabbic restart

# 6-Jul-2020
# display book title from book record in artbook index admin page
#cp bookcovers/admin.py ~/djabbic/bookcovers/

# 31-May-2020
# add navbar 
# tabbed navigation top menu
#cp bookcovers/artist/view_mixin.py ~/djabbic/bookcovers/artist/
#cp bookcovers/author/view_mixin.py ~/djabbic/bookcovers/author/
#cp bookcovers/templates/bookcovers/base.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/index.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/views.py ~/djabbic/bookcovers/
#cp bookcovers/static/bookcovers/style.css ~/djabbic/bookcovers/static/bookcovers/
#cp bookcovers/templates/bookcovers/main_menu.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/subject_list.html ~/djabbic/bookcovers/templates/bookcovers/

# 25-May-2020
# redraw screen for actual browser width to reflow flexible columns 
#cp bookcovers/artist/views.py ~/djabbic/bookcovers/artist/
#cp bookcovers/author/views.py ~/djabbic/bookcovers/author/
#cp bookcovers/base_views.py ~/djabbic/bookcovers/
#cp bookcovers/static/bookcovers/style.css ~/djabbic/bookcovers/static/bookcovers/
#cp bookcovers/templates/bookcovers/subject_list.html ~/djabbic/bookcovers/templates/bookcovers/

# WIP: artbook index
#cp bookcovers/templates/bookcovers/artbook_index.html ~/djabbic/bookcovers/templates/bookcovers/



# 12-May-2020
#cp bookcovers/query_cache.py ~/djabbic/bookcovers/
#cp bookcovers/cover_querys.py ~/djabbic/bookcovers/
#cp bookcovers/debug_helper.py ~/djabbic/bookcovers/
#cp bookcovers/views.py ~/djabbic/bookcovers/
#cp bookcovers/fixtures/ArtbookIndex.json ~/djabbic/bookcovers/
#cp bookcovers/fixtures/Book.json ~/djabbic/bookcovers/
#cp bookcovers/templates/bookcovers/artbook_index.html ~/djabbic/bookcovers/templates/bookcovers/
# don't display pages
#cp bookcovers/templates/bookcovers/book_detail.html ~/djabbic/bookcovers/templates/bookcovers/

# 17-Apr-2020
#cp bookcovers/models.py ~/djabbic/bookcovers/
# add PrintRun to admin
#cp bookcovers/admin.py ~/djabbic/bookcovers/
# make function and template for artist's signature
#cp bookcovers/artist/view_mixin.py ~/djabbic/bookcovers/artist/
#cp bookcovers/artist/views.py ~/djabbic/bookcovers/artist/
#cp bookcovers/templates/bookcovers/artist_artworks.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/artist_sets.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/artist_title.html ~/djabbic/bookcovers/templates/bookcovers/

# 16-Apr-2020
# display artist's signature
#cp bookcovers/artist/views.py ~/djabbic/bookcovers/artist/
#cp bookcovers/templates/bookcovers/artist_artworks.html ~/djabbic/bookcovers/templates/bookcovers/


# 27-Mar-2020
# fix replacing text in evidence when there is no evidence
#cp bookcovers/templatetags/bookcover_tags.py ~/djabbic/bookcovers/templatetags/
 
# 25-Mar-2020
# search in artbook index by artbook title and order by page
#cp bookcovers/models.py ~/djabbic/bookcovers/
#cp bookcovers/admin.py ~/djabbic/bookcovers/
# replace ; with <BR> in evidence with filter in template
#cp bookcovers/templatetags/bookcover_tags.py ~/djabbic/bookcovers/templatetags/bookcover_tags.py
#cp bookcovers/templates/bookcovers/cover_detail.html ~/djabbic/bookcovers/templates/bookcovers/

# 24-Mar-2020 
# fix image not displaying full size when text is long (eg http://www.djabbic.space/bookcovers/artwork/edition/796/ The Darkness on Diamondia
# cp bookcovers/static/bookcovers/style.css ~/djabbic/bookcovers/static/bookcovers/

#fix num pages display and then remove it completely
#cp bookcovers/templates/bookcovers/book_detail.html ~/djabbic/bookcovers/templates/bookcovers/

# 20-Mar-2020
# order artworks by name
#cp bookcovers/models.py ~/djabbic/bookcovers/

# 19-Mar-2020
# fix price display
#cp bookcovers/templates/bookcovers/book_detail.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/base.html ~/djabbic/bookcovers/templates/bookcovers/

# 18-Mar-2020
#cp bookcovers/cover_querys.py ~/djabbic/bookcovers/
#cp bookcovers/templates/bookcovers/artbook_index.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/artbooks.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/urls.py ~/djabbic/bookcovers/
#cp bookcovers/views.py ~/djabbic/bookcovers/

# 13-Mar-2020
# cp bookcovers/templates/bookcovers/print_history.html ~/djabbic/bookcovers/templates/bookcovers/
# cp bookcovers/cover_querys.py ~/djabbic/bookcovers/
#cp bookcovers/templates/bookcovers/book_list.html ~/djabbic/bookcovers/templates/bookcovers/
#cp bookcovers/templates/bookcovers/thumbnail_list.html ~/djabbic/bookcovers/templates/bookcovers/

# 12/13-Mar-2020
# cp bookcovers/templates/bookcovers/print_history.html ~/djabbic/bookcovers/templates/bookcovers/

# 11-Mar-2020
# Views: Add template for index and remove link to home from main menu as no value at the moment"
# cp bookcovers/templates/bookcovers/index.html ~/djabbic/bookcovers/templates/bookcovers/
# cp bookcovers/templates/bookcovers/main_menu.html ~/djabbic/bookcovers/templates/bookcovers/
# cp bookcovers/views.py ~/djabbic/bookcovers/
 
# Models: Order artbooks by title
# Models: correct ordering applied to ArtbookIndex instead of Artbook
# cp bookcovers/models.py ~/djabbic/bookcovers/

# Models: Owned model is named purchases_owned in db 
# NOT COPIED yet cos not dealing with purchases
# cp purchases/models.py ~/djabbic/purchases/

# 10-Mar-2020
#cp bookcovers/admin.py ~/djabbic/bookcovers/
#cp bookcovers/cover_querys.py ~/djabbic/bookcovers/
#cp bookcovers/tests/test_images.py ~/djabbic/bookcovers/
#cp bookcovers/tests/test_pagers.py ~/djabbic/bookcovers/
#cp bookcovers/tests/test_pages.py ~/djabbic/bookcovers/
#cp bookcovers/tests/test_queries.py ~/djabbic/bookcovers/
#cp bookcovers/fixtures/* ~/djabbic/bookcovers/fixtures


# ~/init/djabbic restart
# ~/init/nginx restart	
