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

"""This module contains single linkage with efficient HAC algorithm"""

import numpy

from strategy import Strategy
from priority_dict import PriorityDict

# \file group_average_linkage_ehac.py
# \brief Average Linkage with EfficentHAC algorithm, 
#        time complexity O(N^2 * log N), space complexity O(N^2)
#        based on http://nlp.stanford.edu/IR-book/html/htmledition/
#        time-complexity-of-hac-1.html#
#
# \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
#
class GroupAverageLinkageEfficientHAC(Strategy):
    """Group-Average Linkage with EfficientHAC algorithm"""

    description = "Group-Average Linkage with Efficient HAC algorithm"

    # \brief initializes the algorithm by initializing 
    #        data and datastructures.
    #
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    # \see Strategy#initialize
    #
    def initialize(self, data):
        """Initializes the algorithm by initializing data"""

        super(GroupAverageLinkageEfficientHAC, self).initialize(data)

        normalize = lambda x : x/(numpy.sqrt(numpy.dot(x, x.conj())))

        # normalize data to normalized vectors        
        self.data = [normalize(data.data) for data in data]
        self.data_length = len(self.data)

        # array for counting merged data elements.
        self.amount_in_cluster = [1.0 for cluster in range(0, self.data_length)]

        # storing the vector sums, initial sum is data of data element.
        self.vectorsum = [data for data in self.data]

        # initialize not_merged array (titled 'I' in pseudocode) with 0.
        self.not_merged = [0] * self.data_length
        
        # initialize priority queues array for each initial cluster.
        # titled 'P' in pseudo code
        self.priority_queues = []

        # simialarity matrix (titled 'C' in pseudo code)
        self.simialarities = [[CRecord() for j in range(0, self.data_length)]
            for k in range(0, self.data_length)]

        # time complexity O(N^2) because N^2 + O(N * log N) where N = len(data)
        # space complexity self.simialarities N^2 and self.priority_queues N^2
        for n in range(0, self.data_length):
            for i in range(0, self.data_length):

                self.simialarities[n][i].sim = \
                    numpy.dot(self.data[n], self.data[i])

                self.simialarities[n][i].index = i
                self.not_merged[n] = 1
        
            self.priority_queues.append(PriorityDict())

            for i in range(0, self.data_length):
                if(i != n):
                    self.priority_queues[n][i] = self.simialarities[n][i]
        
    # \brief Implementation of abstract run method, time complexity
    #        O(N^2 * log N), space complexity 0.
    #
    # \see Strategy#run
    # \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
    # 
    def run(self):
        """Implementation of abstract run method"""

        # time complexity O(N^2 * log N), because O(N * (N * log N)) 
        # space complexity 0
        for k in range(0, self.data_length - 1):
            
            # arg max (k: I[k]=1)
            firstRun = True

            # time complexity O(N) where N is amount of clusters
            # space complexity 0
            for z in range(0, self.data_length):
                if self.not_merged[z] != 1: 
                    continue
    
                smallest = self.priority_queues[z].smallest()
                simularity = smallest.sim
                index = smallest.index

                if firstRun: 
                    k1 = z
                    maximum = simularity 
                    maximum_index = index
                    firstRun = False
                if maximum < simularity:
                    k1 = z
                    maximum = simularity
                    maximum_index = index

            k2 = maximum_index
 
            # merge k1 with k2
            self.new_level(k1, k2, maximum)
            self.amount_in_cluster[k1] += self.amount_in_cluster[k2] 
            self.vectorsum[k1] += self.vectorsum[k2]

            self.not_merged[k2] = 0
            self.priority_queues[k1] = PriorityDict() 

            # time complexity O(N * log N) where N is amount of clusters
            # space complexity 0
            for i in range(0, self.data_length):

                if self.not_merged[i] == 1 and i != k1:

                    del self.priority_queues[i][k2]

                    # i to k1
                    amountsum = self.amount_in_cluster[i] + \
                        self.amount_in_cluster[k1]
                    
                    vectorsum = self.vectorsum[i] + self.vectorsum[k1]
                    normalizingfactor = 1.0/((amountsum) * (amountsum - 1))
                    dotp = numpy.dot(vectorsum, vectorsum.conj()) 
                   
                    self.simialarities[i][k1].sim = \
                        normalizingfactor * \
                        (dotp - amountsum)
                          
                    self.priority_queues[i][k1] = self.simialarities[i][k1]

                    # k1 to i

                    self.simialarities[k1][i].sim = self.simialarities[i][k1].sim
                    self.priority_queues[k1][i] = self.simialarities[k1][i]

class CRecord:
    
    def __init__(self):
        self.sim = None
        self.index = None

    def __lt__(self, other):
        if(not isinstance(other, CRecord)):
            raise TypeError("not a CRecord")            
        return self.sim > other.sim

    def __repr__(self):
        return str(self.sim) + " " + str(self.index)
