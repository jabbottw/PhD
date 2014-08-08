"""
/***************************************************************************
Name                 : pyIBrowser1
Description          : Tool set designed to download data over the internet
Date                 : 5/9/2014
copyright            : (C) 2014 by Julian Abbott-Whitley - PhD WFS
email                : jwhitley@phdwellfile.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program has been developed for use by PhD well file services.     *
 *                                                                         *
 ***************************************************************************/
 This script initializes the module.
"""
def name(): 
    return "pyIBrowser2" 
def description():
    return "Internet download tool set"
def version(): 
    return "Version 0.1" 
def qgisMinimumVersion():
    return "2.2.0"
from pyIBrowser2 import WellDataCollector