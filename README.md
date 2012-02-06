# hclu 

Hierarchical clustering for Python 2.7. It's not yet ready for use, but you'll be able to cluster data sets via command-line.

<pre>
usage: hclu [-h] -i I 
  -m {single-linkage,complete-linkage,group-average,centroid} 
  -d {euclidean,quadratic-euclidean,manhatten,maximum}

hierachical clustering

optional arguments:
  -h, --help            show this help message and exit
  -i I                  CSV file with data set to cluster
  -m {single-linkage,complete-linkage,group-average,centroid}
  -d {euclidean,quadratic-euclidean,manhatten,maximum}
</pre>

## Next-Best-Merge Array O(n^2) and Efficient HAC Algorithm O(n^2*log(n))

implements NBM algorithm for Single-Linkage and HAC, GAAC algorithm described in http://nlp.stanford.edu/IR-book/html/htmledition/time-complexity-of-hac-1.html

## License 

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

