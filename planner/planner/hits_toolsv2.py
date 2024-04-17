import numpy as np

class Hits_toolsv2():
    def __init__(self, positions, sizes) -> None:
        self.positions = np.array(positions)
        self.sizeDrone = sizes[0]
        
        for sizeD in sizes:
            if (sizeD > self.sizeDrone):
                self.sizeDrone = sizeD
        
    def hit(self):
        result = []
        index_positions = self.nearest_positions()
        heights = -(int)(len(index_positions)/2)
        for index in index_positions:  #This index are sorted by their height
            result.append((index, heights))  
            heights = heights + 1
        return result
            
    def nearest_positions(self):
        index_with_values = set()  # Use a set to avoid duplicates
        for i in range(len(self.positions)):
            for j in range(i+1, len(self.positions)):
                if (abs(self.positions[i][2] - self.positions[j][2]) <= 1.5):  #In very different heights it does not need hit verification
                    distance = np.linalg.norm(self.positions[i] - self.positions[j])
                    if distance < 4 * self.sizeDrone:
                        index_with_values.add((i, self.positions[i][2]))  # Add the index and its associated value
                        index_with_values.add((j, self.positions[j][2]))  # Add the index and its associated value

        # Sort the list of indices and values based on the associated values
        sorted_index_with_values = sorted(index_with_values, key=lambda x: x[1])

        # Extract only the sorted indices from the sorted list
        positions_result = [idx for idx, _ in sorted_index_with_values]

        return positions_result

# Create some sample positions and sizes
positions = [(4, 4, 1), (1, 1, 1), (2, 2, 1), (4, 4, 3)]
sizes = [1]

# Create an instance of Hits_toolsv2
hits_tool = Hits_toolsv2(positions, sizes)

# Call the hit function and print the result
print(hits_tool.hit())