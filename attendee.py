"""The program aims to join a meeting based on a meeting code.
"""

import os
import sys
from utils import check_system, require_not_none

@check_system('windows')
def join_meeting(meeting_code: str):
    """Automatically join a tencent meeting based on the meeting code. The machine
    running this program should have the 'Tencent Meetings' installed software and 
    have logged in to a valid account.

    Args:
        meeting_code (str): a tencent meeting code, such as '123-456-789' or '123456789'.

    Ref: https://github.com/elliottzheng/auto_wemeet/blob/main/auto_wemeet.py
    """
    meeting_code = require_not_none(meeting_code)
    os.system(f'start wemeet://page/inmeeting?meeting_code={meeting_code}')

if __name__ == '__main__':
    # The second argument from the command line should be a valid meeting code.
    _, meeting_code = sys.argv
    join_meeting(meeting_code)
