# FSAE-Apollo built on QtE-Demo

# Background Template
In order to load different backgrounds you must: 
1. Put the image in /display/backgrounds
2. Add the file as a line to `main.qrc` -> `<file>backgrounds/CompetitionRaceTemplate.png</file>`
3. Change the line in `mainwidget.cpp` with `bg(QPixmap(":/backgrounds/***.png"))` to the name of your png

## How to cross-compile
It is recommended that you use docker to cross-compile your qt app:
https://github.com/friendlyarm/friendlyelec-ubuntu16-docker

To build a local compilation environment, it is recommended to install ubuntu 16.04 64-bit system, and then refer to the following file to install relevant packages in ubuntu:
https://github.com/friendlyarm/friendlyelec-ubuntu16-docker/blob/master/Dockerfile

