#!/usr/bin/env python

import qi
import sys
import time
import math
import rospy
import actionlib
from std_msgs.msg import String
from optparse import OptionParser
from naoqi_bridge_msgs.msg import SpeechWithFeedbackAction, SpeechWithFeedbackGoal


class TalkControllerPepper:
    def __init__(self, sim=False):
        self.sim = sim
        if sim:
            self.head_pub = rospy.Publisher('/talk', String, queue_size=1)
        else:
            self.speech_as = actionlib.SimpleActionClient('/naoqi_tts_feedback', SpeechWithFeedbackAction)
            self.speech_as.wait_for_server(rospy.Duration(2))
        rospy.loginfo("Connected to Speech Client.")

    def say_something(self, _text):
        tts_goal = SpeechWithFeedbackGoal()
        tts_goal.say = _text
        self.speech_as.send_goal(tts_goal)

    def say_something_blocking(self, _text):
        tts_goal = SpeechWithFeedbackGoal()
        tts_goal.say = _text

        if self.sim:
            self.head_pub.publish(_text)
            rospy.sleep(2)
            result = 'success'
        else:
            self.speech_as.send_goal(tts_goal)
            result = self.speech_as.wait_for_result()
            result = 'success'  # remove and use real results
        return result


class VideoIntroduction(object):
    def __init__(self, appl):
        super(VideoIntroduction, self).__init__()
        appl.start()
        session = appl.session
        self.memory = session.service("ALMemory")
        self.motion = session.service("ALMotion")
        self.pubAnimation = rospy.Publisher("/pepper_robot/animation_player", String, queue_size=1)
        self.pubHead = rospy.Publisher("/pepper_robot/head/pose", String, queue_size=1)
        self.tts = TalkControllerPepper()

    # (re-) connect to NaoQI:

    def run(self):
        self.motion.moveTo(0, -0.7, 0)
        self.tts.say_something_blocking("Hi!")
        self.pubAnimation.publish("animations/Stand/Gestures/ShowSky_9")
        self.tts.say_something_blocking(
            "My name is Tobi! I would like to participate in the RoboCup 2018! I will shortly introduce my system architecture!")
        self.tts.say_something("ROS is running on my head, wrapping NaoQi!")
        self.pubAnimation.publish("animations/Stand/Gestures/But_1")
        time.sleep(2)
        self.tts.say_something_blocking(
            "For example: The ROS navigation stack is deployed on my head, this enables me to navigate autonomously!")
        self.tts.say_something_blocking("I am also grabbing and streaming my camera inputs compressed using ROS")
        self.pubHead.publish("0:-70:0")
        time.sleep(1)
        self.tts.say_something(
            "This is my Laptop and the only external computing resource! Additional components like behavior coordination, object recognition and person perception are running on it!")
        self.pubAnimation.publish("animations/Stand/Gestures/ShowSky_5")
        time.sleep(3)
        self.pubHead.publish("0:0:0")
        time.sleep(8)
        self.pubAnimation.publish("animations/Stand/Gestures/Me_7")
        self.tts.say_something_blocking(
            "Lastly, I want to show you my tablet! Where additional information is displayed and which can be used to interact with me.")
        self.tts.say_something_blocking("Now I am going to show you some of my skills with the help of Felix and Kai!")
        self.tts.say_something_blocking(
            "Please remember, I am not the fastest driving robot. But my team is actively working on that!")


class VideoIntroduction2(object):
    def __init__(self, appl):
        super(VideoIntroduction2, self).__init__()
        appl.start()
        session = appl.session
        self.memory = session.service("ALMemory")
        self.motion = session.service("ALMotion")
        self.pubAnimation = rospy.Publisher("/pepper_robot/animation_player", String, queue_size=1)
        self.pubHead = rospy.Publisher("/pepper_robot/head/pose", String, queue_size=1)
        self.tts = TalkControllerPepper()

    # (re-) connect to NaoQI:

    def run(self):
        self.motion.moveTo(0, -0.7, 0)
        self.pubAnimation.publish("animations/Stand/Gestures/ShowSky_9")
        self.tts.say_something_blocking("Hi again!")
        self.tts.say_something_blocking(
            "Now, I am going to show my people perception and recognition skills.")
        self.tts.say_something("My people perception works in 2 and 3D. Thus, I detect people in my color image and then I calculate the corresponding 3D position")
        self.pubAnimation.publish("animations/Stand/Gestures/But_1")
        time.sleep(2)
        self.tts.say_something_blocking("Let's see how this works.")
        self.motion.moveTo(0, 0, math.radians(180.0))


class VideoIntroduction3(object):
    def __init__(self, appl):
        super(VideoIntroduction3, self).__init__()
        appl.start()
        session = appl.session
        self.memory = session.service("ALMemory")
        self.motion = session.service("ALMotion")
        self.pubAnimation = rospy.Publisher("/pepper_robot/animation_player", String, queue_size=1)
        self.pubHead = rospy.Publisher("/pepper_robot/head/pose", String, queue_size=1)
        self.tts = TalkControllerPepper()

    # (re-) connect to NaoQI:

    def run(self):
        self.tts.say_something_blocking("Hi for the last time, I promise!")
        time.sleep(2)
        self.tts.say_something_blocking(
            "My team also developed a simulation environment based on MORSE.")
        time.sleep(5)
        self.tts.say_something("The simulation exposes the same ROS interfaces as my physical representation. For instance, color and depth camera streams as well as simulated laser scans.")
        time.sleep(5)
        self.tts.say_something_blocking("This enables my team members to test new algorithms or do automated regression testing, even if I am not physically available.")
        time.sleep(5)
        self.tts.say_something_blocking("The best thing is, they are going to make the simulation open source soon.")
        time.sleep(5)
        self.tts.say_something_blocking("I hope you enjoyed watching my qualification video. Have a nice day and see you in Montral, hopefully.")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--pip", dest="pip", default=True)
    parser.add_option("--pport", dest="pport", default=True)
    rospy.init_node('pepper_VideoIntroduction', anonymous=True)
    (options, args) = parser.parse_args()
    try:
        connection_url = options.pip + ":" + options.pport
        app = qi.Application(["PepperVideoIntroduction", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi")
        sys.exit(1)

    #vi = VideoIntroduction(app)
    #vi.run()

    #vi2 = VideoIntroduction2(app)
    #vi2.run()

    vi3 = VideoIntroduction3(app)
    vi3.run()
