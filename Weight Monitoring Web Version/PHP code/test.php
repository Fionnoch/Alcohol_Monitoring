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

$Brew_ID = 'RCA_Red_Current_Apple';
$Batch_ID = 2;

//download the weight_ref table and use that to tell if a new batchnumber or batch id needs to be added. 
$pull_ref_table_query = "SELECT * FROM `Reference_Table` WHERE (`Brew_ID_Ref`= '$Brew_ID' AND `Batch_Number_Ref`= '$Batch_ID')"; 
$pull_ref_table = mysqli_query($connection, $pull_ref_table_query); //pull all results which match the brew id and batch number

if (mysqli_num_rows($pull_ref_table) === 0) { 
    echo "added a new row to reference table";
    $Max_row_query = "SELECT MAX(`Timestamp`) FROM `Weight_Monitor` WHERE `Brew ID` = '$Brew_ID' AND `Batch ID` = '$Batch_ID' ";
    $Min_row_query = "SELECT MIN(`Timestamp`) FROM `Weight_Monitor` WHERE `Brew ID` = '$Brew_ID' AND `Batch ID` = '$Batch_ID' ";
  //results are empty, input this as a new batch entery 

  #get_object_vars($obj);

    $Max_row_query_result = (mysqli_query($connection, $Max_row_query));
    $Min_row_query_result = (mysqli_query($connection, $Min_row_query));

    #$row = mysqli_fetch_assoc($result);

    $Max_row_array = $Max_row_query_result->fetch_assoc(); #convert object to array
    $Max_row = implode(" ", $Max_row_array); #convert array to string
    
    $Min_row_array = $Min_row_query_result->fetch_assoc(); #convert object to array
    $Min_row = implode(" ", $Min_row_array); #convert array to string


  $insert_to_ref_table_query =  "INSERT INTO `Reference_Table` (`Brew_ID_Ref`, `Batch_Number_Ref`, `Start Timestamp`, `End Timestamp`) VALUES ('$Brew_ID', '$Batch_ID', '$Min_row', '$Max_row')";

  #echo "<Br>"; 
  #echo "Max_row_query = ";
  #echo $Max_row_query;
  #echo "<Br>"; 
  #echo "Min_row_query = ";
  #echo $Min_row_query;  

  #echo "<Br>"; 
  #echo "Max_row_temp = ";
  #echo $Max_row;
  #echo "<Br>"; 
  #echo "Max_row = ";
  #echo $$Max_row[0];  

  #echo "<Br>"; 
  #echo $insert_to_ref_table_query;

  mysqli_query($connection, $insert_to_ref_table_query);
}
else {
  //update the end timestamp
  echo "Updated reference table";
  $update_end_time_query = "UPDATE `Reference_Table` SET `End Timestamp`='$timestamp' WHERE (`Brew_ID_Ref`= '$Brew_ID' AND `Batch_Number_Ref`= '$Batch_ID') ";
  mysqli_query($connection, $update_end_time_query);
}


?>