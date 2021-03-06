#!/bin/bash +e
# catch signals as PID 1 in a container

# SIGNAL-handler
term_handler() {

  echo "terminating ssh ..."
  /etc/init.d/ssh stop

  exit 143; # 128 + 15 -- SIGTERM
}

# on callback, stop all started processes in term_handler
trap 'kill ${!}; term_handler' INT KILL TERM QUIT TSTP STOP HUP

# run applications in the background
echo "starting ssh ..."
/etc/init.d/ssh start

echo "start python drive application"
sudo nohup python /home/pi/opc-ua-server/drive.py &
#sudo python /home/pi/opc-ua-server/drive.py
echo "starting opc-ua-server"
/home/pi/opc-ua-server/StepMotorOpcServer

# wait forever not to exit the container
while true
do
  tail -f /dev/null & wait ${!}
done

exit 0