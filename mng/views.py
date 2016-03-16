import calendar
import logging
import math
import os
from datetime import date, timedelta

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from bck.backup_util import backup_db
from mng.export import export_xls
from mng.models import Apply, KV, Notice, ApplyFile

logger = logging.getLogger(__name__)


def index(request):
    context = {}
    return render(request, 'mng/index.html', context)


def apply(request):
    context = {}
    return render(request, 'mng/apply.html', context)


# def view(request, year, month, day):
#     context = {'year': year, 'month': month, 'day': day}
#     return render(request, 'mng/view.html', context)


def faq(request):
    context = {}
    return render(request, 'mng/faq.html', context)


def download(request):
    docs = ApplyFile.objects.all()
    context = {'docs': docs}
    return render(request, 'mng/download.html', context)


def publish(request):
    context = {}
    return render(request, 'mng/publish.html', context)


def setting(request):
    settings = KV.objects
    zero_year = 2016
    zero_month = 2
    zero_day = 28
    desk_max = 20
    tent_max = 20
    umbrella_max = 15
    red_max = 5
    cloth_max = 5
    loud_max = 2
    sound_max = 1
    projector_max = 1

    if settings.count() <= 0:
        zero_year_set = KV(set_key='zero_year', set_value=zero_year)
        zero_year_set.save()
        zero_month_set = KV(set_key='zero_month', set_value=zero_month)
        zero_month_set.save()
        zero_day_set = KV(set_key='zero_day', set_value=zero_day)
        zero_day_set.save()
        desk_set = KV(set_key='desk_max', set_value=desk_max)
        desk_set.save()
        tent_set = KV(set_key='tent_max', set_value=tent_max)
        tent_set.save()
        red_set = KV(set_key='red_max', set_value=red_max)
        red_set.save()
        cloth_set = KV(set_key='cloth_max', set_value=cloth_max)
        cloth_set.save()
        umbrella_set = KV(set_key='umbrella_max', set_value=umbrella_max)
        umbrella_set.save()
        loud_set = KV(set_key='loud_max', set_value=loud_max)
        loud_set.save()
        sound_set = KV(set_key='sound_max', set_value=sound_max)
        sound_set.save()
        projector_set = KV(set_key='projector_max', set_value=projector_max)
        projector_set.save()
        settings = KV.objects

    zero_year = settings.filter(set_key='zero_year').first().set_value
    zero_month = settings.filter(set_key='zero_month').first().set_value
    zero_day = settings.filter(set_key='zero_day').first().set_value
    desk_max = settings.filter(set_key='desk_max').first().set_value
    tent_max = settings.filter(set_key='tent_max').first().set_value
    umbrella_max = settings.filter(set_key='umbrella_max').first().set_value
    red_max = settings.filter(set_key='red_max').first().set_value
    cloth_max = settings.filter(set_key='cloth_max').first().set_value
    loud_max = settings.filter(set_key='loud_max').first().set_value
    sound_max = settings.filter(set_key='sound_max').first().set_value
    projector_max = settings.filter(set_key='projector_max').first().set_value
    context = {
        'zero_year': zero_year,
        'zero_month': zero_month,
        'zero_day': zero_day,
        'desk_max': desk_max,
        'tent_max': tent_max,
        'umbrella_max': umbrella_max,
        'red_max': red_max,
        'cloth_max': cloth_max,
        'loud_max': loud_max,
        'sound_max': sound_max,
        'projector_max': projector_max,
    }
    print(context)
    return render(request, "mng/setting.html", context)


