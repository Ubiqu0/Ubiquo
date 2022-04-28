#!/bin/bash


apt install libqmi-utils udhcpc

cp qmi/qmi_connect.service /etc/systemd/system

systemctl daemon-reload

echo "Do you want to activate the connection on reboot? [Y,n]"
read answer
if [  $answer == "Y"  ]; then
      systemctl enable qmi_connect.service
fi
systemctl start qmi_connect.service
echo ""
echo "Disable automatic start with reboot:"
echo ""
echo "  sudo systemctl disable qmi_connect.service"
echo "***"
