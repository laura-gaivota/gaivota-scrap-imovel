# Gaivota: python-nilo-crawler (gaivota_python_nilo_crawler)
[![Python Version](https://img.shields.io/badge/3.8.0%2B-green)](https://pypi.python.org/pypi/ansicolortags/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: Flake8](https://img.shields.io/badge/code%20style-flake8-000.svg)](https://flake8.pycqa.org/en/latest/)
[![Code style: Isort](https://img.shields.io/badge/code%20style-isort-000.svg)](https://pypi.org/project/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Jenkins pipeline status](https://img.shields.io/badge/Build-NOT_SET-red)](https://jenkins.gaivota.ai/)
[![Sonarqube quality](https://img.shields.io/badge/Sonarqube-NOT_SET-red)](http://sonarqube.gaivota.ai/)

TODO: update description
This projects aims to crawl data from a site

### :warning: WARNING: This repository required GDAL in a version that is not available to most Ubuntu distros, we recommend Make or docker-compose commands to develop crawlers

### Technologies & Tools

* [Python](https://python.org): Current version is using Python 3.8.5.
* [pip](https://pip.pypa.io/en/stable/): used to manage project dependency.
* [poetry](https://python-poetry.org/): used to manage project/linter configuration.
* [pre-commit](https://pre-commit.com/): used to enable code policies.
* [Scrapy](https://docs.scrapy.org/): used as framework to build crawlers.

Check [requirements.txt](/requirements.txt) for dependencies. </br>
Check [dev-requirements.txt](/dev-requirements.txt) for test dependencies.

## Database and Infrastructure
Don't forget to configure your crawler migrations on our [Database Migrations Repository](https://github.com/gaivota-ai/gaivota-postgres-db-layers)
</br> The Make commands will use your migrations **if they are in a branch of the same name**  or they will use the develop branch
using the command

You can run the docker-compose configuration individually running: `make configure-database`

To configure your infrastructure, create a repository using [Lara]() and then use our cookiecuter
[Infrastrucute Manifest Cookiecutter](https://github.com/gaivota-ai/gaivota-cookiecutter-argoflow-manifest)


## Install and configure

First, clone the project, then follow proper instructions for your system.
Keep in mind that some dependencies relies on others that cannot be available in some OS or distribution.
Instructions bellow were validated before being written here.

Makefile can always be checked to see what is being done and can be replicated to another environments.

### Ubuntu

Make is needed to automatically install everything:

`sudo apt install make`

After, you can just execute the command bellow, than all dependencies and environment will be installed.

`make install-all`

To see all possible commands, execute:

`make help`

### Windows

#### WSL

You can use [WSL](https://docs.microsoft.com/en-us/windows/wsl/) to install Ubuntu bash support on Windows (10+) than, follow Ubuntu instructions.

#### Powershell

[TODO]: Add powershell instructions here.

### Running

Ensure that you have set all environment variables described in .env.template. You can rename it to .env and just set the variables with the right values.

* On Docker Compose to run the crawler
```
make docker-run
```

* On Docker Compose to run any command
```
make docker-bash
export PATH=/root/.local/bin:$PATH
<BASH OR PYTHON COMMAND>
```
