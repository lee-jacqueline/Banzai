# Banzai - AppSec Pipeline

Project Description:

## Setup

install dependencies
* `pip install defectdojo_api`

run environment
* `sudo docker-compose up`

browser access to DefectDojo
* `localhost:8000`

browser access to StackStorm GUI
* `localhost`

## Docker Network Setup
Docker Containers must be within the same network to be able to talk to each other. When Docker spins up containers, it assigns each container to the default bridge network. Due to the AppSec Pipeline setup, some services within the pipeline connect to a different default bridge network. For example, the StackStorm container will be on a different network, so you must manually connect it to the main `banzaireal_default` bridge network.

Connect containers to the same Docker bridge network
* sudo docker network connect [default_bridge_name] [container_name]

## Data Persistence

See docker-compose.yml for content that persists between your local machine / containers.

__StackStorm Packs__
* local: `./StackStorm/packs.dev`
* container: `./opt/stackstorm/packs.dev`
* Banzai-specific rules, actions, workflows are defined in packs.dev.

## Issues ##

### StackStorm Container: apt-get install ###

`apt-get install [package]` within the containers may have issues with DNS resolution if you are using Ubuntu due to a Network Manager feature..
To fix this, navigate to `/etc/NetworkManager/NetworkManager.conf` and comment out `dns=dnsmasq` line.

OS tested with issues:
* Ubuntu 16.04
* Ubuntu 14.04
OS tested without issues:
* MacOS High Sierra

### Docker-Compose Network Bridge ###

Docker adds containers to a "default bridge network" when they are first run. Due to the Banzai implementation, the StackStorm container will be connected to a separate bridge network than the DefectDojo container. To solve this issue, you must use the command `sudo docker network connect [NETWORK_NAME] [CONTAINER]` to connect your StackStorm container to the network that DefectDojo belongs to, so they can communicate.

See more about Docker Networking here: https://docs.docker.com/engine/userguide/networking/

### Stackstorm Pack Virtualenv - Custom method used in DefectDojo Package ###

`defectdojo_api` is a python wrapper for DefectDojo's API used within the AppSec Pipeline. Currently, the public package does not support the `/reimportscan` API, so we have implemented a method to facilitate this.

The additional method must be included in the Banzai Pack's virtualenv. To do this:
* Open a shell in the StackStorm Docker container. `sudo docker exec -it [stackstorm_container_name] bash`
* Navigate to the main wrapper python file `/opt/stackstorm/virtualenvs/banzai/lib/python2.7/site-packages/defectdojo_api/defectdojo.py` within the container.
* Add the additional code to support the reimport_scan API.

__NOTE: This only needs to be done upon initial setup of the AppSec Pipeline, when a fresh StackStorm container is created. This issue should be solved by persisting the custom method via. mounting a Docker volume.__

### Port Clashes ###

If a port number defined in the docker-compose.yaml is already being used by a running application on your host machine, docker-compose will fail to start up.
You must either stop the application that is using the port, or change the port number in the docker-compose.yaml config file to an unused port number.

For more instructions on editing Docker Compose configuration files, please see: https://docs.docker.com/compose/overview/
