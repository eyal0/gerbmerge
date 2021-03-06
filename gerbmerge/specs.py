#!/usr/bin/env python2
"""
Regular expression, SimpleParse, ane message constants.

Requires:
  
  - SimpleParse 2.1 or higher
              http://simpleparse.sourceforge.net
              

--------------------------------------------------------------------

This program is licensed under the GNU General Public License (GPL)
Version 3.  See http://www.fsf.org for details of the license.

Rugged Circuits LLC
http://ruggedcircuits.com/gerbmerge
"""

import re

from simpleparse.parser import Parser

DISCLAIMER = """
****************************************************
*           R E A D    C A R E F U L L Y           *
*                                                  *
* This program comes with no warranty. You use     *
* this program at your own risk. Do not submit     *
* board files for manufacture until you have       *
* thoroughly inspected the output of this program  *
* using a previewing program such as:              *
*                                                  *
* Windows:                                         *
*          - GC-Prevue <http://www.graphicode.com> *
*          - ViewMate  <http://www.pentalogix.com> *
*                                                  *
* Linux:                                           *
*          - gerbv <http://gerbv.sourceforge.net>  *
*                                                  *
* By using this program you agree to take full     *
* responsibility for the correctness of the data   *
* that is generated by this program.               *
****************************************************
"""[1:-1]

# [Options] section defaults        Data types: "L" = layers (will show layer selection)
#                                               "D" = decimal
#                                               "DP" = possitive decimal
#                                               "I" = integer
#                                               "IP" = integer positive
#                                               "PI" = path input (will show open dialog)
#                                               "PO" = path output (will show save dialog)
#                                               "S" = string
#                                               "B" = boolean
#                                               "BI" = boolean as integer
#
#                                               THESE DATA TYPES ARE FIXED - CODE MUST CHANGE IF TYPES ARE ADDED/MODIFIED
DEFAULT_OPTIONS = { 
    # Spacing in horizontal direction
    'xspacing':                  ('0.125',   "DP",   "XSpacing",                "1 XSPACING_HELP"), 
    # Spacing in vertical direction
    'yspacing':                  ('0.125',   "DP",   "YSpacing",                "2 YSPACING_HELP"), 
    # X-Dimension maximum panel size (Olimex)
    'panelwidth':                ('12.6',    "DP",   "PanelWidth",              "3 PANEL_WIDTH"),  
    # Y-Dimension maximum panel size (Olimex) 
    'panelheight':               ('7.8',     "DP",   "PanelHeight",             "4 PanelHeight"), 
    # e.g., *toplayer,*bottomlayer  
    'cropmarklayers':            (None,      "L",    "CropMarkLayers",          "5 CropMarkLayers"),
    # Width (inches) of crop lines   
    'cropmarkwidth':             ('0.01',    "DP",   "CropMarkWidth",           "6 CropMarkWidth"),
    # as for cropmarklayers   
    'cutlinelayers':             (None,      "L",    "CutLineLayers",           "7 CutLineLayers"),
    # Width (inches) of cut lines   
    'cutlinewidth':              ('0.01',    "DP",   "CutLineWidth",            "8 CutLineWidth"),
    # Minimum dimension for selected layers   
    'minimumfeaturesize':        (None,      "S",    "MinimumFeatureSize",      "Use this option to automatically thicken features on particular layers.\nThis is intended for thickening silkscreen to some minimum width.\nThe value of this option must be a comma-separated list\nof layer names followed by minimum feature sizes (in inches) for that layer.\nComment this out to disable thickening. Example usage is:\n\nMinimumFeatureSize = *topsilkscreen,0.008,*bottomsilkscreen,0.008"),
    # Name of file containing default tool list     
    'toollist':                  (None,      "PI",   "ToolList",                "10 ToolList"),
    # Tolerance for clustering drill sizes
    'drillclustertolerance':     ('.002',    "DP",    "DrillClusterTolerance",  "11 DrillClusterTolerance"),
    # Set to 1 to allow multiple jobs to have non-matching layers   
    'allowmissinglayers':        (0,         "BI",   "AllowMissingLayers",      "12 AllowMissingLayers"),
    # Name of file to which to write fabrication drawing, or None  
    'fabricationdrawingfile':    (None,      "PO",   "FabricationDrawingFile",  "13 FabricationDrawingFile"),  
    # Name of file containing text to write to fab drawing
    'fabricationdrawingtext':    (None,      "PI",   "FabricationDrawingText",  "14 FabricationDrawingText"), 
    # Number of digits after the decimal point in input Excellon files 
    'excellondecimals':          (4,         "IP",   "ExcellonDecimals",        "15 ExcellonDecimals"),
    # Generate leading zeros in merged Excellon output file   
    'excellonleadingzeros':      (0,         "IP",   "ExcellonLeadingZeros",    "16 ExcellonLeadingZeros"),
    # Name of file to which to write simple box outline, or None   
    'outlinelayerfile':          (None,      "PO",   "OutlineLayerFile",        "17 OutlineLayerFile"), 
    # Name of file to which to write scoring data, or None 
    'scoringfile':               (None,      "PO",   "ScoringFile",             "18 ScoringFile"),
    # Inches of extra room to leave on left side of panel for tooling  
    'leftmargin':                (0.0,       "DP",   "LeftMargin",              "19 LeftMargin"), 
    # Inches of extra room to leave on top side of panel for tooling  
    'topmargin':                 (0.0,       "DP",   "TopMargin",               "20 TopMargin"),   
    # Inches of extra room to leave on right side of panel for tooling
    'rightmargin':               (0.0,       "DP",   "RightMargin",             "21 RightMargin"),   
    # Inches of extra room to leave on bottom side of panel for tooling
    'bottommargin':              (0.0,       "DP",   "BottomMargin",            "22 BottomMargin"),  
    # List of X,Y points at which to draw fiducials
    'fiducialpoints':            (None,      "S",    "FiducialPoints",          "23 FiducialPoints"),
}
DEFAULT_OPTIONS_TYPES = ["IP", "I", "DP", "D", "B", "BI", "S", "PI", "PO", "L"] # List of option types in display order

