#!/bin/sh

while true; do

        ping -I wwan0 -c 1 8.8.8.8

        if [ $? -eq 0 ]; then
                echo "Connection up, reconnect not required..."
        else
                echo "Connection down, reconnecting..."
                sudo /home/pi/Ubiquo/qmi/SIM8200-M2_5G_HAT_code/Goonline/simcom-cm
        fi

        sleep 1
done
