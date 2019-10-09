# -*- encoding: utf8 -*-
"""
    GSLB module:  aXAPI GSLB configuration implementation.
        Support the object-oriented interface for the GSLB such as:
            GslbSite
            GslbZone
            GslbPolicy
            GslbDnsProxy
            GslbServiceIp
            GslbSnmpTemplate
            GslbGlobalSettings
    
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/06/2012
"""

import method_call
from  base import AxObject, AxAPIError

class GslbSite(AxObject):
    """
        Implementation of the aXAPI gslb.site.* method to 
        manage the GSLB site configuration as getAll/create/delete/update 
        
        Usage:
            # Site with parameters:
            # name                  (required) Site name
            # weight                weight
            # template              name of GSLB template
            # status                site status is enabled(1) or disabled(0)
            # bandwidth_cost     tag of bandwidth cost
            #     limit bandwidth   limit of bandwidth cost
            #     threshold         threshold of bandwidth cost
            # active_rrt         tag of active RRT
            #     aging_time        aging time of active RRT
            #     bind_geoloc       bind geographic of active RRT
            #     overlap           overlap of active RRT
            #     limit             limit of active RRT
            #     mask_len          mask length of active RRT
            #     range_factor      range factor of active RRT
            #     smooth_factor     smooth factor of active RRT
            # ip_server_list     tag of IP server list
            #     name              name of IP server
            #     ip_addr           IP address of SLB device
            # slb_device_list    tag of SLB device list
            #     name              SLB device name
            #     ip_addr           IP address of SLB device
            #     admin_preference  admin preference option
            #     max_client        max num of clients
            #     gateway gateway
            #     vip_server_list    tag of virtual server list
            #         name            Name of virtual server    
                    
            # Example: 
            # create a GSLB site configuration as:  
            !
            gslb site site1
               bw-cost limit 100 threshold 10
               active-rtt mask /0
               slb-dev ABC 2.4.6.9
                  admin-preference 10
               slb-dev ABD 2.4.6.10
                  admin-preference 10
            !
            #  
            site1 = GslbSite(name="site1")
            site1.weigth = 5
            site1.status = AxAPI.STATUS_ENABLED
            site1.bandwidth_cost["status"]= AxAPI.STATUS_ENABLED
            site1.bandwidth_cost["limit"] = 100
            site1.bandwidth_cost["threshold"] = 10
            site1.active_rrt["aging_time"] = 10
            site1.active_rrt["bind_geoloc"] = 0
            site1.active_rrt["ignore_count"] = 5
            site1.active_rrt["limit"] = 16383
            site1.active_rrt["mask_len"] = 0
            site1.slb_device_list = [{"name":"ABC", "ip_addr":"2.4.6.9", "admin_preference":10, "max_client":32768, "gateway":"0.0.0.0", "passive_rtt_timer":3, "protocol_aging_fast":1, "protocol_aging_time":0, "protocol_compatible":0}, {"name":"ABD", "ip_addr":"2.4.6.10", "admin_preference":10, "max_client":32768, "gateway":"0.0.0.0", "passive_rtt_timer":3, "protocol_aging_fast":1, "protocol_aging_time":0, "protocol_compatible":0}]
            site1.create()
    """
    
    __display__ = ["name", "status"]
    __obj_name__ = 'gslb_site'
    __xml_convrt__ = {"gslb_site_list": "gslb_site", "ip_server_list": "ip_server", "slb_device_list": "slb_device", "vip_server_list": "vip_server"}

    def __init__(self,**params):
        if not params.has_key("bandwidth_cost"):
            params["bandwidth_cost"] = dict()
        if not params.has_key("active_rrt"):
            params["active_rrt"] = dict()
        AxObject._set_properties(self, **params)

    @staticmethod
    def getAll():
        """ method : gslb.site.getAll
            Returns a list of GSLB sites in GslbSite instance.
        """
        try:
            res = method_call.call_api(GslbSite(), method = "gslb.site.getAll", format = "json")
            site_list = []
            for item in res["gslb_site_list"]:
                site_list.append( GslbSite(**item) )
            return site_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: gslb.site.search
            Search the GSLB site by given name.
        """
        try:
            r = method_call.call_api(GslbSite(), method = "gslb.site.search", name = name, format = "json")
            return GslbSite(**r[GslbSite.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: gslb.site.create
            Create the GSLB site.
        """
        try:
            method_call.call_api(self, method = "gslb.site.create", format = "json", post_data = self.getRequestPostDataJson()) 
            return 0
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: gslb.site.delete
            Delete the GSLB site.
        """
        try:
            method_call.call_api(self, method = "gslb.site.delete", format = "json", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: gslb.site.update
            Update the GSLB site.
        """
        try:
            method_call.call_api(self, method = "gslb.site.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code 
#  gslb.site.slb_device.create/update/delete
#  gslb.site.ip_server.create/update/delete

class GslbZone(AxObject):
    """
        Implementation of the aXAPI gslb.zone.* method to 
        manage the GSLB zone configuration as getAll/create/delete/update 
        
        Usage:
            # Zone with parameters:
            # name                   (required) name of GSLB zone
            # ttl                    TTL of GSLB zone
            # policy                 policy of GSLB zone
            # disable_all_services   zone status is enabled(0) or disabled(1)
            # dns_mx_record_list     tag of DNS MX record list
            #     name               name of DNS MX record
            #     priority           priority of DNS MX record
            # dns_ns_record_list     tag of DNS NS record list
            #     name name of DNS DN record
            # service_list           tag of service list
            #     name                        name of service
            #     port                        port of service
            #     policy                      policy of service
            #     action                      action of service
            #     dns_address_record_list     tag of DNS address record list
            #         as_replace              as replace option of DNS address record
            #         no_response             no replace option of DNS address record
            #         static                  static option of DNS address record
            #         weight                  weight option of DNS address record
            #     dns_mx_record_list          tag of DNS MX record list
            #         name                    name of DNS MX record
            #         priority                priority of DNS MX record
            #     dns_cname_record_list       tag of DNS CName record list
            #         name                    name of DNS CName
            #     dns_ns_record_list          tag of DNS NS record list
            #         name                    name of DNS NS record
            #     dns_ptr_record_list         tag of DNS PTR record list
            #         name                    name of DNS PTR record
            
            # Example: 
            # create a GSLB DNS proxy configuration as:  
            !
            gslb zone CCC1
               ttl 1
               service 45 ffdfdd
               service ftp ffffeeee
               dns-a-record service2 as-replace
               ip-order service1 service2
               dns-mx-record ffff 12
               dns-mx-record ffff1 12
            !
            #  The services, service1 and service2, are required.
            z = GslbZone(name="ccc1")
            z.ttl = 1
            z.policy = "default"
            z.disable_all_services = 0
            z.service_list = [{"name":"ffdfdd", "port":45, "policy":"default", "action":0}, {"name":"ffffeeee", "port":21, "policy":"default", "action":0, "dns_address_record_list":[{"vip_order":"service1", "as_replace":0, "no_response":0, "static":0, "weight":0 },{"vip_order":"service2","as_replace":0,"no_response":1,"static":1,"weight":0}], "dns_mx_record_list":[{"name":"ffff","priority":12},{"name":"ffff1","priority":12}]}]
            z.create()
    """
    
    __display__ = ["name", "status"]
    __obj_name__ = 'zone'
    __xml_convrt__ = {"zone_list": "zone", "dns_mx_record_list": "dns_mx_record", "dns_ns_record_list": "dns_ns_record", "service_list": "service"}

    @staticmethod
    def getAll():
        """ method : gslb.zone.getAll
            Returns a list of GSLB zones in GslbZone instance.
        """
        try:
            res = method_call.call_api(GslbZone(), method = "gslb.zone.getAll", format = "json")
            zone_list = []
            for item in res["zone_list"]:
                zone_list.append( GslbZone(**item) )
            return zone_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: gslb.zone.search
            Search the GSLB zone by given name.
        """
        try:
            r = method_call.call_api(GslbZone(), method = "gslb.zone.search", name = name, format = "json")
            return GslbZone(**r[GslbZone.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: gslb.zone.create
            Create the GSLB zone.
        """
        try:
            method_call.call_api(self, method = "gslb.zone.create", format = "json", post_data = self.getRequestPostDataJson())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: gslb.zone.delete
            Delete the GSLB zone.
        """
        try:
            method_call.call_api(self, method = "gslb.zone.delete", format = "json", name = self.name) 
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: gslb.zone.update
            Update the GSLB zone.
        """
        try:
            method_call.call_api(self, method = "gslb.zone.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code 
# gslb.zone.service.create/update/delete

class GslbDnsProxy(AxObject):
    """
        Implementation of the aXAPI gslb.dns_proxy.* method to 
        manage the GSLB DNS proxy configuration as getAll/create/delete/update 
        
        Usage:
            # DNS proxy with parameters:
            # name                        (required) GSLB DNS proxy name
            # ip_address                  (required) IP address of the dns proxy
            # status                      status, enabled(1) or disabled(0)
            # ha_group                    HA group ID (1 - 31)
            # ha_group_dynamic_weight     Dynamic weight of the DNS proxy in the HA group
            # vport_list                  Virtual port list of the GSLB DNS proxy
            #     port_number             Virtual port number (1 - 65535)
            #     service_group           service group(name) of this virtual port
            #     status                  enabled(1) or disabled(0)
            #     connection_limit        connection limit (1 - 8000000)
            #     over_connection_limit_action     over connection limit action, drop(0), reset (1)
            #     source_nat_pool source  NAT pool name
            #     aflex                   aFlex(name) of this virtual port
            #     udp_template            UDP template (name) of this virtual port
            
            # Example: 
            # create a GSLB DNS proxy configuration as:  
            !
            slb virtual-server my_dns_proxy 22.2.2.1
               stats-data-disable
               port 55  udp
                  name _22.2.2.1_UDP_55
                  disable
                  gslb-enable
                  service-group http
                  no def-selection-if-pref-failed
                  stats-data-disable
               port 80  udp
                  name _22.2.2.1_UDP_80
                  gslb-enable
                  service-group http
                  no def-selection-if-pref-failed
                  stats-data-disable
            !
            #  Above service group 'http' has been created before
            dns_proxy = GslbDnsProxy(name="my_dns_proxy", ip_address="22.2.2.1")
            dns_proxy.vport_list = [{"port_number": 55, "service_group": "http", "status": AxAPI.STATUS_DISABLED}, {"port_number": 80, "service_group": "http", "status": AxAPI.STATUS_ENABLED}]
            dns_proxy.create()

            # retrieve all GSLB DNS proxy configuration:
            d_proxies = GslbDnsProxy.getAll()
            for e in d_proxies:
                print e
                e.dump()

    """
    
    __display__ = ["name", "ip_address", "status"]
    __obj_name__ = 'gslb_vserver'
    __xml_convrt__ = {"gslb_vserver_list": "gslb_vserver", "vport_list": "vport"}

    @staticmethod
    def getAll():
        """ method : gslb.dns_proxy.getAll
            Returns a list of GSLB DNS-proxy in GslbDnsProxy instance.
        """
        try:
            res = method_call.call_api(GslbDnsProxy(), method = "gslb.dns_proxy.getAll", format = "json")
            dns_proxy_list = []
            for item in res["gslb_vserver_list"]:
                dns_proxy_list.append( GslbDnsProxy(**item) )
            return dns_proxy_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: gslb.dns_proxy.search
            Search the GSLB DNS-proxy by given name.
        """
        try:
            r = method_call.call_api(GslbDnsProxy(), method = "gslb.dns_proxy.search", name = name, format = "json")
            return GslbDnsProxy(**r[GslbDnsProxy.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: gslb.dns_proxy.create
            Create the GSLB DNS proxy.
        """
        try:
            method_call.call_api(self, method = "gslb.dns_proxy.create", format = "json", post_data = self.getRequestPostDataJson())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: gslb.dns_proxy.delete
            Delete the GSLB DNS proxy.
        """
        try:
            method_call.call_api(self, method = "gslb.dns_proxy.delete", format = "json", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: gslb.dns_proxy.update
            Update the GSLB DNS proxy.
        """
        try:
            method_call.call_api(self, method = "gslb.dns_proxy.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code  
#gslb.dns_proxy.vport.create/update/delete

class GslbPolicy(AxObject):
    """
        Implementation of the aXAPI gslb.policy.* method to 
        manage the GSLB policy configuration as getAll/create/delete/update 
        
        Usage:
            # DNS proxy with parameters:
            # name                        (required) GSLB DNS proxy name
            # name         GSLB policy name
            # metric       tag for the metric list
            #     session_capacity         tag for session capacity
            #         enabled              the status of session capacity
            #         threshold            threshold of session capacity
            #     active_rrt
            #         enabled              the status of active RRT
            #         samples              the number of samples
            #         difference           difference
            #         tolerance            tolerance
            #         time_out             time out
            #         skip                 skip
            #         single_shot          single shot
            #     connection_load
            #         enabled              the status of connection load
            #         limit                connection limit
            #         samples_num          sample number
            #         samples_interval     sample interval
            #     num_session              number       session
            #         enabled              status of number session
            #         tolerance            tolerance
            #     geo_graphic              tag of geographic
            #         enabled              status of geographic option
            #     ordered_ip               tag if ordered IP option
            #         enabled              status of ordered IP option
            #     weighted_site            tag of weighted site option
            #         enabled              status of weighted site option
            #     active_servers           tag of active servers
            #         enabled              status of active servers
            #     weighted_ip              tag of weighted IP option
            #         enabled              status of weighted IP option
            #     bandwidth_cost           tag of bandwidth option
            #         enabled              status of bandwidth
            #     health_check             tag of health check option
            #         enabled              status of health check option
            #     admin_perference         tag of administrator preference
            #         enabled              status of administrator preference option
            #     least_response           tag of least connection option
            #         enabled              status of least response option
            #     round_robin              tag of round robin option
            #         enabled              status of round robin
            # dns_options                  tag of DNS options
            #     action                   action
            #     active_only              action only
            #     best_only                best only
            #     dns_cache                tag of DNS cache
            #         enabled              status of DNS cache
            #         dns_cache_aging_time DNS cache aging time
            #     cname_detect             CName detected
            #     external_ip              external IP
            #     ip_replace               IP replace
            #     geo_location_alias       geographic location alias
            #     geo_location_action      geographic location action
            #     geo_location_policy      geographic location policy
            #     mx_additional            MX additional
            #     server_mode              tag of server mode
            #         enabled              status of server mode
            #         authoritative_mode   authoritative mode
            #         full_server_list     full server list
            #         server_mx            server MX record
            #         server_mx_additional server MX additional record
            #         server_ns            server NS record
            #         server_auto_ns       server auto NS
            #         server_ptr           server PTR
            #         server_auto_ptr      server auto PTR
            #     sticky                   tag of sticky
            #         enabled              status of sticky
            #         sticky_dns_client_ip_mask_len     sticky DNS client IP mask length
            #     ttl                      tag of TTL
            #         enabled              status of TTL
            #         ttl_time_live        TTL time live
            # geo_location                 tag of geographic location
            #     geo_location_match_first     geographic location match first
            #     geo_location_overlap         geographic location overlap
            
            # Example: 
            # create a GSLB policy configuration as:  
            !
            gslb policy policy01
               dns action
               dns ttl 0
               capacity threshold 80
               num-session tolerance 0
               active-rtt tolerance 20
               active-rtt difference 5
               active-rtt samples 8
               active-rtt timeout 2
               active-rtt skip 5
               metric-order health-check geographic weighted-ip active-servers weighted-site capacity active-rtt num-session connection-load admin-preference bw-cost least-response ordered-ip
            !
            #  
            policy1 = GslbPolicy(name="policy01")
            policy1.metric["session_capacity"] = {"enabled": 0, "threshold": 80}
            policy1.metric["active_rrt"] = {"enabled": 0, "samples": 8, "difference": 5, "tolerance": 20, "timeout": 2, "skip": 5, "single_short": 1}
            policy1.metric["connection_load"] = {"enabled": 0, "limit": 0, "samples_num": 5, "samples_interval": 5}
            policy1.metric["num_sessions"] = {"enabled": 0, "tolerance": 0}
            policy1.metric["geo_graphic"] = {"enabled": 1}
            policy1.metric["orderid_ip"] = {"enabled": 0}
            policy1.metric["weighted_site"] = {"enabled": 0}
            policy1.dns_options["dns_cache"] = {"enabled": 1}
            policy1.dns_options["action"] = 1
            policy1.dns_options["active_only"] = 0
            policy1.dns_options["best_only"] = 0
            policy1.dns_options["dns_cache"] = {"enabled": 0, "dns_cache_aging_time": 0}
            policy1.dns_options["cname_detect"] = 1
            policy1.dns_options["external_ip"] = 1
            policy1.dns_options["ip_replace"] = 0
            policy1.dns_options["geo_location_alias"] = 0
            policy1.dns_options["geo_location_action"] = 0
            policy1.dns_options["geo_location_policy"] = 0
            policy1.dns_options["mx_additional"] = 0
            policy1.dns_options["server_mode"] = {"enabled":0, "authoritative_mode":0}
            policy1.dns_options["ttl"] = {"enabled":1, "ttl_time_live":0}
            policy1.create()
    """
    
    __display__ = ["name"]
    __obj_name__ = 'policy'
    __xml_convrt__ = {"policy_list": "policy"}

    def __init__(self,**params):
        if not params.has_key("metric"):
            params["metric"] = dict()
        if not params.has_key("dns_options"):
            params["dns_options"] = dict()
        if not params.has_key("geo_location"):
            params["geo_location"] = dict()
        AxObject._set_properties(self, **params)

    @staticmethod
    def getAll():
        """ method : gslb.policy.getAll
            Returns a list of GSLB policy in GslbPolicy instance.
        """
        try:
            res = method_call.call_api(GslbPolicy(), method = "gslb.policy.getAll", format = "json")
            policy_list = []
            for item in res["policy_list"]:
                policy_list.append( GslbPolicy(**item) )
            return policy_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: gslb.policy.search
            Search the GSLB policy by given name.
        """
        try:
            r = method_call.call_api(GslbPolicy(), method = "gslb.policy.search", name = name, format = "json")
            return GslbPolicy(**r[GslbPolicy.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: gslb.policy.create
            Create the GSLB policy.
        """
        try:
            method_call.call_api(self, method = "gslb.policy.create", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code 

    def delete(self):
        """ method: gslb.policy.delete
            Delete the GSLB policy.
        """
        try:
            method_call.call_api(self, method = "gslb.policy.delete", format = "json", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: gslb.policy.update
            Update the GSLB policy.
        """
        try:
            method_call.call_api(self, method = "gslb.policy.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code 

class GslbServiceIP(AxObject):
    """
        Implementation of the aXAPI gslb.service_ip.* method to 
        manage the GSLB service IP configuration as getAll/create/delete/update 
        
        Usage:
            # GSLB Service IP with parameters:
            # name                    (required) name of service IP
            # ip_address              (required) ip address of service IP
            # external_ip_address     external IP address of service IP
            # health_monitor          health monitor of service IP
            # status                  status of service IP
            # port_list               tag of port list
            #     port_num            port number of port
            #     protocol            protocol of port
            #     health_monitor      health monitor of port
            #     status              status of port    
                    
            # Example: 
            # create a GSLB service IP configuration as:  
            !
            gslb service-ip service6 1.6.61.41
              external-ip 123.123.123.15
              health-check ping
              port 8888 tcp
              port 8787 tcp
                health-check ping
              port 8789 tcp
                health-check ping
            !
            #  
            svc_ip = GslbServiceIP(name="service6", ip_address="1.6.61.41")
            svc_ip.external_ip_address = "123.123.123.15"
            svc_ip.health_monitor = "ping"
            svc_ip.port_list = [{"port_num": 8888, "protocol": AxAPI.PROTO_TCP, "health_monitor": "ping", "status": AxAPI.STATUS_ENABLED}, {"port_num": 8789, "protocol": AxAPI.PROTO_TCP, "health_monitor": "ping", "status": AxAPI.STATUS_ENABLED}]
            svc_ip.create()
    """
    
    __display__ = ["name"]
    __obj_name__ = 'service_ip'
    __xml_convrt__ = {"service_ip_list": "service_ip", "port_list": "port"}

    @staticmethod
    def getAll():
        """ method : gslb.service_ip.getAll
            Returns a list of GSLB service_ip in GslbServiceIP instance.
        """
        try:
            res = method_call.call_api(GslbServiceIP(), method = "gslb.service_ip.getAll", format = "json")
            policy_list = []
            for item in res["service_ip_list"]:
                policy_list.append( GslbServiceIP(**item) )
            return policy_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: gslb.service_ip.search
            Search the GSLB service-ip by given name.
        """
        try:
            r = method_call.call_api(GslbServiceIP(), method = "gslb.service_ip.search", name = name, format = "json")
            return GslbServiceIP(**r[GslbServiceIP.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: gslb.service_ip.create
            Create the GSLB service IP.
        """
        try:
            method_call.call_api(self, method = "gslb.service_ip.create", format = "json", post_data = self.getRequestPostDataJson()) 
            return 0
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: gslb.service_ip.delete
            Delete the GSLB service IP.
        """
        try:
            method_call.call_api(self, method = "gslb.service_ip.delete", format = "json", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code
        
    def update(self):
        """ method: gslb.service_ip.update
            Update the GSLB service IP.
        """
        try:
            method_call.call_api(self, method = "gslb.service_ip.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code 
# gslb.service_ip.port.create/update/delete

class GslbSnmpTemplate(AxObject):
    """
        Implementation of the aXAPI gslb.snmp_template.* method to 
        manage the GSLB DNS proxy configuration as getAll/create/delete/update 
        
        Usage:
            # DNS proxy with parameters:
            # name                  (required) SNMP template name
            # user_name             SNMP template user name
            # community             community
            # host                  host name or host IP
            # port                  SNMP port
            # version               SNMP version
            # oid                   SNMP OID
            # interface             interface
            # security_level        secure level
            # security_engine_id    security engine ID
            # auth_key              authentication key
            # auth_protocol         authentication protocol
            # private_key           private key
            # private_protocol      private protocol
            # context_engine_id     context engine ID
            # context_name          context name
            # interval              interval  
                      
            # Example: 
            # create a GSLB SNMP template configuration as:  
            !
            gslb template snmp template2
               version v2c
               username user1
               community public
            !
            #  
            snmp_temp = GslbSnmpTemplate(name="template2")
            snmp_temp.user_name ="user1"
            snmp_temp.community ="public"
            snmp_temp.port = 161
            snmp_temp.version = 2
            snmp_temp.interval = 3
            snmp_temp.create()
    """
    
    __display__ = ["name"]
    __obj_name__ = 'snmp_template'
    __xml_convrt__ = {"snmp_template_list": "snmp_template"}

    @staticmethod
    def getAll():
        """ method : gslb.snmp_template.getAll
            Returns a list of GSLB service_ip in GslbSnmpTemplate instance.
        """
        try:
            res = method_call.call_api(GslbSnmpTemplate(), method = "gslb.snmp_template.getAll", format = "json")
            temp_list = []
            for item in res["snmp_template_list"]:
                temp_list.append( GslbSnmpTemplate(**item) )
            return temp_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: gslb.snmp_template.search
            Search the GSLB snmp template by given name.
        """
        try:
            r = method_call.call_api(GslbSnmpTemplate(), method = "gslb.sesnmp_templatervice_ip.search", name = name, format = "json")
            return GslbSnmpTemplate(**r[GslbSnmpTemplate.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: gslb.snmp_template.create
            Create the GSLB SNMP template.
        """
        try:
            method_call.call_api(self, method = "gslb.snmp_template.create", format = "json", post_data = self.getRequestPostDataJson()) 
            return 0
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: gslb.snmp_template.delete
            Delete the GSLB SNMP template.
        """
        try:
            method_call.call_api(self, method = "gslb.snmp_template.delete", format = "json", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code
        
    def update(self):
        """ method: gslb.snmp_template.update
            Update the GSLB SNMP template.
        """
        try:
            method_call.call_api(self, method = "gslb.snmp_template.update", format = "json", post_data = self.getRequestPostDataJson()) 
            return 0
        except AxAPIError, e:
            return e.code
        
class GslbGlobalSettings(AxObject):
    """
        Implementation of the aXAPI gslb.global.get/.set method 
        
        Usage:
    """
    
    @staticmethod
    def read():
        """ method : gslb.global.get
            Returns GSLB global settings.
        """
        try:
            r = method_call.call_api(GslbGlobalSettings(), method = "gslb.global.get", format = "json")
            return GslbGlobalSettings(**r)
        except AxAPIError:
            return None

    def update(self):
        """ method : gslb.global.set
            Update GSLB global settings.
        """
        try:
            method_call.call_api(self, method = "gslb.global.set", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code
        
