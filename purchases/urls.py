from django.urls import path

from purchases.views import OwnedList
from purchases.views import OwnedAlphaList

# Reference:
# https://docs.djangoproject.com/en/2.1/topics/http/urls/

# Namespacing url names
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
# this is how Django knows which app view to create for a url when using the {% url %} template tag
# to point at the namespaced  view <a href="{% url 'bookcovers:view path name' question.id %}">
app_name = 'purchases'
urlpatterns = [
    # ex: /purchases/owned/
    path('owned/', OwnedList.as_view(), name='owned'),
    # ex /purchases/owned/A/
    path('owned/<letter>/', OwnedAlphaList.as_view(), name='owned_alpha'),
]

