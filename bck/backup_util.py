import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_163_mail_attach(user, pwd, to_addr, from_addr, subject, attach_path):
    # 创建一个带附件的实例
    msg = MIMEMultipart()

    # 构造附件1
    att1 = MIMEText(open(attach_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="%s"'% attach_path  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)

    # 加邮件头
    msg['to'] = to_addr
    msg['from'] = from_addr
    msg['subject'] = subject
    # 发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.163.com')
        server.login(user, pwd)  # XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
        print('发送成功')
    except smtplib.SMTPConnectError:
        print('SMTPConnectError')


def validate_db_change(db_path, validate_interval):
    modify_time = os.stat(db_path).st_mtime
    cur_time = time.time()
    return cur_time - modify_time < validate_interval


def backup_db():
    db_path = 'db.sqlite3'
#    db_zip_path = 'db.sqlite3.tar'
#    safe_rm(db_zip_path)
#    tar = tarfile.open(db_zip_path, 'w')
#    tar.add(db_path)
#    tar.close()
#    cp(db_zip_path, '0')
    send_163_mail_attach('13660106752', 'xuegongban118',
                         '13660106752@163.com', '13660106752@163.com', 'db_bck', db_path)

