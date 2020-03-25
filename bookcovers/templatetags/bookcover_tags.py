# https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/
# https://stackoverflow.com/questions/5586774/django-template-filters-tags-simple-tags-and-inclusion-tags
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
@register.filter()
def edition(text, edition_id):
    if edition_id:
        reverse_url = reverse('bookcovers:book_edition', kwargs={'edition_id': edition_id})
        render_string = "<a href=\"" + reverse_url + "\">" + text + "</a>"
    else:
        render_string = text
    return mark_safe(render_string)

@register.filter(ineeds_autoescape=True)
def evidence(text):
    the_evidence = text.replace(";", ",<BR>")
    return mark_safe(the_evidence)

# @register.filter(needs_autoescape=True)
# def edition(text, edition_id, autoescape=True):
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#
#     if edition_id:
#         reverse_url = reverse('bookcovers:book_edition', kwargs={'edition_id': edition_id})
#         # TODO some entries have <I></I>, either don't escape or remove html from DB
#         render_string = "<a href=\"" + reverse_url + "\">" + esc(text) + "</a>"
#     else:
#         render_string = esc(text)
#     return mark_safe(render_string)


@register.filter()
def hascover(edition):
    return hasattr(edition, 'theCover')

@register.filter()
def hasprintrun(edition):
    return hasattr(edition, 'thePrintRun')

@register.filter()
def hasfullcover(cover):
    return cover.flags & 0b1