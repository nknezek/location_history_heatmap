from numpy import sqrt
import numpy as np
import matplotlib.pyplot as plt
import re

def getweight(dx,dy,rc,b):
    # Calculates weights for a given distance from an observation
    # input: grid distance x, grid distance y, grid radius cutoff, convergence rate
    # output: weighting value
    r = sqrt(dx**2.0+dy**2.0)
    if rc>=r:
        return 1-(r/rc)**b
    else:
        return 0

def setupGrid(n):
    # Creates a heatmap grid of specified size
    # input: n (number of bins)
    # output: array of n lists, each with n members, initialized to zero
    return [[0 for x in xrange(n)] for x in xrange(n)]

def setupLatLonGrid(latmin,latmax,lonmin,lonmax,n):
    # Creates a heatmap grid of specified size
    # input: latmin, latmax, lonmin, lonmax, n (number of bins)
    # output: array of n lists, each with n members, initialized to zero, vector of latitudes, vector of longitudes 

    grid = [[0 for x in xrange(n)] for x in xrange(n)]
    latvec = np.linspace(latmin,latmax,n)
    lonvec = np.linspace(lonmin,lonmax,n)
    return (grid, latvec, lonvec)

def findBin(x,y,xvec,yvec):
    # figures out which bin each observation falls into
    # input: x (obs),y (obs), xvec, yvec
    # output: xbin, ybin
    
    Nx = len(xvec)-1
    Ny = len(yvec)-1
    if(x<xvec[0] or x>xvec[Nx] or y<yvec[0] or y>yvec[Ny]):
        return(-1,-1)
    else:
        Lx = xvec[Nx] - xvec[0]
        Ly = yvec[Ny] - yvec[0]
        xbin = int(np.floor((x-xvec[0])*Nx/Lx))
        ybin = int(np.floor((y-yvec[0])*Ny/Ly))
        return(xbin,ybin)


def addPoint(grid,xbin,ybin,rc,b):
    # Adds a point to the heatmap, with corresponding bleed to neighboring points
    # input: grid, xbin, ybin (which bin the point falls into), rc (radius cutoff), b (rate of decay)
     
    Nx = len(grid)-1
    Ny = len(grid[1])-1
    if(xbin<0 or xbin>Nx or ybin<0 or ybin>Ny):
        return grid
    else:
        for i in range(0,int(rc)+1):
            for j in range(0,int(rc)+1):
                weight = getweight(abs(i),abs(j),rc,b)
                if (i==0 and j==0):
                    grid[xbin][ybin] = grid[xbin][ybin]+ weight
                elif i==0 and j!=0:
                    if(ybin-j >= 0):
                        grid[xbin][ybin-j] = grid[xbin][ybin-j]+weight
                    if(ybin+j <= Ny):
                        grid[xbin][ybin+j] = grid[xbin][ybin+j]+weight
                elif j==0 and i!=0:
                    if(xbin-i >= 0):
                        grid[xbin-i][ybin] = grid[xbin-i][ybin]+weight
                    if(xbin+i <= Nx):
                        grid[xbin+i][ybin] = grid[xbin+i][ybin]+weight
                else:
                    if(xbin-i >= 0 and ybin-i >= 0):
                        grid[xbin-i][ybin-j] = grid[xbin-i][ybin-j]+weight
                    if(xbin+i <= Nx and ybin-i >= 0):
                        grid[xbin+i][ybin-j] = grid[xbin+i][ybin-j]+weight
                    if(xbin-i >= 0 and ybin+i <= Ny):
                        grid[xbin-i][ybin+j] = grid[xbin-i][ybin+j]+weight
                    if(xbin+i <= Nx and ybin+i <= Ny):
                        grid[xbin+i][ybin+j] = grid[xbin+i][ybin+j]+weight
        return grid
    
def takeLogofGrid(grid):
    # Takes the log of all grid values to smooth heatmap
    # input: grid
    # output: grid (with log taken)
    
    Nx = len(grid)
    for i in range(Nx):
        grid[i] = np.log(map(lambda x: x+1, grid[i]))
    return(grid)
    

def plotGrid(grid): 
    # Plots the heatmap simply
    # input: heatmap values
    # output: displays plot
    
    fig = plt.figure(figsize=(6, 6))
    
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(grid[::-1])
    ax.set_aspect('equal')
    
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()
    
    
def plotLatLonGrid(grid,latVec,lonVec): 
    # Plots the heatmap with latitude and longitude axes
    # input: heatmap values, latitude vector, longitude vector
    # output: displays plot
    
    fig = plt.figure(figsize=(6, 6))
    extent = [lonVec[0], lonVec[len(lonVec)-1], latVec[0], latVec[len(latVec)-1]]
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(grid[::-1],extent=extent)
    ax.set_aspect('equal')
    
    cax = fig.add_axes(extent)
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

def kml2csv(filename):
    # Takes KML file data and writes date, time, lat, lon to a CSV in same directory
    # input: filename
    # output: none
    
    lat = []
    lon = []
    date = []
    time = []
    with open(filename + ".kml",'r') as f:
        lines = (line.rstrip() for line in f) # All lines including the blank ones
        lines = (line for line in lines if line) # Non-blank lines
        for line in lines:
            #print line
            line = line.rstrip()
            line = re.split('<|>| ',line)
            #print line
            if line[1] == 'when':
                datetime = re.split('T',line[2])
                date.append(datetime[0])
                time.append(datetime[1])
            if line[1] == 'gx:coord':
                lon.append(line[2])
                lat.append(line[3])
    fout = open(filename+".csv",'w')
    fout.write("Date, Time, Latitude, Longitude \n")
    for i in range(0,len(date)):
        fout.write(date[i]+', '+time[i]+', '+lat[i]+', '+lon[i] + '\n')
    fout.close()

def readCSV(filename):
    # Reads CSV file with columns of date, time, lat, lon 
    # input: filename
    # output: (date, time, lat, lon) as vectors
    
    lat = []
    lon = []
    date = []
    time = []
    with open(filename + ".csv",'r') as f:
        lines = (line.rstrip() for line in f) # All lines including the blank ones, ignore header
        lines = (line for line in lines if line) # Non-blank lines
        next(lines) # Ignore header
        for line in lines:
            line = re.split(',',line)
            date.append(line[0])
            time.append(line[1])
            lat.append(line[2])
            lon.append(line[3])
    return(date,time,lat,lon)