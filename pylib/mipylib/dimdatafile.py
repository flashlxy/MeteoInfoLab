#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-27
# Purpose: MeteoInfo Dataset module
# Note: Jython
#-----------------------------------------------------
from org.meteoinfo.data.meteodata import MeteoDataInfo
from ucar.ma2 import Section
import dimvariable
from dimvariable import DimVariable
import dimarray
from dimarray import PyGridData, PyStationData

from datetime import datetime

from java.util import Calendar

# Dimension dataset
class DimDataFile():
    
    # dataset must be org.meteoinfo.data.meteodata.MeteoDataInfo
    def __init__(self, dataset=None):
        self.dataset = dataset
        self.filename = dataset.getFileName()
        self.nvar = dataset.getDataInfo().getVariableNum()
        self.fill_value = dataset.getMissingValue()
        self.proj = dataset.getProjectionInfo()
        
    def __getitem__(self, key):
        if isinstance(key, str):
            print key
            return DimVariable(self.dataset.getDataInfo().getVariable(key), self)
        return None
        
    def __str__(self):
        return self.dataset.getInfoText()
        
    def __repr__(self):
        return self.dataset.getInfoText()
        
    def read(self, varname, origin, size, stride):
        return self.dataset.read(varname, origin, size, stride)
        
    def dump(self):
        print self.dataset.getInfoText()
        
    def griddata(self, varname='var', timeindex=0, levelindex=0, yindex=None, xindex=None):
        if self.dataset.isGridData():
            self.dataset.setTimeIndex(timeindex)
            self.dataset.setLevelIndex(levelindex)
            gdata = PyGridData(self.dataset.getGridData(varname))
            return gdata
        else:
            return None
        
    def stationdata(self, varname='var', timeindex=0, levelindex=0):
        if self.dataset.isStationData():
            self.dataset.setTimeIndex(timeindex)
            self.dataset.setLevelIndex(levelindex)
            sdata = PyStationData(self.dataset.getStationData(varname))
            return sdata
        else:
            return None
            
    def gettime(self, idx):
        date = self.dataset.getDataInfo().getTimes().get(idx)
        cal = Calendar.getInstance()
        cal.setTime(date)
        year = cal.get(Calendar.YEAR)
        month = cal.get(Calendar.MONTH) + 1
        day = cal.get(Calendar.DAY_OF_MONTH)
        hour = cal.get(Calendar.HOUR_OF_DAY)
        minute = cal.get(Calendar.MINUTE)
        second = cal.get(Calendar.SECOND)
        dt = datetime(year, month, day, hour, minute, second)
        return dt