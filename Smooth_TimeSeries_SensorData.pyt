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
        self.tools = [SmoothRawAltitudeTool] 

class SmoothRawAltitudeTool(object): 
    def __init__(self): 
        """Define the tool (tool name is the name of the class)."""
        self.label = 'Smooth Raw Altitude'
        self.description = '' 
        self.canRunInBackground = True

    def getParameterInfo(self): 
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = 'Input Raw File', 
                                 name = 'inputRawFile', 
                                 datatype = 'Table', 
                                 parameterType = 'Required',
                                 direction = 'Input')

        param1 = arcpy.Parameter(displayName = 'Altitude Max Threshold', 
                                 name = 'altMax', 
                                 datatype = 'Double', 
                                 parameterType = 'Required', 
                                 direction = 'Input')

        param2 = arcpy.Parameter(displayName = 'Rolling Stats Window Size', 
                                 name = 'window', 
                                 datatype = 'Double', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param3 = arcpy.Parameter(displayName = 'Altitude field', 
                                 name = 'inputAltfield', 
                                 datatype = 'Field', 
                                 parameterType = 'Required', 
                                 direction = 'Input')

        param4 = arcpy.Parameter(displayName = 'Line field', 
                                 name = 'inputLinefield', 
                                 datatype = 'Field', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param5 = arcpy.Parameter(displayName = 'Time field', 
                                 name = 'inputTimefield', 
                                 datatype = 'Field', 
                                 parameterType = 'Required', 
                                 direction = 'Input')                         

        param6 = arcpy.Parameter(displayName = 'AltSmth Temp Directory', 
                                 name = 'altSmthPathway', 
                                 datatype = 'Workspace', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param7 = arcpy.Parameter(displayName = 'Output Pathway', 
                                 name = 'outputPathway', 
                                 datatype = 'Workspace', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        param8 = arcpy.Parameter(displayName = 'Output File Name (tool will append _Altsmth)', 
                                 name = 'outputFileName', 
                                 datatype = 'String', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 
        
        # Default values 
        param1.value = 20
        param2.value = 5
        param3.value = "Field2"
        param4.value = "Field3"
        param5.value = "Field4"
        param6.value = "outfile"

        param3.parameterDependencies = [param0.name]
        param4.parameterDependencies = [param0.name]
        param5.parameterDependencies = [param0.name]
        return [param0, param1, param2, param3, param4, param5, param6, param7,param8] 


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

        altMax=(int(parameters[1].value))
        arcpy.AddMessage('Altitude Maximum Threshold: {}'.format(altMax))

        window=(int(parameters[2].value))
        arcpy.AddMessage('Rolling Stats Window Size: {} points'.format(window))

        inputAltfield=parameters[3].valueAsText

        inputLinefield=parameters[4].valueAsText

        inputTimefield=parameters[5].valueAsText

        altSmthPathway=parameters[6].valueAsText

        outputWorkspace=parameters[7].valueAsText

        outputFileName=parameters[8].valueAsText 

        inputTable=pd.read_csv(r'{}'.format(inputRawFile))
        df=pd.DataFrame(inputTable)
        arcpy.AddMessage("Read raw file")

        # plot raw altitude; use this to confirm or adjust max alt threshold
        plt.style.use('classic')
        x=df['{}'.format(inputTimefield)]
        y=df['{}'.format(inputAltfield)]
        fig,ax=plt.subplots()
        ax.plot(x,y, linewidth=1.0)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(True)
        plt.savefig(r"{}\{}.png".format(altSmthPathway,outputFileName))

        ##iterate a list of unique line names
        lineNameList=df['{}'.format(inputLinefield)].unique()
        arcpy.AddMessage(lineNameList)
        arcpy.AddMessage("Total Number of Lines: {}".format(len(lineNameList)))

        df['{}_dspk'.format(inputAltfield)]=df['{}'.format(inputAltfield)].where(df['{}'.format(inputAltfield)]< altMax)

        ## define a function to perform a rolling stats computation on single line of data
        def rollingStatsperLine(x): 
            arcpy.AddMessage("Line Name: {}".format(lineNameList[x]))
            mask=df['{}'.format(inputLinefield)]==lineNameList[x]
            dfx=df[mask].copy()
            dfx['{}_intp'.format(inputAltfield)]=dfx['{}_dspk'.format(inputAltfield)].interpolate(method='linear')
            dfx['{}_smth'.format(inputAltfield)]=dfx['{}_intp'.format(inputAltfield)].rolling(window,center=True).mean()
            dfx.to_csv(r"{}\{}ln{}.txt".format(altSmthPathway,outputFileName,x),float_format='%.2f',index=False)
        ##plot raw channel
            plt.style.use('classic')
            a=dfx['{}'.format(inputTimefield)]
            b=dfx['{}'.format(inputAltfield)]
            fig,ax=plt.subplots()
            ax.plot(a,b, linewidth=1.0)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(True)
            plt.savefig(r"{}\1_raw_{}_ln{}.png".format(altSmthPathway,outputFileName,x))
        ##plot despike channel result 
            plt.style.use('classic')
            c=dfx['{}'.format(inputTimefield)]
            d=dfx['{}_dspk'.format(inputAltfield)]
            fig,ax=plt.subplots()
            ax.plot(c,d, linewidth=1.0)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(True)
            plt.savefig(r"{}\2_dspk_{}_ln{}.png".format(altSmthPathway,outputFileName,x))
        ##plot smoothed channel result
            plt.style.use('classic')
            e=dfx['{}'.format(inputTimefield)]
            f=dfx['{}_smth'.format(inputAltfield)]
            fig,ax=plt.subplots()
            ax.plot(e,f, linewidth=1.0)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(True)
            plt.savefig(r"{}\3_smth_{}_ln{}.png".format(altSmthPathway,outputFileName,x))
            return


        ## call the function and run as iterations of the line name list
        x=0
        while x <= len(lineNameList):
            rollingStatsperLine(x)
            x +=1
            if x == len(lineNameList):
                break

        ## read directory of CSV files generated for each df split by line, merge into a single df
        path =(r"{}".format(altSmthPathway))
        all_files = glob.glob(os.path.join(path,"{}*.txt".format(outputFileName)))
        df_from_each_file = (pd.read_csv(f,sep=',')for f in all_files)
        df_merged = pd.concat(df_from_each_file,ignore_index=True)
        df_final=df_merged.dropna()
        arcpy.AddMessage("Merged Resutls")

        ## export merged df as full csv file
        os.chdir(r"{}".format(outputWorkspace))
        df_final.to_csv("{}_Altsmth.txt".format(outputFileName),index=False)

        for f in all_files:
            os.remove(f)

        arcpy.AddMessage("completed altitude smoothing")