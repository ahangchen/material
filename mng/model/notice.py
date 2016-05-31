from django.shortcuts import get_object_or_404

from mng.models import Notice


def insert_notice(notice_content):
    notice = Notice(content=notice_content)
    notice.save()


def delete_notice(notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    notice.delete()


def update_notice(notice_id, content):
    Notice.objects.filter(pk=notice_id).update(content=content)


def latest_notices():
    return Notice.objects.order_by("-id")