<?php

//http://beehivemonitor.000webhostapp.com/Micro/ESP8266/from_micro.php?Brew_ID=test&Batch_ID=69

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

foreach ($_REQUEST as $key => $value) { 
    if ($key == "Brew_ID") { //checks key for the term "Brew_ID"
        $Brew_ID = filter_var($value, FILTER_SANITIZE_STRING); //saves the value associated with unit as a new variable called Brew_ID.
        //echo $Brew_ID;
    }
    if ($key == "Batch_ID") { //checks key for the term "Brew_ID"
       $Batch_ID = filter_var($value, FILTER_SANITIZE_NUMBER_INT); //saves the value associated with unit as a new variable called Brew_ID.
        //echo $Brew_ID;
    }
    if ($key == "start_date"){
        $start_date = $value;
    }
    if ($key == "end_date"){
        $end_date = $value;
    }
    if ($key == "start_time"){
        $start_time = $value;
    }
    if ($key == "end_time"){
        $end_time = $value;
    }
}


/* $combined_start = date('Y-m-d H:i:s', strtotime("$start_date $start_time"));
$combined_end = date('Y-m-d H:i:s', strtotime("$end_date $end_time")); */

$combined_start = $start_time .+ " " .+ $start_date;
$combined_end = $end_time .+ " " .+ $end_date;

echo "combined start = $combined_start <br>";
echo "combined end = $combined_end <br>";

/* $combined_start = date('U', strtotime("$start_date $start_time")); //strtotime("14:02:15 01-10-2005" ) <<need to be concatinated to 1 string
$combined_end = date('U', strtotime("$end_date $end_time")); */

$combined_start_unix = date('U', strtotime($combined_start)); //strtotime("14:02:15 01-10-2005" ) <<need to be concatinated to 1 string
$combined_end_unix = date('U', strtotime($combined_end));

$pull_table_query = "SELECT * FROM `Weight_Monitor` WHERE (`Brew ID`= '$Brew_ID' AND `Batch ID`= '$Batch_ID' AND ($combined_start<`Timestamp`<$combined_end))"; 
$pull_table = mysqli_query($connection, $pull_table_query); //pull all results which match the brew id and batch number

$num_of_rows = mysqli_num_rows($pull_table);

$csv_output = "";

if ($num_of_rows>0){ //if there is data
    while($row_data = mysqli_fetch_row($pull_ref_table)){
        for($j = 0; $j<=$num_of_rows; $j++){
            $csv_output .= $row_data[$j].", ";
        }
        $csv_output .="\n";
    }
} 

?>