# [GerbMergeGUI] section defaults
DEFAULT_GERBMERGEGUI = {
    'unit':                     "IN",           # Unit inidicator: IN, MIL, MM
    'layout':                   "AUTOMATIC",    # Indicates layout: GRID, AUTOMATIC, MANUAL, GRID_FILE, MANUAL_FILE
    'runtime':                  10,             # Seconds to run automatic placement
    'rows':                     1,              # Number of rows in grid layout
    'columns':                  1,              # Number of columns in grid layout
    'mergedoutput':             False,          # Path of output directory
    'mergedname':               False,          # Prefix of merged output files
    'layoutfilepath':           "",             # Path of layout file
    'placementfilepath':        "",             # Path of placement file
    'configurationfilepath':    "",             # Path of configuration file
    'configurationcomplete':    False,          # Indicates that run dialog may be skipped to upon load
}

# Job names
RE_VALID_JOB = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$')
RE_VALID_JOB_MESSAGE  = "Vaild Characters: a-z, A-Z, 0-9, underscores, hyphens\nFirst Character must be: a-z, A-Z, 0-9"
RESERVED_JOB_NAMES = ("Options", "MergeOutputFiles", "GerbMergeGUI") ##not implemented yet

# Layer names
RE_VALID_LAYER = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$')
RE_VALID_LAYER_MESSAGE = "Vaild Characters: a-z, A-Z, 0-9, underscores, hyphens\nFirst Character must be: a-z, A-Z, 0-9"
DEFAULT_LAYERS = [  "BoardOutline",
                    "TopCopper",
                    "BottomCopper",
                    "InnerLayer2",
                    "InnerLayer3",
                    "TopSilkscreen",
                    "BottomSilkscreen",
                    "TopSoldermask",
                    "BottomSoldermask",
                    "TopSolderPasteMask",
                    "BottomSolderPasteMask",
                    "Drills"                    ]  
REQUIRED_LAYERS = ["BoardOutline", "Drills"]
RESERVED_LAYER_NAMES = () ##add "mergeout", not implemented yet

#Output names
RE_VALID_OUTPUT_NAME = re.compile(r'^[a-zA-Z0-9_-]+$')
RE_VALID_OUTPUT_NAME_MESSAGE = "Vaild Characters: a-z, A-Z, 0-9, underscores, hyphens"
REQUIRED_LAYERS_OUTPUT = ["BoardOutline", "ToolList", "Placement", "Drills"]

# Default dictionary of layer names to file extensions
FILE_EXTENSIONS = { "boardoutline":             "GBO",     
                    "topcopper":                "GTL",
                    "bottomcopper":             "GBL",
                    "innerlayer2":              "G2",
                    "innerlayer3":              "G3",
                    "topsilkscreen":            "GTO",
                    "bottomsilkscreen":         "GBO",
                    "topsoldermask":            "GTS",
                    "bottomsoldermask":         "GBS",
                    "topsolderpastemask":       "GTP",
                    "bottomsolderpastemask":    "GBP",
                    "drills":                   "GDD",
                    "placement":                "TXT",
                    "toollist":                 "DRL",
                  }
DEFAULT_EXTENSION = "GER"

#Gerbmerge options
PLACE_FILE          = "--place-file="
NO_TRIM_GERBER      = "--no-trim-gerber"
NO_TRIM_EXCELLON    = "--no-trim-excellon"
ROTATED_OCTAGONS    = "--octagons=rotate"
SEARCH_TIMEOUT      = "--search-timeout="
                  

