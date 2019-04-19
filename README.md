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

Now try running it:
``` sh
python main.py
```

Deactivate the virtual environment using: 
``` sh
deactivate
```

## Required `rc.local` changes
```sh 

```
