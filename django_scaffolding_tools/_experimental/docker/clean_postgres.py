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


def run_command_with_grep(commands: List[str], regexp: str) -> List[str]:
    ps = subprocess.run(commands, check=True, capture_output=True)
    # print(ps.stderr.decode('utf-8').strip())
    containers = subprocess.run(['grep', '-E', f'{regexp}'],
                                input=ps.stdout, capture_output=True)
    results = containers.stdout.decode('utf-8').strip().split('\n')
    return results


def get_containers(regexp: str):
    commands = ['docker', 'ps', '-a']
    results = run_command_with_grep(commands, regexp)
    container_list = list()
    if len(results) > 0:
        for r in results:
            data = r.split(' ')
            if len(data[0]) != 0:
                container_list.append({'container_id': data[0], 'image': data[3], 'name': data[-1]})
    return container_list


def get_volumes(regexp):
    commands = ['docker', 'volume', 'ls']
    results = run_command_with_grep(commands, regexp)
    volume_list = list()
    for r in results:
        data = r.split(' ')
        if len(data[0]) != 0:
            volume_list.append({'driver': data[0], 'name': data[-1]})
    return volume_list


def split_and_clean(line: str) -> List[str]:
    line_parts = line.split(' ')
    final = [x for x in line_parts if len(x) > 0]
    return final


def get_images(regexp):
    commands = ['docker', 'image', 'ls']
    results = run_command_with_grep(commands, regexp)
    image_list = list()
    for r in results:
        data = split_and_clean(r)
        if len(data) > 0:
            image_list.append({'name': data[0], 'image_id': data[2]})
    return image_list


def do_cleanup(regexpression: str):
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
            v_res, v_errors = run_commands(delete_volume_command)
            print(f'Deleted {v_res}')
    else:
        print(f'No volumes found for {regexpression}')

    ####################################################################
    # IMAGES

    d_images = get_images(regexpression)
    if len(d_images) > 0:
        for i, d_image in enumerate(d_images):
            print(f'({i}) {d_image["name"]}')
        image_to_delete = input('Image to delete (#, n, a): ')
        delete_image_command = ['docker', 'image', 'rm']
        if image_to_delete.lower() == 'a':
            for d_image in d_images:
                delete_image_command.append(d_image['name'])
        elif image_to_delete.isdigit():
            delete_image_command.append(d_images[int(image_to_delete)]['name'])
        else:
            print('Not deleting any images')
        if len(delete_image_command) > 3:
            i_res, i_errors = run_commands(delete_image_command)
            print(f'Deleted {i_res}')
    else:
        print(f'No images found for {regexpression}')


if __name__ == '__main__':
    reg_expression = r'mail_sender_[a-z_\-]*_postgres'
    do_cleanup(reg_expression)
