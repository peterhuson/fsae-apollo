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

#ifndef WIDGET_H
#define WIDGET_H
#include <QtCore/QtGlobal>
#if QT_VERSION >= 0x050000
#include <QtWidgets>
#else
#include <QtGui>
#endif

#include "tft28lcd.h"

#include <sys/time.h>

class TMainWidget : public QWidget {
    Q_OBJECT

public:
    explicit TMainWidget(QWidget *parent, bool transparency, const QString &surl);
    ~TMainWidget() {}
private slots:
    void onKeepAlive();
    void qtdemoButtonClicked();

private:
    void resizeEvent(QResizeEvent *);
    void paintEvent(QPaintEvent *);
    void customEvent(QEvent *);

private:
    QTimer *mpKeepAliveTimer;
    QString loadAvg;
    QString currentCPUTemp;
    QString maxCPUTemp;
    QString freqStr;
    QString memInfo;
    QString usageInfo;
    QString timeSinceStart;
    QString ctmP;
    QString oilP;
    QString vbaT;
    QString lamB;
    QString lspD;
    QString rspD;
    QString rpM_;
    QString tpS_;
    QString accY;
    QString accZ;
    QPixmap bg;
    QString eth0IP;
    QString wlan0IP;
    QPushButton *qtdemoButton;
    QPushButton *quitButton;
    bool transparent;
    QString sourceCodeUrl;
    bool isUsingTFT28LCD;
    TFT28LCDThread *tft28LCDThread;
    int progresses[3];
    struct timeval startTime;
};

#endif // WIDGET_H
