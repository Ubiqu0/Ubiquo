# QMI connection

These files can be used in case you have an LTE module with 4G or 5G. To install the module and establish an internet connection you first need to define what is the **APN** your service uses. Edit the [qmi_connect.sh](https://github.com/Ubiqu0/Ubiquo/blob/main/LTE/qmi/qmi_connect.sh) file accordingly. 

With the correct APN defined, run the following commands:

(note that this instalation script assumes the SIM card is not protected with a PIN number)

```
chmod +x install_qmi.sh
sudo ./install_qmi.sh
```
