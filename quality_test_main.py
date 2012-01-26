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

import cProfile
from operator import mul
from hclu.hclu import Hclu
from hclu.single_linkage_nbm import SingleLinkageNbm
from hclu.euclidian_distance import EuclidianDistance
from hclu.quadratic_euclidean_distance import QuadraticEuclidianDistance
from hclu.manhatten_distance import ManhattenDistance
from hclu.maximum_distance import MaximumDistance
from hclu.single_linkage_optimized import SingleLinkageOptimized
from hclu.complete_linkage_optimized import CompleteLinkageOptimized
from hclu.group_average_linkage_optimized import GroupAverageLinkageOptimized
from hclu.single_linkage_ehac import SingleLinkageEfficientHAC
from hclu.group_average_linkage_ehac import GroupAverageLinkageEfficientHAC
from hclu.complete_linkage_ehac import CompleteLinkageEfficientHAC
from hclu.centroid_linkage_optimized import CentroidLinkageOptimized

h = Hclu()

h.load_data('../result_10000.csv')

d0 = EuclidianDistance()
d1 = QuadraticEuclidianDistance()
d2 = ManhattenDistance()
d3 = MaximumDistance()
s0 = GroupAverageLinkageEfficientHAC(d0)
s1 = GroupAverageLinkageEfficientHAC(d1)
s2 = GroupAverageLinkageEfficientHAC(d2)
s3 = GroupAverageLinkageEfficientHAC(d3)

print("Starting with s0")
h.quality_test_strategy(s0, 0, 500, 50)
print("Starting with s1")
h.quality_test_strategy(s1, 0, 500, 50)
print("Starting with s2")
h.quality_test_strategy(s2, 0, 500, 50)
print("Starting with s3")
h.quality_test_strategy(s3, 0, 500, 50)
print("Saving data now")
h.save_quality_information_csv(-3, 'class', '../quality_complete.csv', True)
print("Finished")
