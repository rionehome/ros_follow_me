import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_pico
from module import module_follow
from module import module_take
from module import module_arm
from module import module_make_map

from std_msgs.msg import String
from time import sleep

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            String, 'sound_system/command',
            self.command_callback,
            qos_profile_sensor_data
        )

    # recieve a command {Command, Content}
    def command_callback(self, msg):

        self.command = msg.data
        command = msg.data.split(',')

        # Speak a content
        if 'speak' == command[0].replace('Command:', ''):
            if module_pico.speak(command[1].replace('Content:', '')) == 1:
                self.cerebrum_publisher('Return:1,Content:None')

        # Start follow me, content is first or end
        when = ""
        if 'follow' == command[0].replace('Command:', ''):
            when = command[1].replace('Content:', '')
            answer = module_follow.follow(when)
            if str(when) == "first":
                if answer == 1:
                    self.cerebrum_publisher('Retern:0,Content:None')
            elif str(when) == "end":
                if str(answer) == "car":
                    self.cerebrum_publisher('Retern:0,Content:car')

        if 'arm' == command[0].replace('Command:', ''):
            if module_arm.arm() == 1:
                self.cerebrum_publisher('Return:1,Content:None')

        # Where to take the bag
        if 'take' == command[0].replace('Command:', ''):
            answer = module_take.take()
            if str(answer) != "":
                self.cerebrum_publisher('Retern:0,Content:' + str(answer))

        # Make map
        content = None
        if 'make_map' == command[0].replace('Command:', ''):
            content = command[1].replace('Content:', '')
            if content == "go":
                self.cerebrum_publisher('Retern:0,Content:' + str(module_make_map.make_map(content)))
            else:self.cerebrum_publisher('Retern:0,Content:' + str(module_make_map.make_map()))

    # Publish a result of an action
    def cerebrum_publisher(self, message):
        self.senses_publisher = self.create_publisher(
            String, 'cerebrum/command',
            qos_profile_sensor_data
        )

        sleep(2)

        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)

def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
