#!/bin/bash
# Remember to collectstatic if changing style.css

# 25-Apr-2021
cp bookcovers/templates/bookcovers/cover_detail.html ~/djabbic/bookcovers/templates/bookcovers/
 ~/init/djabbic restart
 ~/init/nginx restart	

