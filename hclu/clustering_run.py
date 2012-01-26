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
       
# \file hclu.py
# \brief Class representing one clustering run
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>           
class ClusteringRun(object):
    '''Class representing one clustering run'''

    # \brief Constructor
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>     
    def __init__(
                 self, 
                 filename,
                 strategy_description,
                 distance_function_description,
                 init_start_time,
                 run_start_time,
                 end_time,
                 seconds_needed,
                 clustering
                 ):
        '''Constructor'''
        self.filename = filename
        self.strategy_description = strategy_description
        self.distance_function_description = distance_function_description
        self.init_start_time = init_start_time
        self.run_start_time = run_start_time
        self.end_time = end_time
        self.seconds_needed = seconds_needed
        self.clustering = clustering
