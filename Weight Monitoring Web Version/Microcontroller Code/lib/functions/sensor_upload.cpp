#include <Arduino.h>
#include <WiFiClientSecure.h>
#include "sensor_upload.h"

//#include "scale_read_fctn.h"

int sensor_upload(String host, int httpport, String user, String db_password, String file_location, String Brew_ID, int batch_ID, float volume, float weight, float density, float SG_start, float SG_now, float SG_Target, float ABV)
{

    // connect to the internet to make transmission
    Serial.println("beginning upload process");
    WiFiClient client;
    //int httpport = 80;
    if (!client.connect(host, httpport))
    {
        Serial.println("could not connect to host");
        delay(1000 * 60); //wait and then retry connection
        //internet_issue = true;
        return (-1); //error code. -1 = couldn't connect to host 
    }
    else
    {
        Serial.println("connection to host successful");
        //internet_issue = false;
        Serial.print("weight upload value = "); 
        Serial.println(weight, 4);
        // info needed to create the url to input the data to the database
        String url_authentication = "id=" + user + "&pw=" + db_password;
        String url_values =
            (("&Brew_ID=") + Brew_ID + ("&Batch_ID=") + batch_ID + ("&volume=") + String(volume, 4) +
            ("&weight=") + String(weight,4) + ("&density=") + String(density, 4) + 
            ("&SG_start=") + String(SG_start, 4) + ("&SG_now=") + String(SG_now, 4) +
            ("&SG_Target=") + String(SG_Target, 4) + ("&ABV=") + String(ABV, 4));

        ///Micro/Brewing/Weight Handler.php?id=id13266577_fionn_brew&pw=pi4eyNXnpoJ%$!oq11PM&Brew_ID=Rhubarb Wine&Batch_ID=1&volume=0.01&weight=4551053.00&density=46391980.00&SG_start=1.09&SG_now=46433.77&SG_Target=1.02&ABV=-301590183936.00
        
        Serial.println("url to send:"); // this is the string which if you print and copy into the browser the  function will work
        String php_request_url =
        ("http://" + host + file_location + ("?") + url_authentication + url_values);

        Serial.println(php_request_url); 
        
        // Send data either forms of client.print work, both are just there as a
        // reference
        //Serial.println("sending connection.");
        //Serial.println(file_location + "?" + url_authentication + url_values);
         client.print(String("GET ") + file_location + "?" + url_authentication +
                     url_values + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" +
                     "Connection: close\r\n\r\n"); // fill in the blanks 

        /* client.print(String("GET http://") + host + file_location + "?" +
       url_authentication + url_values
                    + " HTTP/1.1\r\n"
                    + "Host: " + host + "\r\n"
                    + "Connection: close\r\n\r\n");  */
        //fill in the blanks


        Serial.println("printing web response");
        unsigned long connection_timeout = millis();
        while (client.available() == 0)
        {
            if (millis() - connection_timeout > 1000)
            {
                Serial.println("connection timed out!");
                client.stop();
                return (-2); //upload from client failed
            }
        }

        String Row_ID_string;

        while (client.available())
        {
            String line = client.readStringUntil('\r');
            line.trim();
            if (line.substring(0, 7) == "RowID =")
            {
                Row_ID_string = line;
            }
            Serial.println(line);
        }
        Serial.println("");
        Serial.println("Connection closed");
        //Serial.print("line returned: ") ; Serial.println(Row_ID_string);
        Row_ID_string.remove(0, 7);
        int Row_ID = Row_ID_string.toInt();
        return (Row_ID); 
    }
}