from django.db import models


# Create your models here.


class Apply(models.Model):
    act_name = models.CharField(max_length=100)
    applicant = models.CharField(max_length=50)
    tel = models.CharField(max_length=30)
    apply_org = models.CharField(max_length=50)
    assistant = models.CharField(max_length=50, default='no_name')

    char_num = models.IntegerField(default=0)
    desk_num = models.IntegerField(default=0)
    tent_num = models.IntegerField(default=0)
    umbrella_num = models.IntegerField(default=0)
    red_num = models.IntegerField(default=0)
    cloth_num = models.IntegerField(default=0)
    loud_num = models.IntegerField(default=0)
    sound_num = models.IntegerField(default=0)
    projector = models.IntegerField(default=0)

    def __str__(self):
        return self.act_name


class ApplyTime(models.Model):
    apply = models.ForeignKey(Apply, related_name='rap')
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)

    def __str__(self):
        return "time %04d-%02d-%02d" % (self.year, self.month, self.day)


class KV(models.Model):
    set_key = models.CharField(max_length=100)
    set_value = models.CharField(max_length=200)


class Notice(models.Model):
    content = models.CharField(max_length=300)


class ApplyFile(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=300)