def check_info(material_num, material_name, apply_dates):
    invalid_apply = []
    if material_num > 0:
        if material_name == 'projector':
            max_name = 'projector_max'
        else:
            max_name = material_name.replace('_num', '_max')
        material_max = KV.objects.filter(set_key=max_name).first().set_value
        for apply_date in apply_dates:
            cur_sum = Apply.objects.filter(rap__year=apply_date.year, rap__month=apply_date.month, rap__day=apply_date
                                           .day).aggregate(Sum(material_name))[material_name + '__sum']
            if cur_sum is None:
                cur_sum = 0
            if cur_sum + material_num > int(material_max):
                if material_name == 'desk_num':
                    invalid_name = '桌子'
                elif material_name == 'tent_num':
                    invalid_name = '帐篷'
                elif material_name == 'umbrella_num':
                    invalid_name = '雨伞'
                elif material_name == 'red_num':
                    invalid_name = '红布'
                elif material_name == 'cloth_num':
                    invalid_name = '展架'
                elif material_name == 'loud_num':
                    invalid_name = '扩音器'
                elif material_name == 'sound_num':
                    invalid_name = '音响'
                elif material_name == 'projector':
                    invalid_name = '投影仪'
                else:
                    invalid_name = 'ERROR'
                invalid = [invalid_name, material_num, int(material_max) - cur_sum,
                           str(apply_date.year) + '年' + str(apply_date.month) + '月' + str(apply_date.day) + '日']
                invalid_apply.append(invalid)
    return invalid_apply


def check_apply_info(desk_num, tent_num, umbrella_num, red_num, cloth_num, loud_num, sound_num, projector, apply_dates):
    invalid_applies = []
    invalid_applies.extend(check_info(desk_num, 'desk_num', apply_dates))
    invalid_applies.extend(check_info(tent_num, 'tent_num', apply_dates))
    invalid_applies.extend(check_info(umbrella_num, 'umbrella_num', apply_dates))
    invalid_applies.extend(check_info(red_num, 'red_num', apply_dates))
    invalid_applies.extend(check_info(cloth_num, 'cloth_num', apply_dates))
    invalid_applies.extend(check_info(loud_num, 'loud_num', apply_dates))
    invalid_applies.extend(check_info(sound_num, 'sound_num', apply_dates))
    invalid_applies.extend(check_info(projector, 'projector', apply_dates))
    return invalid_applies


def save_apply(request):
    act_name = request.POST['act_name']
    applicant = request.POST['applicant']
    apply_org = request.POST['apply_org']
    tel = request.POST['tel']
    assistant = request.POST['assistant']

    chair_num = request.POST['chair_num']
    desk_num = request.POST['desk_num']
    tent_num = request.POST['tent_num']
    umbrella_num = request.POST['umbrella_num']
    red_num = request.POST['red_num']
    cloth_num = request.POST['cloth_num']
    loud_num = request.POST['loud_num']
    sound_num = request.POST['sound_num']
    projector = request.POST['projector']

    start_year = request.POST['start_year']
    start_month = request.POST['start_month']
    start_day = request.POST['start_day']

    end_year = request.POST['end_year']
    end_month = request.POST['end_month']
    end_day = request.POST['end_day']

    start_week = request.POST['start_week']
    end_week = request.POST['end_week']
    week_num = request.POST['week_num']

    param_size = len(request.POST)
    li_count = math.floor((param_size - 24) / 3)
    apply_dates = []
    invalid_li_count = 0

    for i in range(li_count):
        if request.POST['li_year_%d' % i] == '' or request.POST['li_month_%d' % i] == '' \
                or request.POST['li_day_%d' % i] == '':
            invalid_li_count += 1
            continue
        apply_dates.append(date(int(request.POST['li_year_%d' % i]), int(request.POST['li_month_%d' % i]),
                                int(request.POST['li_day_%d' % i])))
    li_count -= invalid_li_count

    if start_year != '' and start_month != '':
        start_date = date(int(start_year), int(start_month), int(start_day))
        end_date = date(int(end_year), int(end_month), int(end_day))

        for i in range((end_date - start_date).days + 1):
            cur_date = start_date + timedelta(days=i)
            apply_dates.append(cur_date)

    zero_week_year = int(KV.objects.filter(set_key='zero_year').first().set_value)
    zero_week_month = int(KV.objects.filter(set_key='zero_month').first().set_value)
    zero_week_day = int(KV.objects.filter(set_key='zero_day').first().set_value)
    if start_week != '':
        start_week = int(start_week)
        end_week = int(end_week)
        week_num = int(week_num)
        for i in range(end_week - start_week + 1):
            cur_date = date(zero_week_year, zero_week_month, zero_week_day) \
                       + timedelta(weeks=start_week + i - 1, days=week_num - 1)
            apply_dates.append(cur_date)

    invalid_applies = check_apply_info(int(desk_num), int(tent_num), int(umbrella_num),
                                       int(red_num), int(cloth_num), int(loud_num),
                                       int(sound_num), int(projector), apply_dates)
    if len(invalid_applies) <= 0:
        apply_rcd = Apply(act_name=act_name, applicant=applicant, apply_org=apply_org, tel=tel, assistant=assistant,
                          char_num=chair_num, desk_num=desk_num, tent_num=tent_num, umbrella_num=umbrella_num,
                          red_num=red_num, cloth_num=cloth_num, loud_num=loud_num, sound_num=sound_num,
                          projector=projector)
        apply_rcd.save()
        for i in range(len(apply_dates)):
            apply_rcd.rap.create(year=apply_dates[i].year, month=apply_dates[i].month, day=apply_dates[i].day)

        return apply_success(request, apply_rcd.id)
    else:
        return render(request, 'mng/apply_failed.html', {'fails': invalid_applies})


