<?php

//this is used by the app to pull in all the brews and batches without downloading all of the content

//http://beehivemonitor.000webhostapp.com/Micro/ESP8266/from_micro.php?Brew_ID=test&Batch_ID=69

//echo "entered brewing php upload script";

// Create connection to SQL database
$server = "localhost";
$user = "id13266577_fionn_brew";
$password = "LuqJ<nz~_p0z%5G/"; //<<this is the password
$database = "id13266577_brewing"; //if the php code is running on the same server as the database use "localhost"
$connection = mysqli_connect($server, $user, $password, $database); // server, user, password for user, database

// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

// use this to get the name of the 
// pull up all of the reference table in the database.
 
$pull_ref_table_query = "SELECT * FROM `Reference_Table`"; 
$pull_ref_table = mysqli_query($connection, $pull_ref_table_query); //pull all results which match the brew id and batch number
$num_of_rows = mysqli_num_rows($pull_ref_table);
$num_of_cols = mysqli_num_fields($pull_ref_table);

date_default_timezone_set('Europe/Dublin');

$csv_output = "";
$csv_output_temp = "";

//method1
/* if ($num_of_rows>0){ //if there is data
    for ($i = 0; $i<=$num_of_rows; $i++){
        $row_data = mysqli_fetch_array($pull_ref_table);
        for ($j = 0; $j<=$num_of_cols; $j++){
            $csv_output .= $row_data[$j].", ";
        }
        $csv_output .="\n";
    }
} */

//method 2
if ($num_of_rows>0){ //if there is data
    while($row_data = mysqli_fetch_row($pull_ref_table)){
        for($j = 0; $j<=$num_of_cols - 1; $j++){
            if($j < 2){
                $csv_output .= $row_data[$j].", ";
            }
            else{
                $csv_output .= date('H:i:s, d/m/Y', $row_data[$j]).", ";
            }
            //$csv_output_temp .= $row_data[$j].", ";
        }
        $csv_output .= "\n";
        //$csv_output .= "<br>";
        
        //echo ($csv_output_temp); 
        //echo("<br>");
        //$csv_output_temp = "";
    }
}
//echo "$csv_output";
print ($csv_output);
exit();
?>