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

# \file single_linkage_nbm.py
# \brief This is the single linkage strategy for clustering using an NBM Array
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
class CRecord(object):
    '''
    Class representing an CRecord
    '''
    
    def __init__(self, index = None, sim = None):
        self.sim = sim
        self.index = index
        
    def __repr__(self):
        return str(self.sim) + " " + str(self.index)