def save_modify(request, apply_id):
    act_name = request.POST['act_name']
    applicant = request.POST['applicant']
    apply_org = request.POST['apply_org']
    tel = request.POST['tel']
    assistant = request.POST['assistant']

    chair_num = request.POST['chair_num']
    desk_num = request.POST['desk_num']
    tent_num = request.POST['tent_num']
    umbrella_num = request.POST['umbrella_num']
    red_num = request.POST['red_num']
    cloth_num = request.POST['cloth_num']
    loud_num = request.POST['loud_num']
    sound_num = request.POST['sound_num']
    projector = request.POST['projector']

    param_size = len(request.POST)
    li_count = math.floor((param_size - 15) / 3)
    apply_dates = []
    invalid_li_count = 0

    for i in range(li_count):
        if request.POST['li_year_%d' % i] == '' or request.POST['li_month_%d' % i] == '' \
                or request.POST['li_day_%d' % i] == '':
            invalid_li_count += 1
            continue
        apply_dates.append(date(int(request.POST['li_year_%d' % i]), int(request.POST['li_month_%d' % i]),
                                int(request.POST['li_day_%d' % i])))
    li_count -= invalid_li_count

    apply_rcd = get_object_or_404(Apply, pk=apply_id)
    invalid_applies = check_apply_info(int(desk_num) - int(apply_rcd.desk_num), int(tent_num) - int(apply_rcd.tent_num),
                                       int(umbrella_num) - int(apply_rcd.umbrella_num),
                                       int(red_num) - int(apply_rcd.red_num), int(cloth_num) - int(apply_rcd.cloth_num),
                                       int(loud_num) - int(apply_rcd.loud_num),
                                       int(sound_num) - int(apply_rcd.sound_num),
                                       int(projector) - int(apply_rcd.projector), apply_dates)
    if len(invalid_applies) <= 0:
        apply_rcd.act_name = act_name
        apply_rcd.applicant = applicant
        apply_rcd.tel = tel
        apply_rcd.apply_org = apply_org
        apply_rcd.assistant = assistant
        apply_rcd.char_num = chair_num
        apply_rcd.desk_num = desk_num
        apply_rcd.tent_num = tent_num
        apply_rcd.umbrella_num = umbrella_num
        apply_rcd.red_num = red_num
        apply_rcd.cloth_num = cloth_num
        apply_rcd.loud_num = loud_num
        apply_rcd.sound_num = sound_num
        apply_rcd.projector = projector
        apply_rcd.rap.all().delete()
        for i in range(len(apply_dates)):
            apply_rcd.rap.create(year=apply_dates[i].year, month=apply_dates[i].month, day=apply_dates[i].day)
        apply_rcd.save()

        return apply_success(request, apply_rcd.id)
    else:
        return render(request, 'mng/apply_failed.html', {'fails': invalid_applies})


