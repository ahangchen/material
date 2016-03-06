import time

from bck.backup_util import backup_db, validate_db_change


def listen_backup():
    change_interval = 6 * 60
    validate_interval = 5 * 60
    while(True):
        if validate_db_change('db.sqlite3', change_interval):
            backup_db()
        time.sleep(validate_interval)
