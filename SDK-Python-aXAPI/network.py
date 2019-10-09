# -*- encoding: utf8 -*-
"""
    Network module:  aXAPI network configuration implementation.
        Support the object-oriented interface for the network such as:
            Interface
            VirtualInterface
            MgmtInterface
            GatewayConfig
            Trunk
            VlanConfig
            NetworkRoute
            NetworkArp
            NetworkDns
                        
    
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/08/2012
"""

import method_call
from  base import AxObject, AxAPIError

class Interface(AxObject):
    """
        Implementation of the aXAPI network.interface.* method to 
        manage the interface configuration as getAll/get/set/ipv4.add/ipv4.delete/ipv6.add/ipv6.delete, 
        and interface global.set/global.get 
        
        Usage:
            # interface with options:
            # port_num         (required) interface number
            # type             interface type, always be ‘ethernet’
            # name             interface name
            # status           interface status, disabled(0) or enabled(1)
            # mac_addr         interface MAC address
            # duplexity        interface duplexity setting, ‘auto’,’ half’ or ‘full’
            # speed            interface speed setting, ‘auto’, ‘10M’, ‘100M’ or ‘1G’
            # flow_ctl         flow control
            # normal_rate      ICMP normal rate, if this option is set, ICMP rate limit is enabled, if
            #                  this option is not set, ICMP rate limit is disabled on this virtual port.
            # lockup_rate      ICMP lockup rate
            # lockup_period    ICMP lockup period
            # ipv4_addr_list   tag for the collection of interface IPv4 info list
            #     ipv4_addr         IPv4 address of this interface
            #     ipv4_mask         IPv4 mask
            # ipv4_acl         IPv4 access list
            # ipv6_addr_list   tag for the collection of interface IPv6 info list
            #     ipv6_addr                     interface IPv6 address
            #     ipv6_prefix_len               interface IPv6 prefix length
            #     ipv6_is_any_cast_addr         yes(1), no(0)
            #     ipv6_auto_link_local          whether to link local address automatic or not
            #     ipv6_link_local_config        tag for interfaces IPv6 link local configuration.
            #         ipv6_link_local_addr            IPv6 link local address
            #         ipv6_link_local_prefix          IPv6 link local prefix length
            #         ipv6_link_local_is_any_cast     yes(1), no(0)
            # ipv6_acl                  IPv6 access list
            # allow_promiscuous_vip     allow promiscuous VIP status, disabled(0) or enabled(1)
            # tcp_sync_cookie           TCP syn cookie status, disabled(0) or enabled(1)
            # ha_status                 interface HA status, disabled(0) or enabled(1)
            # ha_type                   none(0), router-interface(1), server-interface(2) or both(3)
            # ha_heartbeat              status when HA status enabled, disabled(0) or enabled(1)
            # ha_vlan                   vlan id, only when interface HA status is enabled(1)
            
            # Example: 
    """
    
    __display__ = ["port_num", "status", "name"]
    __obj_name__ = 'interface'
    __xml_convrt__ = {"interface_list": "interface", "ipv4_addr_list": "ipv4", "ipv6_addr_list": "ipv6"}

    @staticmethod
    def getAll():
        """ method : network.interface.getAll
            Returns a list of interface configuration in Interface instance.
        """
        try:
            res = method_call.call_api(Interface(), method = "network.interface.getAll", format = "url")
            a_list = []
            for item in res["interface_list"]:
                a_list.append( Interface(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def get(port_num):
        """ method: network.interface.get
            Get the interface configuration by given port number.
        """
        try:
            r = method_call.call_api(Interface(), method = "network.interface.get", port_num = port_num, format = "url")
            return Interface(**r[Interface.__obj_name__])
        except AxAPIError:
            return None

    def configure(self):
        """ method: network.interface.set
            Configure an interface.
        """
        try:
            method_call.call_api(self, method = "network.interface.set", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteIpv4Address(self, addr, mask):
        """ method: network.interface.ipv4.delete
            Delete the IPv4 address, addr/mask for given interface.
        """
        try:
            method_call.call_api(self, method = "network.interface.ipv4.delete", format = "url", port_num=self.port_num, ipv4_addr=addr, ipv4_mask=mask)
            return 0 
        except AxAPIError, e:
            return e.code

    def addIpv4Address(self, addr, mask):
        """ method: network.interface.ipv4.add
            Add the IPv4 address, addr/mask for given interface.
        """
        try:
            method_call.call_api(self, method = "network.interface.ipv4.add", format = "url", port_num=self.port_num, ipv4_addr=addr, ipv4_mask=mask)
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteIpv6Address(self, v6_addr, v6_addr_prefix_len):
        """ method: network.interface.ipv6.delete
            Delete the IPv6 address, v6_addr/v6_addr_prefix_len for given interface.
        """
        try:
            method_call.call_api(self, method = "network.interface.ipv6.delete", format = "url", port_num=self.port_num, ipv6_addr=v6_addr, ipv6_prefix_len=v6_addr_prefix_len)
            return 0 
        except AxAPIError, e:
            return e.code

    def addIpv6Address(self, v6_addr, v6_addr_prefix_len):
        """ method: network.interface.ipv6.add
            Add the IPv6 address, v6_addr/v6_addr_prefix_len for given interface.
        """
        try:
            method_call.call_api(self, method = "network.interface.ipv6.add", format = "url", port_num=self.port_num, ipv6_addr=v6_addr, ipv6_prefix_len=v6_addr_prefix_len)
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteAllIPv4Addr(self):
        try:
            if self.getObjectDict.has_key("ipv4_addr_list"):
                addr_list = self.getObjectDict()["ipv4_addr_list"]
                for addr in addr_list:
                    self.deleteIpv4Address(addr.ipv4_addr, addr.ipv4_mask)
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteAllIPv6Addr(self):
        try:
            if self.getObjectDict.has_key("ipv6_addr_list"):
                addr_list = self.getObjectDict()["ipv6_addr_list"]
                for addr in addr_list:
                    self.deleteIpv6Address(addr.ipv6_addr, addr.ipv6_prefix_len)
            return 0 
        except AxAPIError, e:
            return e.code

class VirtualInterface(AxObject):
    """
        Implementation of the aXAPI network.ve.* method to 
        manage the virtual interface configuration as getAll/get/set/ipv4.add/ipv4.delete/ipv6.add/ipv6.delete.
        
        Usage:
            # ve with options:
            # port_num         (required) virtual interface number
            # name             virtual interface name
            # status           virtual interface status, disabled(0) or enabled(1)
            # normal_rate      icmp normal rate limit, if option is set, icmp rate limit is enabled,
            #                  if option is not set, icmp rate limit is disabled on this virtual port.
            # lookup_rate      icmp lookup rate.
            # lookup_period    icmp lookup period.
            # ipv4_addr_list   tag of IPv4 address list.
            #     ipv4_addr         IPv4 address
            #     ipv4_mask         IPv4 mask
            # ipv4_acl         IPv4 access list
            # ipv6_addr_list   tag of IPv6 address list
            #     ipv6_addr         IPv6 address
            #     ipv6_prefix_len   IPv6 prefix length
            #     ipv6_is_any_cast_addr     any cast status of address, enabled (1), disabled (0)
            # ipv6_auto_link_local          automatic link local status, enabled(1), disabled(0)
            # ipv6_link_loal_cfg            tag of manual IPv6 link local address.
            #     ipv6_link_local_addr           IPv6 link local address
            #     ipv6_link_local_prefix_len     the prefix length of this IPv6 address
            #     ipv6_link_local_is_any_cast    any cast status of address. Enabled (1), disabled (0)
            # ipv6_acl                  IPv6 access name
            # allow_promiscuous_vip     status, enabled (1), disabled (0)
            # tcp_sync_cookie           TCP sync cookie status, enabled (1), disabled (0)     
                  
            # Example: 
    """
    
    __display__ = ["port_num", "status", "name"]
    __obj_name__ = 've'
    __xml_convrt__ = {"ve_list": "ve", "ipv4_addr_list": "ipv4", "ipv6_addr_list": "ipv6_addr"}

    @staticmethod
    def getAll():
        """ method : network.ve.getAll
            Returns a list of ve configuration in VirtualInterface instance.
        """
        try:
            res = method_call.call_api(VirtualInterface(), method = "network.ve.getAll", format = "url")
            a_list = []
            for item in res["ve_list"]:
                a_list.append( VirtualInterface(**item) )
            return a_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def get(port_num):
        """ method: network.ve.get
            Get the interface configuration by given port number.
        """
        try:
            r = method_call.call_api(VirtualInterface(), method = "network.ve.get", port_num = port_num, format = "url")
            return Interface(**r[VirtualInterface.__obj_name__])
        except AxAPIError:
            return None

    def configure(self):
        """ method: network.ve.set
            Configure a ve.
        """
        try:
            method_call.call_api(self, method = "network.ve.set", format = "url", post_data = self.getRequestPostDataXml())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteIpv4Address(self, addr, mask):
        """ method: network.ve.ipv4.delete
            Delete the IPv4 address, addr/mask for given interface.
        """
        try:
            method_call.call_api(self, method = "network.ve.ipv4.delete", format = "url", port_num=self.port_num, ipv4_addr=addr, ipv4_mask=mask)
            return 0 
        except AxAPIError, e:
            return e.code

    def addIpv4Address(self, addr, mask):
        """ method: network.ve.ipv4.add
            Add the IPv4 address, addr/mask for given interface.
        """
        try:
            method_call.call_api(self, method = "network.ve.ipv4.add", format = "url", port_num=self.port_num, ipv4_addr=addr, ipv4_mask=mask)
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteIpv6Address(self, v6_addr, v6_addr_prefix_len):
        """ method: network.interface.ipv6.delete
            Delete the IPv6 address, v6_addr/v6_addr_prefix_len for given interface.
        """
        try:
            method_call.call_api(self, method = "network.ve.ipv6.delete", format = "url", port_num=self.port_num, ipv6_addr=v6_addr, ipv6_prefix_len=v6_addr_prefix_len)
            return 0 
        except AxAPIError, e:
            return e.code

    def addIpv6Address(self, v6_addr, v6_addr_prefix_len):
        """ method: network.interface.ipv6.add
            Add the IPv6 address, v6_addr/v6_addr_prefix_len for given interface.
        """
        try:
            method_call.call_api(self, method = "network.ve.ipv6.add", format = "url", port_num=self.port_num, ipv6_addr=v6_addr, ipv6_prefix_len=v6_addr_prefix_len)
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteAllIPv4Addr(self):
        try:
            if self.getObjectDict.has_key("ipv4_addr_list"):
                addr_list = self.getObjectDict()["ipv4_addr_list"]
                for addr in addr_list:
                    self.deleteIpv4Address(addr.ipv4_addr, addr.ipv4_mask)
            return 0 
        except AxAPIError, e:
            return e.code
        
    def deleteAllIPv6Addr(self):
        try:
            if self.getObjectDict.has_key("ipv6_addr_list"):
                addr_list = self.getObjectDict()["ipv6_addr_list"]
                for addr in addr_list:
                    self.deleteIpv6Address(addr.ipv6_addr, addr.ipv6_prefix_len)
            return 0 
        except AxAPIError, e:
            return e.code

