# -*- encoding: utf8 -*-
"""
    System module:  aXAPI system management implementation.
    
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/07/2012
"""

import method_call
from  base import AxObject, AxAPIError

class SystemNtp(AxObject):
    """
        Implementation of the aXAPI system.ntp.* method to 
        set up the NTP 
        
        Usage:
            # create the NTP server at 2.2.2.2 at disabled status
            ntp1 = SystemNtp(server="2.2.2.2", status=STATUS_DISABLED)
            ntp1.add()
            # enable the NTP server:
            ntp1.status = STATUS_ENABLED.
            ntp1.update()

            # get all NTP configuration
            ntp_list = SystemNtp.getAll()
            for aNtp in ntp_list:
                # use aNtp here
                ...
    """
    
    __display__ = ["server", "status"]
    __obj_name__ = 'ntp'
    __xml_convrt__ = {"ntp_list": "ntp"}

    @staticmethod
    def getAll():
        """ method : system.ntp.get
            Returns a list of NTP configuration in SystemNtp instance.
        """
        try:
            res = method_call.call_api(SystemNtp(), method = "system.ntp.get", format = "url")
            smtp_list = []
            for item in res["smtp_template_list"]:
                smtp_list.append( SystemNtp(**item) )
            return smtp_list
        except AxAPIError:
            return None
    
    def add(self):
        """ method: system.ntp.add
            Create the NTP entry.
        """
        try:
            alist = list()
            alist.append(self.getObjectDict())
            ntp = SystemNtp(ntp_list = alist)
            method_call.call_api(self, method = "system.ntp.add", format = "url", post_data = ntp.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: system.ntp.delete
            Delete the NTP entry.
        """
        try:
            alist = list()
            alist.append(self.getObjectDict())
            ntp = SystemNtp(ntp_list = alist)
            method_call.call_api(self, method = "system.ntp.delete", format = "url", post_data = ntp.getRequestPostDataXml()) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: system.ntp.update
            Update the NTP entry.
        """
        try:
            alist = list()
            alist.append(self.getObjectDict())
            ntp = SystemNtp(ntp_list = alist)
            method_call.call_api(self, method = "system.ntp.update", format = "url", post_data = ntp.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code


