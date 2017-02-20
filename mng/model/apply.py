import shutil
from datetime import date, datetime

from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404

from mng.models import KV, Apply
from mng.utils.mt_date import add_months, gen_calendar
from mng.utils.network import post
from mng.utils.sync import run_in_background


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
                    invalid_name = '相机'
                elif material_name == 'cloth_num':
                    invalid_name = '展架'
                elif material_name == 'loud_num':
                    invalid_name = '麦克风'
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


def insert_apply(act_name, applicant, apply_org, tent_num, tel, assistant,
                 desk_num, chair_num, umbrella_num, red_num, cloth_num, loud_num, sound_num, projector, apply_dates):
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

        return apply_rcd.id, True, None
    else:
        return -1, False, invalid_applies


def modify_apply(apply_id, act_name, applicant, apply_org, tent_num, tel, assistant,
                 desk_num, chair_num, umbrella_num, red_num, cloth_num, loud_num, sound_num, projector, apply_dates):
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
        return invalid_applies


def remove_apply(apply_id):
    apply_rcd = get_object_or_404(Apply, pk=apply_id)
    apply_rcd.delete()
    return apply_rcd.act_name, apply_rcd.tel


def query_when(year, month, day):
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
    return context


# 对接校会oa系统同步需求
URL_HEADER = 'http://114.215.146.135/record/'
URL_SAVE = URL_HEADER + 'saveRecord.do'
URL_REMOVE = URL_HEADER + 'deleteRecord.do'


def save_record(event_name, applicant, phone, org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, exhibition):
    start_date = "%d-%02d-%02d" % (start_year, start_month, start_day)
    end_date = "%d-%02d-%02d" % (end_year, end_month, end_day)
    post(URL_SAVE, {
            "eventName": event_name,
            "header": applicant,
            "phone": phone,
            "Unit": org,
            "startDate": start_date,
            "endDate": end_date,
            "materials": str(desk_num) + "," + str(tent_num) + "," + str(umbrella_num) + "," + str(exhibition)
        })


def remove_record(event_name, phone):
    post(URL_REMOVE, {
        "eventName": event_name,
        "phone": phone
    })


def modify_record(event_name, applicant, phone, org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, exhibition):
    remove_record(event_name, phone)
    save_record(event_name, applicant, phone, org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, exhibition)


def async_apply(act_name, applicant, tel, apply_org,
                      start_year, start_month, start_day, end_year, end_month, end_day,
                desk_num, tent_num, umbrella_num, red_num):
    run_in_background(save_record, act_name, applicant, tel, apply_org,
                      int(start_year), int(start_month), int(start_day), int(end_year), int(end_month), int(end_day),
                      desk_num, tent_num, umbrella_num, red_num)


def async_rm_apply(act_name, tel):
    run_in_background(remove_record, act_name, tel)


def async_modify(act_name, applicant, tel, apply_org,
                      start_year, start_month, start_day, end_year, end_month, end_day,
                desk_num, tent_num, umbrella_num, red_num):
    run_in_background(modify_record, act_name, applicant, tel, apply_org,
                      start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, red_num)


def clean_record():
    shutil.copyfile('db.sqlite3', str(datetime.now()) + 'db.sqlite.bck')
    Apply.objects.all().delete()