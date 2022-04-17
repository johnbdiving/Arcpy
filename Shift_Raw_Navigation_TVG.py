import os
import pandas as pd
import csv
import glob

## read csv file into dataframe
rawFile=arcpy.GetParameterAsText(0)
eastingShift=arcpy.GetParameterAsText(1)
northingShift=arcpy.GetParameterAsText(2)
COGeastingField=arcpy.GetParameterAsText(3)
COGnorthingField=arcpy.GetParameterAsText(4)
PORTeastingField=arcpy.GetParameterAsText(5)
PORTnorthingField=arcpy.GetParameterAsText(6)
STBDeastingField=arcpy.GetParameterAsText(7)
STBDnorthingField=arcpy.GetParameterAsText(8)
outputWorkspace=arcpy.GetParameterAsText(9)
outputFileName=arcpy.GetParameterAsText(10)

df=pd.read_csv(rawFile)
arcpy.AddMessage(df.columns)
arcpy.AddMessage(df.size)

##run conversions to shift X and Y navigation at instrument cog
df['easting_shift']=float(eastingShift)
df['X_cog']=(df['{0}'.format(COGeastingField)]+df['easting_shift']).round(2)
df['northing_shift']=float(northingShift)
df['Y_cog']=(df['{0}'.format(COGnorthingField)]+df['northing_shift']).round(2)

##shift X and Y navigation at tvg port node
df['easting_shift']=float(eastingShift)
df['X_portNode']=(df['{0}'.format(PORTeastingField)]+df['easting_shift']).round(2)
df['northing_shift']=float(northingShift)
df['Y_portNode']=(df['{0}'.format(PORTnorthingField)]+df['northing_shift']).round(2)

##shift X and Y navigation at tvg starboard node
df['easting_shift']=float(eastingShift)
df['X_stbdNode']=(df['{0}'.format(STBDeastingField)]+df['easting_shift']).round(2)
df['northing_shift']=float(northingShift)
df['Y_stbdNode']=(df['{0}'.format(STBDnorthingField)]+df['northing_shift']).round(2)

arcpy.AddMessage(df.columns)
arcpy.AddMessage(df.size)

##select columns to remove prior to export into ouput table 
del df['easting_shift']
del df['northing_shift']
del df['{0}'.format(COGeastingField)]
del df['{0}'.format(COGnorthingField)]
del df['{0}'.format(PORTeastingField)]
del df['{0}'.format(PORTnorthingField)]
del df['{0}'.format(STBDeastingField)]
del df['{0}'.format(STBDnorthingField)]

arcpy.AddMessage(df.columns)
arcpy.AddMessage(df.size)

## export result as csv file
os.chdir(outputWorkspace)
df.to_csv('{0}.txt'.format(outputFileName),index=False)

arcpy.AddMessage("Navigation Shifting Completed")

