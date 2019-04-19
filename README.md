# fsae-apollo

This project contains the bare bones for the Brown FSAE Driver Feedback Project. Feel free to play around with `main.py` and figure out how PyQt5 works. 

## Compile Qt 

To compile the Qt package, you will need to run the following: 

```
cd build/
# Generate the Makefile 
/usr/local/Trolltech/Qt-5.10.0-nexell32-sdk/bin/qmake ../display/QtE-Demo.pro 
# idk, it just works
make
```

## Pi setup

wpa_supplicant.conf
```sh
update_config=1
country=CN

network={
        ssid="Rhodedendron"
        psk="********"
}
```

rc.local
```sh
exec 1>/tmp/rc.local.log 2>&1  # send stdout and stderr from rc.local to a log file
set -x

. /usr/bin/setqt5env
/usr/bin/lcd2usb_print "CPU: {{CPU}}" "Mem: {{MEM}}" "IP: {{IP}}" "LoadAvg: {{LOADAVG}}" 2>&1 > /dev/null&
##/opt/QtE-Demo/run.sh&

bash /root/fsae-apollo/master_run.sh &
```
/root/.bashrc
```sh
. /usr/bin/setqt5env

source ~/fsae-apollo/venv/bin/activate
cd ~
```

TODO: Flash a friendlycore image onto the NanoPi and get it to boot reliably. I tried with the image they have at the following link, but it seemed to have console logging disabled and/or would not boot. https://drive.google.com/drive/folders/1177wtytvjXfSYFHc6MyalHUWK_ilKIlr

## Install fsae-apollo 
You will need Python 3.7 installed to run fsae-apollo. 

Set up your working environment: 
``` sh
git clone https://github.com/peterhuson/fsae-apollo.git && cd fsae-apollo
python3 -m venv venv
```

Activate your virtual environment, and install required packages: 
``` sh 
source venv/bin/activate
pip install -r requirements.txt
```

Deactivate the virtual environment using: 
``` sh
deactivate
```