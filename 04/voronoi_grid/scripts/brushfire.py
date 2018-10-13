#!/usr/bin/env python

import rospy
from voronoi_grid.msg import GridInfo

gridInfo = GridInfo()

def gridInfoCb(gridInfo):
	print 'In gridInfoCb'
	#print gridInfo.grid.data

	brushfire(gridInfo)

def oneDToTwo(i, width):
	return [i / width, i % width]

def twoDToOne(r, c, width):
	return (r * width) + c

def getNeighbors(i, width):

	row, col = oneDToTwo(i, width)

	if(row > 0):
		up = twoDToOne(row - 1, col, width)
	else:
		up = -1

	if(row < width - 1):
		down = twoDToOne(row + 1, col, width)
	else:
		down = -1

	if(col > 0):
		left = twoDToOne(row, col - 1, width)
	else:
		left = -1

	if(col < width - 1):
		right = twoDToOne(row, col + 1, width)
	else:
		right = -1

	return [up, down, left, right]
	

def brushfire(gridInfo):
	print 'In brushfire'

	#print gridInfo.grid
	#print gridInfo.obs

	width = gridInfo.grid.info.width
	#print "width: %s" % width

	for i in range(0, len(gridInfo.grid.data)):

		#print i

		# row = i / width
		# col = i % width

		neighbors = getNeighbors(i, width)

		# print "up, down, left, right: %s" % neighbors


		# make an array of all zeros, set the obstacles, then set brushfire
		for n in neighbors:
			if gridInfo.grid.data[n] == 0:
				gridInfo.grid.data[n] += 1

	print gridInfo.grid

def main():
    print 'In main'

    rospy.init_node('brushfire', anonymous=True)

    sub_gridInfo = rospy.Subscriber('/mapInfo', GridInfo, gridInfoCb)

    rospy.spin()

if __name__ == '__main__':
    main()
