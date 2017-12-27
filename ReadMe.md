Beehive Monitoring
==================

This is my small project for a beehive scale (Stockwaage) based on

- a Raspberry Pi,
- a WittyPy
- a Bosche H30A weight cell
- driven by a HX711 weight cell amplifier
- additional uses a DHT22 for an environmental monitoring

I tried to make the thing a bit sustainable. So the Raspi comes up
only once an hour and only o daylight times (implemented with WittyPi)
and sends it's measures to my shared hosting provider, where the data
storage and visualization is done.