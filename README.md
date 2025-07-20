# Aufgabe:
Erstelle oder verwende einen existierenden Docker Container (Stack) der einen Webserver und PHP (oder eben anderweitiges Framework) bereitstellt und 
stelle damit eine kleine REST API bereit.

- freie Wahl des Frameworks oder Plain PHP
- Zeitangaben sind nicht statisch (hart codiert) sondern dynamisch 
- Zeitangabe im Format 10 to 3 pm statt hh:mm

- Endpunkte
/hello
{message:'hello'}
/howareyou
{message: 'I\'m fine'}
/whattimeisit

{message:'It\'s 10 to 4 pm'}

/in/
Variante 1 per GET timezone
london
Variante 2 per POST timezone
{city: 'london'}

{message:'It\'s 10 to 3 pm'} 


PHPUnit - Test
- wenn bekannt Test mit Codeception


Fleißaufgaben

- Authentifizeriung
- HTTP Basic Auth oder Token
