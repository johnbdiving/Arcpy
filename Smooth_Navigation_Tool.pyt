import sys
import os
import arcpy 
import numpy 
import datetime
import math
import pandas as pd
import glob
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from arcpy.sa import *

class Toolbox(object): 
    def __init__(self): 
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = 'Magnetometer Survey Toolbox'
        self.alias = '' 

        # List of tool classes associated with this toolbox 
        self.tools = [SmoothRawNavigationTool] 

class SmoothRawNavigationTool(object): 
    def __init__(self): 
        """Define the tool (tool name is the name of the class)."""
        self.label = 'Smooth Raw Navigation'
        self.description = '' 
        self.canRunInBackground = True

    def getParameterInfo(self): 
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = 'Input Raw File', 
                                 name = 'inputRawFile', 
                                 datatype = 'Table', 
                                 parameterType = 'Required',
                                 direction = 'Input')

        param1 = arcpy.Parameter(displayName = 'Rolling Stats Window Size', 
                                 name = 'window', 
                                 datatype = 'Double', 
                                 parameterType = 'Required', 
                                 direction = 'Input')

        param2 = arcpy.Parameter(displayName = 'X field', 
                                 name = 'xfield', 
                                 datatype = 'Field', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param3 = arcpy.Parameter(displayName = 'Y field', 
                                 name = 'yfield', 
                                 datatype = 'Field', 
                                 parameterType = 'Required', 
                                 direction = 'Input')

        param4 = arcpy.Parameter(displayName = 'Line field', 
                                 name = 'inputLinefield', 
                                 datatype = 'Field', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param5 = arcpy.Parameter(displayName = 'NavSmth Temp Directory', 
                                 name = 'navSmthPathway', 
                                 datatype = 'Workspace', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param6 = arcpy.Parameter(displayName = 'Output Pathway', 
                                 name = 'outputPathway', 
                                 datatype = 'Workspace', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param7 = arcpy.Parameter(displayName = 'Output File Name (append _smth)', 
                                 name = 'outputFileName', 
                                 datatype = 'String', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 
        # Default values 
        param1.value = 5
        param2.value = "Field1"
        param3.value = "Field2"
        param6.value = "outfile"

        param2.parameterDependencies = [param0.name]
        param3.parameterDependencies = [param0.name]
        param4.parameterDependencies = [param0.name]
        return [param0, param1, param2, param3, param4, param5, param6, param7] 


    def isLicensed(self): 
        """Set whether tool is licensed to execute."""
        try: 
            if arcpy.SetProduct('arcinfo') == "NotLicensed": 
                raise Exception 
        except Exception: 
            return False
        return True

    def updateParameters(self, parameters): 
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        # Set input variables 
        inputRawFile = parameters[0].valueAsText 
        arcpy.AddMessage('Raw File: {}'.format(inputRawFile))

        window=(int(parameters[1].value))
        arcpy.AddMessage('Rolling Stats Window Size: {} points'.format(window))

        inputXfield=parameters[2].valueAsText

        inputYfield=parameters[3].valueAsText

        inputLinefield=parameters[4].valueAsText

        navSmthPathway=parameters[5].valueAsText

        outputWorkspace=parameters[6].valueAsText

        outputFileName=parameters[7].valueAsText 

        inputTable=pd.read_csv(r'{}'.format(inputRawFile))
        df=pd.DataFrame(inputTable)
        arcpy.AddMessage("Read raw file")

        ##iterate a list of unique line names
        lineNameList=df['{}'.format(inputLinefield)].unique()
        arcpy.AddMessage(lineNameList)
        arcpy.AddMessage("Total Number of Lines: {}".format(len(lineNameList)))

        ## define a function to perform a rolling stats computation on single line of data
        def rollingStatsperLine(x): 
            arcpy.AddMessage("Line Name: {}".format(lineNameList[x]))
            mask=df['{}'.format(inputLinefield)]==lineNameList[x]
            dfx=df[mask].copy()
            dfx['{}_smth'.format(inputXfield)]=dfx['{}'.format(inputXfield)].rolling(window,center=True).mean()
            dfx['{}_smth'.format(inputYfield)]=dfx['{}'.format(inputYfield)].rolling(window,center=True).mean()
            dfx.to_csv(r"{}\{}{}.txt".format(navSmthPathway,outputFileName,x),float_format='%.2f',index=False)
            return

        ## call the function and run as iterations of the line name list
        x=0
        while x <= len(lineNameList):
            rollingStatsperLine(x)
            x +=1
            if x == len(lineNameList):
                break

        ## read directory of CSV files generated for each df split by line, merge into a single df
        path =(r"{}".format(navSmthPathway))
        all_files = glob.glob(os.path.join(path,"{}*.txt".format(outputFileName)))
        df_from_each_file = (pd.read_csv(f,sep=',')for f in all_files)
        df_merged = pd.concat(df_from_each_file,ignore_index=True)
        df_final=df_merged.dropna()
        arcpy.AddMessage("Merged Resutls")

        ## export merged df as full csv file
        os.chdir(r"{}".format(outputWorkspace))
        df_final.to_csv("{}_navsmth.txt".format(outputFileName),index=False)

        for f in all_files:
            os.remove(f)

        arcpy.AddMessage("completed line smoothing")

