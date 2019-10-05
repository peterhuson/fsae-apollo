// Copyright (C) Guangzhou FriendlyARM Computer Tech. Co., Ltd.
// (http://www.friendlyarm.com)
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, you can access it online at
// http://www.gnu.org/licenses/gpl-2.0.html.

#include "mainwidget.h"
#include "util.h"
#include "sys/sysinfo.h"
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include "boardtype_friendlyelec.h"
#include "sys/sysinfo.h"
#include "util.h"

#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int fd1;
fd_set set;
struct timeval timeout;
int rv;

TMainWidget::TMainWidget(QWidget *parent, bool transparency, const QString &surl) :
    QWidget(parent),
    currentDisplayMode(debug), // `debug`, `acceleration`, and `regular` enum
    bg(QPixmap(":/backgrounds/blueno.png")),
    transparent(transparency),
    sourceCodeUrl(surl) {
    const QString qwsDisplay = QString(qgetenv("QWS_DISPLAY"));
    isUsingTFT28LCD = qwsDisplay.contains("/dev/fb-st7789s");
    tft28LCDThread = NULL;
    for (unsigned int i = 0; i < sizeof(progresses) / sizeof(int); i++) {
        progresses[i] = 0;
    }
    if (isUsingTFT28LCD) {
        tft28LCDThread = new TFT28LCDThread(this, this);
        tft28LCDThread->start();
    }

    mpKeepAliveTimer = new QTimer();
    mpKeepAliveTimer->setSingleShot(false);
    QObject::connect(mpKeepAliveTimer, SIGNAL(timeout()), this, SLOT(onKeepAlive()));
    mpKeepAliveTimer->start(35);

    gettimeofday(&startTime, NULL);

    // FIFO file path
    const char *myfifo = "/tmp/myfifo2";
    mkfifo(myfifo, 0666);
    fd1 = open(myfifo, O_RDONLY);
    timeout.tv_sec = 0;
    timeout.tv_usec = 4000;
}

void TMainWidget::resizeEvent(QResizeEvent *) {
    // Do nothing.
}

static inline double time_diff(struct timeval _tstart, struct timeval _tend) {
    double t1 = 0.;
    double t2 = 0.;

    t1 = ((double) _tstart.tv_sec * 1000 + (double) _tstart.tv_usec / 1000.0);
    t2 = ((double) _tend.tv_sec * 1000 + (double) _tend.tv_usec / 1000.0);

    return t2 - t1;
}

char *readline(int fd, char *buffer) {
    char c;
    int counter = 0;
    while (read(fd, &c, 1) != 0) {
        if (c == '\n') {
            break;
        }
        buffer[counter++] = c;
    }
    return buffer;
}

