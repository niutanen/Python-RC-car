from gpiozero import LED
from pyPS4Controller.controller import Controller
from time import sleep

direction_pin = LED(13)
step_pin = LED(19)
halfstepping = LED(4)
reset = LED(2)
halfstepping.on() # Sets A4988 to halfstepping
reset.on(); direction_pin.on(); step_pin.on()


'''
When pin 2 and 3 motors stop

If pin4 is set to high, the A4988 is in half-stepping mode
when pin 2 switched to low the motors cycle through the following set:


step      | 1   2   3   4   5   6   7   8
------------------------------------------
motor1    | 1   0  -1  -1  -1   0   1   1
motor2    | 1   1   1   0  -1  -1  -1   0
------------------------------------------
direction | ↑   ↗   →   ↘   ↓   ↙   ←   ↖

'''

def motor_signal(motor_left,motor_right):
    step_pin.on()
    reset.off()
    reset.on()
    motor_signal = 0
    if motor_left==1 and motor_right==1:
        motor_signal = 1
    elif motor_left==0 and motor_right==1:
        motor_signal = 2
    elif motor_left==-1 and motor_right==1:
        motor_signal = 3
    elif motor_left==-1 and motor_right==0:
        motor_signal = 4
    elif motor_left==-1 and motor_right==-1:
        motor_signal = 5
    elif motor_left==0 and motor_right==-1:
        motor_signal = 6
    elif motor_left==1 and motor_right==-1:
        motor_signal = 7
    elif motor_left==1 and motor_right==-0:
        motor_signal = 8
    elif motor_left==0 and motor_right==0:
        motor_signal = 0
        step_pin.on()
    count = 0
    while count < motor_signal:
        step_pin.on()
        step_pin.off()
        count=count+1
    print(str(count)+'  motor_left: ' +str(motor_left)+'  motor_right: '+str(motor_right))
    
    
    
class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.motor_left=0
        self.motor_right=0
        self.l2_active = False
        self.r2_active = True
    
    # Resetting motor values if a button fails to register
    def on_options_press(self):
        self.motor_left=0
        self.motor_right=0
    

    # Power right motor backwards
    def on_R1_press(self):
        self.motor_right=self.motor_right-1
        motor_signal(self.motor_left,self.motor_right)
        
    def on_R1_release(self):
        self.motor_right = self.motor_right + 1
        motor_signal(self.motor_left,self.motor_right)
        
    # Power left motor backwards    
    def on_L1_press(self):
        self.motor_left=self.motor_left-1
        motor_signal(self.motor_left,self.motor_right)
        
    def on_L1_release(self):
        self.motor_left = self.motor_left+1 
        motor_signal(self.motor_left,self.motor_right)
        
    # Power right motor forwards
    def on_R2_press(self,value):
        if self.r2_active==False:
            self.r2_active=True
            self.motor_right=self.motor_right+1
            motor_signal(self.motor_left,self.motor_right)
     
    def on_R2_release(self):
        self.r2_active=False
        self.motor_right=self.motor_right-1
        motor_signal(self.motor_left,self.motor_right)

    # Power left motor forwards   
    def on_L2_press(self,value):
        if self.l2_active==False:
            self.motor_left=self.motor_left+1
            self.l2_active=True
            motor_signal(self.motor_left,self.motor_right)
    
    def on_L2_release(self):
        self.l2_active=False
        self.motor_left=self.motor_left-1
        motor_signal(self.motor_left,self.motor_right)

    # Debugging and testing    
    def on_circle_press(self):
        step_pin.on()
        print("direction_pin:  "+ str(direction_pin.is_active)+"   step_pin: "+str(step_pin.is_active))
    
    def on_square_press(self):
        step_pin.off()
        print("direction_pin:  "+ str(direction_pin.is_active)+"   step_pin: "+str(step_pin.is_active))
        
    def on_triangle_press(self):
        direction_pin.off()
        print("direction_pin:  "+ str(direction_pin.is_active)+"   step_pin: "+str(step_pin.is_active))
    
    def on_x_press(self):
        direction_pin.on()
        print("direction_pin:  "+ str(direction_pin.is_active)+"   step_pin: "+str(step_pin.is_active))



controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()


