import utime, random
from machine import Pin
from picodfplayer import DFPlayer

clock_led = Pin(13, Pin.OUT)
alarm_trigger = Pin(4, Pin.IN, Pin.PULL_UP)
mode_on = Pin(21, Pin.IN, Pin.PULL_UP)
device_on = Pin(20, Pin.IN, Pin.PULL_UP)

# DFPlayer
UART_INSTANCE=0
TX_PIN = 16
RX_PIN=17
BUSY_PIN=22

player=DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

# Volume Control
POTENTIOMETER_PIN = 26

# Stepper Motor
STEPS_PER_MINUTE = 25

IN1 = Pin(9, Pin.OUT)
IN2 = Pin(7, Pin.OUT)
IN3 = Pin(8, Pin.OUT)
IN4 = Pin(6, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

# Read the pot for volume control
def read_potentiometer_value(pin):
    return pin.read_u16()

# Ordinary Operation
def music_box():
  if mode_on.value() != 1:
    player.setPlaybackMode(1)
    clock_led.value(1)
    
  if alarm_trigger.value() != 1:
    alarm()

# Trigger a specific song when alarm is triggered.
def alarm():
  clock_led.value(1)    

  if random.randint(1, 10) == 10 and device_on.value() != 1:

    # Play Rick Astley's infamous single, 'Never Going to Give You Up'
    player.playTrack(2,1)
    print("I'm never going to give [up this joke].")

  elif mode_on.value() != 1 or device_on.value() != 1:

    # Play Sonny & Cher 'I Got You Babe' 
    player.playTrack(2,2)
    print("Urgh, Groundhog Day. Another Day.")

  else:
    print("Exited. Alarm triggered when clock off.")

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

  # Read the analog value from the potentiometer
  potentiometer_value = read_potentiometer_value(machine.ADC(POTENTIOMETER_PIN))

  # Map the potentiometer value to the volume range of DFPlayer Mini (0-30)
  volume = int(30 * potentiometer_value / 65535)

  # Set the volume of DFPlayer Mini
  player.setVolume(volume)

  # Consider device on if set to 'On' or 'Manual'
  if device_on.value() != 1 or mode_on.value() != 1:
    music_box()

  # Else, consider the clock off.
  else:
    player.pause()
    clock_led.value(0)

  utime.sleep_ms(100)
