import rclpy
from rclpy.node import Node
from syst_msgs.srv import AdvService, Waypoints

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

        self.req.drone_id = drone_id
        self.req.speed = self.declare_parameter('max_speed', 30.0).get_parameter_value().double_value
        self.req.tof = self.declare_parameter('tof', 50.0).get_parameter_value().double_value
        self.req.ancho_de_barrido = self.declare_parameter('sweep_width', 33.0).get_parameter_value().double_value
        self.req.coordx = self.declare_parameter('coordx', -200.0).get_parameter_value().double_value
        self.req.coordy = self.declare_parameter('coordy', 0.0).get_parameter_value().double_value
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

is_server_done = False

class MinimalServer(Node):

    def __init__(self, dname: str):
        super().__init__('minimal_server_async')
        self.srv = self.create_service(Waypoints, f'{dname}_service', self.receive_wps_callback)
    
    def receive_wps_callback(self, request, response):
        global is_server_done
        wps_array = np.array(request.wps, dtype=np.float64).reshape((int)(len(request.wps)/3), 3)
        self.get_logger().info(f'data received {wps_array}')
        
        #print(wps_array)
        #print(f'las coord son {wps_array[0][0]} : {wps_array[0][1]}')

        response.ready = 1
        is_server_done = True
        return response

def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request()
    minimal_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (12.3, 50.2, response.response))

    minimal_client.destroy_node()
    
    minimal_server = MinimalServer(drone_id)
    while not is_server_done:
        rclpy.spin_once(minimal_server)
    minimal_server.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()