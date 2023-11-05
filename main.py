import utime
from machine import Pin

clock_led = Pin(13, Pin.OUT)
alarm_trigger = Pin(4, Pin.IN, Pin.PULL_UP)
rick_on = Pin(21, Pin.IN, Pin.PULL_UP)
device_on = Pin(20, Pin.IN, Pin.PULL_UP)

STEPS_PER_MINUTE = 25

IN1 = Pin(9, Pin.OUT)
IN2 = Pin(7, Pin.OUT)
IN3 = Pin(8, Pin.OUT)
IN4 = Pin(6, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

# Ordinary Operation
def music_box():
  clock_led.value(1)    

def rick_roll():
  clock_led.value(1)

while True:
  # Fetch current time
  current_time = utime.localtime()
  
  if current_time[5] == 0:

    # Advance the stepper motor
    for _ in range(STEPS_PER_MINUTE):
      for step in sequence:
        for i in range(len(pins)):
          pins[i].value(step[i])
          utime.sleep(0.001)
    
  # If device is set to 'on', arm alarm and start DFPlayer
  if device_on.value() != 1:
    music_box()
    
  # If device is set to 'auto', queue Rick Astley's infamous single.
  elif rick_on.value() != 1:
    rick_roll()

  # Else, consider the clock off.
  else:
    clock_led.value(0)
