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
# \brief Class for representing one data file which was been loaded
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>   
class DataFile(object):
    '''Class for representing one data file which was been loaded'''
    
    # \brief Constructor
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>       
    def __init__(self):
        ''' Constructor'''
        self.elements = []
        self.filename = None
        self.attributes = None
        self.numOfElements = None