void TMainWidget::onKeepAlive() {
    static char ipStr[50];
    memset(ipStr, 0, sizeof(ipStr));
    int ret = Util::getIPAddress("eth0", ipStr, 49);
    if (ret == 0) {
        eth0IP = QString(ipStr);
    } else {
        eth0IP = "0.0.0.0";
    }

    memset(ipStr, 0, sizeof(ipStr));
    ret = Util::getIPAddress("wlan0", ipStr, 49);
    if (ret == 0) {
        wlan0IP = QString(ipStr);
    } else {
        wlan0IP = "0.0.0.0";
    }

    struct sysinfo sys_info;
    if (sysinfo(&sys_info) == 0) {
        qint32 totalmem = (qint32)(sys_info.totalram / 1048576);
        qint32 freemem = (qint32)(sys_info.freeram / 1048576); // divide by 1024*1024 = 1048576
        // float f = ((sys_info.totalram-sys_info.freeram)*1.0/sys_info.totalram)*100;
        // memInfo = QString("%1%,F%2MB").arg(int(f)).arg(freemem);
        memInfo = QString("%1/%2 MB").arg(totalmem - freemem).arg(totalmem);
        usageInfo = QString("%1 Bytes").arg(sys_info.totalram - sys_info.freeram);
    }

    BoardHardwareInfo *retBoardInfo;
    int boardId;
    boardId = getBoardType(&retBoardInfo);
    if (boardId >= 0) {
        if ((boardId >= S5P4418_BASE && boardId <= S5P4418_MAX) || (boardId >= S5P6818_BASE && boardId <= S5P6818_MAX)) {
            QString templ_filename("/sys/class/hwmon/hwmon0/device/temp_label");
            QString tempm_filename("/sys/class/hwmon/hwmon0/device/temp_max");
            QFile f1(templ_filename);
            QFile f2(tempm_filename);
            if (f1.exists()) {
                currentCPUTemp = Util::readFile(templ_filename).simplified();
            }
            if (f2.exists()) {
                maxCPUTemp = Util::readFile(tempm_filename).simplified();
            }

        } else if (boardId >= ALLWINNER_BASE && boardId <= ALLWINNER_MAX) {
            QString str;
            bool ok = false;
            QString templ_filename("/sys/class/thermal/thermal_zone0/temp");
            QFile f3(templ_filename);
            if (f3.exists()) {
                float _currentCPUTemp = Util::readFile(templ_filename).simplified().toInt(&ok);
                if (ok) {
                    if (_currentCPUTemp > 1000) {
                        _currentCPUTemp = _currentCPUTemp / 1000;
                    }
                    currentCPUTemp = str.sprintf("%.1f", _currentCPUTemp);
                    maxCPUTemp = currentCPUTemp;
                }
            }
        }

        // Temp Parsing

        QString str;
        bool ok = false;
        QString templ_filename("/sys/class/thermal/thermal_zone0/temp");
        QFile f3(templ_filename);
        if (f3.exists()) {
            float _currentCPUTemp = Util::readFile(templ_filename).simplified().toInt(&ok);
            if (ok) {
                if (_currentCPUTemp > 1000) {
                    _currentCPUTemp = _currentCPUTemp / 1000;
                }
                currentCPUTemp = str.sprintf("%.1f", _currentCPUTemp);
                maxCPUTemp = currentCPUTemp;
            }
        }

        bool ok1 = false;
        float _currentCPUTemp = currentCPUTemp.toInt(&ok1);
        if (_currentCPUTemp > 1000.0 && ok1) {
            QString str;
            currentCPUTemp = str.sprintf("%.1f", _currentCPUTemp / 1000.0);
        }
        bool ok2 = false;
        float _maxCPUTemp = maxCPUTemp.toInt(&ok2);
        if (_maxCPUTemp > 1000.0 && ok2) {
            QString str;
            maxCPUTemp = str.sprintf("%.1f", _maxCPUTemp / 1000.0);
        }
    }

    QString contents = Util::readFile("/proc/loadavg").simplified();
    QStringList values = contents.split(" ");
    int vCount = 2;
    loadAvg = "";
    foreach (const QString &v, values) {
        QString str = v.simplified();
        if (!str.isEmpty()) {
            if (!loadAvg.isEmpty()) {
                loadAvg += "/";
            }
            bool ok = false;
            float f = str.toFloat(&ok);
            if (ok) {
                QString toprint;
                loadAvg += toprint.sprintf("%.1f", f);
            }
            vCount--;
            if (vCount <= 0) {
                break;
            }
        }
    }

    QString fileName = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq";
    QFile f5(fileName);
    freqStr = "";
    if (f5.exists()) {
        QString str = Util::readFile(fileName).simplified();
        bool ok = false;
        int freq = str.toInt(&ok, 10);

        if (ok) {
            QString str;
            if (freq > 1000000) {
                freqStr = str.sprintf("%.1fG", freq * 1.0 / 1000000);
            } else if (freq > 1000) {
                freqStr = str.sprintf("%dM", freq / 1000);
            } else {
                freqStr = str.sprintf("%d", freq);
            }
        }
    }

    struct timeval endTime;
    gettimeofday(&endTime, NULL);
    double global_time = time_diff(startTime, endTime);
    timeSinceStart = "";
    QString timestr;
    timeSinceStart = timestr.sprintf("%.2fms", global_time);

    // First open in read only and read
    // char str1[20];
    // size_t bytes_read = read(fd1, str1, 10);
    // size_t bytes_read = read(fd1, str1, 10);
    // if (bytes_read <= 6) {
    //     printf("Got garbage string: %s\n", str1);
    //     return;
    // }
    for (int i = 0; i < 10; i++) {
        char str1[20];
        memset(str1, 0, 20);

        FD_ZERO(&set); /* clear the set */
        FD_SET(fd1, &set); /* add our file descriptor to the set */

        rv = select(fd1 + 1, &set, NULL, NULL, &timeout);
        if (rv == -1)
            perror("select \n"); /* an error accured */
        else if (rv == 0) {
            // printf("timeout \n"); /* a timeout occured */
            continue;
        } else
            readline(fd1, str1);
        // printf("iteration: %d Data: %s\n", i, str1);

        QString value = QString(&str1[5]);
        // printf("%s Value: %s\n", str1, value.toStdString().c_str());
        // printf("strncmp for oilp: %d\n", strncmp(str1, "oilp", 4));
        // printf("strncmp for ctmp: %d\n", strncmp(str1, "ctmp", 4));

        if (strncmp(str1, "oilp", 4) == 0) {
            oilP = value;
        } else if (strncmp(str1, "ctmp", 4) == 0) {
            ctmP = value;
        } else if (strncmp(str1, "vbat", 4) == 0) {
            vbaT = value;
        } else if (strncmp(str1, "lamb", 4) == 0) {
            lamB = value;
        } else if (strncmp(str1, "lspd", 4) == 0) {
            lspD = value;
        } else if (strncmp(str1, "rspd", 4) == 0) {
            rspD = value;
        } else if (strncmp(str1, "rpm_", 4) == 0) {
            rpM_ = value;
        } else if (strncmp(str1, "tps_", 4) == 0) {
            tpS_ = value;
        } else if (strncmp(str1, "accy", 4) == 0) {
            accY = value;
        } else if (strncmp(str1, "accz", 4) == 0) {
            accZ = value;
        } else {
            printf("Unknown string: '%s'\n", str1);
            return;
        }
    }

    update();
}

