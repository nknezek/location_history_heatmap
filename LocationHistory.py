from datetime import datetime
from datetime import timedelta
from time import mktime, strptime
import numpy as np
import re
        
class LocationHistory(object):
    def __init__(self):
        self.date = []
        self.time = []
        self.lat = []
        self.lon = []
        self.d = []
        self.t=[]
        self.dt = []
        self.v = []
    
    def deleteObs(self,ind):
        self.date.pop(ind)
        self.time.pop(ind)
        self.lat.pop(ind)
        self.lon.pop(ind)
        self.d.pop(ind)
        self.t.pop(ind)
        self.dt.pop(ind)
        self.v.pop(ind)
            
    def importCSV(self,filename):
        # Reads CSV file with columns of date, time, lat, lon 
        # input: filename
        # output: (date, time, lat, lon) as vectors
        with open(filename + ".csv",'r') as f:
            lines = (line.rstrip() for line in f) # All lines including the blank ones, ignore header
            lines = (line for line in lines if line) # Non-blank lines
            next(lines) # Ignore header
            for line in lines:
                line = re.split(',',line)
                self.date.append(line[0])
                self.time.append(line[1])
                self.lat.append(line[2])
                self.lon.append(line[3])

    def importKML(self,filename):
        # Takes KML file data and writes date, time, lat, lon to a CSV in same directory
        # input: filename
        # output: none

        with open(filename + ".kml",'r') as f:
            lines = (line.rstrip() for line in f) # All lines including the blank ones
            lines = (line for line in lines if line) # Non-blank lines
            for line in lines:
                #print line
                line = line.rstrip()
                line = re.split('<|>| ',line)
                #print line
                if line[1] == 'when':
	            dateandtime = re.split('T',line[2])
        	    self.date.append(dateandtime[0])
                    self.time.append(dateandtime[1])
                if line[1] == 'gx:coord':
                    self.lon.append(line[2])
                    self.lat.append(line[3])      

    def exportCSV(self,suffix):
        filename = self.date[0]+'_to_'+self.date[len(self.date)-1]+suffix
        fout = open(filename+".csv",'w')
        fout.write("Date, Time, Latitude, Longitude \n")
        for i in range(0,len(self.date)):
            fout.write(self.date[i]+', '+self.time[i]+', '+self.lat[i]+', '+self.lon[i] + '\n')
        fout.close() 
           
    def getDistance(self,lat1,lat2,lon1,lon2):
        # Calculate distance using haversine formula
        R = 6371.0
        lat1 = np.radians(float(lat1))
        lat2 = np.radians(float(lat2))
        lon1 = np.radians(float(lon1))
        lon2 = np.radians(float(lon2))
        dlat = np.abs(lat2-lat1)
        dlon = np.abs(lon2-lon1)
        a = np.sin(dlat/2)**2.0 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2.0
        c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
        d = R*c
        return(d)
    
    def calculateVel(self):
        for i in range(0,len(self.date)):
            self.t.append(datetime.strptime(self.date[i]+" "+re.split("-",self.time[i])[0] + "000","%Y-%m-%d %H:%M:%S.%f"))
        self.dt.append(timedelta(0,0,0))
        self.d.append(0)
        self.v.append(0)
        for i in range(1,len(self.t)):
            self.d.append(self.getDistance(self.lat[i-1],self.lat[i],self.lon[i-1],self.lon[i]))
            self.dt.append(self.t[i]-self.t[i-1])
            self.v.append(self.d[i]/self.dt[i].total_seconds()*3600)
    
    def filterByVel(self,maxVel):
        for i in range(len(self.date)-1,-1,-1):
            if self.v[i] > maxVel:
                self.deleteObs(i)
    
    def makeGoogleHeatmap(self): 
        filename = self.date[0]+'_to_'+self.date[len(self.date)-1]
        htmlfile = 'gHM_'+filename+'.html'
        template = open("gHeatmapTemplate.html",'r')
        f = open(htmlfile,'w')
        for line in template:
            line = line.rstrip()
            if(line == "// Insert Location Data Here"):
                for i in range(len(self.date)):
                    f.write('new google.maps.LatLng('+self.lat[i]+', '+self.lon[i]+'),\n')
            else:
                f.write(line + '\n')
        f.close()
        template.close()