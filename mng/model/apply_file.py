import os

from django.shortcuts import get_object_or_404

from mng.models import ApplyFile


def all_files():
    return ApplyFile.objects.all()


def upload_file(name, f):
    file_cnt = ApplyFile.objects.count()
    path = '../../static/doc/%d.%s' % (file_cnt, name.split('.')[1])
    with open(path.replace('../..', 'mng'), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    doc = ApplyFile(name=name, path=path)
    doc.save()


def remove_file(doc_id):
    doc = get_object_or_404(ApplyFile, pk=doc_id)
    path = doc.path
    print(os.path.abspath('.'))
    os.remove((path.replace('../..', 'mng')))
    doc.delete()