void TMainWidget::drawAccelerationScreen(QPainter &p) {
    p.fillRect(0, 0, width(), height(), QBrush(QColor(200, 255, 200)));
    p.drawPixmap(0, 0, width(), height(), bg);
    p.setPen(QPen(QColor(255, 255, 255)));

    int smallHeight = 40;
    p.setFont(QFont("Courier",45, QFont::Bold));
    p.drawText(40, 20, 720, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("RPM"));
    p.drawText(40, 420, 720, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("MPH"));
    // p.drawText(590, 210, 150, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("RPM"));
    // p.drawText(470, 430, 150, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("MPH"));


    int valuespacing = height() / 2;
    int itemHeight = valuespacing;
    int bigborder = 80;
    p.setFont(QFont("Courier",170, QFont::Bold));
    p.drawText(40, 80, 720, 170, Qt::AlignRight | Qt::AlignVCenter, rpM_);
    p.drawText(40, 250, 720, 170, Qt::AlignRight | Qt::AlignVCenter, rspD);
}

void TMainWidget::drawDebugScreen(QPainter &p) {
    p.fillRect(0, 0, width(), height(), QBrush(QColor(255, 255, 255)));

    p.setPen(QPen(QColor(0, 0, 0)));

    int rightborder = 15;

    int valuespacing = height() / 3 - 20;
    int rightcolX = width()/2 + rightborder;
    int leftcolX = rightborder;
    int itemWidth = (width() / 2) - rightborder * 2;
    int itemHeight = valuespacing;

    p.setFont(QFont("Courier",110, QFont::Bold));
    p.drawText(leftcolX, valuespacing * 1, itemWidth, itemHeight, Qt::AlignRight | Qt::AlignVCenter, ctmP);
    p.drawText(leftcolX, valuespacing * 2, itemWidth, itemHeight, Qt::AlignRight | Qt::AlignVCenter, vbaT);
    p.drawText(rightcolX, valuespacing * 1, itemWidth, itemHeight, Qt::AlignRight | Qt::AlignVCenter, oilP);
    p.drawText(rightcolX, valuespacing * 2, itemWidth, itemHeight, Qt::AlignRight | Qt::AlignVCenter, lamB);

    int bigborder = 120;
    p.setFont(QFont("Courier",130, QFont::Bold));
    p.drawText(bigborder, valuespacing * 0, width() - bigborder * 2, itemHeight, Qt::AlignRight | Qt::AlignVCenter, rpM_);

    int smallHeight = 40;
    p.setFont(QFont("Courier",30, QFont::Bold));
    p.drawText(40, 80, 750, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("RPM"));
    p.drawText(leftcolX, valuespacing * 1 + 120, itemWidth, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("Water Tmp"));
    p.drawText(leftcolX, valuespacing * 2 + 120, itemWidth, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("Batt V"));
    p.drawText(rightcolX, valuespacing * 1 + 120, itemWidth, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("Oil psi"));
    p.drawText(rightcolX, valuespacing * 2 + 120, itemWidth, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("Lambda"));

    QString ip = eth0IP;
    if (ip == "0.0.0.0") {
        ip = wlan0IP;
    }
    int tinyHeight = 20;
    int space = 3;
    p.setFont(QFont("Courier",11, QFont::Bold));
    p.drawText(space,
               tinyHeight * 23,
               width() - space * 2,
               tinyHeight,
               Qt::AlignLeft | Qt::AlignVCenter,
               QString("CPU:%1/T%2C").arg(freqStr).arg(currentCPUTemp));
    p.drawText(
        space * 52, tinyHeight * 23, width() - space * 2, tinyHeight, Qt::AlignLeft | Qt::AlignVCenter, QString("Memory: %1").arg(memInfo));
    p.drawText(space * 120,
               tinyHeight * 23,
               width() - space * 2,
               tinyHeight,
               Qt::AlignLeft | Qt::AlignVCenter,
               QString("Load:%1").arg(loadAvg));
    p.drawText(space * 180, tinyHeight * 23, width() - space * 2, tinyHeight, Qt::AlignLeft | Qt::AlignVCenter, QString("%1").arg(ip));
    p.drawText(5, tinyHeight * 23, width() - space * 9, tinyHeight, Qt::AlignRight | Qt::AlignVCenter, QString("t=%1").arg(timeSinceStart));
}

