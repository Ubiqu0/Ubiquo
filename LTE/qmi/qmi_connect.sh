#!/bin/bash

APN="net2.vodafone.pt"

while true; do

        ping -I wwan0 -c 1 8.8.8.8

        if [ $? -eq 0 ]; then
                echo "Connection up, reconnect not required..."
        else
                echo "Connection down, reconnecting..."
                ip link set dev wwan0 down
                echo Y > /sys/class/net/wwan0/qmi/raw_ip
                ip link set dev wwan0 up
                qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4,apn=$APN" --client-no-release-cid
                udhcpc -q -f -n -i wwan0
        fi

        sleep 1
done
