# -*- encoding: utf8 -*-
"""
    Source NAT module:  aXAPI source NAT configuration implementation.
        Support the object-oriented interface for the source NAT such as:
            NatPool: 
            NatPoolGroup:
            StaticNat
            NatRange
            AclBinding  
            NatInterface
            NatGlobalSetting         
    
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/08/2012
"""

import method_call
from  base import AxObject, AxAPIError