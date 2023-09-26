# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:13:04 2023

@author: M Kress
"""
#
import os
import csv
from decimal import Decimal, ROUND_DOWN
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#
#   Define subroutine for reading csv file with gis data
#
def GetCsvTable(FileName):
#
#   Read text files with Coordinates of Loop Road Stream Sensor
#
#   Define File Name, Open file, Read file header and data.
#
# initializing the titles and rows list
#
    print(' FileName\n ',FileName)
    print(os.getcwd())
    print(os.path.exists(FileName))
    fields = []
    Rows = []
# opening the CSV file
    with open(FileName, mode ='r')as file:
# reading the CSV file
        csvFile = csv.reader(file,delimiter=',')
        fields = next(csvFile)
        print(' Fields \n', fields)
        #print(csvFile.dt)
        print(' End fields \n')
        for row in csvFile:
            Rows.append(row)
    return Rows, csvFile.line_num
#
#   End GetCsvTable
######################
#
def PlotCompare(X1,Y1,Y2,PltTitle,X1Label,Y1Label,Y2Label,Legend1,Legend2,
                ShareYaxis,PltFile):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    fig = plt.figure(figsize=(8,4), dpi=200) #Inches Width, Height
    fig.suptitle(PltTitle)
    axis_1 = fig.add_subplot(2,1,1)
    axis_1.plot(X1, Y1, '-g' ,label=Legend1)
    axis_1.set_ylabel(Y1Label)
    axis_1.grid("xy")
    axis_1.legend()
    #
    #   Next do axis2
    #   Second Axis
    #
    if (ShareYaxis==1):
        axis_2 = fig.add_subplot(2,1,2, sharex=axis_1,sharey=axis_1)
    else:
        axis_2 = fig.add_subplot(2,1,2, sharex=axis_1)
    axis_2.plot(X1, Y2, color = 'g',label=Legend2)
    axis_2.set_ylabel(Y2Label)
    axis_2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
    axis_2.grid("xy")
    axis_2.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(PltFile)
    plt.show()
    #
    #    End PlotCompare.
    #
#
#    Set working directory
#
print(os.getcwd())
#WDirectory='C:\\Zhanyang\\SensorData\\CompoundFlooding\\SWMM\\PySWMM\\Campus\\Check'
#WDirectory='C:\\Zhanyang\\SensorData\\CompoundFlooding\\SWMM\\PySWMM\\Campus\\All4_3'
WDirectory=r'C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodModel\MesoNetSensorComparison\JanFeb2023App\PlotInFeet'
os.chdir(WDirectory)
print(os.getcwd())
#StreamSensorRows,LenStreamSensorRows=GetCsvTable("CampusStreamSensor.txt")
SensorDataRows,LenSensorDataRows=GetCsvTable("CSI020423DepthFtLine012223.csv")
print('\n FloodNet Sensor SensorDataRows \n')
print(SensorDataRows[0:10],LenSensorDataRows)
#
#PlotCompare(X1=time_stamps,Y1=linkOne_depth,Y2=link_depth,
#            PltTitle="CulvertOne and Sensor Depth"+SCtitle,
#            X1Label="Time",Y1Label="Depth (ft)",Y2Label="Depth (ft)",
#            Legend1="CulvertOne",Legend2="Sensor",ShareYaxis=1,PltFile=CulDeptPltFileName)
#PlotCompare(X1=SensorDataRows[:][0],Y1=SensorDataRows[:][1],Y2=SensorDataRows[2][:],
#            PltTitle="Sensor DEpth and Sensor Depth",
#            X1Label="Time",Y1Label="Depth (ft)",Y2Label="Depth (ft)",
#            Legend1="CulvertOne",Legend2="Sensor",ShareYaxis=1,PltFile="Test.jpg")

print(' Last Line')
#
dt=[]
depth=[]
Row=[]
depthjunk=[]
xrow=[]

for rows in range(LenSensorDataRows-1):
    Row.append(SensorDataRows[rows])
    dt.append(Row[rows][0])
    depth.append(Row[rows][1])
    print(rows)
    depthjunk.append(rows*3.0)
    xrow.append(rows)
#
PlotCompare(X1=dt,Y1=depth,Y2=depth,
            PltTitle="Sensor DEpth and Sensor Depth",
            X1Label="Time",Y1Label="Depth (ft)",Y2Label="Depth (ft)",
            Legend1="CulvertOne",Legend2="Sensor",ShareYaxis=1,PltFile="Test.jpg")

fig = plt.figure(figsize=(8,4), dpi=200)
axis_1 = fig.add_subplot(1,1,1)
#axis_1.plot(time_stamps, node_head, '-g', label="Running Sim")
axis_1.plot(dt, depth, '-g' ,label="Sensor Depth")
plt.show()
#
