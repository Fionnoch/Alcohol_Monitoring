/* 
// libraries. !!remeber to include automatic dependency finder in platformio.ini
// file, not alway there automatically!!
#include <Arduino.h>
#include <HX711.h>
#include <RunningMedian.h>

float weight, total_weight, weight_median; // 
float tare= -277114 -49738;
float calibration_factor = -132580;// -210720;// -210720.0000 : -134851.0000
float calibration_weight = 1.220;// 9.484; //kg
float weight_avg;
int i = 0;
int number_of_samples = 20;

int hx711_SCK_PIN_1 = D1;
int hx711_DOUT_PIN_1 = D2;

HX711 scale;

RunningMedian samples_1 = RunningMedian(number_of_samples);

void setup()
{
    Serial.begin(115200);

    delay(1000);

    Serial.println("starting code");
    calibration_factor = calibration_factor/(calibration_weight);// -58285.0000 : -98454.0000
    // HX711 circuit wiring
    scale.begin(hx711_DOUT_PIN_1, hx711_SCK_PIN_1);
    Serial.println("scale 1 initialised");
    //scale_2.begin(hx711_DOUT_PIN_2, hx711_SCK_PIN_2);
    //Serial.println("scale 2 initialised");

    scale.set_gain(128); 
    //scale_2.set_gain(64);

    scale.power_up();
    //scale_2.power_up();
}

void loop()
{
    Serial.println("scale initialised");

    scale.set_gain(128);

    scale.power_up();

    RunningMedian samples = RunningMedian(number_of_samples);
    for (i = 0; i <= number_of_samples; i++)
    {
        weight = scale.read();
        //weight = (weight - tare);
        weight = (weight - tare) / calibration_factor;
        samples.add(weight);

        delay(50);
    }
     weight_median = samples.getMedian();

    Serial.print("weight = "); 
    Serial.println(weight_median, 6);

    scale.power_down();
    delay(5 * 1000);

}
 */