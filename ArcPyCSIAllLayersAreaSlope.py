#
#   July 1, 2023
#   ArcPyCSIListGroupLayer
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
#
#   List the layers in a Group and subgroup
#   Calculate the area of the polygons and average slope
#   of the raster slope.
#
import arcpy, os
from arcpy import env
from arcpy.sa import *
#   Check out the Spatial Analysis Tool Box to prevent license error.
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
#
#   End Header -----
#
def shedarea(in_poly, atype, aunits):
    sumarea = 0
    with arcpy.da.SearchCursor(in_poly, "SHAPE@") as rows:
        for row in rows:
            sumarea += row[0].getArea(atype, aunits)
    return sumarea
#
#   Average Slope
#
def aveslope(inslope):
    # Process: Get Raster Properties
    MeanSlope = arcpy.GetRasterProperties_management(inslope, "MEAN", "")
    return MeanSlope
#
WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodingPythonSource\DEMtoSubcatchmentWork"
os.chdir(WDirectory)
print("Working Directory for the resulting txt file "+os.getcwd())
#
CatchDir="C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\ShapeOutfall\\"
OutputFileAS="CSISCAreaSlope.txt"
outputAS = file(OutputFileAS, "w")  
print("Opened Output " + OutputFileAS +" \n")
outputAS.write("Name, Area (Acrea), Average Slope \n")
#
OutputFile="CSISCLayers.txt"
outputSC = file(OutputFile, "w")  
print("Opened Output " + OutputFile +" \n")
outputSC.write("Name, Area (Acrea), Average Slope \n")
OutputFileRas="CSISCLayersRas.txt"
outputRas = file(OutputFileRas, "w")  
print("Opened Output " + OutputFileRas +" \n")
outputRas.write("Name, Area (Acrea), Average Slope \n")
#
def listGroupLayer(glayername):
    #   If standalone ues:
    Map=r"C:\Zhanyang\SensorData\CompoundFlooding\VRVis\Transfer\NYC_DEM_Revised\NYCDEMRevised.mxd"
    #   Else use the following:
    #mxd = arcpy.mapping.MapDocument('CURRENT')
    mxd = arcpy.mapping.MapDocument(Map)
    df = mxd.activeDataFrame
    layers = arcpy.mapping.ListLayers(df)
    count = 0
    SCGroup=list(range(2,92,4))
    SCPoly=list(range(3,92,4))
    SCRaster=list(range(5,94,4))
    SCAllLayers=[]
    for l in layers:
        if l.isGroupLayer and l.name == glayername:
            print "Layers in " + glayername + ":"
            glayers = arcpy.mapping.ListLayers(l)
            for gl in glayers:
                count = count + 1
                SCAllLayers.append(gl.name)
                if count in SCGroup:
                    outputAS.write(gl.name+",")
                    print("gl.name"+gl.name)
                if count in SCPoly:
                    outputSC.write(gl.name+",")
                    CatchFile=CatchDir+gl.name+".shp"
                    print("catchfile"+CatchFile+",",gl.name)
                    #
                    #   Area ---
                    #
                    atype="GEODESIC"
                    aunits="ACRES"
                    sumarea = shedarea(CatchFile, atype, aunits)
                    print(CatchFile+","+gl.name)
                    print(sumarea)
                    outputAS.write(str(sumarea)+",")
                if count in SCRaster:
                    outputRas.write(gl.name+",")
                    SlopeFile=CatchDir+gl.name
                    #
                    #   Average slope
                    #
                    #print(SlopeFile)
                    MeanSlope = aveslope(SlopeFile)
                    outputAS.write(str(MeanSlope)+"\n")
                    print(MeanSlope)

# use as 
listGroupLayer("CSISubcatchments")
outputSC.write("\n")
outputSC.close()
outputRas.write("\n")
outputRas.close()
outputAS.write("\n")
outputAS.close()
#listGroupLayer("MyGroupLayer")

#Reference:  https://community.esri.com/t5/python-questions/listing-layers-in-a-group/td-p/736543
