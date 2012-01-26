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

#h.load_data('../result_10.csv')
#h.load_data('../result_100.csv')
#h.load_data('../result_1000.csv')
h.load_data('../result_10000.csv')

d = EuclidianDistance()
s0 = SingleLinkageNbm(d)
d = QuadraticEuclidianDistance()
s1 = SingleLinkageNbm(d)

#s0 = SingleLinkageNbm(d)
#s1 = SingleLinkageEfficientHAC(d)
#s2 = SingleLinkageOptimized(d)
#s3 = CompleteLinkageEfficientHAC(d)
#s4 = CompleteLinkageOptimized(d)
#s5 = GroupAverageLinkageEfficientHAC(d)
#s6 = GroupAverageLinkageOptimized(d)
#s7 = CentroidLinkageOptimized(d)

#h.cluster(s0)
#h.cluster(s1)
#h.cluster(s2)
#h.cluster(s3)
#h.cluster(s4)
#h.cluster(s5)
#h.cluster(s6)
#h.cluster(s5)
#h.cluster(s6)
#h.cluster(s7)
#h.speed_test_strategy(s1, 2, 10)
#h.speed_test_strategy(s3, 2, 10)
#h.speed_test_strategy(s5, 2, 10)
h.quality_test_strategy(s0, 0, 300, 50)
h.save_quality_information_csv(-3, 'class', '../quality_nbm.csv', True)


#print " "
#h.save_run_information_csv('../run_informations.csv', True)

#print(h.get_information_string(0))
#print(h.get_distribution_of_clustering(0, -3, 'class'))
#print(h.determine_clustering_error(0, -3, 'class'))

#print(h.get_information_string(1))
#print(h.get_distribution_of_clustering(1, -3, 'class'))

#print(h.get_information_string(2))
#print(h.get_distribution_of_clustering(2, -3, 'class'))

#print(h.get_information_string(3))
#print(h.get_distribution_of_clustering(3, -3, 'class'))

#print(h.get_information_string(4))
#print(h.get_distribution_of_clustering(4, -3, 'class'))

#print(h.get_information_string(5))
#print(h.get_distribution_of_clustering(5, -3, 'class'))


#cProfile.run('h.cluster(s1)')
