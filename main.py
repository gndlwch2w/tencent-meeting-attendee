import sys
import os
from os.path import dirname, abspath, sep
from datetime import datetime
from typing import Optional, Union
from utils import (
    get_system_name,
    check_system,
    join,
    require_not_none,
    require_not_none_else,
    parse_datetime)

system_name = get_system_name()
if system_name == 'darwin':
    import getpass
    from crontab import CronTab

def get_task_name(meeting_code: str, comment: Optional[str] = None) -> str:
    """Returns a task name for a scheduling task name."""
    comment = require_not_none_else(comment, '').replace(' ', '')
    return join('TencentMeeting', meeting_code, comment, separator='-')

@check_system('windows')
def build_scheduling_task_on_windows(meeting_code: str,
                                     starting_time: Union[str, datetime],
                                     time_format: Optional[str] = None,
                                     comment: Optional[str] = None):
    """Build a windows scheduling task to automatically call the 'attendee' program to attend a
    designated Tencent meeting when time conditions are met. When you success to build a windows
    scheduling task, you can find it in 'Computer Management / System Tools / Task Scheduler /
    Task Scheduler Library'. Tips: If you want the task can be called on time it is necessary that
    let your machine do not sleep, and you need to set your machine never to sleep.

    Ref: [1] https://zhuanlan.zhihu.com/p/430602325
    """
    meeting_code = require_not_none(meeting_code).replace('-', '')
    task_name = get_task_name(meeting_code, comment)
    attendee = join(dirname(abspath(__file__)), 'attendee.py', separator=sep)
    command = f'"{sys.executable} {attendee} {meeting_code}"'
    starting_time = parse_datetime(starting_time, time_format)
    sd, st = starting_time.strftime('%Y/%m/%d %H:%M').split(' ')  # [1]
    os.system(f'SchTasks /Create /SC ONCE /TN {task_name} /TR {command} /ST {st} /SD {sd}')

@check_system('darwin')
def build_scheduling_task_on_mac(meeting_code: str,
                                 starting_time: Union[str, datetime],
                                 time_format: Optional[str] = None,
                                 comment: Optional[str] = None):
    """Building a crontab scheduling task to automatically call the 'attendee' program to attend
    a designated Tencent meeting when time conditions are met. When you success to build a crontab
    scheduling task, you can find it by the command 'crontab -l' [2]. Tips: A task have same task
    name will be overridden and if you want the task can be called on time it is necessary that
    let your machine do not sleep, and you need to set your machine never to sleep.

    Ref: [1] https://baijiahao.baidu.com/s?id=1778201922082641060&wfr=spider&for=pc,
         [2] https://zhuanlan.zhihu.com/p/680144927
    """
    meeting_code = require_not_none(meeting_code).replace('-', '')
    task_name = get_task_name(meeting_code, comment)
    attendee = join(dirname(abspath(__file__)), 'attendee.py', separator=sep)
    command = f'{sys.executable} {attendee} {meeting_code}'
    cron = CronTab(user=getpass.getuser())
    cron.remove_all(comment=task_name)  # [2]
    job = cron.new(command=command, comment=task_name)
    time = parse_datetime(starting_time, time_format)
    # minute hour day month week command
    job.setall(f'{time.minute} {time.hour} {time.day} {time.month} *')  # [1]
    cron.write_to_user(getpass.getuser())

def main():
    config = {
        'meeting_code': '961-243-675',
        'starting_time': '2024-02-02 08:10:01',
        'comment': 'GroupReport'
    }

    if system_name == 'windows':
        build_scheduling_task_on_windows(**config)
    elif system_name == 'darwin':
        build_scheduling_task_on_mac(**config)
    else:
        raise RuntimeError(f'Unsupported system: {system_name}')

if __name__ == '__main__':
    main()
