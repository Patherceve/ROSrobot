#!/usr/bin/env python
import rospy
import random
from nav_msgs.msg import OccupancyGrid
from voronoi_grid.msg import GridInfo
from voronoi_grid.msg import ObPixels


def createRandomGrid(width, height, resolution=0.5):
    grid = OccupancyGrid()
    grid.info.width = width
    grid.info.height = height
    grid.info.resolution = resolution
    for r in range(0,height):
        for c in range(0,width):
            v = 0 # if random.randint(0,4) % 2 == 0 else 100
            grid.data.append(v)

    return grid


def setRandomRectOb(grid, x, y, width, height):
    obPixels = ObPixels()
    print 'In setRandomRectOb, x: %s y: %s width: %s height: %s' % (x, y, width, height)
    for r in range(0,width):
        for c in range(0,height):
            i = ((r+y)*grid.info.width)+c+x
            print 'r: %s c: %s i: %s' % (r, c, i)
            grid.data[i] = 100
            obPixels.i_pixels.append(i)
    return obPixels
            


def main():
    print 'In main'
    rospy.init_node('pubGrid', anonymous=False)

    pub = rospy.Publisher('/map', OccupancyGrid, queue_size=100)
    pub_info = rospy.Publisher('/mapInfo', GridInfo, queue_size=100)

    # 400 - 20m square
    # 200 - 10m square
    # 100 - 5m square
    grid = createRandomGrid(100,100,0.05)

    # Create some random obstacles
    num_obs = 2
    obs = []
    for i in range(0,num_obs):
        w = random.randint(10, 30)
        h = random.randint(10, 30)
        x = random.randint(0, grid.info.width-w-1)
        y = random.randint(0, grid.info.height-h-1)

        pixels = setRandomRectOb(grid, x, y, w, h)
        obs.append(pixels)

    gridInfo = GridInfo()
    gridInfo.grid = grid
    gridInfo.obs = obs

    rospy.sleep(0.5)
    pub.publish(gridInfo.grid)
    pub_info.publish(gridInfo)




if __name__ == '__main__':
    main()
    print('\nExiting normally')
