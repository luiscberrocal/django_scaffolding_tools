from typing import List, Optional

from django_scaffolding_tools._experimental.docker.commnads import run_commands, run_command_with_grep
from django_scaffolding_tools._experimental.docker.containers import get_containers, delete_containers
from django_scaffolding_tools._experimental.docker.enums import ProjectPostgresRegExp, TerminalColor


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
    containers = get_containers(regexpression)
    delete_containers(containers, regexpression)

    d_vols = get_volumes(regexpression)
    # print(d_vols)
    if len(d_vols) != 0:
        for i, d_vol in enumerate(d_vols):
            volume_name = d_vol["name"]
            print(f'({i}) {volume_name}')

        volume_to_delete = input('Volume to delete (#, None [n], All [a]):')
        delete_volume_command = ['docker', 'volume', 'rm']
        if volume_to_delete.lower() == 'a':
            for d_vol in d_vols:
                delete_volume_command.append(d_vol['name'])
        elif volume_to_delete.isdigit():
            delete_volume_command.append(d_vols[int(volume_to_delete)]['name'])
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


def bold_text(text: str, color: Optional[TerminalColor] = None):
    if color is None:
        color_code = ''
    else:
        color_code = color
    return f'{TerminalColor.BOLD}{color_code}{text}{TerminalColor.END_COLOR}'


if __name__ == '__main__':
    reg_expr = ProjectPostgresRegExp.PCA
    reg_expr = 'new_provider'
    do_cleanup(reg_expr)
