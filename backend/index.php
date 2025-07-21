<?php

/**
 * Formats a given Unix timestamp into a human-readable English time string.
 *
 * The output describes the time in terms such as "o'clock", "quarter past", "half past",
 * "quarter to", or "minutes past/to" the hour, including the AM/PM period.
 *
 * Examples:
 *   - 08:00 AM => "8 o'clock am"
 *   - 08:15 AM => "quarter past 8 am"
 *   - 08:30 AM => "half past 8 am"
 *   - 08:45 AM => "quarter to 9 am"
 *   - 08:05 AM => "5 past 8 am"
 *   - 08:55 AM => "5 to 9 am"
 *
 * @param int $timestamp Unix timestamp to format.
 * @return string Human-readable formatted time string.
 */
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

/**
 * Handles different actions and returns a response array based on the action.
 *
 * Supported actions:
 * - 'howareyou': Returns a message indicating well-being.
 * - 'hello': Returns a greeting message.
 * - 'whattimeisit' or 'in': Returns the current time in the specified timezone.
 *      Requires 'timezone' in $params. Returns an error if missing or invalid.
 *
 * @param string $action The action to handle.
 * @param array $params Optional parameters for the action. For time-related actions, expects 'timezone'.
 * @return array Response containing either a 'message' or an 'error'.
 */
function handleAction(string $action, array $params = []): array {
    if ($action === 'howareyou') {
        return ["message" => "I'm fine"];
    }

    if ($action === 'hello') {
        return ["message" => "hello"];
    }

    if ($action === 'whattimeisit' || $action === 'in') {
        $tz = $params['timezone'] ?? '';
        if (!$tz) {
            return ["error" => "missing timezone"];
        }

        if (!in_array($tz, DateTimeZone::listIdentifiers())) {
            return ["error" => "unknown timezone"];
        }

        date_default_timezone_set($tz);
        $time = format_time(time());
        return ["message" => "It's $time"];
    }

    return ["error" => "No valid action"];
}

/**
 * Handles HTTP requests for the backend API.
 *
 * - Sets the response content type to JSON if not running in CLI mode.
 * - Determines the requested action from GET or POST parameters.
 * - Parses request parameters from JSON body for POST requests, or from GET for others.
 * - Calls handleAction() with the action and parameters, and returns the result as JSON.
 */
if (php_sapi_name() !== 'cli') {
    header('Content-Type: application/json');

    $action = $_GET['action'] ?? $_POST['action'] ?? '';
    $params = $_SERVER['REQUEST_METHOD'] === 'POST'
        ? json_decode(file_get_contents('php://input'), true) ?? []
        : $_GET;

    echo json_encode(handleAction($action, $params));
}
