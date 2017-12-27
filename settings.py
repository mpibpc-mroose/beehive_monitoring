# settings for the scale
# this is the raw value when no weight is on the scale
OFFSET = 160000
# that's the change/delta of the raw value per kilogramm
# you could e.g. put a known weight on the scale and calculate
# from the measures
SLOPE = 28350

# how many measures to do for a singe task
WEIGHT_MEASURE_COUNT = 3
# how long to wait between weight measures
WEIGHT_MEASURE_WAIT_TIME = 30
