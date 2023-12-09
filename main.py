import utime, time, random
from machine import Pin
from picodfplayer import DFPlayer

# DFPlayer
UART_INSTANCE = 0
TX_PIN = 16
RX_PIN = 17
BUSY_PIN = 22

# Between 0-30
DEFAULT_VOLUME = 18

player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

# Clock I/O
CLOCK_LED = Pin(13, Pin.OUT)
ALARM = Pin(12, Pin.IN, Pin.PULL_UP)
MODE_1= Pin(21, Pin.IN, Pin.PULL_UP)
MODE_2= Pin(20, Pin.IN, Pin.PULL_UP)

# Stepper Motor
IN1 = Pin(9, Pin.OUT)
IN2 = Pin(7, Pin.OUT)
IN3 = Pin(8, Pin.OUT)
IN4 = Pin(6, Pin.OUT)

# Adjust to match the Copal mechanism
STEPS_PER_MINUTE = 60

pins = [IN1, IN2, IN3, IN4]
sequence = [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

def rickroll():
  player.playTrack(2,1)
  
  while player.queryBusy() == True:
    time.sleep(0.5)
    CLOCK_LED.value(1)
    time.sleep(0.5)
    CLOCK_LED.value(0)

  # Once song has finished, it should resume to main loop.

def groundhog():
  player.playTrack(1,1)

  while player.queryBusy() == True:
    CLOCK_LED.value(1)
    
  # Once song has finished, it should resume to main loop.

def alarm():

  # Pick a number between 1 and 10 to decide what alarm.
  if random.randint(1, 10) == 10:
    print("I'm never going to give [up this joke].")
    rickroll()
  else:
    print("Urgh, Groundhog Day. Another Day.")
    groundhog()

  # Turn the LED off and return to main loop.
  CLOCK_LED.value(0)

def clock():
  current_time = utime.localtime()

  # Advance the stepper motor if the time has advanced (as it should?)
  if current_time[5] == 0:

    for _ in range(STEPS_PER_MINUTE):
      for step in sequence:
        for i in range(len(pins)):
          pins[i].value(step[i])
          utime.sleep(0.001)
    
    print("Moved the clocks forward, Master.")

def init():

  # Make sure LED is off before we do anything else.
  CLOCK_LED.value(0)
  
  # Set a default volume. 30 is VERY LOUD with this radio's tiny speaker.
  player.setVolume(DEFAULT_VOLUME)
  
  mainLoop()

#
# To help ole' mate. We're going to use 01 for music, 02 for the alarm.
# I've wired a USB plug to a TRRS jack so he can change the music as he wishes.
#
# I use init() to reset the clock back. mainLoop is where the magic happens.
#
#

def mainLoop():
  while True:
    clock()

    if MODE_1.value() != 1:
      # Shuffle songs on flash drive
      player.setPlaybackMode(3)
    else:
      player.pause()
      
    if ALARM.value() != 1:
      alarm()
    
    # Save some CPU cycles.
    time.sleep(1)

init()
