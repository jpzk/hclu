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

from c_record import CRecord
from strategy import Strategy
from operator import mul
import copy

# \file single_linkage_naive.py
# \brief Optimized naive Centroid-Linkage Implementation.
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
class CentroidLinkageOptimized(Strategy):
    '''
    Optimized naive Centroid-Linkage Implementation
    '''
    
    #Strategy Description
    description = "Optimized naive Centroid-Linkage Implementation"

    # \brief Initialize the Alogrithm
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def initialize(self, data):
        '''
        Initialize the Alogrithm
        '''
        
        # Calling super Constructor
        super(CentroidLinkageOptimized, self).initialize(data)
        
        # Counting Elements. Building c_matrix and complete c_matrix
        self.num_of_rec = len(data)
        self.c_matrix = {}
        self.complete_c_matrix = {}
        
        for i in xrange(self.num_of_rec):
            self.c_matrix[i] = {}
            self.complete_c_matrix[i] = {}
        
        for n in xrange(self.num_of_rec):
            for i in xrange(n+1):
                sim = self.distance_function.distance(data[n].data, data[i].data)
                
                tmp_record = CRecord(i,sim)
                tmp_record2 = CRecord(i,sim)
                self.c_matrix[n][i] = tmp_record
                self.complete_c_matrix[n][i] = tmp_record2

                tmp_record = CRecord(n,sim)
                tmp_record2 = CRecord(i,sim)
                self.c_matrix[i][n] = tmp_record
                self.complete_c_matrix[i][n] = tmp_record2    
                            
        self.cluster_index_lists = {}
        for i in xrange(self.num_of_rec):
            self.cluster_index_lists[i]=[i]
                
    def run(self):
        '''
        Run the Algorithm
        '''
        
        for n in xrange(self.num_of_rec-1):
            # Searching next best
            best = None
            i1 = None
            for i, sub_matrix in self.c_matrix.iteritems():
                for c_record in sub_matrix.itervalues():
                    if (c_record.index != i and \
                        (best == None or best.sim > c_record.sim)):
                            best = c_record
                            i1 = i
                    
            # Merge
            self.new_level(i1, best.index, best.sim)

            for i in self.c_matrix[i1].iterkeys():
                # No Sim for new cluster with his self
                if i != i1 and i != best.index:
                    # Calculate the number of the sims between both cluster before
                    # the new Merge. (Fakultaet fuer anzahl elemente minus 1)
                    #num_of_sims = \
                    #    reduce(mul, xrange(2, len(self.cluster_index_lists[i1])+len(self.cluster_index_lists[i])), 1)
                    num_of_sims = 0
                    
                    # Init current value
                    #curr_value = self.c_matrix[i1][i]*num_of_sims
                    curr_value = 0
                    
                    for ind1 in self.cluster_index_lists[i1]:
                        for ind2 in self.cluster_index_lists[i]:
                            curr_value+=\
                                self.complete_c_matrix[ind1][ind2].sim
                            num_of_sims += 1
                    
                    # New Sim
                    new_sim = curr_value / num_of_sims
                    
                    self.c_matrix[i1][i].sim = new_sim
                    self.c_matrix[i][i1].sim = new_sim
                    
            # Update Cluster Index List
            self.cluster_index_lists[i1].append(best.index)
            #del(self.cluster_index_lists[best.index])
            
            # Delete merged Cluster
            del(self.c_matrix[best.index])
            for sub_matrix in self.c_matrix.itervalues():
                del(sub_matrix[best.index])
