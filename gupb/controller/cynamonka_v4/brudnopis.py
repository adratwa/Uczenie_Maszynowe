import math

# Example list of coordinates on the map
points = [(1, 3), (4, 6), (2, 2), (9, 7)]

# Calculate the average x and y coordinates
avg_x = sum(x for x, _ in points) / len(points)
avg_y = sum(y for _, y in points) / len(points)

# Calculate distances from each point to the calculated center
distances = [math.sqrt((x - avg_x) ** 2 + (y - avg_y) ** 2) for x, y in points]

# Find the index of the point closest to the calculated center
closest_point_index = distances.index(min(distances))

closest_point = points[closest_point_index]
print("Point closest to the center of the map:", closest_point)
