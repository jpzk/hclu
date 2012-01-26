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

from numpy import linalg 
from distance_function import DistanceFunction
import math

# \file manhatten_distance.py
# \brief This is the manhatten distance function between two vectors
# \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de> 
class ManhattenDistance(DistanceFunction):
    
    description = "Manhatten Distance"
    
    def distance(self, data1, data2):
        distance = 0
        for i in range(0, len(data1)):
            distance += abs(data1[i] - data2[i])

        return distance
