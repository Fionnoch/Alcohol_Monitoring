<?php

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

//declaire all variables in case a value is not assigned
$Brew_ID = "n/a";
$Batch_ID = 999;
$volume = 999;
$weight = 999;
$density = 999;
$SG_start = 999;
$SG_now = 999;
$SG_Target = 999;
$ABV = 999;

//loop through and grab variables off the URL
foreach ($_REQUEST as $key => $value) { //_REQUEST refers to the information being passed in ie unit=1&sensor=123. this is shortened to key for ease
  // => $value means that within the information in the key the information to the right fo each term will be called value

  if ($key == "Brew_ID") { //checks key for the term "Brew_ID"
    $Brew_ID = filter_var($value, FILTER_SANITIZE_STRING); //saves the value associated with unit as a new variable called Brew_ID.
    //echo $Brew_ID;
  }
  if ($key == "Batch_ID") {
    $Batch_ID = filter_var($value, FILTER_SANITIZE_NUMBER_INT);
    //$Batch_ID = filter_input( INPUT_GET, 'quantity', FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    //filter_input(INPUT_GET, 'quantity', FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    //echo floatval($Batch_ID)."<br>";
    //$Batch_ID = floatval($Batch_ID);
  }
  if ($key == "volume") {
    $volume = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $volume = number_format ((float)$volume, 5, '.', '' );
  }
  if ($key == "weight") {
    $weight = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $weight = number_format ((float) $value , 5, '.', '' );
  }
  if ($key == "density") {
    $density = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $density = number_format ((float) $density, 5, '.', '' );      
  }
  if ($key == "SG_start") {
      $SG_start = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $SG_start = number_format ((float) $SG_start, 5, '.', '' );
  }
  if ($key == "SG_now") {
      $SG_now = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $SG_now = number_format ((float) $SG_now, 5, '.', '' );
    
  }
  if ($key == "SG_Target") {
      $SG_Target = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $SG_Target = number_format ((float) $SG_Target, 5, '.', '' );
    
  }
  if ($key == "ABV") {
      $ABV = filter_var($value, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);
    $ABV = number_format ((float) $ABV, 5, '.', '' );
    
   }
} //for each

//if we need to get the time from the internet, use this.  This sets the timezone
date_default_timezone_set('Europe/Dublin');
$time = date("r"); //many different possible formats, but this gives 12 hr format, and returns 1:23 as 123
$timestamp = date("U");

//echo "weight = $weight <br>";
//echo "density = $density <br>";
//echo "SG_start = $SG_start <br>";


//$table_col_names = ['Row ID', `Date`, `Brew ID`,  `Batch ID`, `Weight`,  'Volume', `Density`,   'Current SG',  `Target SG`, `Initial SG`,  `Alcohol Percent`, `Comment`];
//$table_col_values = [Null,    $time,    $Brew_ID,     $Batch_ID,    $weight,      $volume,   $density,      $SG_now,     $SG_Target,    $SG_start,     $ABV,    'blank'];


//INSERT INTO table_name (column1, column2, column3,...)
//VALUES (value1, value2, value3,...)

$sql_add_row_query = "INSERT INTO `Weight_Monitor` (`Row ID`, `Date`, `Timestamp`, `Brew ID`, `Batch ID`, `Weight`, `Volume`, `Density`, `Current SG`, `Target SG`, `Initial SG`, `Alcohol Percent`, Comment) 
                                            VALUES (Null,    '$time',  $timestamp, '$Brew_ID',  '$Batch_ID',  '$weight',  '$volume',  '$density',  '$SG_now',      '$SG_Target',  '$SG_start',    '$ABV', 'blank')";
//echo "$sql_add_row_query <br>";

