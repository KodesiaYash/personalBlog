from invoke import task

@task
def run(c):
    c.run("uvicorn main:app --reload")

@task
def lint(c):
    c.run("black . && isort . && flake8 .")

@task
def test(c):
    c.run("pytest")