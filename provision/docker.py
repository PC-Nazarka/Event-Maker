from invoke import task

from . import common

START_COMMAND = "docker-compose -f local.yml"


@task
def build(context):
    """Build project."""
    return context.run(f"{START_COMMAND} build")


@task
def run(context):
    """Run postgres, redis, django."""
    return context.run(f"{START_COMMAND} up")


@task
def run_container(context, command=""):
    """Base template for commands with django container."""
    return context.run(f"{START_COMMAND} run --rm django {command}")


@task
def delcont(context):
    """Delete all docker containers."""
    return context.run("docker rm -f $(docker ps -a -q)")


@task
def clear(context):
    """Stop and remove all containers defined in docker-compose.

    Also remove images.

    """
    common.success("Clearing docker-compose")
    context.run(f"{START_COMMAND} rm -f")
    context.run(f"{START_COMMAND} down -v --rmi all --remove-orphans")


def docker_compose_exec(context, service, command):
    """Run ``exec`` using docker-compose.

    docker-compose exec <service> <command>
    Run commands in already running container.

    Used function so lately it can be extended to use different docker-compose
    files.

    Args:
        context: Invoke context
        service: Name of service to run command in
        command: Command to run in service container

    """
    return context.run(f"{START_COMMAND} exec {service} {command}")
