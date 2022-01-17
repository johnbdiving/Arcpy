import arcpy
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
InputFC = arcpy.GetParameterAsText(1)
arcpy.AddMessage(InputFC)
OutputFC = arcpy.GetParameterAsText(2)
arcpy.management.Merge(InputFC, OutputFC)
arcpy.AddMessage("\nScript Complete")

