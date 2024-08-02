import time


class TimerError(Exception):
    """An exception to indicate timer-related errors"""
    pass


class Timer:
    """A class to measure time"""

    def __init__(self):
        """Initialize the Timer object"""
        self._start_time = None

    def start(self) -> None:
        """Start the timer"""
        if self._start_time is not None:
            raise TimerError("Timer is already running")
        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer and return the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running")
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return elapsed_time

    def reset(self) -> None:
        """Reset the timer"""
        self._start_time = None

    def seconds_elapsed(self) -> float:
        """Return the elapsed time without stopping the timer"""
        return time.perf_counter() - self._start_time if self._start_time is not None else 0

    def time_elapsed_string(self) -> str:
        """Return the elapsed time as a formatted string"""
        if self._start_time is None:
            return "00:00"
        elapsed_time = time.perf_counter() - self._start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes:02}:{seconds:02}"

    def is_running(self) -> bool:
        """Return whether the timer is currently running"""
        return self._start_time is not None
