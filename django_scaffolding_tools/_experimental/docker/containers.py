from typing import List, Dict, Any

from tqdm import tqdm

from django_scaffolding_tools._experimental.docker.commnads import run_commands, run_command_with_grep


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


def delete_containers(containers: List[Dict[str, Any]], reg_expression: str):
    if len(containers) != 0:
        for i, container in enumerate(containers):
            print(f'{i} {container["container_id"]} {container["image"]} {container["name"]}')
        container_to_delete = input(f'Type the number of the container to delete (#, None [n], All [all]):')
        if container_to_delete.isdigit():
            container_id = int(container_to_delete)

            delete_container_command = ['docker', 'rm', containers[container_id]['container_id']]
            dc_res, errors = run_commands(delete_container_command)
            print(f'Deleted container {dc_res}')
        elif container_to_delete.lower() == 'all':
            for container in tqdm(containers):
                delete_container_command = ['docker', 'rm', container['container_id']]
                dc_res, errors = run_commands(delete_container_command)
                print(f'Deleted container {dc_res}')
        else:
            print('No containers were deleted')
    else:
        print(f'No container found for {reg_expression}')


def main(reg_expression: str):
    containers = get_containers(reg_expression)
    delete_containers(containers, reg_expression)


if __name__ == '__main__':
    r = r"seleniumlms"
    main(r)
