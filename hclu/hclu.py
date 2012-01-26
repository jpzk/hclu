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
        """Generate new clustering runs with a given strategy and all loaded datafiles.
        Save results, strategy description and time needed of the run."""

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
    
    # \brief Generate Test Runs of given strategy over parts of file with
    #        given index. Parts will grow each run with step_size.
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>    
    def speed_test_strategy(self, strategy, index_of_file, step_size):
        '''
        Generate Test Runs of given strategy over parts of file with
        given index. Parts will grow each run with step_size.
        '''
        if (not isinstance(strategy, Strategy)):
            raise TypeError('strategy is no Strategy Object')            
        
        if (len(self.data_files) < index_of_file):
            raise HcluException("There is no file with given index loaded.")
        
        orig_file = self.data_files[index_of_file]
        
        curr_step = step_size
        
        while (curr_step <= len(orig_file.elements)):
            curr_file = copy.deepcopy(orig_file)
            
            curr_file.elements = curr_file.elements[:curr_step]
            curr_file.filename+="["+str(curr_step)+"]"
            
            self._cluster(curr_file, strategy)
            
            curr_step += step_size
            
    # \brief Generate given number of est Runs of given strategy. Uses samples 
    #        with given size from given file. 
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>    
    def quality_test_strategy(self, strategy, index_of_file, sample_size, 
                              num_of_tests):
        ''' Generate given number of est Runs of given strategy. Uses samples 
        with given size from given file. '''
        
        if (not isinstance(strategy, Strategy)):
            raise TypeError('strategy is no Strategy Object')            
        
        if (len(self.data_files) < index_of_file):
            raise HcluException("There is no file with given index loaded.")
                
        curr_file = copy.deepcopy(self.data_files[index_of_file])
        
        for i in xrange(num_of_tests):
            curr_file.elements = random.sample(
                self.data_files[index_of_file].elements, sample_size)

            self._cluster(curr_file, strategy)
        
    
    # \brief Returns the Distribution of given Attribute in given Level 
    #        of given Clustering Run. Result will be returned as a 2 level 
    #        dictionary: Level 1 key is the cluster id, Level 2 key the
    #        content of the Attribute, Level 2 Value the number of Elements 
    #        with that content.
    #
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def get_distribution_of_clustering(self, 
        num_of_clustering_run, num_of_level, attribute):
        """Returns the Distribution of given Attribute in given Level of 
           given Clustering Run. Result will be returned as a 2 level dictionary: 
           Level 1 key is the cluster id, Level 2 key the content of the Attribute, 
           Level 2 Value the number of Elements with that content."""
        
        # Check existence of Clustering
        if (len(self.runs) < num_of_clustering_run):
            raise HcluException("There are no clustering run with given number!")
        
        run = self.runs[num_of_clustering_run]

        # Check existence of Level
        if (len(run.clustering) < num_of_level):
            raise HcluException("There are no level with given number!")
        
        level = run.clustering[num_of_level]
        
        # Preparing Result
        result = {}
        
        # Iterating and counting
        for key, cluster in level.iteritems():
            tmp = {}

            for elem in cluster.elements:
                if (elem.attributes[attribute] not in tmp):
                    tmp[elem.attributes[attribute]] = 1
                else:
                    tmp[elem.attributes[attribute]] += 1
                    
            result[key] = tmp
            
            
        # Returnin Result
        return result
    
    # \brief Determines the error of the clustering with given index on given 
    #        attribute and level
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def determine_clustering_error(self, 
        num_of_clustering_run, num_of_level, attribute):
        ''' Determines the error of the clustering with given index on given 
        attribute and level'''
        
        dist = self.get_distribution_of_clustering(num_of_clustering_run,\
            num_of_level, attribute)
        
        orig_dist = dist.copy()

        # Determine cluster name
        named_cluster = {}
        used_keys = {}
        none_counter = 0
        
        for i in xrange(len(dist)):
            search = None
            for id, cluster in dist.iteritems():
                for key, value in cluster.iteritems():
                    # Init Used Keys at first iteration
                    if (i == 0): used_keys[key] = False
                    if (not used_keys[key]) and (search == None or search[2] < value):
                        search = (id,key,value)
            
            if (search == None):
                # No Result. Use first unused key with first unused cluster
                for key, status in used_keys.iteritems():
                    if (status == False):
                        for id in dist.iterkeys():
                            search = (id,key,0)
                            break
                        break
                    
            if (search == None):
                for id in dist.iterkeys():
                    search = (id,'unknown_'+str(none_counter),0)
                    none_counter +=1
                    break
            
            named_cluster[search[1]] = search[0]
            used_keys[search[1]] = True
            
            #Update dist
            del(dist[search[0]])
            
        counter = 0.0 
        error_counter = 0.0
        
        for key, id in named_cluster.iteritems():
            for key2, num_of in orig_dist[id].iteritems():
                counter += num_of
                if (key != key2): error_counter += num_of
        
        return error_counter/counter
                      
    
    # \brief Returns an Information string about the clustering run with the given
    #        index
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def get_information_string(self, num_of_clustering_run):
        """ Returns an Information string about the clustering run with the given
        index """

        # Check existence of Clustering
        if (len(self.runs) < num_of_clustering_run):
            raise HcluException("There are no clustering run with given number!")
        
        clustering = self.runs[num_of_clustering_run]
        format = "%d.%m.%Y %H:%M:%S"
        
        s = "Run of: '"+clustering.strategy_description+ "' "
        s += "with '"+clustering.distance_function_description+"' as distance function "
        s += "over file '"+clustering.filename+"'. "
        s += "Init start at: "+clustering.init_start_time.strftime(format)+" "
        s += "Run start at: "+clustering.run_start_time.strftime(format)+" "
        s += "Ended at: "+clustering.end_time.strftime(format)+". " 
        s += "Complete Time needed "+str(clustering.seconds_needed.total_seconds())+\
            " seconds."
        
        return s
    
    # \brief Returns the run information of all clustering runs as an csv string
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def get_run_information_csv(self):
        """ Returns the information of all clustering runs as an csv string """
        
        timestamp_format = "%d.%m.%Y %H:%M:%S"
        
        s = ""
        
        for clustering in self.runs:
            s += clustering.filename
            s +=";"+clustering.strategy_description
            s +=";"+clustering.distance_function_description
            s +=";"+clustering.init_start_time.strftime(timestamp_format)
            s +=";"+clustering.run_start_time.strftime(timestamp_format)
            s +=";"+clustering.end_time.strftime(timestamp_format) 
            s +=";"+str(clustering.seconds_needed.total_seconds())
            s +="\n"
        
        return s
    
    # \brief Saves as csv File with the run Informations
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def save_run_information_csv(self, targetfile, append=True):
        '''Saves as csv File with the run Informations'''
        
        # Determine write modus
        if (append): modus='a'
        else: modus='w'
        
        # open targetfile
        file_handle = open(targetfile, modus)
        
        file_handle.write(self.get_run_information_csv())
    
    # \brief Returns the quality information of all clustering runs as an csv string
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def get_quality_information_csv(self, num_of_level, attribute):
        """ Returns the quality information of all clustering runs as an csv string """
        
        timestamp_format = "%d.%m.%Y %H:%M:%S"
        
        s = ""
        
        for i in xrange(len(self.runs)):
            s+=self.runs[i].strategy_description
            s+=";"+self.runs[i].distance_function_description
            s+=";"+self.runs[i].init_start_time.strftime(timestamp_format)
            s+=";"+str(self.determine_clustering_error(i, num_of_level, attribute))
            s+="\n" 
        
        return s    
    
    # \brief Saves as csv File with the quality Informations
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>        
    def save_quality_information_csv(self, 
        num_of_level, attribute, targetfile, append=True):

        '''Saves as csv File with the quality Informations'''
        
        # Determine write modus
        if (append): modus='a'
        else: modus='w'
        
        # open targetfile
        file_handle = open(targetfile, modus)

        file_handle.write(self.get_quality_information_csv(num_of_level, attribute))
