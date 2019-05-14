from django.shortcuts import get_object_or_404

def transform_slug(slug):
    slug = slug.replace('__', '%')
    slug = slug.replace('-', ' ')
    slug = slug.replace('%', '-')

    return slug

def get_subject_record(model, subject_id=None, name=None, slug=None):

    print (f"get_subect_record: subject_id={subject_id} name={name} slug={slug}")
    if subject_id:
        kwargs = {'pk': subject_id}
    elif name:
        kwargs = {'name': name}
    elif slug:
        slug = transform_slug(slug)
        kwargs = {'slug': slug}
    # TODO default or exception if no value supplied

    for key, value in kwargs.items():
        print (f"key {key} is '{value}'")

    record = get_object_or_404(model, **kwargs)
    return record