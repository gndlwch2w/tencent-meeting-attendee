"""The program aims to join a meeting based on a meeting code.
"""

import os
import sys
from utils import (
    check_system,
    require_not_none,
    get_start_command)

@check_system(['windows', 'darwin'])
def join_meeting(meeting_code: str):
    """Automatically join a tencent meeting based on the meeting code. The machine
    running this program should have the 'Tencent Meetings' installed software and 
    have logged in to a valid account.

    Args:
        meeting_code (str): a tencent meeting code, such as '123456789'.

    Ref: [1] https://github.com/elliottzheng/auto_wemeet/blob/main/auto_wemeet.py
    """
    meeting_code = require_not_none(meeting_code)
    os.system(f'{get_start_command()} wemeet://page/inmeeting?meeting_code={meeting_code}')  # [1]

if __name__ == '__main__':
    # The second argument from the command line should be a valid meeting code.
    _, meeting_code = sys.argv
    join_meeting(meeting_code)
