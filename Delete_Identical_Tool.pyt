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
        self.tools = [DeleteIdenticalTool] 


class DeleteIdenticalTool(object): 
    def __init__(self): 
        """Define the tool (tool name is the name of the class)."""
        self.label = 'Delete Identical Points'
        self.description = '' 
        self.canRunInBackground = True

    def getParameterInfo(self): 
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = 'Input Survey Point Feature Class', 
                                 name = 'inputSurveyFeatures', 
                                 datatype = 'DEFeatureClass', 
                                 parameterType = 'Required',
                                 direction = 'Input')

        param1 = arcpy.Parameter(displayName = 'Spatial Tolerance ([dist] [unit])', 
                                 name = 'tolerance', 
                                 datatype = 'String', 
                                 parameterType = 'Required', 
                                 direction = 'Input') 

        # Default values 
        param1.value = '0.01 METERS'
        return [param0, param1] 

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
        inputSurveyFeatures = parameters[0].valueAsText 
        arcpy.AddMessage('input Survey Features: {}'.format(inputSurveyFeatures))

        inputTolerance = parameters[1].value
        arcpy.AddMessage('Tolerance: {}'.format(inputTolerance))

        arcpy.management.DeleteIdentical(inputSurveyFeatures,"SHAPE", inputTolerance, 0)
        arcpy.AddMessage(arcpy.GetMessages())
        arcpy.AddMessage("Tool Complete")

