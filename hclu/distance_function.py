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

"""This module contains the abstract class for distance functions."""

# \brief This class is a distance function strategy base class.
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
# \author Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
class DistanceFunction(object):
    """This class is a distance function strategy base class."""

    def distance(self, data1, data2):
        pass

