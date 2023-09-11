from django_scaffolding_tools._experimental.docker.containers import get_containers


def test_get_containers():
    regexp =r'\.*alpha_clinic.*'
    container_list = get_containers(regexp)
    for container in  container_list:
        print(container)
