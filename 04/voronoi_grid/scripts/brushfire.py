#!/usr/bin/env python

import rospy
from voronoi_grid.msg import GridInfo
from nav_msgs.msg import OccupancyGrid
import time

gridInfo = GridInfo()

def gridInfoCb(gridInfo):
	print 'In gridInfoCb'
	brushfire(gridInfo)

def oneDToTwo(i, width):
	return [i / width, i % width]

def twoDToOne(r, c, width):
	return (r * width) + c

def inLine(grid):
	outGrid = OccupancyGrid()
	for i_r, r in enumerate(grid):
		for j_c, c in enumerate(r):
			outGrid.data.append(c)

	outGrid.header.frame_id = 'map'
	outGrid.info.width = 100
	outGrid.info.height = 100
	outGrid.info.resolution = 0.05
	return outGrid

def getNeighbors2D(row, col):
	# up, down, left, right
	return [[row-1, col], [row+1, col], [row, col-1], [row, col+1]]

def brushfire(gridInfo):
	print 'In brushfire'

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
		# print 'top left: r: %s c: %s' %(tlR, tlC)
		# print 'bottom right: r: %s c: %s' %(brR, brC)
		for obsCol in range(tlC, brC+1):
			brushGrid[tlR-1][obsCol] = 2
			brushGrid[brR+1][obsCol] = 2
		for obsRow in range(tlR, brR+1):
			brushGrid[obsRow][tlC-1] = 2
			brushGrid[obsRow][brC+1] = 2
	
	# listing all non 0 locations
	nonZeroLocations = list()
	for r in range(0, width):
		for c in range(0, width):
			if not(brushGrid[r][c] == 0):
				nonZeroLocations.append([r, c])

#
# WORK ZONE
#

	# setting count for distance value
	count = 2
	# setting the grid on fire
	while not(len(nonZeroLocations) == 0):
		print 'In while'
		for e in nonZeroLocations:
			print 'In nonZeroLocations'
			current = nonZeroLocations.pop(nonZeroLocations.index(e))
			# setting the neighbors list
			neighbors = list()
			neighbors = getNeighbors2D(current[0], current[1])
			print 'len(neighbors): %s' % len(neighbors)
			# finding neighbors with count value i, and assining i+1 to current location
			for n in neighbors:
				# n[o]>-1 and < height and n[1]...
				if(brushGrid[n[0]][n[1]] == 0):
					brushGrid[n[0]][n[1]] = count + 1

		count += 1

#
# END WORK ZONE
#

	pub.publish(inLine(brushGrid))
	pub.publish(inLine(brushGrid))
	time.sleep(1)
	pub.publish(inLine(brushGrid))
	pub.publish(inLine(brushGrid))
	time.sleep(1)
	pub.publish(inLine(brushGrid))
	pub.publish(inLine(brushGrid))
	time.sleep(1)

	# # output to file
	# o = open('out.txt', 'w')
	# for e in brushGrid:
	# 	o.write(' '.join(map(str, e)) + '\n')
	# o.close

def main():
    print 'In main'

    rospy.init_node('brushfire', anonymous=True)

    sub_gridInfo = rospy.Subscriber('/mapInfo', GridInfo, gridInfoCb)

    rospy.spin()

if __name__ == '__main__':
    main()
