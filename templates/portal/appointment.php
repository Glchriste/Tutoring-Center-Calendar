<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);
header('content-type: application/json; charset=utf-8');
header("access-control-allow-origin: *");

echo $_POST["InputName"];
echo $_POST["InputEmail"];
?>