def save_notice(request):
    notice_content = request.POST['content']
    notice = Notice(content=notice_content)
    notice.save()

    return HttpResponse("<script>alert(\"发布成功，请在右侧通知栏查看\");location.href=\"../publish\"</script>")


def remove_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    notice.delete()
    return get_notice(request, 1)


def modify_notice(request, notice_id):
    content = request.POST['content']
    Notice.objects.filter(pk=notice_id).update(content=content)
    return get_notice(request, 1)


def get_notice(request, page_num):
    notices = Notice.objects.order_by("-id")
    if notices.count() <= 0:
        return HttpResponse("暂时没有通知")
    limit = 5
    paginator = Paginator(notices, limit)
    page = page_num
    try:
        notice_pages = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        notice_pages = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        notice_pages = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'mng/notice.html', {'notice_pages': notice_pages})


def apply_success(request, apply_id):
    return render(request, 'mng/apply_success.html', {'apply_id': apply_id})


def apply_modify(request, apply_id):
    apply_rcd = get_object_or_404(Apply, pk=apply_id)
    return render(request, 'mng/apply_modify.html', {'apply': apply_rcd})


def apply_remove(request, apply_id):
    apply_rcd = get_object_or_404(Apply, pk=apply_id)
    apply_rcd.delete()
    today = date.today()
    return HttpResponse("<script>alert(\"已删除\");"
                        "location.href=\"../../" + str(today.year) + "/" + str(today.month) + "/" + str(
        today.day) + "/" + "view\";</script>")


def save_setting(request):
    zero_year = request.POST['zero_year']
    zero_month = request.POST['zero_month']
    zero_day = request.POST['zero_day']
    desk_max = request.POST['desk_max']
    tent_max = request.POST['tent_max']
    umbrella_max = request.POST['umbrella_max']
    red_max = request.POST['red_max']
    cloth_max = request.POST['cloth_max']
    loud_max = request.POST['loud_max']
    sound_max = request.POST['sound_max']
    projector_max = request.POST['projector_max']

    KV.objects.filter(set_key='zero_year').update(set_value=zero_year)
    KV.objects.filter(set_key='zero_month').update(set_value=zero_month)
    KV.objects.filter(set_key='zero_day').update(set_value=zero_day)
    KV.objects.filter(set_key='desk_max').update(set_value=desk_max)
    KV.objects.filter(set_key='tent_max').update(set_value=tent_max)
    KV.objects.filter(set_key='umbrella_max').update(set_value=umbrella_max)
    KV.objects.filter(set_key='red_max').update(set_value=red_max)
    KV.objects.filter(set_key='cloth_max').update(set_value=cloth_max)
    KV.objects.filter(set_key='loud_max').update(set_value=loud_max)
    KV.objects.filter(set_key='sound_max').update(set_value=sound_max)
    KV.objects.filter(set_key='projector_max').update(set_value=projector_max)

    return setting(request)


def gen_calendar(year, month):
    month_first = date(year, month, 1)
    calendar_first = month_first - timedelta(days=month_first.weekday())
    calendar_dates = []

    for i in range(6):
        week_dates = []
        for j in range(7):
            week_date = calendar_first + timedelta(days=j + i * 7)
            date_items = [week_date.year, week_date.month, week_date.day]
            week_dates.append(date_items)

        calendar_dates.append(week_dates)

    return calendar_dates


