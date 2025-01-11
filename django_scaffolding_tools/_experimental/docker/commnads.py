import subprocess
from typing import List, Tuple


def run_commands(commands: List[str], encoding: str = "utf-8") -> Tuple[List[str], List[str]]:
    """:param commands: <list> The command and paraemters to run
    :param encoding: <str> Encoding for the shell
    :return: <tuple> Containing 2 lists. First one with results and the Second one with errors if any.
    """
    result = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, check=False)
    result_lines = result.stdout.decode(encoding).split("\n")[:-1]
    error_lines = result.stderr.decode(encoding).split("\n")[:-1]
    return result_lines, error_lines


def run_command_with_grep(commands: List[str], regexp: str) -> List[str]:
    ps = subprocess.run(commands, check=True, capture_output=True)
    # print(ps.stderr.decode('utf-8').strip())
    containers = subprocess.run(["grep", "-E", f"{regexp}"], input=ps.stdout, capture_output=True, check=False)
    results = containers.stdout.decode("utf-8").strip().split("\n")
    return results
