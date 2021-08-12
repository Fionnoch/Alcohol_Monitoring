/**
 *
 * HX711 library for Arduino - example file
 * https://github.com/bogde/HX711
 *
 * MIT License
 * (c) 2018 Bogdan Necula
 *
**/
#include <Arduino.h>
#include <HX711.h>
#include <RunningMedian.h>
#include "scale_read_fctn.h"

float scale_read_fctn(int LOADCELL_DOUT_PIN, int LOADCELL_SCK_PIN)
{
    float weight, weight_median;        //
    float tare=  -277114 -49738; //includes the weight of backet and airlock
    float calibration_factor = -132580;          // set this from calibration routine
    float calibration_weight = 1.220;              //kg
    int i = 0;
    int number_of_samples = 20;

    int hx711_SCK_PIN_1 = D1;
    int hx711_DOUT_PIN_1 = D2;

    HX711 scale;

    RunningMedian samples = RunningMedian(number_of_samples);

    calibration_factor = calibration_factor / (calibration_weight); // -58285.0000 : -98454.0000
    // HX711 circuit wiring
    scale.begin(hx711_DOUT_PIN_1, hx711_SCK_PIN_1);
    Serial.println("scale 1 initialised");

    scale.set_gain(128);

    scale.power_up();

    // Initialize library with data output pin, clock input pin and gain factor.
    // Channel selection is made by passing the appropriate gain:
    // - With a gain factor of 64 or 128, channel A is selected
    // - With a gain factor of 32, channel B is selected
    // By omitting the gain factor parameter, the library
    // default "128" (Channel A) is used here.

    for (i = 0; i <= number_of_samples; i++)
    {
        weight = scale.read();
        weight = (weight - tare) / calibration_factor;
        samples.add(weight);

        delay(50);
    }

    weight_median = samples.getMedian();


    //Serial.println(weight_median, 4);

    scale.power_down(); // put the ADC in sleep mode

    return weight_median;
}