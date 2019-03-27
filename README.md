# backup_mysql
backup mysql with python 3

# Requirement 
- Ubuntu / CentOS
- python 3
- git 
- crontab

# Feature 

- Backup mysql database.
- Gửi thông báo backup đến slack + telegram.
- Tự động sync đến FTP server.
- Xóa các folder backup cũ trong vòng **x** ngày

# How to (Example with CentOS 7)

#### 1. Install Requirement Packages

```
yum groupinstall "Development Tools" -y
yum install git -y
```

#### 2. Install python 3.6

```
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python-devel -y
yum install python36-devel -y
yum install python36 -y
yum install python36u-mod_wsgi -y

yum install python-pip -y
yum install python36u-pip -y
pip3.6 install virtualenv
```

#### 3. Clone repo

```
cd /opt/
git clone https://github.com/huytm/backup_mysql.git
```

#### 4. Create virtual environmet and install python lib

```
cd /opt/backup_mysql
virtualenv env
source env/bin/activate
pip install -r requirement.txt
```

#### 5. Change setting

Modify your setting in /opt/backup_mysql/settings/settings.json

```json
{
    "mysql": {
        "user": "USER_MYSQL",
        "password": "PASSWORD_MYSQL",
        "database": "DATABASE_MYSQL_TO_BACKUP"
    },
    "backup": {
        "backup_folder": "/opt/my_backup_folder",
        "backup_file_name": "my_backup_file",
        "ftp_server": "10.10.10.10",
        "remote_sync_path": "/backup/folder/in/ftp/server",
        "remove_days": 10 #Keep folder in 10 days
    },
    "telegram": {
        "token": "your_telegram_token",
        "chat_id": "your_telegram_chat_id"
    },
    "slack": {
        "token": "your_slack_token",
        "channel": "your_slack_channel"
    }
}
```

#### 6. Add script to crontab

```
crontab -e
```

Add the following line. Interval backup in 2 hours

```
0 */2 * * * source /opt/backup_mysql/env/bin/activate && python /opt/backup_mysql/run_backup.py
```

