#
#   July 1, 2023
#   ArcPyCSIListGroupLayer
#   Michael E. Kress, Ph. D.
#   College of Staten Island, CUNY
#
#   List the layers in a Group and subgroup

import arcpy, os
from arcpy import env
from arcpy.sa import *
#   Check out the Spatial Analysis Tool Box to prevent license error.
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
#
#   End Header -----
#
def listGroupLayer(glayername):
    #   If standalone ues:
    Map=r"C:\Zhanyang\SensorData\CompoundFlooding\VRVis\Transfer\NYC_DEM_Revised\NYCDEMRevised.mxd"
    #   Else use the following:
    #mxd = arcpy.mapping.MapDocument('CURRENT')
    mxd = arcpy.mapping.MapDocument(Map)
    df = mxd.activeDataFrame
    layers = arcpy.mapping.ListLayers(df)
    for l in layers:
        if l.isGroupLayer and l.name == glayername:
            print "Layers in " + glayername + ":"
            glayers = arcpy.mapping.ListLayers(l)
            for gl in glayers:
                print gl.name
                # apply symbology
                #arcpy.ApplySymbologyFromLayer_management(gl,r"C:\GIS\lyrfiles\mylayersymbology.lyr")

# use as 
listGroupLayer("CSISubcatchments")
#listGroupLayer("MyGroupLayer")

#Reference:  https://community.esri.com/t5/python-questions/listing-layers-in-a-group/td-p/736543
