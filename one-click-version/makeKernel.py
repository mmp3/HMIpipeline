#!/usr/bin/env python

# Author: Matthew Parks
# derived from tie `tiedie` executable.

from __future__ import print_function
from __future__ import division
import os, sys
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime

parser = OptionParser()
##
## required options
##
parser.add_option("-n","--network",dest="network",action="store",default=None,help="\
.sif network file for the curated pathway to search. <source>   <(-a>,-a|,-t>,-t|,-component>)> <target>")

parser.add_option("-o","--output_folder",dest="output_folder",action="store",default='TieDIE')
(opts, args) = parser.parse_args()

# local imports assume the directory structure from github .
script_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_directory.replace("bin","lib"))

from kernel import Kernel
from ppr import PPrDiffuser
from permute import NetBalancedPermuter
from tiedie_util import *
from master_reg import *
from os import path
import pickle
from kernel_scipy import SciPYKernel

## Basic input validation
if opts.network is None:
	sys.stderr.write("Warning: Must supply an input network")
	sys.exit(1)

# set the output folder
output_folder = opts.output_folder
if not os.path.exists(output_folder):
	os.mkdir(output_folder)


# parse network file: use for input validation if heat nodes are not in network
sys.stderr.write("Parsing Network File..\n")
network = parseNet(opts.network)

sys.stderr.write("Using SCIPY to compute the matrix exponential, t=0.1... [%s]\n" % str(datetime.now()) )

out_file = output_folder+"/tiedie_kernel.pkl"

diffuser = SciPYKernel(opts.network)
pk_file = open(out_file, 'wb')
pickle.dump(diffuser, pk_file)
pk_file.close()

sys.stderr.write("DONE!\n")
sys.stderr.write("%s\n" % str(datetime.now()) )
