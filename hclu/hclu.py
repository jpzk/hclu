"""
This file is part of hclu.

hclu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

hclu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with hclu.  If not, see <http://www.gnu.org/licenses/>.
"""

"""This is the main module containing the Hclu facade"""

import copy
import csv
import numpy as np
import traceback
import sys
import datetime
import random

from strategy import Strategy
from data_file import DataFile
from data_element import DataElement
from hclu_exception import HcluException
from clustering_run import ClusteringRun

# \file hclu.py
# \brief This is the main module containing the Hclu facade.
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
# \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> 
class Hclu(object):
    """This is the main class containing the Hclu facade"""

    # \brief Initialize the Hclu facade.
    def __init__(self):

        self.data_loaded = False
        
        # List with DataElements, which are loaded from file.
        self.data_files = []
       
        # List of clustering runs with additional information.
        self.runs = []

    # \brief This method is used to load data using CSV format.
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    # \pre filename encodes existing file.
    # \post data is loaded.
    # \throw HcluException { throws if loading data failed. }
    def load_data(self, filename):
        """This method is used to load data using CSV format."""

        if(not isinstance(filename, str)):
            raise TypeError("filename is not instance of str.")
        
        data_file = DataFile()
        data_file.filename = filename
        
        try:
            tmp_row = []
            reader = csv.reader(open(filename, 'rb'), delimiter=',')
            for datarow in reader:
                tmp_row.append(datarow)

            data_file.attributes = tmp_row[0]
            for i in xrange(1, len(tmp_row)):
                tmp_data = []
                
                # Convert string values to float
                for element in tmp_row[i][2:]:
                    tmp_data.append(float(element))
                    
                # Generating and appending Data Element
                data_file.elements.append(DataElement(
                    np.array(tmp_data), 
                    tmp_row[i][:2], 
                    data_file.attributes[:2])) 

        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise HcluException("load data failed. terminating.")
        
        data_file.numOfElements = len(tmp_row)-1
        self.data_files.append(data_file)
        
        self.data_loaded = True
        
        print ("Loaded " + str(len(tmp_row)-1) + " datasets")
        
    # \brief Generate new clustering runs with a given strategy and all loaded
    #        datafiles. 
    #        Save results, strategy description and time needed of the run.
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    def cluster(self, strategy):
        """Generate new clustering runs with a given strategy and all 
        loaded datafiles. Save results, strategy description and time 
        needed of the run."""

        if (not isinstance(strategy, Strategy)):
            raise TypeError('strategy is no Strategy Object')
        
        if (not self.data_loaded):
            raise HcluException('There is no data ready for clustering')
        
        for data_file in self.data_files:
            self._cluster(data_file, strategy)
    
    # \brief Help Method for the clustering. Initialize and runs given Strategy
    #        with given data_file and saves the results and run informations.
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def _cluster(self, data_file, strategy):
        """Help Method for the clustering. Initialize and runs given Strategy
        with given data_file and saves the results and run informations."""
        
        # Init Strategy
        init_start_time = datetime.datetime.now()
        strategy.initialize(data_file.elements)

        # Run Strategy
        run_start_time = datetime.datetime.now()
        strategy.run()
        end_time = datetime.datetime.now()
        
        complete_runtime = end_time - init_start_time
        
        # Save Run Resuls
        self.runs.append(ClusteringRun(\
            data_file.filename,
            strategy.description, 
            strategy.distance_function.description, 
            init_start_time, 
            run_start_time, 
            end_time,
            complete_runtime,
            strategy.clustering))
