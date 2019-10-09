# -*- encoding: utf8 -*-
"""
    SSL management module:  aXAPI SSL certificate/key management implementation.
        Support the object-oriented interface for the SSL management such as:
            SslCertKeyMgmt:           
            TemplateClientSsl
            TemplateServerSsl
    
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/08/2012
"""

import method_call
from  base import AxObject, AxAPIError