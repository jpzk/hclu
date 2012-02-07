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

"""This module contains the abstract clustering strategy class."""

import datetime

from distance_function import DistanceFunction
from hclu_exception import HcluException
from cluster import Cluster

# \file strategy.py
# \brief This class is a strategy base class for clustering methods.
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
# \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> 
class Strategy(object):
    """This class is a strategy base class for clustering methods."""        

    print_mod = 1

    def __init__(self, distance_function):
        if (not isinstance(distance_function, DistanceFunction)):
            raise TypeError(\
            "distance_function is not a DistanceFunction Object")
        
        # Distance Function
        self.distance_function = distance_function
        
        # List for Cluster History
        self.clustering = []
        
        # Level Counter
        self.level_counter = 0
    
    # \brief Implementation of base functions for init algorithm. 
    #        Generating the Cluster Objects
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    def initialize(self, data):
        """Implementation of base functions for init algorithm.
        E.g. generating initial cluster objects."""

        self.print_message("Initializing "+self.description)
        
        # Reset List for Cluster History
        self.clustering = []
        
        # Reset Level Counter
        self.level_counter = 0
        
        # Level 0 cluster list
        level_0 = {}
        
        # Generating Cluster Objects
        for i in xrange(len(data)):
            level_0[i] = Cluster(data[i])
        
        # Save level 0
        self.clustering.append(level_0)
    
    # \brief Generate new clustering level by merging given indices
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    def new_level(self, index1, index2, sim=None):
        """Generate new clustering level by merging given indices"""
        #print (index1,index2,sim)
        
        # Status Message and counter
        if (self.level_counter == 0):
            self.print_message("First Merge")
            
        self.level_counter += 1
        
        if (self.level_counter % self.print_mod == 0):
            self.print_message("Level " +\
                str(self.level_counter) +\
                ": Merging "+str(index1)+\
                " with " + str(index2) +\
                " Sim is "+str(sim))
        
        # Copy latest level
        level = self.clustering[len(self.clustering) - 1].copy()
        
        # Generating and storing new cluster object. Delete old Object        
        level[index1] = Cluster(level[index1], level[index2], sim)
        del level[index2]
        
        # Save new level
        self.clustering.append(level)
        
    # \brief Prints given message with timestamp
    # \autohr Bjoern Borgmann <bjoern.borgmann@gmx.de>
    def print_message(self, msg):
        """Prints given message with timestamp"""
        d = datetime.datetime.now()
        
        timestring = d.strftime("%d.%m.%Y %H:%M:%S")
        
        print (timestring+" || "+msg)
        
    # \brief Abstract method, for running the clustering strategy.
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    def run(self):
        """Abstract method, the implementation runs the clustering 
        algorithm."""

        raise HcluException("Method run is abstract")
