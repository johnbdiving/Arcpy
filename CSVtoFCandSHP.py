##script executes a function to import XY point data from a table to a feature class within a defined GDB as well as a shapefile in another defined folder or workspace
##script needs to be implemented in ArcGIS Pro

import arcpy

arcpy.env.workspace=arcpy.GetParameterAsText(0)
## parameter 0 = user defined workspace GDB, data type is workspace
arcpy.env.overwriteOutput = True

InputCSV=arcpy.GetParameterAsText(1)
## parameter 1 = input table, data type is table
XField=arcpy.GetParameterAsText(2)
## parameter 2 = Longitude or Northing, data type is field, dependency upon InputCSV
YField=arcpy.GetParameterAsText(3)
## parameter 3 = Latitude or Easting, data type is field, dependency upon InputCSV
OutputFCName=arcpy.GetParameterAsText(4)
## parameter 4 = output feature class name, data type is string, name of output FC, note: cannot start with number
sr=arcpy.GetParameterAsText(5)
## parameter 5 = spatial reference, data type is spatial reference to match CRS in in put table

arcpy.management.XYTableToPoint(InputCSV, OutputFCName, XField, YField, None, sr) 
arcpy.AddMessage("Point Feature Class Created")

InputFC=OutputFCName 
## this takes to created FC rom the first step and adds to the next FC conversion task 
NetworkSHPFolder=arcpy.GetParameterAsText(6)
## parameter 6 = output folder; data type is folder, navigate to workspace for writing addtional shapefile
OutputSHP=arcpy.GetParameterAsText(7)
##parameter 7 = output SHP File name, data type is string, name of shapefile 
 
arcpy.conversion.FeatureClassToFeatureClass(InputFC, NetworkSHPFolder, OutputSHP)
arcpy.AddMessage("Point Features Exported to SHP")

arcpy.AddMessage("\nScript Complete")

