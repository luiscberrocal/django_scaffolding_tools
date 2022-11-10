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


def get_containers(regexp):
    ps = subprocess.run(['docker', 'ps', '-a'], check=True, capture_output=True)
    # print(ps.stderr.decode('utf-8').strip())
    containers = subprocess.run(['grep', '-E', f'{regexp}'],
                                input=ps.stdout, capture_output=True)
    results = containers.stdout.decode('utf-8').strip().split('\n')
    container_list = list()
    for r in results:
        data = r.split(' ')
        container_list.append({'container_id': data[0], 'image': data[3], 'name': data[-1]})
    return container_list


if __name__ == '__main__':
    regexp = 'lms_[a-z_]*_postgres'

    res = get_containers(regexp)
    for i, r in enumerate(res, ):
        print(f'{i} {r["container_id"]} {r["image"]}')
    container_to_delete = input(f'Type the number of the container to delete (#):')
    container_id = int(container_to_delete)
    print(res[container_id])

