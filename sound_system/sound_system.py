import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_pico
from module import module_follow
from module import module_take
from module import module_arm
from module import module_make_map

from rione_msgs.msg import Command

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            Command, 'sound_system/command',
            self.command_callback,
            10
        )

        self.senses_publisher = self.create_publisher(
            Command,
            'cerebrum/command',
            10
        )


    # recieve a command {Command, Content}
    def command_callback(self, msg):

        # Speak a content
        if 'speak' == msg.command:
            if module_pico.speak(msg.content) == 1:
                self.cerebrum_publisher(0,"speak")

        # Start follow me, content is first or end
        when = ""
        if 'follow' == msg.command:
            when = msg.content
            answer = module_follow.follow(when)
            if str(when) == "first":
                if answer == 1:
                    self.cerebrum_publisher(0,"follow_first")
            elif str(when) == "end":
                if str(answer) == "car":
                    self.cerebrum_publisher(0,"follow_end","car")

        if 'arm' == msg.command:
            if module_arm.arm() == 1:
                self.cerebrum_publisher(0,"arm")

        # Where to take the bag
        if 'take' == msg.command:
            answer = module_take.take()
            if str(answer) != "":
                self.cerebrum_publisher(0,"take",str(answer))

        # Make map
        content = None
        if 'make_map' == msg.command:
            content = msg.content
            if content == "go":
                self.cerebrum_publisher(0,"make_map_go",str(module_make_map.make_map(content)))
            else:self.cerebrum_publisher(0,"make_map_else",(module_make_map.make_map()))

    # Publish a result of an action
    def cerebrum_publisher(self, flag, command, content=""):

        _trans_message = Command()
        _trans_message.flag = flag
        _trans_message.command = command
        _trans_message.content = content
        _trans_message.sender = "sound"

        self.senses_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)


def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
