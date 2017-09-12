#!/usr/bin/env python
"""
Author: Arpan Rau
Install packages for dynamics class using conda
"""
import subprocess

packages = """\
numpy
scipy 
matplotlib 
jupyter 
-c https://conda.anaconda.org/kne pybox2d
-c tlatorre pygame
"""

pkgs = packages.strip().split("\n")

Failed = False #keep track if we've failed

for pkg in pkgs:

    try:
        cmd = "conda install -y "+pkg
        
        print "attempting to install %s " % pkg
        retcode = subprocess.call(cmd,shell = True)

        if retcode == 1:
        	Failed = True
        	print "Warning could not install %s " % pkg

    except OSError:
        print "Warning could not install %s " % pkg
        Failed = True
    

if Failed ==True:
	print "Could not install all packages! Go back and manually install failed packages."
	print "YOUR ENVIORNMENT IS NOT SET UP. DO NOT PROCEED."
else:
	print "All packages installed!"

