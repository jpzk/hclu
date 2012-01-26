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

import numpy as np

# \file data_element.py
# \brief Representing one Element (or one line) of the input data
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
class DataElement(object):

    def __init__(self, data, attributes=None, attributes_name=None):
        if (not isinstance(data, np.ndarray)):
            raise TypeError("data is not a numpy array")
        
        self.data = data
        self.attributes={}
        
        for i in xrange(len(attributes)):
            self.attributes[attributes_name[i]] = attributes[i]
