[![aioneers_logo](etc/aioneers_logo.png)](https://aioneers.com/about/open-source-aio-data-science/)
![Python_Version](https://img.shields.io/badge/Python%20Version-3.7%20%7C%203.8-blue)
[![Documentation Status](https://readthedocs.org/projects/aioneersaio/badge/?version=latest)](https://aioneersaio.readthedocs.io/en/latest/reference)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Be%20kind%20to%20each%20other-yellow)](CODE_OF_CONDUCT.md)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)
[![aioneers](https://img.shields.io/badge/With%20love%20from-aioneers-blue)](https://aioneers.com/about/open-source-aio-data-science/)

# Our Motivation

At [**aioneers**](https://aioneers.com/), we place a lot of importance on giving back to our community.<br>
<br>
We operate in the field of supply chains, helping organizations close their supply chain performance gap whilst
retaining resilience and furthering sustainability. ([See our Manifesto](https://aioneers.com/about/why/)).<br>
<br>
We want a part of our work to be providing the supply chain data science community with open source,
free-to-use code for building applications. This will be accompanied by insightful explanations and tutorials,
so that data scientists across the world can achieve the same things we aim for; strengthened resilience, sustainability, and an optimized supply chain performance.<br>
<br>
We happily welcome contributions from anyone sharing the same goal, to build and spread better supply chain data science tools.<br>
<br>
We are dedicated to spending up to 5% of our time on sharing, exchanging and curating guides,
with the end goal of accelerating our community’s efforts to build a more sustainable world.
<br>
<br>
The documentation can be found here: [![Documentation Status](https://readthedocs.org/projects/aioneersaio/badge/?version=latest)](https://aioneersaio.readthedocs.io/en/latest/?badge=latest)

# Install

## Clone the repository

Clone the master branch of the Git repository

```
$ git clone -b master https://github.com/aioneers/aio
```

## Install the Python library

Install the library in a way that the most recent version on the local machine is always used

```
$ pip install -e aio
```

## Install and configure Azure CLI

For a lot of our functions we use the Azure CLI repository.

To install the current release, Azure CLI is necessary as a prerequisite: [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

On Windows, the installation guide can be found here: [Windows az CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)

On macOS the Azure CLI can be installed with Homebrew on a command line: [macOS az CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-macos)

```
$ brew update && brew install azure-cli
```

On Linux, the Azure CLI can be installed via apt: [Linux az CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux)

```
$ curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Then the Azure CLI needs to be signed, which is easiest with this command (for all systems):

```
$ az login
```

<!-- ## Install the Python library on Databricks

from pathlib import Path
import shlex
import subprocess
import os

# function to run and print output from shell

def run_process_func(exe):
p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True: # returns None while subprocess is running
retcode = p.poll()
line = p.stdout.readline().decode("utf8")
yield line
if retcode is not None:
break

def run_process(exe):
print(f"running cmd: {exe}")
for line in run_process_func(shlex.split(exe)):
print(line)

# add ssh key

ssh_key = dbutils.secrets.get(scope="aio-data-science-key", key="ssh-key")
filename = Path("/root/.ssh/id_rsa")
filename.parent.mkdir(parents=True, exist_ok=True)
with open(filename, "w") as f:
f.write(ssh_key)

# add known hosts so that the ssh does not ask to proceed

filename = Path("/root/.ssh/known_hosts")
known_hosts = """ssh.dev.azure.com,51.144.61.32 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7Hr1oTWqNqOlzGJOfGJ4NakVyIzf1rXYd4d7wo6jBlkLvCA4odBlL0mDUyZ0/QUfTTqeu+tm22gOsv+VrVTMk6vwRU75gY/y9ut5Mb3bR5BV58dKXyq9A9UeB5Cakehn5Zgm6x1mKoVyf+FFn26iYqXJRgzIZZcZ5V6hrE0Qg39kZm4az48o0AUbf6Sp4SLdvnuMa2sVNwHBboS7EJkm57XQPVU3/QpyNLHbWDdzwtrlS+ez30S3AdYhLKEOxAG8weOnyrtLJAUen9mTkol8oII1edf7mWWbWVf0nBmly21+nZcmCTISQBtdcyPaEno7fFQMDD26/s0lfKob4Kw8H
"""
with open(filename, "w") as f:
f.write(known_hosts)

# Do not check the ip address, only the dns address

filename = Path("/root/.ssh/ssh_config")
ssh_config = "CheckHostIP no"
with open(filename, "w") as f:
f.write(ssh_config)

# give a more detailed log for ssh

os.environ["GIT_SSH_COMMAND"] = "ssh -v"

# change access rights to owner for the key

run_process("chmod 400 /root/.ssh/id_rsa")

# remove the directory if exists

run_process("rm aio-data-science -R")

# copy files from git to current directory

run_process(
"git clone ssh://git@ssh.dev.azure.com/v3/Aio-Platform/aio-platform/aio-data-science"
)

# Databricks command to install a library

%pip install -U "aio-data-science/aio_data_science_py"

import aio_data_science_py as aio
aio.set_dbutils(dbutils) -->

# Contribution guidelines

First of all, thank you for considering contributing to this repository. Any contribution, from correcting a typo, forking the repo to adding another function or an insightful tutorial is very welcome.

**If you want to contribute to aioneers, be sure to review the
[contribution guidelines](CONTRIBUTING.md). This project adheres to aioneers'
[code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to
uphold this code.**

**We use [GitHub issues](https://github.com/aioneers/aio/issues) for
tracking requests and bugs and please direct specific questions to
[maintainer e-mail address](mailto:maintainer@@aioneers.com).**

# License

[![License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)
