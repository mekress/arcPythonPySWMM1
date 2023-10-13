#
#   July 1, 2023
#   ArcPyCSIAllLayersAreaSlope
#   Derived from:  ArcPyCSIListGroupLayer
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
#
#   ArcPyCSIAllLayersAreaSlope.py
#
#   The purpose of this routine is to calculate the area
#   and average slope of subcatchments.  The file names are
#   obtained from the map file and depends on the groups and the order
#   that the shape and raster files are listed.
#   This routine is based on ArcPyCSIGetAreaAverageSlope.py which
#   does the same calculation but less automated.
#
#   A key component of the automation process is listGroupLayer which
#   lists the layers in a Group and subgroup
#   Calculate the area of the polygons and average slope
#   of the raster slope.
#   Note:  This depends on the order of the subcatchment polygon shape file,
#       pour point shape file and slope raster file in each member of the group.
#   July 1, 2023, initial coding.
#   July 21, 2023,  code clean-up, testing and verification.
#   Oct 10, 2023,  Rerun with different catchments and slopes and
#   code clean up.
#   Future development think about specify fewer run specific
#   parameters and calculate the file names.
#
# ---------------------------------------------------------------------------
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
#   Define subroutines. -----------------------------
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
#   Define the subroutine which traverses the subdirectories and do calculations.
#
def listGroupLayer(glayername):
    #   If standalone ues:
    #Map=r"C:\Zhanyang\SensorData\CompoundFlooding\VRVis\Transfer\NYC_DEM_Revised\NYCDEMRevised.mxd"
    Map=r"C:\Zhanyang\SensorData\CompoundFlooding\VRVis\Transfer\NYC_DEM_Revised\NYCDEMReviDecDeg.mxd"
    #   Else use the following:
    #mxd = arcpy.mapping.MapDocument('CURRENT')
    mxd = arcpy.mapping.MapDocument(Map)
    df = mxd.activeDataFrame
    layers = arcpy.mapping.ListLayers(df)
    #print('Layers')
    #print(layers)
    count = 0
    #
    #   Specify the indices of the shape and raster files.
    #
    #SCGroup=list(range(2,92,4))
    SCGroup=list(range(2,15,4))
    #SCPoly=list(range(3,92,4))
    SCPoly=list(range(3,16,4))
    #SCRaster=list(range(5,94,4))
    SCRaster=list(range(5,18,4))
    SCAllLayers=[]
    for l in layers:
        if l.isGroupLayer and l.name == glayername:
            #print "Layers in " + glayername + ":"
            glayers = arcpy.mapping.ListLayers(l)
            for gl in glayers:
                count = count + 1
                SCAllLayers.append(gl.name)
                if count in SCGroup:
                    outputAS.write(gl.name+",")
                    print("gl.name"+gl.name)
                if count in SCPoly:
                    outputSC.write(gl.name+"\n")
                    CatchFile=CatchDir+gl.name+".shp"
                    #print("catchfile"+CatchFile+",",gl.name)
                    #
                    #   Area ---
                    #
                    atype="GEODESIC"
                    aunits="ACRES"
                    sumarea = shedarea(CatchFile, atype, aunits)
                    #print(CatchFile+","+gl.name)
                    print('Area=',sumarea)
                    outputAS.write(str(sumarea)+",")
                if count in SCRaster:
                    outputRas.write(gl.name+"\n")
                    SlopeFile=CatchDir+gl.name
                    #
                    #   Average slope
                    #
                    #print(SlopeFile)
                    MeanSlope = aveslope(SlopeFile)
                    outputAS.write(str(MeanSlope)+"\n")
                    print('Average Slope=',MeanSlope)
#
#   Do Calculation. --------------------------------------
#
#   --- Specify the run specific directories and file names:
#
#   Specify working directory for output text file and output file names.
#
WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\SWMM\PySWMM\Campus\Juy2023Subcatchments"
#WDirectory=r"C:\Zhanyang\SensorData\CompoundFlooding\CompoundFloodingPythonSource\DEMtoSubcatchmentWork"
os.chdir(WDirectory)
print("Working Directory for the resulting txt file "+os.getcwd())
#
#OutputFileAS="CSISCAreaSlope1.txt"
OutputFileAS="S2RevSCAreaSlope1.txt"
outputAS = file(OutputFileAS, "w")  
print("Opened Output " + OutputFileAS +" \n")
outputAS.write("Name, Area (Acrea), Average Slope \n")
#
#OutputFile="CSISCLayers1.txt"
OutputFile="S2RevSCLayers1.txt"
outputSC = file(OutputFile, "w")  
print("Opened Output " + OutputFile +" \n")
outputSC.write("Shape file names \n")
#
#OutputFileRas="CSISCLayersRas1.txt"
OutputFileRas="S2RevSCLayersRas1.txt"
outputRas = file(OutputFileRas, "w")  
print("Opened Output " + OutputFileRas +" \n")
outputRas.write("Raster file names \n")
#
#
#   Specify the location of the GIS files containing the subcatchment shape files and raster slope files.
#
CatchDir="C:\\Zhanyang\\SensorData\\CompoundFlooding\\SWMM\\PySWMM\\Campus\\Juy2023Subcatchments\\"
#CatchDir="C:\\Zhanyang\\SensorData\\CompoundFlooding\\CompoundFloodModel\\DEMtoSubcatchment\\ShapeOutfall\\"
#
#   
#   --- Execute the routine on the group name, CSISubcatchments the
#       original data and later of S2Revised.
#
#listGroupLayer("CSISubcatchments")
listGroupLayer("S2Revised")
outputSC.write("\n")
outputSC.close()
outputRas.write("\n")
outputRas.close()
outputAS.write("\n")
outputAS.close()
#
#   Fini
#
#Reference:  https://community.esri.com/t5/python-questions/listing-layers-in-a-group/td-p/736543

