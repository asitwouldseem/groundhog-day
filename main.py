import utime, time, random
from machine import Pin
from picodfplayer import DFPlayer

# DFPlayer
UART_INSTANCE = 0
TX_PIN = 16
RX_PIN = 17
BUSY_PIN = 22

# Between 0-30
DEFAULT_VOLUME = 10

player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

# Clock I/O
CLOCK_LED = Pin(13, Pin.OUT)
ALARM = Pin(12, Pin.IN, Pin.PULL_UP)
MODE_1= Pin(21, Pin.IN, Pin.PULL_UP)

# Stepper Motor
IN1 = Pin(9, Pin.OUT)
IN2 = Pin(7, Pin.OUT)
IN3 = Pin(8, Pin.OUT)
IN4 = Pin(6, Pin.OUT)

# Adjust to match the Copal mechanism
STEPS_PER_MINUTE = 90

pins = [IN1, IN2, IN3, IN4]
sequence = [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

# Used to advance through the folder.
current_song = 0

# Once a first alarm has triggered, we'll start randomising.
initial_rand = 1

def rickroll():
  player.playTrack(2,2)
  
  while player.queryBusy() == True:
    time.sleep(0.5)
    CLOCK_LED.value(1)
    time.sleep(0.5)
    CLOCK_LED.value(0)

  # Once song has finished, it should resume to alarm() function.

def groundhog():
  player.playTrack(2,1)

  while player.queryBusy() == True:
    CLOCK_LED.value(1)
    
  # Once song has finished, it should resume to alarm() function.

def alarm():
  global initial_rand
  
  # Pick a number between 1 and 10 to decide what alarm.
  if initial_rand == 10:
    print("I'm never going to give [up this joke].")
    rickroll()
  else:
    print("Urgh, Groundhog Day. Another Day.")
    groundhog()
  
  # Turn the LED off and return to main loop.
  CLOCK_LED.value(0)
    
  # Once that initial alarm has triggered, we arm Rick Astley.
  initial_rand = random.randint(1, 10)
  print(initial_rand)

def clock():
  current_time = utime.localtime()

  # Advance the stepper motor if the time has advanced (as it should?)
  if current_time[5] == 0:

    for _ in range(STEPS_PER_MINUTE):
      for step in sequence:
        for i in range(len(pins)):
          pins[i].value(step[i])
          utime.sleep(0.001)
    
    print("Moved the clocks forward.")

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
  global current_song
    
  while True:
    if ALARM.value() != 1:
      player.pause()
      alarm()      
      
    # Determine if the clock is on. If it is, we'll use it as a normal MP3 player.
    # Turning it on/off does have the effect of skipping a track. But that's a 'feature.'
    while MODE_1.value() != 1:
      playing = current_song + 1
      clock()

      if player.queryBusy() == False:
        player.playTrack(1, playing)

        current_song = playing

    else:
      # Yeah, I know this isn't great. But it works.
      player.pause()
      clock()
    
    # Save some CPU cycles.
    time.sleep(1)

init()
