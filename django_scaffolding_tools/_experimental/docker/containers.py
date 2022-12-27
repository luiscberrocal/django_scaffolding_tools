from django_scaffolding_tools._experimental.docker.clean_postgres import run_command_with_grep


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
