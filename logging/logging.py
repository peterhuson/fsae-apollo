from datetime import datetime
from colorama import init, Fore, Style
from enum import Enum


init()  # Initialize color logging


class MessageType(Enum):
    MESSAGE = Fore.BLUE
    WARNING = Fore.YELLOW
    ERROR = Fore.RED


def get_formatted_time() -> str:
    now = datetime.now()
    return now.strftime("[%b %-d %Y | %-H:%M:%S]")


def log_message(message: str, message_type: MessageType) -> None:
    # Build message and print it (flush to allows send to file immediately)
    final_log_msg = f"{Fore.LIGHTBLUE_EX}{get_formatted_time()}"\
                    + f" {message_type.value}{message_type.name}:" \
                    + f" {message}{Style.RESET_ALL}"

    print(final_log_msg, flush=True)
