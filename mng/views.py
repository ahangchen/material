import logging
import math
from datetime import date, timedelta, datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from bck.backup_util import backup_db
from mng.export import export_xls
from mng.model.apply import insert_apply, modify_apply, remove_apply, query_when, async_apply, async_modify, \
    async_rm_apply
from mng.model.apply_file import all_files, upload_file, remove_file
from mng.model.notice import insert_notice, delete_notice, update_notice, latest_notices
from mng.model.sysset import kvs, zero_date, save_settings
from mng.models import Apply
from mng.utils.js import script
from mng.utils.sync import run_in_background

logger = logging.getLogger(__name__)


def index(request):
    context = {}
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/index.html', context)


def apply(request):
    context = {}
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/apply.html', context)


def faq(request):
    context = {}
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/faq.html', context)


def download(request):
    docs = all_files()
    context = {'docs': docs}
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/download.html', context)


def publish(request):
    context = {}
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/publish.html', context)


def setting(request):
    context = kvs()
    print(context)
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, "mng/setting.html", context)


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

    zero_week_year, zero_week_month, zero_week_day = zero_date()
    if start_week != '':
        start_week = int(start_week)
        end_week = int(end_week)
        week_num = int(week_num)
        for i in range(end_week - start_week + 1):
            cur_date = date(zero_week_year, zero_week_month, zero_week_day) \
                       + timedelta(weeks=start_week + i - 1, days=week_num - 1)
            apply_dates.append(cur_date)

    apply_id, ret, invalid_applies = insert_apply(act_name, applicant, apply_org, tent_num, tel, assistant,
                                                  desk_num, chair_num, umbrella_num, red_num, cloth_num, loud_num,
                                                  sound_num, projector, apply_dates)
    async_apply(act_name, applicant, tel, apply_org,
                      start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, red_num)
    if ret:
        return apply_success(request, apply_id)
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

    invalids = modify_apply(apply_id, act_name, applicant, apply_org, tent_num, tel, assistant,
                            desk_num, chair_num, umbrella_num, red_num, cloth_num, loud_num, sound_num, projector,
                            apply_dates)
    start_date = apply_dates[0]
    end_date = apply_dates[-1]
    start_year = start_date.year
    start_month = start_date.month
    start_day = start_date.day
    end_year = end_date.year
    end_month = end_date.month
    end_day = end_date.day
    if len(invalids) <= 0:
        async_modify(act_name, applicant, tel, apply_org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, red_num)
        return apply_success(request, apply_id)
    else:
        return render(request, 'mng/apply_failed.html', {'fails': invalids})


def save_notice(request):
    notice_content = request.POST['content']
    insert_notice(notice_content)
    return HttpResponse("<script>alert(\"发布成功，请在右侧通知栏查看\");location.href=\"../publish\"</script>")


def remove_notice(request, notice_id):
    delete_notice(notice_id)
    return get_notice(request, 1)


def modify_notice(request, notice_id):
    content = request.POST['content']
    update_notice(notice_id, content)
    return get_notice(request, 1)


def get_notice(request, page_num):
    notices = latest_notices()
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
    act_name, tel = remove_apply(apply_id)
    async_rm_apply(act_name, tel)
    today = date.today()
    return HttpResponse("<script>alert(\"已删除\");"
                        "location.href=\"../../" + str(today.year) + "/" + str(today.month) + "/" + str(today.day) +
                        "/" + "view\";</script>")


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

    save_settings(zero_year, zero_month, zero_day,
                  desk_max, tent_max, umbrella_max, red_max, cloth_max, loud_max, sound_max, projector_max)
    return setting(request)


def view(request, year, month, day):
    context = query_when(year, month, day)
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/view.html', context)


def view_mobile(request, year, month, day):
    context = query_when(year, month, day)
    return render(request, 'mng/view_mobile.html', context)


def view_mobile_today(request):
    today = datetime.today()
    return view_mobile(request, today.year, today.month, today.day)


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
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')
    return render(request, 'mng/export.html', {})


def upload(request):
    name = request.POST['name']
    f = request.FILES['file']
    upload_file(name, f)
    return render(request, 'mng/download.html', {'docs': all_files()})


def rm_doc(request, doc_id):
    remove_file(doc_id)
    docs = all_files()
    return render(request, 'mng/download.html', {'docs': docs})


def login(request):
    return render(request, 'mng/login.html', {})


def key_valid(request):
    if request.POST['key'] == '39380123@xgb':
        request.session['legal'] = True
        return script('location.href="http://" + location.host')
    else:
        return login(request)


def session_valid(request):
    try:
        legal = request.session['legal']
    except KeyError:
        legal =False
    return legal


def need_login(request):
    if not session_valid(request):
        return script('location.href="http://" + location.host + "/login"')