void TMainWidget::drawEnduranceScreen(QPainter &p) {
    p.fillRect(0, 0, width(), height(), QBrush(QColor(200, 255, 200)));
    p.drawPixmap(0, 0, width(), height(), bg);
    p.setPen(QPen(QColor(255, 255, 255)));

    int smallHeight = 40;
    p.setFont(QFont("Courier",45, QFont::Bold));
    p.drawText(40, 20, 720, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("MPH"));
    p.drawText(40, 420, 720, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("WatTmp"));
    p.drawText(590, 210, 150, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("OilPre"));
    // p.drawText(470, 430, 150, smallHeight, Qt::AlignRight | Qt::AlignVCenter, QString("MPH"));


    int valuespacing = height() / 2;
    int itemHeight = valuespacing;
    int bigborder = 80;
    p.setFont(QFont("Courier",170, QFont::Bold));
    p.drawText(40, 80, 720, 170, Qt::AlignRight | Qt::AlignVCenter, rspD);
    p.drawText(40, 250, 720, 170, Qt::AlignRight | Qt::AlignVCenter, ctmP);
    p.drawText(40, 420, 720, 170, Qt::AlignRight | Qt::AlignVCenter, oilPre);
}

void TMainWidget::paintEvent(QPaintEvent *) {
    QPainter p(this);

    if (rspD.toFloat() > 5.f){
        currentDisplayMode = acceleration;
    } else {
        currentDisplayMode = debug;
    }

    switch (currentDisplayMode) {
    case acceleration:
        drawAccelerationScreen(p);
        return;
    default:
        drawDebugScreen(p);
        return;
        break;
    }

    int space = 3;
    int itemWidth = (width() - space * 2) * 2;
    int itemHeight = 40;

    if (!transparent) {
        p.fillRect(0, 0, width(), height(), QBrush(QColor(0, 0, 0)));
        p.drawPixmap(0, 0, width(), height(), bg);
    }

    QString ip = eth0IP;
    if (ip == "0.0.0.0") {
        ip = wlan0IP;
    }

    p.setPen(QPen(QColor(0, 0, 0)));
    p.drawText(space,
               itemHeight * 23,
               width() - space * 2,
               itemHeight,
               Qt::AlignLeft | Qt::AlignVCenter,
               QString("CPU: %1/T%2").arg(freqStr).arg(currentCPUTemp));
    p.drawText(
        space * 50, itemHeight * 23, width() - space * 2, itemHeight, Qt::AlignLeft | Qt::AlignVCenter, QString("Memory: %1").arg(memInfo));
    p.drawText(space * 120,
               itemHeight * 23,
               width() - space * 2,
               itemHeight,
               Qt::AlignLeft | Qt::AlignVCenter,
               QString("LoadAvg: %1").arg(loadAvg));
    p.drawText(space * 180, itemHeight * 23, width() - space * 2, itemHeight, Qt::AlignLeft | Qt::AlignVCenter, QString("IP: %1").arg(ip));

    // p.drawText(0,itemHeight*8,width()-space*9,itemHeight + 30,Qt::AlignRight | Qt::AlignVCenter,QString("Memory: %1").arg(usageInfo));
    p.drawText(5, itemHeight * 23, width() - space * 9, itemHeight, Qt::AlignRight | Qt::AlignVCenter, QString("t=%1").arg(timeSinceStart));

    //// 6 Main Number items on dash

    int blockHeight = 40;
    int sideBorder = 30;
    int fieldWidth = 190;

    p.drawText(sideBorder + 120, blockHeight * 10, fieldWidth, blockHeight, Qt::AlignCenter | Qt::AlignVCenter, vbaT);
    p.setFont(QFont("Arial", 35));

    p.drawText(sideBorder, blockHeight * 2 + 15, fieldWidth, blockHeight, Qt::AlignCenter | Qt::AlignVCenter, rpM_);
    p.drawText(sideBorder, blockHeight * 5 + 15, fieldWidth, blockHeight, Qt::AlignCenter | Qt::AlignVCenter, ctmP);
    p.drawText(sideBorder, blockHeight * 8 + 20, fieldWidth, blockHeight, Qt::AlignCenter | Qt::AlignVCenter, QString(lamB));

    p.drawText(sideBorder, blockHeight * 2 + 15, width() - fieldWidth + 50, blockHeight, Qt::AlignRight | Qt::AlignVCenter, oilP);

    // Voltage in 2nd right position
    p.drawText(sideBorder, blockHeight * 5 + 15, width() - fieldWidth + 50, blockHeight, Qt::AlignRight | Qt::AlignVCenter, vbaT);

    // p.drawText(sideBorder,blockHeight*5+15,width()-fieldWidth+50,blockHeight,Qt::AlignRight | Qt::AlignVCenter,tpS_);
    p.drawText(sideBorder, blockHeight * 8 + 20, width() - fieldWidth + 50, blockHeight, Qt::AlignRight | Qt::AlignVCenter, tpS_);

    p.setFont(QFont("Arial", 150));
    p.drawText(220, blockHeight * 3, 360, 300, Qt::AlignCenter | Qt::AlignVCenter, rspD);

    if (1) {
        const int keyCount = sizeof(progresses) / sizeof(int);
        const int maxProgressBarWidth = width() - 20;
        const int space = 5;
        const int progressBarX = 10;
        const int progressBarHeight = 20;

        int progressBarY = height() - progressBarHeight * keyCount - space * (keyCount - 1);
        for (unsigned int i = 0; i < sizeof(progresses) / sizeof(int); i++) {
            int progressBarWidth = int(maxProgressBarWidth * (progresses[i] / 100.0));
            QRect rect(progressBarX, progressBarY, progressBarWidth, progressBarHeight);
            if (i == 0) {
                p.setBrush(QColor(255, 0, 0));
            } else if (i == 1) {
                p.setBrush(QColor(0, 255, 0));
            } else if (i == 2) {
                p.setBrush(QColor(0, 0, 255));
            } else {
                p.setBrush(QColor(255, 0, 255));
            }
            p.drawRect(rect);
            progressBarY += progressBarHeight + space;
        }
    }
}

void TMainWidget::customEvent(QEvent *e) {
    if (e->type() == TFT28LCDKeyEvent::TFT28LCDKEY_EVENT_TYPE) {
        struct timeval endTime;
        gettimeofday(&endTime, NULL);
        if (time_diff(startTime, endTime) < 1000) {
            // ignore first event
            QWidget::customEvent(e);
            return;
        }
        TFT28LCDKeyEvent *ee = (TFT28LCDKeyEvent *) e;
        if (ee->key == TFT28LCDKeyEvent::KEY1) {
            progresses[0] += 10;
            if (progresses[0] > 100) {
                progresses[0] = 10;
            }
            update();
        } else if (ee->key == TFT28LCDKeyEvent::KEY2) {
            progresses[1] += 10;
            if (progresses[1] > 100) {
                progresses[1] = 10;
            }
            update();
        } else if (ee->key == TFT28LCDKeyEvent::KEY3) {
            progresses[2] += 10;
            if (progresses[2] > 100) {
                progresses[2] = 10;
            }
            update();
        }
    } else {
        QWidget::customEvent(e);
    }
}
