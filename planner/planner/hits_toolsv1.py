import numpy as np

class Hits_toolsv1():
    def __init__(self, wps1, wps2, size1, size2) -> None:
        self.points = []
        self.wps1 = wps1
        self.wps2 = wps2
        if (size1 < size2):
            self.size = size2
        else:
            self.size = size1 

    def hit(self):
        distance = self.distance_between_lines()
        if (distance > self.size*2 + 1):
            self.points = []  #The distance was not small enough to be a danger
        return self.points

    def distance_between_lines(self):
        # Calculate the direction vectors of both lines
        v1 = np.array([self.wps1[1][0] - self.wps1[0][0], self.wps1[1][1] - self.wps1[0][1], self.wps1[1][2] - self.wps1[0][2]])
        v2 = np.array([self.wps2[1][0] - self.wps2[0][0], self.wps2[1][1] - self.wps2[0][1], self.wps2[1][2] - self.wps2[0][2]])
        
        # Calculate the vector from a point on one line to the other
        w0 = np.array([self.wps2[0][0] - self.wps1[0][0], self.wps2[0][1] - self.wps1[0][1], self.wps2[0][2] - self.wps1[0][2]])
        
        # Calculate the direction matrix of the line
        A = np.vstack([v1, -v2]).T
        
        # Find the inverse of the direction matrix
        A_inv = np.linalg.pinv(A)
        
        # Calculate the parameter vector
        params = np.dot(A_inv, w0)
        
        # Calculate the closest point on the first line
        point1 = self.wps1[0] + params[0] * v1
        
        # Calculate the closest point on the second line
        point2 = self.wps2[0] + params[1] * v2

        #Save the points where the distance is minimum
        self.points = [point1, point2]
        
        # Calculate the distance between the two closest points
        min_distance = np.linalg.norm(point1 - point2)
        
        return min_distance
