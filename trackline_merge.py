import arcpy
import pandas as pd
import os

arcpy.env.workspace=arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput=True
inputTracklines=arcpy.GetParameterAsText(1)
mergeFC=arcpy.GetParameterAsText(2)
outputFolder=arcpy.GetParameterAsText(3)
outputCSV=arcpy.GetParameterAsText(4)

inputList=arcpy.ListFeatureClasses()
for fc in inputList:
    arcpy.DeleteField_management(fc,["Line Path","Resolution","Locked","modTime","dataConfid","rawDataPat"])

arcpy.env.workspace=arcpy.GetParameterAsText(5)
arcpy.env.overwriteOutput=True

arcpy.management.Merge(inputTracklines,mergeFC)
arcpy.conversion.TableToTable(mergeFC,outputFolder,outputCSV)

mergeFCtable=pd.read_csv("{}\{}".format(outputFolder,outputCSV))
df=pd.DataFrame(mergeFCtable)
df['Min_Time']=pd.to_datetime(df['Min_Time'],format='%Y-%m-%d  %H:%M:%S.%f')
df['Max_Time']=pd.to_datetime(df['Max_Time'],format='%Y-%m-%d  %H:%M:%S.%f')
df['Online_Time']=(df.Max_Time - df.Min_Time)/pd.Timedelta(hours=1)

onlineTime=df['Online_Time'].sum().round(2)
arcpy.AddMessage("Total Online Time: {} hours".format(onlineTime))

tracklineLength=df['length'].sum().round(3)
arcpy.AddMessage("Total Online Distance: {} meters".format(tracklineLength))

averageSpeed=df['speed'].mean().round(2)
arcpy.AddMessage("Average Online Speed: {} m/s".format(averageSpeed))

os.remove("{}\{}".format(outputFolder,outputCSV))
os.remove("{}\{}.xml".format(outputFolder,outputCSV))   

arcpy.AddMessage("Script Complete")
