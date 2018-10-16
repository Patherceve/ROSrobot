#!/usr/bin/env python

import rospy
import time
from voronoi_grid.msg import GridInfo
from nav_msgs.msg import OccupancyGrid


gridInfo = GridInfo()

def gridInfoCb(gridInfo):
	brushfire(gridInfo)

def oneDToTwo(i, width):
	return [i / width, i % width]

def twoDToOne(r, c, width):
	return (r * width) + c

def inLine(grid):
	# make a 1D Occupancy Grid out of 2D list
	outGrid = OccupancyGrid()
	for i_r, r in enumerate(grid):
		for j_c, c in enumerate(r):
			outGrid.data.append(c)

	outGrid.header.frame_id = 'map'
	outGrid.info.width = 100
	outGrid.info.height = 100
	outGrid.info.resolution = 0.05

	return outGrid

def getNeighbors2D(loc, width):
	# up, down, left, right
	neighbors = list()
	temp = [[loc[0]-1, loc[1]], [loc[0]+1, loc[1]], [loc[0], loc[1]-1], [loc[0], loc[1]+1]]
	# filter for non-existing out of range neighbors
	for n in temp:
		if not(n[0] < 0 or n[1] < 0 or n[0] >= width or n[1] >= width):
			neighbors.append(n)

	return neighbors

def distLocation(grid, width, distVal):
	# listing all locations at distVal
	loc = list()
	for r in range(0, width):
		for c in range(0, width):
			if grid[r][c] == distVal:
				loc.append([r, c])

	return loc

def brushfire(gridInfo):
	pub = rospy.Publisher('/bf_map', OccupancyGrid, queue_size=100)

	# getting the width of the map
	width = gridInfo.grid.info.width

	# making an 2D list of 0
	brushGrid = [[0]*width for _ in xrange(width)]
	
	# setting the edges of the map to 2
	for i in [0, width-1]:
		brushGrid[i] = [2]*width
	for i in range(1, width-1):
		brushGrid[i] = [2]+([0]*(width-2))+[2]

	# setting the obstacle to 1 and the obstacle's neighbors to 2
	for obstacle in range(0, len(gridInfo.obs)):
		for p in gridInfo.obs[obstacle].i_pixels:
			r, c = oneDToTwo(p, width)
			brushGrid[r][c] = 1
		# coordinates of the top left corner
		tlR, tlC = oneDToTwo(gridInfo.obs[obstacle].i_pixels[0], width)
		# coordinates of the bottom right corner
		brR, brC = oneDToTwo(gridInfo.obs[obstacle].i_pixels[len(gridInfo.obs[obstacle].i_pixels)-1], width)
		# assiging 2 with out of range verification
		for obsCol in range(tlC, brC+1):
			if tlR-1 >= 0:
				brushGrid[tlR-1][obsCol] = 2
			if brR+1 <= width-1:
				brushGrid[brR+1][obsCol] = 2
		for obsRow in range(tlR, brR+1):
			if tlC-1 >= 0:
				brushGrid[obsRow][tlC-1] = 2
			if brC+1 <= width-1:
				brushGrid[obsRow][brC+1] = 2
	
	# begins at distance 2
	currentDist = 2
	openList = distLocation(brushGrid, width, currentDist)

	# setting the grid on fire
	while len(openList) != 0:
		# for each location at current distance
		for location in openList:
			# clean/get location's neighbors list
			neighbors = list()
			neighbors = getNeighbors2D(location, width)
			# for each neighbors
			for n in neighbors:
				if brushGrid[n[0]][n[1]] == 0:
					brushGrid[n[0]][n[1]] = currentDist + 1

		# updating current distance value and openList
		currentDist += 1
		openList = distLocation(brushGrid, width, currentDist)

	# making reeeeeeeally sure it publishes
	pub.publish(inLine(brushGrid))
	pub.publish(inLine(brushGrid))
	time.sleep(1)
	pub.publish(inLine(brushGrid))
	pub.publish(inLine(brushGrid))
	time.sleep(1)
	pub.publish(inLine(brushGrid))
	pub.publish(inLine(brushGrid))
	time.sleep(1)

def main():
    print 'In main'

    rospy.init_node('brushfire', anonymous=True)

    sub_gridInfo = rospy.Subscriber('/mapInfo', GridInfo, gridInfoCb)

    rospy.spin()

if __name__ == '__main__':
    main()
