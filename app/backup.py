import os
import time
import datetime
from .slack_notify import Slack
from .telegram_notify import Telegram
import logging
from utils import common

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='/var/log/backup.log',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

class Backup(object):
    def __init__(self, settings):
        self.settings = settings
        self.db_user_name   = settings["mysql"]["user"]
        self.db_password    = settings["mysql"]["password"]
        self.database       = settings["mysql"]["database"]
        self.output_startw  = settings["backup"]["backup_file_name"]
        self.backup_folder  = settings["backup"]["backup_folder"]
        self.slack_token    = settings["slack"]["token"]
        self.slack_channel  = settings["slack"]["channel"]
        self.telegram_token = settings["telegram"]["token"]
        self.telegram_channel = settings["telegram"]["chat_id"]


    def backup_database(self):
        notify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        backup_dir = self.backup_folder + "/" + current_date
        create_backup_dir = "mkdir -p "+ backup_dir
        if (self.db_password).strip() != '' and self.db_password is not None:
            backup_command = "mysqldump -u" + self.db_user_name + " -p" + self.db_password + " " + self.database + " 2>/dev/null | gzip > " + backup_dir + "/"+ self.output_startw + "_" + current_time +".sql.gz"
        else:
            backup_command = "mysqldump -u" + self.db_user_name + " " + self.database + " 2>/dev/null | gzip > " + backup_dir + "/"+ self.output_startw + "_" + current_time +".sql.gz"    

        try:
            os.system(create_backup_dir) 
            os.system(backup_command)
            backup_size = self.check_file_size(backup_dir + "/"+ self.output_startw + "_" + current_time +".sql.gz")
            telegram_message = common.render_message_telegram(datetime=notify_date, file_size=backup_size, 
                                                                    file_name=self.output_startw + "_" + current_time +".sql.gz" )
            slack_message = common.render_message_telegram(datetime=notify_date, file_size=backup_size, 
                                                                    file_name=self.output_startw + "_" + current_time +".sql.gz" )
            # Delete old folder and sync
            common.remove_old_folder(self.settings)           
            common.sync_to_ftp(self.settings)

            telegram = Telegram(self.telegram_token, self.telegram_channel, telegram_message)
            slack = Slack(self.slack_token , self.slack_channel, slack_message)

            telegram.send_message()
            slack.send_message() 
        except Exception as ex:
            logging.warning("backup " + ex)

    def check_file_size(self, file_path):
        file_info = os.stat(file_path).st_size
        return common.convert_bytes(file_info)