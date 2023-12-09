# groundhog-day
For legal reasons, not inspired by the film of the same name. A joke gift for a colleague at work.

## Bill of Materials
- 1x Sanyo RM 5010
- 1x Raspberry Pi Pico ($6.30)
- 1x 28BYJ-48 Stepper Motor + ULN2003 Driver (A$10)
- 1x DFPlayer Mini ($10)
- 1x warm white LED (A$0.07)
- 3x 330ohm resistor (A$0.30)
- Scrap aluminium for brackets + fasteners

## AI
Full disclosure. As this was for a silly joke, I used Generative AI to help me write the code for the stepper motor. I was planning to reuse the existing Copal motor, but I wasn't comfortable with my work co-existing with the 220V mains. Everything else is my own doing.

# Power Draw
Rough napkin maths...
- Raspberry Pi Pico (5V, 50mA)
- 28BYJ-48 Stepper Motor (5V, 240mA)
- DFPlayer Mini (5V, 20mA)
- LED (2.7V, 20mA)

330mA... Ahhh... I'll recommend 1A.
