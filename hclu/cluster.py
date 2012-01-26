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

"""This module contains the cluster class"""

from data_element import DataElement

# \file cluster.py
# \brief This is a cluster element
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
# \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> 
class Cluster(object):

    # \brief Initialize cluster with optionally children and simialarity.
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    def __init__(self, c1, c2 = None, sim = None):
        """This is the main module containing the cluster object"""
        
        # Init Object Variables
        # children of cluster.
        self.c1 = None
        self.c2 = None
        
        # All data elements in the cluster.
        self.elements = []

        # Determine if cluster of clusters or leaf cluster with one DataElement
        if (isinstance(c1, DataElement) and c2 == None and sim == None):
            # Initialize with Data Element
            self.elements.append(c1)
        elif (isinstance(c1, Cluster) and isinstance(c2, Cluster)):
            self.c1 = c1
            self.c2 = c2
            
            self.elements = c1.elements + c2.elements
            
            # Check if sim is available.
            if (sim != None):
                if (not isinstance(sim, float)): 
                    raise TypeError("sim is not a float value")
                else: self.sim = sim
        else:
            raise TypeError(
                "Constructor of Cluster need one DataElement Objects and " + 
                "nothing or two Cluster Objects and a float sim " + 
                "value if avaible")
