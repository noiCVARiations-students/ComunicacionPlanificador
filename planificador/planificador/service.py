from syst_msgs.srv import AdvService, Waypoints
import rclpy
from rclpy.node import Node

from planning_algorithm.main import verdugo
import numpy as np

i = 2
service_active = True
drones = []
drones_names = []

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AdvService, 'adv_service', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        global service_active, drones, i

        response.response = request.tof + request.speed
        self.get_logger().info('Incoming request\ndrone_id: %s speed: %d tof: %d ancho_de_barrido: %d\ncoordx: %d, coordy: %d' % (request.drone_id, \
                        request.speed, request.tof, request.ancho_de_barrido, request.coordx, request.coordy))
        
        drones.append([request.coordx, request.coordy, request.ancho_de_barrido, request.speed, request.tof])
        drones_names.append(request.drone_id)

        i = i-1
        if i == 0:
            service_active = False
        return response

class MinimalClient(Node):

    def __init__(self, drone_id, waypoints):
        super().__init__('minimal_client')
        self.client = self.create_client(Waypoints, f'{drone_id}_service')
        self.waypoints = waypoints
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Waypoints.Request()

    def send_request(self):
        #np_array = np.array([[1.0, 2.0, 3.0, 4.0], [21.0, 3.0, 4.0, 5.0]], dtype=float)
        np_array = self.waypoints
        self.req.wps = np_array.flatten().tolist()
        self.future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main():
    rclpy.init()

    minimal_service = MinimalService()

    while service_active:
        rclpy.spin_once(minimal_service)

    wps = verdugo(drones)

    print(drones)
    minimal_service.destroy_node()

    index = 0
    print("waypoints")
    print(wps)
    for drone_wps in wps[0]:
        print(i)
        minimal_client = MinimalClient(drones_names[index], drone_wps)
        cli_response = minimal_client.send_request()
        minimal_client.get_logger().info(
            'Is ready ? %d' %
            (cli_response.ready))

        minimal_client.destroy_node()
        index = index+1

    rclpy.shutdown()

if __name__ == '__main__':
    main()