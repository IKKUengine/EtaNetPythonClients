import pigpio 
import time

pi = pigpio.pi()
pi.set_mode(18, pigpio.OUTPUT)
pi.set_PWM_frequency(18, 1000)
pi.set_PWM_dutycycle(18, 0)

pi.set_mode(12, pigpio.OUTPUT)
pi.set_PWM_frequency(12, 1000)
pi.set_PWM_dutycycle(12, 0)

    


