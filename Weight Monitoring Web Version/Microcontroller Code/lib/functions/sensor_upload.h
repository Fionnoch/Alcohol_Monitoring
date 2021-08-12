#ifndef SENSOR_UPLOAD_FCTN_H
#define SENSOR_UPLOAD_FCTN_H

int sensor_upload(String host, int httpport, String user, String db_password, String file_location, String Brew_ID, int batch_ID, float volume, float weight, float density, float SG_start, float SG_now, float SG_Target, float ABV);


#endif 