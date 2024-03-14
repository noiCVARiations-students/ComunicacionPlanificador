import rclpy
from rclpy.node import Node
from syst_msgs.srv import AdvService
from syst_msgs.msg import Waypoints

import numpy as np

drone_id = ''

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AdvService, 'adv_service')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AdvService.Request()

    def send_request(self):
        global drone_id
        drone_id = self.declare_parameter('drone_id', 'drone_x').get_parameter_value().string_value
        self.get_logger().info(drone_id)
        self.req.drone_id = drone_id
        self.req.speed = self.declare_parameter('speed', 30.0).get_parameter_value().double_value
        self.req.tof = self.declare_parameter('tof', 50.0).get_parameter_value().double_value
        self.req.ancho_de_barrido = self.declare_parameter('ancho_de_barrido', 33.0).get_parameter_value().double_value
        self.req.coordx = self.declare_parameter('coordx', -200.0).get_parameter_value().double_value
        self.req.coordy = self.declare_parameter('coordy', 0.0).get_parameter_value().double_value
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

wps_received = False

class MinimalSubscriber(Node):

    def __init__(self, dname: str):
        super().__init__('minimal_subscriber')
        #self.wps_subscription = self.create_subscription(Waypoints, f'{dname}_wps', self.listener_callback, 10)  #drone_id is already defined
        self.wps_subscription = self.create_subscription(Waypoints, f'{dname}_wps', self.listener_callback, 10)
        self.wps_subscription

    def listener_callback(self, msg):
        global drone_id, wps_received
        wps_array = np.array(msg.wps, dtype=np.float64).reshape((int)(len(msg.wps)/2), 2)
        self.get_logger().info(f'data received {wps_array}')
        wps_received = True
"""
class MinimalServer(Node):

    def __init__(self, dname: str):
        super().__init__('minimal_server_async')
        self.srv = self.create_service(Waypoints, f'{dname}_service', self.receive_wps_callback)
    
    def receive_wps_callback(self, request, response):
        global is_server_done
        wps_array = np.array(request.wps, dtype=np.float64).reshape((int)(len(request.wps)/2), 2)
        self.get_logger().info(f'data received {wps_array}')
        
        #print(wps_array)
        #print(f'las coord son {wps_array[0][0]} : {wps_array[0][1]}')

        response.ready = 1
        is_server_done = True
        return response
"""
def main():
    global wps_received
    rclpy.init()

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request()
    minimal_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (12.3, 50.2, response.response))

    minimal_client.destroy_node()
    
    minimal_subscriber = MinimalSubscriber(drone_id)
    while not wps_received:
        rclpy.spin_once(minimal_subscriber, timeout_sec=0.5)
    minimal_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()