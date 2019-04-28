# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
# remember to restart dev server when adding a new tag
from django import template
from django.urls import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

# "assignment" tag - set a variable in the context
# usage:
# {% set "False" as break %}
# {% set "True" as break %}
# {% if break == "False" %}
@register.simple_tag
def set(value):
    return value

# renders the edition line for print history
# usage:
# {{ cover.print|edition:cover.edition_id }}
@register.filter(needs_autoescape=True)
def edition(text, edition_id, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    if edition_id:
        reverse_url = reverse('bookcovers:book_edition', kwargs={'edition_id': edition_id})
        render_string = "<a href=\"" + reverse_url + "\">" + esc(text) + "</a>"
    else:
        render_string = esc(text)
    return mark_safe(render_string)
