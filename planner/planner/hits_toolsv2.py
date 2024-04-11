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
        index_positions = self.nearest_positions(self.positions)
        heights = -(int)(len(index_positions)/2)
        for index in index_positions:  #This index are sorted by their height
            result.append((index, heights))  
            heights = heights + 1
        return result
            
    def nearest_positions(self):
        index_with_values = set()  # Use a set to avoid duplicates
        for i in range(len(self.positions)):
            for j in range(i+1, len(self.positions)):
                distance = np.linalg.norm(self.positions[i] - self.positions[j])
                if distance < 4 * self.sizeDrone:
                    index_with_values.add((i, self.positions[i][2]))  # Add the index and its associated value
                    index_with_values.add((j, self.positions[j][2]))  # Add the index and its associated value

        # Sort the list of indices and values based on the associated values
        sorted_index_with_values = sorted(index_with_values, key=lambda x: x[1])

        # Extract only the sorted indices from the sorted list
        positions_result = [idx for idx, _ in sorted_index_with_values]

        return positions_result
