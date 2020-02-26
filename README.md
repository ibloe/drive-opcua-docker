# drive-opcua-docker
Docker Container with OPC UA server to drive a motor with the NPIX DI DO Module on netPi

## Usage 
1. Open the Docker user interface
2. Edit the parameters under **Containers > Add Container**
	* **Image**: `ibloe/drive-opcua-docker:latest`
	* **Network > Network**: `host`
	* **Restart policy** : `always`
	* **Runtime & Ressources > Priviliged mode** : true
	* **Runtime & Ressources > Devices > add device** : `/dev/gpiomem -> /dev/gpiomem`

3. Press the button **Actions > Start container**

## Hardware 
Npix IO Module PinOut, drive IOs with 24V:



| | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|
| External GND| PWM| Direction | Enable (Out) |-| External 24V|
| **ISO0V** | **OUT0** | **OUT1** | **OUT2** | **OUT3** |**24V**|
| | | | | | |
| **ISO0V** | **IN0**  | **IN1**  | **IN2**  | **IN3**  |**24V**|
| -| Enable (In)| -| -| -|-|
| | | | | | |
