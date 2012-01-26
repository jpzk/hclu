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

'''
Created on Jan 18, 2012

@author: bjoern.borgmann <bjoern.borgmann@uni-oldenburg.de>
'''

# \file single_linkage_naive.py
# \brief Optimized naive Complete Linkage Implementation.
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
class CompleteLinkageOptimized(Strategy):
    '''
    Optimized naive Complete Linkage Implementation
    '''
    
    #Strategy Description
    description = "Optimized naive Complete Linkage Implementation"

    # \brief Initialize the Alogrithm
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def initialize(self, data):
        '''
        Initialize the Alogrithm
        '''
        
        # Calling super Constructor
        super(CompleteLinkageOptimized, self).initialize(data)
        
        # Counting Elements. Building c_matrix
        self.num_of_rec = len(data)
        self.c_matrix = {}
        for i in xrange(self.num_of_rec):
            self.c_matrix[i] = {}
        
        for n in xrange(self.num_of_rec):
            for i in xrange(n+1):
                sim = self.distance_function.distance(data[n].data, data[i].data)
                
                tmp_record = CRecord(i,sim)
                self.c_matrix[n][i] = tmp_record
                
                tmp_record = CRecord(n,sim)
                self.c_matrix[i][n] = tmp_record
         
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
            
            # Determine new Sim
            for i in self.c_matrix[i1].iterkeys():
                if i != i1 and i != best.index:
                    if (self.c_matrix[best.index][i].sim>self.c_matrix[i1][i].sim):
                        self.c_matrix[i1][i].sim = self.c_matrix[best.index][i].sim
                        self.c_matrix[i][i1].sim = self.c_matrix[best.index][i].sim
            
            # Delete merged Cluster
            del(self.c_matrix[best.index])
            for sub_matrix in self.c_matrix.itervalues():
                del(sub_matrix[best.index])
