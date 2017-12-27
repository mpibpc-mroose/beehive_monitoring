Cabeling
========
| RPi Pin | GPIO  | HX711 | Cable    | Connector | Weight Cell |
|--------:|-------|-------|----------|----------:|-------------|
|  2      | 5V    | VCC   |          |           |             |
|  6      | GND   | GND   |          |           |             |
|  29     | GPIO5 | DOUT  |          |           |             |
|  31     | GPIO6 | PDSCK |          |           |             |
|         |       | A+    | green    |    3      |  green      |
|         |       | A-    | violett  |    1      |  white      |
|         |       | E-    | blue     |    2      |  black      |
|         |       | E+    | orange   |    4      |  red        |


DHT22
=====
```
   -------
  /   o   \
  =========
  =  ---  =
  =  ---  =
  =  ---  =
  =  ---  =
  =========
   | | | |
   1 2 3 4
```

https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/

| RPi Pin | GPIO  | DHT22  |                    |
|--------:|--------|-------|--------------------|
|  1      | 3.3    | 1     | |
|         | ---    | 2     | via pullup resistor 4.7k to 3.3V on pin 1|
|  11     | GPIO17 | 3     | |
|  9      | GND    | 4     | |
