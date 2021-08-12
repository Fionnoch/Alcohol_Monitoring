/* 
// libraries. !!remeber to include automatic dependency finder in platformio.ini
// file, not alway there automatically!!
#include <Arduino.h>

// DIY Functions
#include "scale_read_fctn.h"
#include "sensor_upload.h"

// WIFI setup
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h> // Include the Wi-Fi-Multi library
#include <WiFiClientSecure.h>

ESP8266WiFiMulti wifiMulti; // Create an instance of the ESP8266WiFiMulti class,
                            // called 'wifiMulti'
WiFiClientSecure client;
const char *ssid1 = "D-link 5";
const char *ssid2 = "Fionns Room ";
const char *ssid3 = "Heath-AP";
const char *wifi_password1 = NULL; //"YOUR_WIFI_PASSWORD_HERE";
const char *wifi_password2 = NULL;
const char *wifi_password3 = NULL;
bool internet_issue = false;

// HTML PHP parameters
String host = "beehivemonitor.000webhostapp.com";
String db_password = "pi4eyNXnpoJ%$!oq11PM"; // "LuqJ<nz~_p0z%5G/" <=needed for database; //or
                                             // pi4eyNXnpoJ%$!oq11PM <=needed for filemanager
String file_location = "/Micro/Brewing/Weight_Handler.php";
String database = "id13266577_brewing";
String table_name = "Weight_Monitor";
String user = "id13266577_fionn_brew";
int httpport = 80;
const char *user_char = user.c_str(); //some functions require the username and password to be in the from of a cont char and some dont.
const char *db_password_char = db_password.c_str();

// Pin definitions
int hx711_SCK_PIN = D1;
int hx711_DOUT_PIN = D2;

// function parameters
String Brew_ID = "Rhubarb_Wine";
int batch_ID = 1;
float SG_start = 1.096;
float SG_now;
float SG_Target = 1.02;
float volume = 10; //in liters
float density;
float density_h20 = 999.10; //kg/m^3 at 15 celcuis
float ABV;

unsigned long sleep_time = 30 * 60 * 1e6;

//weight = mass *9.81;
//mass = volume * density;
//weight = volume * density * 9.81;
//density = weight/(volume * 9.81);

//ABV =(76.08 * (og-fg) / (1.775-og)) * (fg / 0.794)

bool use_target_SG = true; // if false use target percentage to calculate taget sg

float weight;

//====== !!!! when deep sleep is preformed only the setup loop is preformed!!! ===========
void setup()
{
    //           SETUP
    //----------------------------------------------------------------
    delay(5000);
    Serial.begin(115200);
    while (!Serial)
    {
    }
    Serial.println("");
    Serial.println(F("======Acohol monitor by weight======"));
    

    //digitalWrite(D0, HIGH);
    //Serial.println("D0 set high to wake up esp");

    wifiMulti.addAP(ssid1, wifi_password1); // add Wi-Fi networks you want to connect to
    wifiMulti.addAP(ssid2, wifi_password2);
    wifiMulti.addAP(ssid3, wifi_password3);

    Serial.print("Connecting ..."); // connect to wifi
    while (wifiMulti.run() != WL_CONNECTED)
    { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks,
        // and connect to the strongest of the networks above
        delay(500);
        Serial.print('.');
    }
    Serial.println();
    Serial.print("Connected to ");
    Serial.println(WiFi.SSID()); // Tell us what network we're connected to
    Serial.print("IP address:\t");
    Serial.println(
        WiFi.localIP()); // Send the IP address of the ESP8266 to the computer

    volume = volume / 1000; //convert to m^3

    //          Main commands
    //---------------------------------------------------------
    int number_of_attempts = 10;
    for (int i = 0; i < number_of_attempts; i++)
    {
        if (internet_issue == false)
        { //used later on, if readings were taken but there was an issue uploading the data the code loops back around to try again but this stops all the values being recorded again.

            //weight = scale_read_fctn(hx711_DOUT_PIN, hx711_SCK_PIN);

            weight = 10;

            density = (weight - 0.786646) / (volume);

            SG_now = density / density_h20;

            ABV = (76.08 * (SG_start - SG_now) / (1.775 - SG_start)) * (SG_now / 0.794);

            Serial.print("weight = ");
            Serial.print(weight, 4);
            Serial.println(" Kg");
            Serial.print("volume = ");
            Serial.print(volume);
            Serial.println(" m^3");
            Serial.print("density = ");
            Serial.print(density);
            Serial.println("kg/m^3");
            Serial.print("Starting Specific gravity = ");
            Serial.println(SG_start, 4);
            Serial.print("Current Specific gravity = ");
            Serial.println(SG_now, 4);
            Serial.print("Target Specific gravity = ");
            Serial.println(SG_Target);
            Serial.print("Current alcohol content = ");
            Serial.print(ABV);
            Serial.println(" %");
        }
        // upload to website
        //int row_ID = sensor_upload(host, httpport, user, db_password, file_location, Brew_ID, batch_ID, volume, weight, density, SG_start, SG_now, SG_Target, ABV);
        int row_ID = 1;

        if (row_ID < 0)
        { //if row id is a negative number it means there has been an error and the data couldn't be uploaded thus we need to loop back and
            internet_issue = true;
            Serial.println("issue uploading to internet. will wait and then try again");
            Serial.print("This is attempt number ");
            Serial.println(i);
            if (i==number_of_attempts){
                Serial.println("Maximum number of attempts reached");
            }
            delay(60 * 1000); // wait 1 minute
        }
        else
        {
            Serial.println("successfully uploaded data");
            internet_issue = false;
            break;
        }
    }
    Serial.print("Going to sleep for ");
    Serial.print(sleep_time / (60 * 1e6));
    Serial.println(" minutes");
    //delay(sleep_time/1000);
    delay(500);
    ESP.deepSleep(10*1e6);//sleep_time); //likely not needed just here in case while loop exits before
    delay(500);
}

void loop() //cannot run loop with deepsleep
{   
}
 */