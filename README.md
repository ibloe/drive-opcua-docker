# drive-opcua-docker
Docker Container with OPC UA server to drive a motor with the NPIX DI DO Module on netPi

## Usage 
1. Open the Docker user interface
2. Edit the parameters under **Containers > Add Container**
	* **Image**: `ibloe/drive-opcua-docker:latest`
	* **Port mapping > map additional port**: `22 -> 22`
	* **Port mapping > map additional port**: `4840 -> 4840`
	* **Network > Network**: `host`
	* **Restart policy** : `always`
	* **Runtime & Ressources > Priviliged mode** : true
	* **Runtime & Ressources > Devices > add device** : `/dev/gpiomem -> /dev/gpiomem`

3. Press the button **Actions > Start container**