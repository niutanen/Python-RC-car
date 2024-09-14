# Remote controlled raspberry pi car controlled by ps4 contoller

## Motivation

I was bored, and decided to make a remote controlled car. However, I did not want to spend money on something I was likely to use for a couple of hours and then forget about. Therefore, I decided to make it out of components I had lying around. In my mind a RC car would require the following list of items:
* 1 motor to go straight and backward
* 1 servo or motor to change direction
* 1 battery to drive the motors
* 1 control board to regulate the power to the motors
* 1 data reciever
* 1 data transmitter 

I looked around for what components I had that would fit these purposes and found that i had a couple of motors that could be used for the power and replace the servo with direct directional driving. I could use an arduino for the control system, but it did not have wireless connectivity so I decided that rather than buy a new wireless module, I could buy a used raspberry pi and ps4 remote for a comparable price that would give me greater flexibility in projects in the future. I found a cheap powerbank that I had not been using for the battery, and got to work on getting the motors to spin. In case of shorting my connections, i first started the wiring with an arduino board.

## The wrong way

In order to enable the motors to spin foreward and backward, I connecting the motor to two data pins of an arduino board. Then I set one of the pins to high and the other to low and hoped it would spin by running current from one pin to the other. THIS WAS A MISTAKE. The arduino data pins provided just enough power to move a free axle, but they would stop with any additional load. Additionally, there was a chance that the motors could induce current from the motor coils, that could destroy the arduino.

## Second failure

I decided to do some research. I found out that the arduino pins can provide 5v only at very low currents (about 14mA) which were orders of magnitude smaller than what I needed. From this I learned that I would need a separate power supply at a higher volage that could power the motors at a lower current. For this I attempted to make a H-bridge from components taken from an old vcr. I managed to make it work, but the power was still too low to power the motor when it was under load. After troubleshooting the connections I figured out that the components caused a voltage drop when current was pulled through the circuit, thus making the board incompatible with the project. The final nail in the coffin for this approach was hammered in when I connected the bridge backwards and got magic black smoke from one of the npn transistors. 

## Using the A4988 to drive DC motors

After thiking for a while, I remembered that I had motor controllers on my 3D printer. Although the controllers were for stepper motors, perhaps they could be adapted to run in the setup I had. In principle it should work, so i grabbed the components from the printer and put my research skills to test. I found [this forum post](https://www.robotshop.com/community/forum/t/very-low-cost-2a-dual-dc-motor-driver-with-cool-features/13183). I understood the principle so I looked up the [datasheet](https://www.pololu.com/file/0J450/a4988_DMOS_microstepping_driver_with_translator.pdf) of my controller and set it up. After getting the basic components hooked up and tested with the arduino, I moved to the raspberry pi. To make it as simple as possible I chose to write the control program in python. 


![image](https://user-images.githubusercontent.com/35771181/154839701-328e4d8f-546e-4992-8a2c-d71574f8bde8.png)

## Parts list:

* 1 raspberry pi 3 b+
* 2 dc motors 
* 1 ps4 controller
* 1 A4988 stepper motor controller 
* 1 5V powerbank
* 1 9 -12 V battery

## The code:
The code uses the following raspberry pi compatible python libraries: 
* [gpiozero](https://gpiozero.readthedocs.io/en/stable/) - for the pin outputs
* [pyPS4Controlller](https://pypi.org/project/pyPS4Controller/) - for easy ps4 commands

By playing around with the inputs and reading the datasheet I found out that the motor cycled through the following set of outputs:

When step pin and direction pins are set to high both motors stop.
When setting step to low it cycles through the following settings:
step      | 1  | 2 | 3  | 4  
----------|:--:|:--:|:----:|:----:
motor1    | 1  |-1 |-1  | 1
motor2    | 1  | 1 |-1  | 1 
direction | ↑  |→  | ↓  | ← 

If  is set to high, the A4988 is in half-stepping mode which adds a step allowing driving of a single motor at a time with the following cycle:

step      | 1 |  2 |  3 |  4 |  5 |  6 |  7 |  8
----------|:---:|:----:|:----:|:----:|:----:|:----:|:----:|:----:
motor1    |.7 |  0 |-.7 | -1 |-.7 |  0 | .7 |  1
motor2    |.7 |  1 | .7 |  0 |-.7 | -1 |-.7 |  0
direction | ↑ |  ↗ |  → |  ↘ |  ↓ |  ↙ |  ← |  ↖  

While testing, if the interval between pulses was too short, and the direction pin was was pulled to high, the A4988 would not register some of the steps, leading to inconsistent controls. My original was to return the controller to the starting step after the release of any button by sending pulses until it was in the start "position", but if the motor controller was missing steps this would not work. By resetting the A4988 before each command this was rectified. If the A4988 would miss a step, the command could be resent, the board would reset and retried.  

Based on this hack i had a working RC car, which i then promptly used for 45 minutes until i got bored. It sat on a shelf for a week until i took it apart and used the components for another project.

