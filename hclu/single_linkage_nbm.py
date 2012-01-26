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

# \file single_linkage_nbm.py
# \brief This is the single linkage strategy for clustering using an NBM Array
# \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
class SingleLinkageNbm(Strategy):

    #Strategy Description
    description = "Single Linkage with Using of an Next Best Match (NBM) Array"

    #nOfRec = 0
    #cArray = []
    #iArray = []
    #nbmArray = []
    #aArray = []
    
    # Debug Switch
    debug = False
    
    # Message switch
    message = False
    
    # Level Printing
    printLevel=10

    # \brief Initialize the Alogrithm
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def initialize(self, data):
        '''
        Initialize the Alogrithm
        '''
        if (self.message):
            print "Init Single Linkage NBM:"
            print "    - Calling Parent Method"
        
        super(SingleLinkageNbm, self).initialize(data)
        
        if (self.message):
            print "    - Creating Datastructures. Counting Data Elements"
        
        self.nOfRec = len(data)
        self.cArray = [[CRecord() for j in xrange(self.nOfRec)]for k in xrange(self.nOfRec)]
        
        # Calculating cArray the optimized Way
        if (self.message):
            print "    - Calculating cArray"
        
        for n in xrange(self.nOfRec):
            for i in xrange(n+1):
                sim = self.distance_function.distance(data[n].data, data[i].data)
                self.cArray[n][i].sim = sim
                self.cArray[n][i].index = i
                
                self.cArray[i][n].sim = sim
                self.cArray[i][n].index = n
        
        #print self.cArray
            
        # Filling the ohter Arrays
        if (self.message):
            print "    - Filling iArray and nbmArray"
        
        self.iArray =  []
        self.nbmArray = []
        for n in xrange(self.nOfRec):
            self.iArray.append(n)
            self.nbmArray.append(self._get_Best_Match(n, False))
        
        if (self.debug):
            for i in xrange(self.nOfRec):
                for j in xrange(self.nOfRec):
                    print (i,j,self.cArray[i][j].sim)
            
            for i in xrange(self.nOfRec):
                print(i, self.nbmArray[i].index, self.nbmArray[i].sim)
        
        
    # \brief Run the Alogrithm
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def run(self):
        if (self.message):
            print "Run Single Linkage NBM:"
        
        for n in xrange(self.nOfRec-1):
            if self.debug:
                print ("    - Level "+str(n))
                print self.iArray
            elif (self.message and self.printLevel != None and n%self.printLevel==0):
                print ("    - Level "+str(n))
            
            # Search for next Element pair
            bestRec = None
            best = None
            for i in xrange(len(self.nbmArray)):
                if self.iArray[i]==i and (
                    bestRec == None or bestRec.sim > self.nbmArray[i].sim
                ): 
                    if (self.debug):
                        if (bestRec != None): 
                            print (i, bestRec.sim, self.nbmArray[i].sim)
                        else: 
                            print (i, None, self.nbmArray[i].sim)
                        
                    best = i
                    bestRec = self.nbmArray[i]
                
            i1 = best
            i2 = self.iArray[bestRec.index]
            
            # Append new Clustering level
            self.new_level(i1, i2, bestRec.sim)
            #self.aArray.append((i1,i2))
            
            # Update Arrays
            for i in xrange(self.nOfRec):
                if self.iArray[i] == i and i != i1 and i != i2:
                    if (self.cArray[i1][i].sim <= self.cArray[i2][i].sim): 
                        newSim = self.cArray[i1][i].sim
                    else: newSim = self.cArray[i2][i].sim
                    self.cArray[i1][i].sim = newSim
                    self.cArray[i][i1].sim = newSim
                if self.iArray[i] == i2: self.iArray[i] = i1
            
            self.nbmArray[i1] = self._get_Best_Match(i1, True)
             
            
    # \brief Get Best Match Record for the Record with given index
    # \author Bjoern Borgmann <bjoern.borgmann@uni-oldenburg.de>
    def _get_Best_Match(self, index, checkIArray):
        bestRec = None
        for i in xrange(len(self.cArray[index])):
            # Not the Same Element
            if (i != index):
                if (bestRec == None or bestRec.sim > self.cArray[index][i].sim):
                    if (checkIArray == False or self.iArray[i]==i): 
                        bestRec = self.cArray[index][i]
        return bestRec
