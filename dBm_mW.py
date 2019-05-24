#!/usr/bin/python
# -*- coding: utf-8 -*-​
import sys
from math import log10

# Function to extract numbers from string
def getdigits(ch):
                    if "," in ch:
                        ch = ch.replace(',','.')
                    if '.' in ch:
                        return float(''.join(ele for ele in ch if ele.isdigit() or ele == '.'))
                    else:
                        return int(''.join(ele for ele in ch if ele.isdigit()))
# Function to convert from dBm to mW
def dBm2mW(dBm):
    return 10**((dBm)/10.)


# varsinainen funktio
def dBm_to_mW(arvo):
                    #dBm = getdigits(arvo)
                    dBm = arvo
                    if "-" in arvo:
                            dBm = -dBm
                            mW = dBm2mW(dBm)
                            return(mW)
                    else:
                            mW = dBm2mW(dBm)
                            return(mW)