//echo $sql_add_row_query; 
//add new row. must ensure table name is correct
//$sql_add_row_query = "INSERT INTO `Weight_Monitor` (`Row ID`, `Date`,    `Location`,     `Inside Temperature`, `Outside Temperature`, `Inside Humidity`, `Outside Humidity`, `Inside Heat Index`, `Outside Heat Index`, `ABV`, `Comment`) 
//                                           VALUES (Null, '$time',   '$Brew_ID',     '$Batch_ID',               '$ABV',              '$density',          '$SG_start',           '$SG_now',           '$SG_Target',          '$ABV', 'blank')";

//$sql_add_row_query = "INSERT INTO `Beehive_Table` (`ID`, `Time`, `Location`, `Inside_Temperature`, `Outside Temperature`, `Inside Humidity`, `Outside Humidity`, `Inside Heat Index`, `Outside Heat Index`, `ABV`, `Comment`) VALUES (NULL, '2020-04-15', 'blah', '5', '5', '2', '3', '2', '1', '10', 'blah')";

mysqli_query($connection, $sql_add_row_query);

$row_ID_Query = "SELECT MAX( CAST( `Row ID` AS UNSIGNED) ) as Current_ID FROM `Weight_Monitor`"; 

$query_result = mysqli_query($connection, $row_ID_Query); #returns as an object 

$ID_array = $query_result->fetch_assoc(); #convert object to array

$row_ID = implode(" ", $ID_array); #convert array to string

echo ("RowID = $row_ID <br>");
//echo "PHP code finished <br>";

/*
//pull out the table
$result = mysqli_query($con,"SELECT * FROM ESPtable");//table select

//loop through the table and filter out data for this unit id
while($row = mysqli_fetch_array($result)) {
if($row['id'] == $unit){
$d1 = $row['LED'];
$d2 = $row['SENSOR'];
echo "_t1$t1##_d1$d1##_d2$d2##";
}

}//while

if($sensor >200){//send alarm as text message using email function
mail("0001112222@vtext.com", "ALARM", "Sensor=$sensor", "Unit=$unit");
}

*/

//download the weight_ref table and use that to tell if a new batchnumber or batch id needs to be added. 
$pull_ref_table_query = "SELECT * FROM `Reference_Table` WHERE (`Brew_ID_Ref`= '$Brew_ID' AND `Batch_Number_Ref`= '$Batch_ID')"; 
$pull_ref_table = mysqli_query($connection, $pull_ref_table_query); //pull all results which match the brew id and batch number

if (mysqli_num_rows($pull_ref_table) === 0) { 

  echo "added a new row to reference table";
  $Max_row_query = "SELECT MAX(`Timestamp`) FROM `Weight_Monitor` WHERE `Brew ID` = '$Brew_ID' AND `Batch ID` = '$Batch_ID' ";
  $Min_row_query = "SELECT MIN(`Timestamp`) FROM `Weight_Monitor` WHERE `Brew ID` = '$Brew_ID' AND `Batch ID` = '$Batch_ID' ";

  $Max_row_query_result = (mysqli_query($connection, $Max_row_query));
  $Min_row_query_result = (mysqli_query($connection, $Min_row_query));

  $Max_row_array = $Max_row_query_result->fetch_assoc(); #convert object to array
  $Max_row = implode(" ", $Max_row_array); #convert array to string
  
  $Min_row_array = $Min_row_query_result->fetch_assoc(); #convert object to array
  $Min_row = implode(" ", $Min_row_array); #convert array to string

  $insert_to_ref_table_query =  "INSERT INTO `Reference_Table` (`Brew_ID_Ref`, `Batch_Number_Ref`, `Start Timestamp`, `End Timestamp`) VALUES ('$Brew_ID', '$Batch_ID', '$Min_row', '$Max_row')";

  mysqli_query($connection, $insert_to_ref_table_query);

}
else {
  //update the end timestamp
  $update_end_time_query = "UPDATE `Reference_Table` SET `End Timestamp`='$timestamp' WHERE (`Brew_ID_Ref`= '$Brew_ID' AND `Batch_Number_Ref`= '$Batch_ID')";
  mysqli_query($connection, $update_end_time_query);
}


?>
