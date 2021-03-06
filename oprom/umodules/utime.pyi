# utime
"time related functions"
from typing import Tuple, Union


def localtime(secs: int = None) -> Tuple[int, int, int, int, int, int, int, int]:
    """Convert a time expressed in seconds since the Epoch (see above) into an 8-tuple which contains: (year, month, mday, hour, minute, second, weekday, yearday) If secs is not provided or None, then the current time from the RTC is used.

    year includes the century (for example 2014).
    month is 1-12
    mday is 1-31
    hour is 0-23
    minute is 0-59
    second is 0-59
    weekday is 0-6 for Mon-Sun
    yearday is 1-366
    """
    pass


def mktime():
    "This is inverse function of localtime. It’s argument is a full 8-tuple which expresses a time as per localtime. It returns an integer which is the number of seconds since Jan 1, 2000."
    pass


def sleep(seconds: Union[int, float]):
    "Sleep for the given number of seconds. Some boards may accept seconds as a floating-point number to sleep for a fractional number of seconds. Note that other boards may not accept a floating-point argument, for compatibility with them use sleep_ms() and sleep_us() functions."
    pass


def sleep_ms(ms):
    "Delay for given number of milliseconds, should be positive or 0."
    pass


def sleep_us(us):
    "Delay for given number of microseconds, should be positive or 0."
    pass


def ticks_ms():
    "Returns an increasing millisecond counter with an arbitrary reference point, that wraps around after some value."
    pass


def ticks_us():
    "Just like ticks_ms() above, but in microseconds."
    pass


def ticks_cpu():
    """Similar to ticks_ms() and ticks_us(), but with the highest possible resolution in the system. This is usually CPU clocks, and that’s why the function is named that way. But it doesn’t have to be a CPU clock, some other timing source available in a system (e.g. high-resolution timer) can be used instead. The exact timing unit (resolution) of this function is not specified on utime module level, but documentation for a specific port may provide more specific information. This function is intended for very fine benchmarking or very tight real-time loops. Avoid using it in portable code.
    """
    pass


def ticks_add(ticks, delta):
    """Offset ticks value by a given number, which can be either positive or negative. Given a ticks value, this function allows to calculate ticks value delta ticks before or after it, following modular-arithmetic definition of tick values (see ticks_ms() above). ticks parameter must be a direct result of call to ticks_ms(), ticks_us(), or ticks_cpu() functions (or from previous call to ticks_add()). However, delta can be an arbitrary integer number or numeric expression. ticks_add() is useful for calculating deadlines for events/tasks. (Note: you must use ticks_diff() function to work with deadlines.)
    """
    pass


def ticks_diff(ticks1, ticks2):
    """Measure ticks difference between values returned from ticks_ms(), ticks_us(), or ticks_cpu() functions, as a signed value which may wrap around.
    The argument order is the same as for subtraction operator, ticks_diff(ticks1, ticks2) has the same meaning as ticks1 - ticks2. However, values returned by ticks_ms(), etc. functions may wrap around, so directly using subtraction on them will produce incorrect result. That is why ticks_diff() is needed, it implements modular (or more specifically, ring) arithmetics to produce correct result even for wrap-around values (as long as they not too distant inbetween, see below). The function returns signed value in the range [-TICKS_PERIOD/2 .. TICKS_PERIOD/2-1] (that’s a typical range definition for two’s-complement signed binary integers). If the result is negative, it means that ticks1 occurred earlier in time than ticks2. Otherwise, it means that ticks1 occurred after ticks2. This holds only if ticks1 and ticks2 are apart from each other for no more than TICKS_PERIOD/2-1 ticks. If that does not hold, incorrect result will be returned. Specifically, if two tick values are apart for TICKS_PERIOD/2-1 ticks, that value will be returned by the function. However, if TICKS_PERIOD/2 of real-time ticks has passed between them, the function will return -TICKS_PERIOD/2 instead, i.e. result value will wrap around to the negative range of possible values.
    Informal rationale of the constraints above: Suppose you are locked in a room with no means to monitor passing of time except a standard 12-notch clock. Then if you look at dial-plate now, and don’t look again for another 13 hours (e.g., if you fall for a long sleep), then once you finally look again, it may seem to you that only 1 hour has passed. To avoid this mistake, just look at the clock regularly. Your application should do the same. “Too long sleep” metaphor also maps directly to application behavior: don’t let your application run any single task for too long. Run tasks in steps, and do time-keeping inbetween.
    """
    pass


def time() -> int:
    """Returns the number of seconds, as an integer, since the Epoch, assuming that underlying RTC is set and maintained as described above. If an RTC is not set, this function returns number of seconds since a port-specific reference point in time (for embedded boards without a battery-backed RTC, usually since power up or reset). If you want to develop portable MicroPython application, you should not rely on this function to provide higher than second precision. If you need higher precision, use ticks_ms() and ticks_us() functions, if you need calendar time, localtime() without an argument is a better choice."""
    pass


def time_world() -> int:
    pass


def time_up() -> float:
    pass


def time_cpu() -> float:
    pass
