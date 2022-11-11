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



def get_containers(regexp):
    ps = subprocess.run(['docker', 'ps', '-a'], check=True, capture_output=True)
    # print(ps.stderr.decode('utf-8').strip())
    containers = subprocess.run(['grep', '-E', f'{regexp}'],
                                input=ps.stdout, capture_output=True)
    results = containers.stdout.decode('utf-8').strip().split('\n')
    container_list = list()
    if len(results) > 0:
        for r in results:
            data = r.split(' ')
            if len(data[0]) != 0:
                container_list.append({'container_id': data[0], 'image': data[3], 'name': data[-1]})
    return container_list


def get_volumes(regexp):
    ps = subprocess.run(['docker', 'volume', 'ls'], check=True, capture_output=True)
    # print(ps.stderr.decode('utf-8').strip())
    volumes = subprocess.run(['grep', '-E', f'{regexp}'],
                             input=ps.stdout, capture_output=True)
    results = volumes.stdout.decode('utf-8').strip().split('\n')
    volume_list = list()
    for r in results:
        data = r.split(' ')
        volume_list.append({'driver': data[0], 'name': data[-1]})
    return volume_list


if __name__ == '__main__':
    regexpression = r'lms-graph[a-z_\-]*_postgres'

    res = get_containers(regexpression)
    if len(res) != 0:
        for i, r in enumerate(res):
            print(f'{i} {r["container_id"]} {r["image"]}')
        container_to_delete = input(f'Type the number of the container to delete (#):')
        container_id = int(container_to_delete)
        # print(res[container_id])

        delete_container_command = ['docker', 'rm', res[container_id]['container_id']]
        dc_res, errors = run_commands(delete_container_command)
        print(f'Deleted container {dc_res}')
    else:
        print(f'No container found for {regexpression}')

    d_vols = get_volumes(regexpression)
    # print(d_vols)
    if len(d_vols) != 0:
        for i, d_vol in enumerate(d_vols):
            print(f'({i}) {d_vol["name"]}')

        volume_to_delete = input('Volume to delete (#, n, a):')
        delete_volume_command = ['docker', 'volume', 'rm']
        if volume_to_delete.lower() == 'a':
            for d_vol in d_vols:
                delete_volume_command.append(d_vol['name'])
        elif isinstance(volume_to_delete, int):
            delete_volume_command.append(d_vols[volume_to_delete]['name'])
        else:
            print('Not deleting any volumes')
        if len(delete_volume_command) > 3:
            v_res,v_errors = run_commands(delete_volume_command)
            print(f'Deleted {v_res}')
    else:
        print(f'No volumes found for {regexpression}')


