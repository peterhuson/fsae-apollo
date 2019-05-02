// demo: CAN-BUS Shield, receive data with check mode
// send data coming to fast, such as less than 10ms, you can use this way
// loovee, 2014-6-13


#include <SPI.h>
#include "mcp_can.h"


// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin

void setup()
{
    Serial.begin(115200);

    while (CAN_OK != CAN.begin(CAN_1000KBPS))              // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println(" Init CAN BUS Shield again");
        delay(100);
    }
    Serial.println("CAN BUS Shield init ok!");
}


void loop()
{
    unsigned char len = 0;
    unsigned char buf[8];

//     Serial.println("rpm_:10500");
//     delay(100);
    
    // Serial.println("ctmp:34.56");
    // delay(100);

    if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
    {
//      Serial.println("got can!");
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

        unsigned int canId = CAN.getCanId();

//            Serial.print("Get data from ID: ");
//            Serial.println(canId, HEX);
//        
//            for(int i = 0; i<len; i++)    // print the data
//            {
//                Serial.print(buf[i], HEX);
//                Serial.print("\t");
//            }

          if(canId == 0x703){
              float *high, *low;
              unsigned long high_buf, low_buf;
              low_buf = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
              high_buf = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
              high = (float *)&high_buf;
              low = (float *)&low_buf;
//              Serial.print("h");
//              Serial.print(canId, HEX);
//              Serial.print(":");
//              Serial.println(*high);
//              Serial.println();
              Serial.print("l");
              Serial.print(canId, HEX);
              Serial.print(":");
              Serial.println(*low);
          }
          
    //    if(canId == 0x700){
    //        float *ctmp;
    //        unsigned long coolant_temp;
    //        coolant_temp = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
    //        ctmp = (float *)&coolant_temp;
    //        Serial.print("ctmp:");
    //        Serial.println(*ctmp);

    //        float *oilp;
    //        unsigned long oil_pressure;
    //        oil_pressure = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
    //        oilp = (float *)&oil_pressure;
    //        Serial.print("oilp:");
    //        Serial.println(*oilp);
    //    }

    //    if(canId == 0x701){
           
    //        float *bv;
    //        unsigned long bat_voltage;
    //        bat_voltage = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
    //        bv = (float *)&bat_voltage;
    //        Serial.print("vbat:");
    //        Serial.println(*bv);

    //        float *lam;
    //        unsigned long lambda;
    //        lambda = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
    //        lam = (float *)&lambda;
    //        Serial.print("lamb:");
    //        Serial.println(*lam);
    //    }
//
//
//        if(canId == 0x702){
//
//            float *lspd;
//            unsigned long left_speed;
//            left_speed = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
//            lspd = (float *)&left_speed;
//            Serial.print("lspd:");
//            Serial.println(*lspd);
//            
//            float *rspd;
//            unsigned long right_speed;
//            right_speed = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
//            rspd = (float *)&right_speed;
//            Serial.print("rspd:");
//            Serial.println(*rspd);
//        }

    //    if(canId == 0x703){

    //        float *rpm;
    //        unsigned long engine_rpm;
    //        engine_rpm = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
    //        rpm = (float *)&engine_rpm;
    //        Serial.print("rpm_:");
    //        Serial.println(*rpm);
           
    //        float *accx;
    //        unsigned long x_acceleration;
    //        x_acceleration = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
    //        accx = (float *)&x_acceleration;
    //        Serial.print("accx:");
    //        Serial.println(*accx);
    //    }
//        
//        if(canId == 0x704){
//            
//            float *accy;
//            unsigned long y_acceleration;
//            y_acceleration = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
//            accy = (float *)&y_acceleration;
//            Serial.print("accy:");
//            Serial.println(*accy);
//
//            float *accz;
//            unsigned long z_acceleration;
//            z_acceleration = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
//            accz = (float *)&z_acceleration;
//            Serial.print("accz:");
//            Serial.println(*accz);
//        }
//        if(canId == 0x118){
//          Serial.println("got 118! ------------------------------------------");
//        }
//        if(canId == 0x705){
//          Serial.println("got 705! ------------------------------------------");
//        }
//       
    }
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
