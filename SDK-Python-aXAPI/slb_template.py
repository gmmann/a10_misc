# -*- encoding: utf8 -*-
"""
    SLB Template module:  aXAPI template configuration implementation.
        Support the object-oriented interface for the SLB templates such as:
            TemplateSmtp:            
            TemplateCache:            
            TemplateVirtualServer:    
            TemplateVipPort:            
            TemplateServer:
            TemplateServerPort
            TemplateHttp
            TemplatePbslb
            TemplateSip
            TemplateRtsp
            TemplateConnReuse
            TemplateTcp
            TemplateUdp
            TemplateCookiePersist
            TemplateSourceIpPersist
            TemplateDestinationIp
            TemplateSslPersist
            TemplateTcpProxy
            TemplateDns
            TemplateDiameter
    
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/07/2012
"""

import method_call
from  base import AxObject, AxAPIError

class TemplateSmtp(AxObject):
    """
        Implementation of the aXAPI slb.template.smtp.* method to 
        manage the SLB SMTP template as getAll/create/delete/update 
        
        Usage:
            # SMTP template with options:
            # name                     (required)
            # starttls                 STARTTLS, disabled(0), enforced(2) or optional(1)
            # EXPN                     SMTP command EXPN, enabled(0) or disabled(1)
            # TURN                     SMTP command TURN, enabled(0) or disabled(1)
            # VRFY                     SMTP command VRFY, enabled(0) or disabled(1)
            # server_domain            server domain
            # service_ready_message    service ready message
            # client_domain_switching_list   tag for the collection of client switchings
            #     client_domain              client domain
            #     service_group              service group name
            #     match_type                 match type, contains(0), starts with(1), ends with(2)
            
            # Example: create a smtp template like
            # !
            # slb template smtp my_smpt_temp1
            #    client-domain-switching contains domain1 service-group sg1
            # !
            smtp = TemplateSmtp(name="my_smpt_templ")
            smtp.client_domain_switching_list = [{"client_domain": "domain1", "service_group": "sg1", "match_type": 0}]
            smtp.create()
            # get all SMTP templates
            a_list = TemplateSmtp.getAll()
            for aSmtp in a_list:
                # use aSmtp here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'smtp_template'
    __xml_convrt__ = {"smtp_template_list": "smtp_template", "client_domain_switching_list": "client_domain_switching"}

    @staticmethod
    def getAll():
        """ method : slb.template.smtp.getAll
            Returns a list of SMTP template in TemplateSmtp instance.
        """
        try:
            res = method_call.call_api(TemplateSmtp(), method = "slb.template.smtp.getAll", format = "url")
            smtp_list = []
            for item in res["smtp_template_list"]:
                smtp_list.append( TemplateSmtp(**item) )
            return smtp_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.smtp.search
            Search the SMTP template by given name.
        """
        try:
            r = method_call.call_api(TemplateSmtp(), method = "slb.template.smtp.search", name = name, format = "url")
            return TemplateSmtp(**r[TemplateSmtp.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.smtp.create
            Create the SMTP template.
        """
        try:
            method_call.call_api(self, method = "slb.template.smtp.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.smtp.delete
            Delete the SMTP template.
        """
        try:
            method_call.call_api(self, method = "slb.template.smtp.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.smtp.update
            Update the SMTP template.
        """
        try:
            method_call.call_api(self, method = "slb.template.smtp.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateCache(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            # age                (second)
            # max_cache          max cache size (MB)
            # min_content        min content size (Bytes)
            # max_content        max content size (Bytes)
            # rep_policy         least frequently used(0)
            # acc_rel_req        accept reload request, disabled(0) or enabled(1)
            # veri_host          verify host, disabled(0) or enabled(1)
            # def_pol_no_cache   default policy no cache, disabled(0) or enabled(1)
            # insert_age         insert age, disabled(0) or enabled(1)
            # insert_via         insert via, disabled(0) or enabled(1)
            # policy_list        XML tag for the collection of policys
            #     uri                URI
            #     action             cache(0), no cache(1) or invalidate(2)
            #     duration           duration (second), only when act is cache(0)
            #     pattern            only when act is invalidate(2)
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateCache instance.
        """
        try:
            res = method_call.call_api(TemplateCache(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateCache(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateCache(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateCache(**r[TemplateCache.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
class TemplateVirtualServer(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB virtual server template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateCache instance.
        """
        try:
            res = method_call.call_api(TemplateVirtualServer(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateVirtualServer(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateVirtualServer(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateVirtualServer(**r[TemplateVirtualServer.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateVipPort(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateCache instance.
        """
        try:
            res = method_call.call_api(TemplateVipPort(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateVipPort(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateVipPort(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateVipPort(**r[TemplateVipPort.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateServer(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateServer instance.
        """
        try:
            res = method_call.call_api(TemplateServer(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateServer(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateServer(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateServer(**r[TemplateServer.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateServerPort(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateServerPort instance.
        """
        try:
            res = method_call.call_api(TemplateServerPort(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateServerPort(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateServerPort(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateServerPort(**r[TemplateServerPort.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateHttp(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateHttp instance.
        """
        try:
            res = method_call.call_api(TemplateHttp(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateHttp(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateHttp(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateHttp(**r[TemplateHttp.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplatePbslb(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplatePbslb instance.
        """
        try:
            res = method_call.call_api(TemplatePbslb(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplatePbslb(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplatePbslb(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplatePbslb(**r[TemplatePbslb.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateSip(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateCache instance.
        """
        try:
            res = method_call.call_api(TemplateSip(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateSip(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateSip(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateSip(**r[TemplateSip.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateRtsp(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateRtsp instance.
        """
        try:
            res = method_call.call_api(TemplateRtsp(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateRtsp(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateRtsp(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateRtsp(**r[TemplateRtsp.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateConnReuse(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateConnReuse instance.
        """
        try:
            res = method_call.call_api(TemplateConnReuse(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateConnReuse(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateConnReuse(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateConnReuse(**r[TemplateConnReuse.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateTcp(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateTcp instance.
        """
        try:
            res = method_call.call_api(TemplateTcp(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateTcp(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateTcp(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateTcp(**r[TemplateTcp.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateUdp(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateUdp instance.
        """
        try:
            res = method_call.call_api(TemplateUdp(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateUdp(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateUdp(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateUdp(**r[TemplateUdp.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateCookiePersist(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateCookiePersist instance.
        """
        try:
            res = method_call.call_api(TemplateCookiePersist(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateCookiePersist(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateCookiePersist(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateCookiePersist(**r[TemplateCookiePersist.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateSourceIpPersist(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateSourceIpPersist instance.
        """
        try:
            res = method_call.call_api(TemplateSourceIpPersist(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateSourceIpPersist(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateSourceIpPersist(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateSourceIpPersist(**r[TemplateSourceIpPersist.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateDestinationIp(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateDestinationIp instance.
        """
        try:
            res = method_call.call_api(TemplateCache(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateCache(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateCache(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateCache(**r[TemplateCache.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class Template(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateCache instance.
        """
        try:
            res = method_call.call_api(TemplateDestinationIp(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateDestinationIp(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateDestinationIp(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateDestinationIp(**r[TemplateDestinationIp.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateSslPersist(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateSslPersist instance.
        """
        try:
            res = method_call.call_api(TemplateSslPersist(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateSslPersist(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateSslPersist(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateSslPersist(**r[TemplateSslPersist.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateTcpProxy(AxObject):
    """
        Implementation of the aXAPI slb.template.cache.* method to 
        manage the SLB cache template as getAll/searchByName/create/delete/update 
        
        Usage:
            # cache template with options:
            # name               (required) cache template name 
            
            # Example: create a cache template
            # !
            # slb template cache my_cache_templ1
            #    policy uri abc nocache
            #    policy uri 123 nocache
            # !
            cache1 = TemplateRamCache(name="my_cache_templ1")
            cache1.policy_list = [{"uri": "abc", "action": 1}, {"uri": "123", "action": 1}]
            cache1.create()
            # get all cache templates
            caches = TemplateRamCache.getAll()
            for e in caches:
                print e
                # use aCache here
                ...
    """
    
    __display__ = ["name"]
    __obj_name__ = 'cache_template'
    __xml_convrt__ = {"cache_template_list": "cache_template", "policys": "policy", "policy_list": "policy"}

    @staticmethod
    def getAll():
        """ method : slb.template.cache.getAll
            Returns a list of cache template in TemplateTcpProxy instance.
        """
        try:
            res = method_call.call_api(TemplateTcpProxy(), method = "slb.template.cache.getAll", format = "url")
            a_list = []
            for item in res["cache_template_list"]:
                a_list.append( TemplateTcpProxy(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.cache.search
            Search the cache template by given name.
        """
        try:
            r = method_call.call_api(TemplateTcpProxy(), method = "slb.template.cache.search", name = name, format = "url")
            return TemplateTcpProxy(**r[TemplateTcpProxy.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.cache.create
            Create the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.cache.delete
            Delete the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.cache.update
            Update the cache template.
        """
        try:
            method_call.call_api(self, method = "slb.template.cache.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code

class TemplateDns(AxObject):
    """
        Implementation of the aXAPI slb.template.dns.* method to 
        manage the SLB dns template as getAll/searchByName/create/delete/update 
        
        Usage:
            # dns template with options:
            # name               (required) cache template name 
            # name                             dns template name
            # malformed_query                  malformed query, disabled(0), drop(1), forward to service group(2)
            # service_group_malformed_query    service group name, only malformed_query is 2
            # status                           dns template status, disabled(0) or enabled(1)
            # def_policy                       default policy, no cache(0) or cache(1)
            # log_period                       log period (Minutes)
            # max_cache_size
            # class_list         tag for the class list
            #     name                 class list name
            #     lid_list             tag for the collection of LID
            #         id                   LID id
            #         dns_cache_status     DNS cache status, enabled(1) or disabled(0)
            #         ttl
            #         weight
            #         conn_rate_limit      connection rate limit
            #         conn_rate_limit_per  connection rate limit interval
            #         over_limit_action    drop(0), forward(1),
            #         enable               DNS cache(2) or disable dns cache(3)
            #         lockout              lockout
            #         log_status           log status, enabled(1). disabled(0)
            #         log_interval         log interval
    """
    
    __display__ = ["name"]
    __obj_name__ = 'dns_template'
    __xml_convrt__ = {"dns_template_list": "dns_template", "lid_list": "lid"}

    @staticmethod
    def getAll():
        """ method : slb.template.dns.getAll
            Returns a list of dns template in TemplateDns instance.
        """
        try:
            res = method_call.call_api(TemplateDns(), method = "slb.template.dns.getAll", format = "url")
            a_list = []
            for item in res["dns_template_list"]:
                a_list.append( TemplateDns(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.dns.search
            Search the dns template by given name.
        """
        try:
            r = method_call.call_api(TemplateDns(), method = "slb.template.dns.search", name = name, format = "url")
            return TemplateDns(**r[TemplateDns.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.dns.create
            Create the dns template.
        """
        try:
            method_call.call_api(self, method = "slb.template.dns.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.dns.delete
            Delete the dns template.
        """
        try:
            method_call.call_api(self, method = "slb.template.dns.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.dns.update
            Update the dns template.
        """
        try:
            method_call.call_api(self, method = "slb.template.dns.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
   
class TemplateDiameter(AxObject):
    """
        Implementation of the aXAPI slb.template.diameter.* method to 
        manage the SLB diameter template as getAll/searchByName/create/delete/update 
        
        Usage:
            # diameter template with options:
            # name               (required) cache template name 
            # name                     diameter template name
            # multiple_origin_host     multiple origin host
            # origin_host              origin host
            # origin_realm             origin realm
            # product_name             product name
            # vendor_id                vendor id
            # idle_timeout             idle timeout
            # dwr_time_interval        dwr time interval
            # session_age              session age
            # customizing_cea_response     customizing cea response
            # duplicate_avp_code       duplicate avp code
            # duplicate_pattern        duplicate pattern
            # duplicate_service_name   duplicate service name
            # avps                     tag for collection of avps
            #     code                 code
            #     mandatory            mandatory
            #     type                 INT32 (1), INT64(2), String(3)
            #     value                value
            # message_codes            tag for collection of message codes
            #     value                 message code
    """
    
    __display__ = ["name"]
    __obj_name__ = 'diameter_template'
    __xml_convrt__ = {"diameter_template_list": "diameter_template", "avps": "avp", "message_codes": "code"}

    @staticmethod
    def getAll():
        """ method : slb.template.diameter.getAll
            Returns a list of diameter template in TemplateDiameter instance.
        """
        try:
            res = method_call.call_api(TemplateDiameter(), method = "slb.template.diameter.getAll", format = "url")
            a_list = []
            for item in res["diameter_template_list"]:
                a_list.append( TemplateDiameter(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.template.diameter.search
            Search the diameter template by given name.
        """
        try:
            r = method_call.call_api(TemplateDiameter(), method = "slb.template.diameter.search", name = name, format = "url")
            return TemplateDiameter(**r[TemplateDiameter.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.template.diameter.create
            Create the diameter template.
        """
        try:
            method_call.call_api(self, method = "slb.template.diameter.create", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.template.diameter.delete
            Delete the diameter template.
        """
        try:
            method_call.call_api(self, method = "slb.template.diameter.delete", format = "url", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.template.diameter.update
            Update the diameter template.
        """
        try:
            method_call.call_api(self, method = "slb.template.diameter.update", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        