#!/usr/bin/env python3

import serial
import time
import rospy
from sensor_msgs.msg import Range

def ultrasound_publisher():
    pub = rospy.Publisher('ultrasound_data', Range, queue_size = 10)
    rospy.init_node('ultrasound_probe', anonymous = True)
    msg_us = Range()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        try:
            msg_us.range = ultrasound_reader()
            pub.publish(msg_us)
            rate.sleep()
        except SystemExit:
            rospy.logerr("Process has exited unexpectedly")


def ultrasound_reader():
    #defining serial port, baud rate and delay (refer to documentation)
    serial_port = '/dev/ttyUS'  # replace with the appropriate UART device
    baud_rate = 9600
    delay = 2/1000000.0 #set to 2 microseconds
    
    # initialize UART communication
    us = serial.Serial(serial_port, baud_rate, timeout = 1)

    #sending series of bytes for communication (refer to documentation)
    while True:
        #serial port address
        us.write(bytes([0xe8]))
        time.sleep(delay)

        #register
        us.write(bytes([0x02]))
        time.sleep(delay)

        #detection command
        us.write(bytes([0x68])) #use 0x6a for us value
        time.sleep(delay)

        #16 bits so 2 bytes 
        data = us.read(2)

        #convert bytes to int
        data_int = int.from_bytes(data, byteorder="big")

        rospy.loginfo(data_int)

        time.sleep(0.1)

        return data_int
    

if __name__ == '__main__':
    try:
        ultrasound_publisher()
    except rospy.ROSInterruptException:
        pass
