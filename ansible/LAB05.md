# Architecture overview
- Ansible version: 2.19.4
- Target VM OS and version: ubuntu server 24.04
- Role structure:
```
roles
├── app_deploy
├── common
└── docker
```
- [Why roles instead of playbooks](./LAB05.md#Key Decisions)


# Roles Documentation
## Common
- Purpose: Common setup
- Variables: `common_packages` - list of packages to install
- Handlers: None
- Dependencies: None

## Docker
- Purpose: Setup docker
- Variables: `ansible_distribution_release` - version of VM OS
- Handlers: `restart docker` - restarts docker daemon after installation
- Dependencies: `common` role

## App_deploy
- Purpose: Deploy application
- Variables:
    - `dockerhub_username`: login for dockerhub account
    - `dockerhub_password`: password for dockerhub account
    - `app_name`: name of application
    - `docker_image`: name of docker image in registry
    - `docker_image_tag`: tag of image in registry
    - `docker_port`: port inside a docker container
    - `local_port`: port on vm to connect to container
    - `port_mapping`: docker port mapping
    - `app_container_name`: name for container
- Handlers: `stop container` - stops and removes container after image updated
- Dependencies: `docker` role


# Idempotency Demonstration
## First run
```
PLAY [Provision web servers] *************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************
ok: [DevOpsVM]

TASK [common : Update apt cache] *********************************************************************************************
ok: [DevOpsVM]

TASK [common : Install common packages] **************************************************************************************
ok: [DevOpsVM]

TASK [common : Setup timezone] ***********************************************************************************************
ok: [DevOpsVM]

TASK [docker : Install Docker prerequisites] *********************************************************************************
ok: [DevOpsVM]

TASK [docker : Add Docker GPG key] *******************************************************************************************
ok: [DevOpsVM]

TASK [docker : Add Docker repository] ****************************************************************************************
ok: [DevOpsVM]

TASK [docker : Install Docker] ***********************************************************************************************
changed: [DevOpsVM]

RUNNING HANDLER [docker : restart docker] ************************************************************************************
changed: [DevOpsVM]

PLAY RECAP *******************************************************************************************************************
DevOpsVM                   : ok=9    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Second run
```
PLAY [Provision web servers] *******************************************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [common : Update apt cache] ***************************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [common : Install common packages] ********************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [common : Setup timezone] *****************************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [docker : Install Docker prerequisites] ***************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [docker : Add Docker GPG key] *************************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [docker : Add Docker repository] **********************************************************************************************************************************************************
ok: [DevOpsVM]

TASK [docker : Install Docker] *****************************************************************************************************************************************************************
ok: [DevOpsVM]

PLAY RECAP *************************************************************************************************************************************************************************************
DevOpsVM                   : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
## Analysis
What changed: Docker installed
What didn't change second time: Nothing changed

## Explanation
First run installs docker(and triggers restart service handler)
and this step is not runned on second run, since docker
is already installed


# Ansible Vault Usage
- I store credentilas securely with usage of Ansible Vault
- I manage vault password with gitignored password file
- [Example of encrypted file](./roles/app_deploy/defaults/main.yml)
- [Why ansible Vault is important](./LAB05.md#Key Decisions)


# Deployment Verification
Output of `deploy.yml` run
```
PLAY [Deploy application] ****************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************
ok: [DevOpsVM]

TASK [app_deploy : Login] ****************************************************************************************************
ok: [DevOpsVM]

TASK [app_deploy : Pull Image] ***********************************************************************************************
ok: [DevOpsVM]

TASK [app_deploy : run container] ********************************************************************************************
changed: [DevOpsVM]

TASK [app_deploy : Verify Container Running] *********************************************************************************
ok: [DevOpsVM]

TASK [app_deploy : Check Health] *********************************************************************************************
ok: [DevOpsVM]

PLAY RECAP *******************************************************************************************************************
DevOpsVM                   : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
`docker ps` output:
```
CONTAINER ID   IMAGE                              COMMAND                  CREATED         STATUS         PORTS                      NAMES
aeca03f980be   ub3rch/infoservice:python-latest   "fastapi run infoser…"   8 seconds ago   Up 8 seconds   127.0.0.1:5000->8000/tcp   Xantusia
```
`curl` outputs:
- `curl http:/127.0.0.1:5000/`
```
{"system":{"hostname":"aeca03f980be","platform":"Linux","platform_version":"#100-Ubuntu SMP PREEMPT_DYNAMIC Tue Jan 13 16:40:06 UTC 2026","architecture":"x86_64","python_version":"3.13.12"},"service":{"name":"DevOps Info Service","version":"0.1.1","description":"DevOps course info service","framework":"fastapi"},"runtime":{"uptime_seconds":64,"uptime_human":"0 hours, 1 minutes","current_time":"2026-02-24T12:13:04.779840+00:00","timezone":"UTC"},"request":{"client_ip":"172.17.0.1","user_agent":"curl/8.5.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}
```
- `curl http:/127.0.0.1:5000/health`
```
{"status":"healthy","timestamp":"2026-02-24T12:13:09.770103+00:00","uptime_seconds":69}
```

# Key Decisions
## Why roles instead of playbooks?
Roles give reusability and modularity to playbooks

## How do roles improve reusability?
Different playbooks can use same roles to
usilize common setup steps

## What makes task idempotent?
Since tasks are declarative, checking
if declared state is already reached, then
the step is skipped.

## How do handlers improve efficiency?
Handler run only if trigerred from
tasks. Since tasks skipped in most
of cases (since they are idempotent), then
Handler tasks not even check their state, but
skipped instantly.

## Why is Ansible Vault necessary?
Ansible Vault allows storing configuration
in version control, at the same time keeping
secrets protected, since vaults are encrypted.
