import functools
import logging
from requests.exceptions import Timeout, ConnectionError, HTTPError
from typing import Any, Callable

logger = logging.getLogger("car_scout_agent")


def handle_tool_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)

        except Timeout:
            logger.error(f"Timeout error in {func.__name__}")
            return "Ошибка: Время ожидания ответа от сервера истекло. Попробуй позже."

        except ConnectionError:
            logger.error(f"Connection error in {func.__name__}")
            return "Ошибка: Не удалось подключиться к серверу API. Проверь интернет-соединение."

        except HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} in {func.__name__}")
            return f"Ошибка сервера (HTTP {e.response.status_code}). Попробуй другую марку."

        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            return "Ошибка: Локальная база данных временно недоступна."

        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}")
            return f"Произошла непредвиденная ошибка: {str(e)}"

    return wrapper