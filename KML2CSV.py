import re
def klm2csv(filename):
    lat = []
    lon = []
    date = []
    time = []
    #filename = raw_input("please enter the kml filename (without .kml) ")
    with open("./"+filename + ".kml",'r') as f:
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
    
def excludePts(data,latin,lonin,ep):
    pass
    
def keepPts(data,latin,lonin,ep):
    pass
    
def computeHeatmap(data):
    pass
