"""
/***************************************************************************
Name		     : pgAccessTool
Description          : Database query tool set
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
    return "pgAccessTool" 
def description():
    return "Database query tool set"
def version(): 
    return "Version 0.1" 
def qgisMinimumVersion():
    return "2.2.0"
from pgAccessTool import DB_Processor
