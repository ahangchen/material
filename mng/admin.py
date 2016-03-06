from django.contrib import admin

# Register your models here.
from mng.models import Apply, ApplyTime, KV, Notice

admin.site.register(Apply)
admin.site.register(ApplyTime)
admin.site.register(KV)
admin.site.register(Notice)
