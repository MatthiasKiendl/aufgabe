<?php
function format_time($timestamp): string {
    $hour = (int)date('g', $timestamp); 
    $minute = (int)date('i', $timestamp); 
    $ampm = date('a', $timestamp);

    if ($minute === 0) {
        return "$hour o'clock $ampm";
    } elseif ($minute === 15) {
        return "quarter past $hour $ampm";
    } elseif ($minute === 30) {
        return "half past $hour $ampm";
    } elseif ($minute === 45) {
        $nextHour = ($hour % 12) + 1;
        return "quarter to $nextHour $ampm";
    } elseif ($minute < 30) {
        $minuteStr = $minute === 1 ? "one minute" : "$minute";
        return "$minuteStr past $hour $ampm";
    } else {
        $minutesTo = 60 - $minute;
        $nextHour = ($hour % 12) + 1;
        $minuteStr = $minutesTo === 1 ? "one minute" : "$minutesTo";
        return "$minuteStr to $nextHour $ampm";
    }
}

$action = $_GET['action'] ?? $_POST['action'] ?? '';

if ($action === 'howareyou') {
    echo json_encode(["message" => "I'm fine"]);
}

else if ($action === 'hello') {
    echo json_encode(["message" => "hello"]);
}

else if ($action === 'whattimeisit') {
    $tz = $_GET['timezone'] ?? '';

    if (!$tz || !in_array($tz, DateTimeZone::listIdentifiers())) {
        echo json_encode(["error" => "unknown timezone"]);
        exit;
    }

    date_default_timezone_set($tz);
    $time = format_time(time());
    echo json_encode([
        "message" => "It's $time"
    ]);
}

else if ($action === 'in') {
    $tz = $_GET['timezone'] ?? '';

    if (!$tz) {
        echo json_encode(["error" => "missing timezone"]);
        exit;
    }

    if (in_array($tz, DateTimeZone::listIdentifiers())) {
        date_default_timezone_set($tz);
        $time = format_time(time());
        echo json_encode(["message" => "It's $time"]);
    } else {
        echo json_encode(["error" => "unknown timezone"]);
    }
}

else {
    echo json_encode(["error" => "No valid action"]);
}
?>
