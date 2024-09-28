# Cronjob Extractor From Syslog

This Python script is for developers (including myself) who are at risk of unintentionally losing all their cron jobs 
due to the `crontab -r` command.

It helps recover the original cron jobs by retrieving them from cron-related logs left in the Linux syslog.

## Requirements

- Python 3.7 or higher

## How to Use

```
curl -sSL https://raw.githubusercontent.com/Seunghan-Jung/cronjob-extractor/refs/heads/main/cronjob_extractor.py | sudo python3.8 -
```
