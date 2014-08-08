"""
/***************************************************************************
Name			 	 : COGCC_DL
Description          : Download well data from the COGCC website
Date                 : 30/Apr/14 
copyright            : (C) 2014 by Julian Abbott-Whitley - PhD WFS
email                : jwhitley@phdwellfile.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "COGCC_DL" 
def description():
  return "Download well data from the COGCC website"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "2.2.0"
def classFactory(iface): 
  # load COGCC_Download class from file COGCC_Download
  from COGCC_Download import COGCC_Download 
  return COGCC_Download(iface)
