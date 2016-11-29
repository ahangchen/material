from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^apply/$', views.apply, name='apply'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/view/$', views.view, name='view'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/view_mobile/$', views.view_mobile, name='view_mobile'),
    url(r'^view_today/$', views.view_mobile_today, name='view_today'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^download/$', views.download, name='download'),
    url(r'^setting/$', views.setting, name='setting'),
    url(r'^publish/$', views.publish, name='publish'),
    url(r'^save_apply/$', views.save_apply, name='save_apply'),
    url(r'^save_setting/$', views.save_setting, name='save_setting'),
    url(r'^(?P<apply_id>[0-9]+)/apply_modify/$', views.apply_modify, name='apply_modify'),
    url(r'^(?P<apply_id>[0-9]+)/apply_remove/$', views.apply_remove, name='apply_remove'),
    url(r'^(?P<apply_id>[0-9]+)/save_modify/$', views.save_modify, name='save_modify'),
    url(r'^save_notice/$', views.save_notice, name='save_notice'),
    url(r'^(?P<page_num>[0-9]+)/get_notice/$', views.get_notice, name='get_notice'),
    url(r'^(?P<notice_id>[0-9]+)/modify_notice/$', views.modify_notice, name='modify_notice'),
    url(r'^(?P<notice_id>[0-9]+)/remove_notice/$', views.remove_notice, name='remove_notice'),
    url(r'^backup/$', views.backup, name='backup'),
    url(r'^export/$', views.export, name='export'),
    url(r'^export_html/$', views.export_html, name='export_html'),
    url(r'upload/$', views.upload, name='upload'),
    url(r'^(?P<doc_id>[0-9]+)/rm_doc/$', views.rm_doc, name='rm_doc'),
]
