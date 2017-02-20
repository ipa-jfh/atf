#!/usr/bin/python
import unittest
import rospy
import rostest
import tf
import math
import sys

from atf_core import ATF
from simple_script_server import *

class Application:
    def __init__(self):
        # ATF code
        self.atf = ATF()

        # native app code
        self.pub_freq = 20.0 # Hz
        self.br = tf.TransformBroadcaster()
        rospy.sleep(1) #wait for tf broadcaster to get active (rospy bug?)
        self.sss = simple_script_server()

    def execute(self):

        # small testblock (circle r=0.5, time=3)
        self.atf.start("testblock_small")
        rospy.sleep(20)
        #self.sss.move("base", [25.0,68.5,0.0])
        self.atf.stop("testblock_small")

        # large testblock (circle r=1, time=5
        #self.atf.start("testblock_large")
        #self.pub_tf_circle("link1", "link2", radius=2, time=5)
        #self.atf.stop("testblock_large")
        
        self.atf.shutdown()

    def pub_tf_circle(self, parent_frame_id, child1_frame_id, radius=1, time=1):
        rate = rospy.Rate(int(self.pub_freq))
        for i in range(int(self.pub_freq * time) + 1):
            t = i / self.pub_freq / time
            self.br.sendTransform(
                    (-radius * math.cos(2 * math.pi * t) + radius, -radius * math.sin(2 * math.pi * t), 0),
                    tf.transformations.quaternion_from_euler(0, 0, 0),
                    rospy.Time.now(),
                    child1_frame_id,
                    parent_frame_id)
            rate.sleep()

class Test(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        pass

    def test_Recording(self):
        self.app.execute()

if __name__ == '__main__':
    rospy.init_node('test_name')
    if "standalone" in sys.argv:
        app = Application()
        app.execute()
    else:
        rostest.rosrun('application', 'recording', Test, sysargs=None)