def add_months(source_date, months):
    month = int(source_date.month) - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def view(request, year, month, day):
    applies = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day)
    chair_left = '不限'
    chair_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('char_num'))['char_num__sum']
    if chair_sum is None:
        chair_sum = 0
    desk_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('desk_num'))['desk_num__sum']
    if desk_sum is None:
        desk_sum = 0
    desk_sum = int(desk_sum)
    desk_max = int(KV.objects.filter(set_key='desk_max').first().set_value)
    desk_left = desk_max - desk_sum

    tent_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('tent_num'))['tent_num__sum']
    if tent_sum is None:
        tent_sum = 0
    tent_sum = tent_sum
    tent_max = int(KV.objects.filter(set_key='tent_max').first().set_value)
    tent_left = tent_max - tent_sum

    umbrella_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('umbrella_num'))['umbrella_num__sum']
    if umbrella_sum is None:
        umbrella_sum = 0
    umbrella_sum = int(umbrella_sum)
    umbrella_max = int(KV.objects.filter(set_key='umbrella_max').first().set_value)
    umbrella_left = umbrella_max - umbrella_sum

    red_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('red_num'))['red_num__sum']
    if red_sum is None:
        red_sum = 0
    red_sum = int(red_sum)
    red_max = int(KV.objects.filter(set_key='red_max').first().set_value)
    red_left = red_max - red_sum

    cloth_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('cloth_num'))['cloth_num__sum']
    if cloth_sum is None:
        cloth_sum = 0
    cloth_sum = int(cloth_sum)
    cloth_max = int(KV.objects.filter(set_key='cloth_max').first().set_value)
    cloth_left = cloth_max - cloth_sum

    loud_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('loud_num'))['loud_num__sum']
    if loud_sum is None:
        loud_sum = 0
    loud_sum = int(loud_sum)
    loud_max = int(KV.objects.filter(set_key='loud_max').first().set_value)
    loud_left = loud_max - loud_sum

    sound_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('sound_num'))['sound_num__sum']
    if sound_sum is None:
        sound_sum = 0
    sound_sum = int(sound_sum)
    sound_max = int(KV.objects.filter(set_key='sound_max').first().set_value)
    sound_left = sound_max - sound_sum

    projector_sum = Apply.objects.filter(rap__year=year, rap__month=month, rap__day=day) \
        .aggregate(Sum('projector'))['projector__sum']
    if projector_sum is None:
        projector_sum = 0
    projector_sum = int(projector_sum)
    projector_max = int(KV.objects.filter(set_key='projector_max').first().set_value)
    projector_left = projector_max - projector_sum

    previous_month_date = add_months(date(int(year), int(month), int(day)), -1)
    next_month_date = add_months(date(int(year), int(month), int(day)), 1)
    context = {'cur_year': year, 'cur_month': month, 'cur_day': day,
               'dates': gen_calendar(int(year), int(month)),
               'applies': applies, 'apply_cnt': len(applies),
               'pre_year': previous_month_date.year, 'pre_month': previous_month_date.month,
               'next_year': next_month_date.year, 'next_month': next_month_date.month,
               'chair_sum': chair_sum, 'chair_left': chair_left,
               'desk_sum': desk_sum, 'desk_left': desk_left,
               'tent_sum': tent_sum, 'tent_left': tent_left,
               'umbrella_sum': umbrella_sum, 'umbrella_left': umbrella_left,
               'red_sum': red_sum, 'red_left': red_left,
               'cloth_sum': cloth_sum, 'cloth_left': cloth_left,
               'loud_sum': loud_sum, 'loud_left': loud_left,
               'sound_sum': sound_sum, 'sound_left': sound_left,
               'project_sum': projector_sum, 'projector_left': projector_left
               }
    return render(request, 'mng/view.html', context)


def backup(request):
    backup_db()
    return HttpResponse("success")


def export(request):
    start_year = int(request.POST['start_year'])
    start_month = int(request.POST['start_month'])
    start_day = int(request.POST['start_day'])

    end_year = int(request.POST['end_year'])
    end_month = int(request.POST['end_month'])
    end_day = int(request.POST['end_day'])

    return export_xls(date(start_year, start_month, start_day), date(end_year, end_month, end_day))


def export_html(request):
    return render(request, 'mng/export.html', {})


def upload(request):
    name = request.POST['name']
    path = '../../static/doc/%s' % name

    f = request.FILES['file']
    with open('mng/' + path.replace('../../', ''), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    docs = ApplyFile.objects.all()

    doc = ApplyFile(name=name, path=path)
    doc.save()
    return render(request, 'mng/download.html', {'docs': docs})


def rm_doc(request, doc_id):
    doc = get_object_or_404(ApplyFile, pk=doc_id)
    path = doc.path
    os.remove('mng/' + path.replace('../../', ''))
    doc.delete()
    docs = ApplyFile.objects.all()
    return render(request, 'mng/download.html', {'docs': docs})
