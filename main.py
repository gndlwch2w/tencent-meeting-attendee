import sys
import os
from os.path import dirname, abspath, sep
from datetime import datetime
from typing import Optional
from utils import check_system, join, require_not_none, require_not_none_else, parse_datetime

def get_task_name(meeting_code: str, comment: Optional[str] = None) -> str:
    """Returns a task name for a windows scheduling task name."""
    comment = require_not_none_else(comment, '').replace(' ', '')
    return join('TencentMeeting', meeting_code, comment, separator='-')

@check_system('windows')
def build_scheduling_task(meeting_code: str,
                          starting_time: str | datetime,
                          time_format: Optional[str] = None,
                          comment: Optional[str] = None):
    """Build a windows scheduling task to automatically call the 'attendee' program to attend a
    designated Tencent meeting when time conditions are met. When you success to build a windows
    scheduling task, you can find it in 'Computer Management / System Tools / Task Scheduler /
    Task Scheduler Library'. Tips: If you want the task can be called on time it is necessary that
    let your machine do not sleep, and you need to set your machine never to sleep.

    Ref: https://zhuanlan.zhihu.com/p/430602325
    """
    meeting_code = require_not_none(meeting_code).replace('-', '')
    task_name = get_task_name(meeting_code, comment)
    attendee = join(dirname(abspath(__file__)), 'attendee.py', separator=sep)
    command = f'"{sys.executable} {attendee} {meeting_code}"'
    starting_time = parse_datetime(starting_time, time_format)
    sd, st = starting_time.strftime('%Y/%m/%d %H:%M').split(' ')
    os.system(f'SchTasks /Create /SC ONCE /TN {task_name} /TR {command} /ST {st} /SD {sd}')

from crontab import CronTab

def mac(meeting_code: str,
        starting_time: str | datetime,
        time_format: Optional[str] = None,
        comment: Optional[str] = None):
    meeting_code = require_not_none(meeting_code).replace('-', '')
    task_name = get_task_name(meeting_code, comment)
    attendee = join(dirname(abspath(__file__)), 'attendee.py', separator=sep)
    command = f'{sys.executable} {attendee} {meeting_code}'
    cron = CronTab(user=True)
    job = cron.new(command=command, comment=task_name)
    time = parse_datetime(starting_time, time_format)
    job.minutes.on(time.minute)
    job.hour.on(time.hour)
    job.day.on(time.day)
    job.month.on(time.month)
    job.frequency_at_year(time.year)
    # job.setall(f'{time.second} {time.minute} {time.hour} {time.day} {time.month} ? {time.year}')
    cron.write_to_user(os.getlogin())

def main():
    config = {
        'meeting_code': '961-243-675',
        'starting_time': '2024-02-02 08:10:01',
        'comment': 'GroupReport'
    }
    mac(**config)

if __name__ == '__main__':
    main()
