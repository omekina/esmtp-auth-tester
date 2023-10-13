ANSI_START = "\033["
ANSI_END = "m"
ANSI_RESET = ANSI_START + "0" + ANSI_END
ANSI_RED = ANSI_START + "31" + ANSI_END
ANSI_GREEN = ANSI_START + "32" + ANSI_END
ANSI_BLUE = ANSI_START + "34" + ANSI_END
ANSI_YELLOW = ANSI_START + "33" + ANSI_END


def print_event(info: str, is_error: bool = False) -> None:
    prefix = (ANSI_RED + "Error: ") if is_error else ("Info: ")
    print(prefix + info + ANSI_RESET)


def print_stream(data: str, direction: bool) -> None:
    prefix = (ANSI_GREEN + "-> ") if direction else (ANSI_BLUE + "<- ")
    print(prefix + data.replace("\r\n", "") + ANSI_RESET)
