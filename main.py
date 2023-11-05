import utime
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

# Stepper Motor
STEPS_PER_MINUTE = 25

IN1 = Pin(9, Pin.OUT)
IN2 = Pin(7, Pin.OUT)
IN3 = Pin(8, Pin.OUT)
IN4 = Pin(6, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

def music_box():
  clock_led.value(1)
  print("Starting playback.")
  player.setPlaybackMode(1)
  
  if alarm_trigger.value() != 1:
    alarm()

# Ordinary Operation
def alarm():
  print("Alarm triggered.")

  if mode_on.value() != 1:
    # Play Rick Astley's 'Never Going to Give You Up'
    player.playTrack(2,1)
  else:
    # Play Sonny & Cher 'I Got You Babe' 
    player.playTrack(2,2)

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
    
  # Consider device on if set to 'On' or 'Manual'
  if device_on.value() != 1 or mode_on.value() != 1:
    music_box()

  # Else, consider the clock off.
  else:
    print("Turning off.")
    player.pause()
    clock_led.value(0)
