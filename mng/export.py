import datetime

import xlwt
from django.http import HttpResponse

from mng.models import Apply


def export_xls(start_date, end_date):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('%04d年%02d月%02d日--%04d年%02d月%02d日' %
                      (start_date.year, start_date.month, start_date.day, end_date.year, end_date.month, end_date.day))
    # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    # style_date = xlwt.easyxf(num_format_str='D-MMM-YY')
    # style_k=xlwt.easyxf('font: bold on,colour_index green,height 360;align: wrap off;borders:left 1,right 1,top 1,bottom 1;pattern: pattern alt_bars, fore_colour gray25, back_colour gray25')
    style_title = xlwt.easyxf('font: bold on,colour_index green;')

    ws.col(0).width = 0x0f00
    ws.col(2).width = 0x1800
    ws.col(3).width = 0x1200
    ws.col(5).width = 0x0f00

    ws.write(0, 0, '时间', style_title)
    ws.write(0, 1, '审批人', style_title)
    ws.write(0, 2, '活动名称', style_title)
    ws.write(0, 3, '申请单位', style_title)
    ws.write(0, 4, '申请人', style_title)
    ws.write(0, 5, '联系电话', style_title)
    ws.write(0, 6, '胶凳', style_title)
    ws.write(0, 7, '桌子', style_title)
    ws.write(0, 8, '帐篷', style_title)
    ws.write(0, 9, '太阳伞', style_title)
    ws.write(0, 10, '相机', style_title)
    ws.write(0, 11, '展架', style_title)
    ws.write(0, 12, '扩音器', style_title)
    ws.write(0, 13, '投影仪', style_title)
    ws.write(0, 14, '音响', style_title)
    j = 1
    for i in range((end_date - start_date).days + 1):
        cur_date = start_date + datetime.timedelta(days=i)
        applies = Apply.objects.filter(rap__year=cur_date.year, rap__month=cur_date.month, rap__day=cur_date.day)
        for apply in applies:
            ws.write(j, 0, '%04d年%02d月%02d日' % (cur_date.year, cur_date.month, cur_date.day))
            ws.write(j, 1, apply.assistant)
            ws.write(j, 2, apply.act_name)
            ws.write(j, 3, apply.apply_org)
            ws.write(j, 4, apply.applicant)
            ws.write(j, 5, apply.tel)
            ws.write(j, 6, apply.char_num)
            ws.write(j, 7, apply.desk_num)
            ws.write(j, 8, apply.tent_num)
            ws.write(j, 9, apply.umbrella_num)
            ws.write(j, 10, apply.red_num)
            ws.write(j, 11, apply.cloth_num)
            ws.write(j, 12, apply.loud_num)
            ws.write(j, 13, apply.projector)
            ws.write(j, 14, apply.sound_num)
            j += 1
    response = HttpResponse(content_type="application/ms-excel")

    response['Content-Disposition'] = 'attachment;filename="%04d-%02d-%02d-%04d-%02d-%02d-material.xls"' % \
                                      (start_date.year, start_date.month, start_date.day, end_date.year, end_date.month,
                                       end_date.day)
    wb.save(response)
    return response
