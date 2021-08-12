#include "esphome.h"
#include "HX711.h"
#include "RunningMedian.h"

class custom_scale_reader : public PollingComponent, public Sensor
{
public:
    int hx711_SCK_PIN_1 = D1;
    int hx711_DOUT_PIN_1 = D2;
    int i = 0;
    int number_of_samples = 20;
    float weight, weight_median;
    HX711 scale;

    custom_scale_reader() : PollingComponent(5 * 1000) {}

    void setup() override
    {
    }

    void update() override
    {

        RunningMedian samples = RunningMedian(number_of_samples);

        if (scale.wait_ready_retry(10))
        {

            //long reading = scale.read();
            //Serial.print("HX711 reading: ");
            //Serial.println(reading);

            i = 0;
            scale.begin(hx711_DOUT_PIN_1, hx711_SCK_PIN_1);
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
                //weight = (weight - tare) / calibration_factor;
                samples.add(weight);

                delay(50);
            }

            weight_median = samples.getMedian();
            scale.power_down();
            publish_state(weight_median);
        }
        else
        {
            Serial.println(" Error: HX711 not found.");
            publish_state(NAN);
        }
    }
};