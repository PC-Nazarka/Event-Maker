from invoke import Collection

from provision import django, docker, linters, project, tests

ns = Collection(
    django,
    docker,
    linters,
    project,
    tests,
)

ns.configure(
    dict(
        run=dict(
            pty=True,
            echo=True,
        ),
    ),
)
