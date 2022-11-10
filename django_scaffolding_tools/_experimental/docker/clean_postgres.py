import subprocess
from typing import List, Tuple


def run_commands(commands: List[str], encoding: str = 'utf-8') -> Tuple[List[str], List[str]]:
    """
    :param commands: <list> The command and paraemters to run
    :param encoding: <str> Encoding for the shell
    :return: <tuple> Containing 2 lists. First one with results and the Second one with errors if any.
    """
    result = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    result_lines = result.stdout.decode(encoding).split('\n')[:-1]
    error_lines = result.stderr.decode(encoding).split('\n')[:-1]
    return result_lines, error_lines


def run_command2(cmd):
    # cmd = "ps -A|grep 'process_name'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output, ['err']


def run_grepped_command(regexp):
    # regexp = 'puntopago[a-z_]*_postgres'
    # regexp = 'clave_[a-z_]*_postgres'
    ps = subprocess.run(['docker', 'ps', '-a'], check=True, capture_output=True)
    # print(ps.stderr.decode('utf-8').strip())
    containers = subprocess.run(['grep', '-E', f'{regexp}'],
                                input=ps.stdout, capture_output=True)
    results = containers.stdout.decode('utf-8').strip().split('\n')
    return results


if __name__ == '__main__':
    # regexp = 'puntopago[a-z_]*_postgres'
    # command_str = f'docker ps -a | grep -E \'{regexp}\''
    # # command_str = f'docker ps -a | grep puntopago'
    # command = command_str.split(' ')
    # results, errors = run_command2(command_str)
    # for res in results:
    #     print(res)
    # for error in errors:
    #     print(error)
    regexp = 'clave_[a-z_]*_postgres'
    res = run_grepped_command(regexp)
    for r in res:
        print(r)
