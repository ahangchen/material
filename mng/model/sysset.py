from mng.models import KV


def kvs():
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

    return {
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


def zero_date():
    return int(KV.objects.filter(set_key='zero_year').first().set_value), \
           int(KV.objects.filter(set_key='zero_month').first().set_value), \
           int(KV.objects.filter(set_key='zero_day').first().set_value)


def save_settings(zero_year, zero_month, zero_day,
                  desk_max, tent_max, umbrella_max, red_max, cloth_max, loud_max, sound_max, projector_max):
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
