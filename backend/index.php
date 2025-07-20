<?php
header('Content-Type: application/json');


function format_time($timestamp): string {
    $hour = date('g', $timestamp);
    $minute = date('i', $timestamp);
    $am_or_pm = date('a', $timestamp);
    # TODO:
    # Logik -> if ... 
    #
    return "$hour $minute $am_or_pm";
}

$action = $_GET['action'] ?? $_POST['action'] ?? '';

# Endpunkte /hello {message:'hello'} /howareyou {message: 'I'm fine'}

if ($action === 'hello') {
    echo json_encode(["message" => "hello"]);
}
else if ($action === 'howareyou') {
    echo json_encode(["message" => "I'm fine"]);
}
else if ($action === 'whattimeisit') {
    $time_zone = $_GET['timezone'] ?? '';
    if (!time_zone) {
        echo json_encode(["Error" => "Timezone parameter is missing!"]);
        exit;
    }
    $allTimezones = DateTimeZone::listIdentifiers();                            #List of all Timezones, Format ex.: Europe/Berlin
    if (!in_array($time_zone, $allTimezones)) {
        echo json_encode(["Error" => "Not a Timezone!"]);
        exit;
    }
    date_default_timezone_set($time_zone);
    $time = format_time(time());
    echo json_encode(["message" => "It's $time"]);
}
# /in/.. Filler atm
else if ($action === 'in') {
    $time = format_time(time());
    echo json_encode(["message" => "It's $time"]);
}