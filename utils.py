import platform
from datetime import datetime
from typing import TypeVar, Union, Tuple, Any, Collection, Callable
from functools import wraps

T = TypeVar('T')
U = TypeVar('U')

__all__ = [
    'require_not_none',
    'require_not_none_else',
    'parse_datetime',
    'check_system',
    'join'
]

def is_not_empty(obj: Any) -> bool:
    if isinstance(obj, str):
        return len(obj.strip()) != 0
    if isinstance(obj, Collection):
        return len(obj) != 0
    return obj is not None

def require_not_none(obj: T, msg: str = None) -> T:
    msg = require_not_none_else(msg, 'the obj must not be None')
    assert obj is not None, msg
    return obj

def require_not_none_else(obj: T, other: U) -> Union[T, U]:
    return other if obj is None else obj

def parse_datetime(time: Union[str, datetime], formats: str = None) -> datetime:
    """Parse a time string or datetime by a specific format."""
    if isinstance(time, datetime):
        return time
    if isinstance(time, str):
        formats = require_not_none_else(formats, '%Y-%m-%d %H:%M:%S')
        return datetime.strptime(time, formats)
    raise TypeError(f'cannot parsing time type: {type(time)}')

def check_system(target: str) -> Callable:
    """Check whether the system is running on the target system."""
    def _check_system(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            msg = f'the system {platform.system()} is not supported'
            assert platform.system().lower() == target.lower(), msg
            return func(*args, **kwargs)
        return wrapper
    return _check_system

def join(*args: Tuple[str], separator: str = None) -> str:
    """Concat a string sequence orderly using a given separator, which default is space."""
    separator = require_not_none_else(separator, ' ')
    return separator.join(filter(lambda e: is_not_empty(e), args))
