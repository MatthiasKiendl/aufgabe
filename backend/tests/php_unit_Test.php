/**
 * php_unit_Test
 *
 * PHPUnit test case class for testing the handleAction function.
 *
 * This class contains tests for various actions handled by the handleAction function,
 * including:
 * - 'hello': Should return a message "hello".
 * - 'howareyou': Should return a message "I'm fine".
 * - 'whattimeisit': Should return the current time in a valid timezone, or an error for an invalid timezone.
 * - 'in': Should return the current time for a valid timezone, an error for missing or invalid timezone.
 * - Invalid actions: Should return an error for unknown actions.
 *
 * Each test method verifies the expected output or error message for the corresponding action.
 */

<?php
use PHPUnit\Framework\TestCase;

require_once __DIR__ . '/../index.php';


class php_unit_Test extends TestCase
{
    public function testHello() {
        $res = handleAction('hello');
        $this->assertEquals("hello", $res['message']);
    }

    public function testHowAreYou() {
        $res = handleAction('howareyou');
        $this->assertEquals("I'm fine", $res['message']);
    }

    public function testWhatTimeIsItWithValidTimezone() {
        $res = handleAction('whattimeisit', ['timezone' => 'Europe/Berlin']);
        $this->assertArrayHasKey('message', $res);
        $this->assertStringContainsString("It's", $res['message']);
    }

    public function testWhatTimeIsItWithInvalidTimezone() {
        $res = handleAction('whattimeisit', ['timezone' => 'Fake/Zone']);
        $this->assertEquals('unknown timezone', $res['error']);
    }

    public function testInWithValidTimezone() {
        $res = handleAction('in', ['timezone' => 'Europe/London']);
        $this->assertArrayHasKey('message', $res);
        $this->assertStringContainsString("It's", $res['message']);
    }

    public function testInWithMissingTimezone() {
        $res = handleAction('in', []);
        $this->assertEquals('missing timezone', $res['error']);
    }

    public function testInWithInvalidTimezone() {
        $res = handleAction('in', ['timezone' => 'Nowhere']);
        $this->assertEquals('unknown timezone', $res['error']);
    }

    public function testInvalidAction() {
        $res = handleAction('gibberish');
        $this->assertEquals('No valid action', $res['error']);
    }
}