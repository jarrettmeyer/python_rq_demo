import logging
import time
from . import logger
from .task_result import TaskResult


def send_message(message: str, sleep_duration: float):
    start_time = time.time()
    logger.debug('message length: %d, duration: %f', len(message), sleep_duration)
    time.sleep(sleep_duration)
    end_time = time.time()
    duration = end_time - start_time
    logger.debug('Done, duration: %f', duration)
    return TaskResult(title='Done', message=message, duration=duration)
