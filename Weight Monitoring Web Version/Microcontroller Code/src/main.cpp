
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
String Brew_ID = "RCA_Red_Current_Apple";
int batch_ID = 2;
float SG_start = 1.06; 
float SG_now;
float SG_Target = 1.025;
float volume = 15; //in liters
float density; 
float density_h20 = 999.10; //kg/m^3 at 15 celcuis
float ABV;

float offset_weight = 0.32; //kg the weight of the bucket


//weight = mass *9.81; 
//mass = volume * density;
//weight = volume * density * 9.81;
//density = weight/(volume * 9.81);

//ABV =(76.08 * (og-fg) / (1.775-og)) * (fg / 0.794)



bool use_target_SG = true; // if false use target percentage to calculate taget sg 

float weight;

void setup()
{
   
  Serial.begin(115200);
  while(!Serial) { }
  Serial.println("");
  Serial.println("Acohol monitor by weight");

  wifiMulti.addAP(ssid1, wifi_password1); // add Wi-Fi networks you want to connect to
  wifiMulti.addAP(ssid2, wifi_password2);
  wifiMulti.addAP(ssid3, wifi_password3);

  Serial.print("Connecting ..."); // connect to wifi
  while ( wifiMulti.run() != WL_CONNECTED)
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

  volume = volume/1000; //convert to m^3

}

void loop()
{

  if (internet_issue == false)
  { //used later on, if readings were taken but there was an issue uploading the data the code loops back around to try again but this stops all the values being recorded again.

    weight = scale_read_fctn(hx711_DOUT_PIN, hx711_SCK_PIN);

    density = (weight-offset_weight)/(volume);

    SG_now = density/density_h20; 

    ABV =(76.08 * (SG_start-SG_now) / (1.775-SG_start)) * (SG_now / 0.794); 

    Serial.print("weight = ");
    Serial.print(weight, 4);
    Serial.println(" Kg");

    Serial.println("volume = "); Serial.print( volume); Serial.println( " m^3"); 
    Serial.println("density = " ); Serial.print( density ); Serial.println( "kg/m^3"); 
    Serial.println("Starting Specific gravity = " ); Serial.println( SG_start, 4);
    Serial.println("Current Specific gravity = " ); Serial.println( SG_now, 4);
    Serial.println("Target Specific gravity = " ); Serial.println( SG_Target);
    Serial.println("Current alcohol content = " ); Serial.println( ABV);
 
  }
  // upload to website

  int row_ID = sensor_upload(host, httpport, user, db_password, file_location, Brew_ID, batch_ID, volume, weight, density, SG_start, SG_now, SG_Target, ABV);

  if (row_ID<0){ //if row id is a negative number it means there has been an error and the data couldn't be uploaded thus we need to loop back and 
    internet_issue = true;
    Serial.println("issue uploading to internet. will wait and then try again"); 
    delay (60*1000); // wait 1 minute
  }
  else {
    internet_issue = false;
    Serial.println("successfully uploaded data starting sleep");
    delay(30*60*1000);

  }

 
}
