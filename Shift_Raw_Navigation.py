import os
import pandas as pd
import csv
import glob

## read csv file into dataframe
rawFile=arcpy.GetParameterAsText(0)
eastingShift=arcpy.GetParameterAsText(1)
eastingField=arcpy.GetParameterAsText(2)
northingShift=arcpy.GetParameterAsText(3)
northingField=arcpy.GetParameterAsText(4)
outputWorkspace=arcpy.GetParameterAsText(5)
outputFileName=arcpy.GetParameterAsText(6)

df=pd.read_csv(rawFile)
arcpy.AddMessage(df.columns)
arcpy.AddMessage(df.size)

##run conversions to shift X and Y navigation 
df['easting_shift']=float(eastingShift)
df['X']=(df['{0}'.format(eastingField)]+df['easting_shift']).round(2)
df['northing_shift']=float(northingShift)
df['Y']=(df['{0}'.format(northingField)]+df['northing_shift']).round(2)

arcpy.AddMessage(df.columns)
arcpy.AddMessage(df.size)

##select columns to remove prior to export into ouput table 
del df['easting_shift']
del df['northing_shift']
del df['{0}'.format(eastingField)]
del df['{0}'.format(northingField)]

arcpy.AddMessage(df.columns)
arcpy.AddMessage(df.size)

## export result as csv file
os.chdir(outputWorkspace)
df.to_csv('{0}.txt'.format(outputFileName),index=False)

arcpy.AddMessage("Navigation Shifting Completed")

