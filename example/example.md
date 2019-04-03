
## Some settings example

### 1 Backup **all** database và **delete** old file in 10 day: 

```
...
    "mysql": {
        "user": "MYSQL_USER",
        "password": "MYSQL_PASSWORD",
        "backup_type": "all", 
    ...

    "delete_old_file": {
        "delete_old_file": true,
        "remove_days": 10
    },
```

### 2. Backup 1 database và send notify to slack:

```
...
    "mysql": {
        "user": "MYSQL_USER",
        "password": "MYSQL_PASSWORD",
        "backup_type": "database",
        "database": "my_database",
    ...
    
    "slack": {
        "send_notify": true,
        "token": "your_slack_token",
        "channel": "your_slack_channel"
    }
```

### 3. Backup 3 tables, sync to ftp server, send notify to telegram

```
...
    "mysql": {
        "user": "MYSQL_USER",
        "password": "MYSQL_PASSWORD",
        "backup_type": "table",
        "database": "my_database",
        "tables": "table1, table2, table3"
    ...

    "sync": {
        "sync": true,
        "ftp_server": "10.10.10.10",
        "remote_sync_path": "/backup/folder/in/ftp/server"
    },

    ...
    "telegram": {
        "send_notify": true,
        "token": "your_telegram_token",
        "chat_id": "your_telegram_chat_id"
    },
```

### 4. Backup 1 table, send notify to telegram, and dont send notify slack

```
...
    "mysql": {
        "user": "MYSQL_USER",
        "password": "MYSQL_PASSWORD",
        "backup_type": "table",
        "database": "my_database",
        "tables": "table1, table2, table3"
    ...

    "sync": {
        "sync": true,
        "ftp_server": "10.10.10.10",
        "remote_sync_path": "/backup/folder/in/ftp/server"
    },

    ...
    "telegram": {
        "send_notify": true,
        "token": "your_telegram_token",
        "chat_id": "your_telegram_chat_id"
    },
    ...

    "slack": {
        "send_notify": false,
        "token": "your_slack_token",
        "channel": "your_slack_channel"
    }
```