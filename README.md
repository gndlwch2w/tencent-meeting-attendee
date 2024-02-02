# Tencent Meeting Attendee

Automatically join a tencent meeting based on the tencent meeting code. [**Supports Windows and macOS**]

### Get started

- Build a scheduling task via `main.py`, and here you need
  provide `a tencent meeting code`, `a starting time that you want to join the meeting`,
  and `(Optional) a comment for easily finding the task in Task Scheduler`.
  ```python
  config = {
    'meeting_code': '961-243-675',
    'starting_time': '2024-02-02 08:55:00',
    'comment': 'GroupReport'
  }
  ```
- Then, you will receive a message send from Task Scheduler (only Windows) whether the task was created successfully. If successful,
  you should not to operate (e.g. move, delete, ...) the file `attendee.py`.
