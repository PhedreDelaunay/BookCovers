#!/bin/bash

# 24-Mar-2020 fix num pages display and then remove it completely
cp bookcovers/templates/bookcovers/book_detail.html ~/djabbic/bookcovers/templates/bookcovers/
~/init/djabbic restart

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
