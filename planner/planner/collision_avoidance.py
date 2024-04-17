from geometry_msgs.msg import PoseStamped
from syst_msgs.msg import StringArray

from rclpy.node import Node

drone_ids = []

class Collision_avoidance(Node):
    def __init__(self):
        global drone_ids
        super().__init__('Collision_avoidance')
        self.wps_subscription = self.create_subscription(StringArray, f'drone_ids', self.drone_ids_callback, 10)
        
    def drone_ids_callback(self, msg):
        global drone_ids
        drone_ids = msg.drone_ids