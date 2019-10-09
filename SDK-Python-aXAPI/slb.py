# -*- encoding: utf8 -*-
"""
    SLB module:  aXAPI server load balancing implementation.
        Support the object-oriented interface for the SLB such as:
            ServiceGroup        configure the service groups
            ServiceGroupStats   collect the statistics of service group
            RealServer          configure the servers
            RealServerStats     collect the statistics of servers
            VirtualServer       configure the virtual servers and services
            VirtualServerStats  collect the statistics of virtual servers
            
    Author : Richard Zhang, A10 Networks (c)
    email  : rzhang@a10networks.com
    Date   : 03/06/2012
"""

import method_call
from  base import AxObject, AxAPIError

class ServiceGroup(AxObject):
    """
        Implementation of the aXAPI slb.service_group.* method to 
        manage the SLB service groups as getAll/create/delete/update 
        
        Usage:
            # Service group with parameters:
            # name         (required) service group name.
            # protocol     (required) service group type, either TCP(2) or UDP(3).
            # lb_method     desired load-balancing algorithm on the service group with:
            #     0    RoundRobin (default)
            #     1    WeightedRoundRobin
            #     2    LeastConnection
            #     3    WeightedLeastConnection
            #     4    LeastConnectionOnServicePort
            #     5    WeightedLeastConnectionOnServicePort 
            #     6    FastResponseTime
            #     7    LeastRequest
            #     8    StrictRoundRobin
            #     9    StateLessSourceIPHash
            #     10    StateLessSourceIPHashOnly
            #     11    StateLessDestinationIPHash
            #     12    StateLessSourceDestinationIPHash
            #     13    StateLessPerPacketRoundRobin
            # health_monitor      health monitor method used at the service group member.
            # min_active_member   min active members.
            # status              status of min active members, enabled(1) or disabled(0)
            # number              number of min active members.
            # priority_set        priority option of min active members: 
            #     0    Do nothing
            #     1    Skip Priority Set
            #     2    Dynamic PriorityRequired, please fill in a valid number.(1 - 63)
            # client_reset    send client reset when server selection fail enabled(1) or disabled(0)
            # stats_data            stats data, either enabled(1) or disabled(0)
            # extended_stats        extended stats, either enabled(1) or disabled(0)
            # member_list     tag for service group members
            #     server      server name (or IPv4, IPv6 address) of this member
            #     port        server port number
            #     template    server port template name
            #     priority    member priority
            #     stats_data  member stats data, either enabled(1) or disabled(0)
            
            # Example: 
            # retrieve all service groups
            svc_group_list = ServiceGroup.getAll()
            for sg in svc_group_list:
                # work sg
                print sg
            # search for service group with name, g1    
            svc = ServiceGroup.searchByName("g1")
            #  check svc.name, svc.health_monitor, svc.member_list
            
            # create a service group, g3 with members:
            #    1.1.1.2:80 
            #    1.1.1.3:80
            svc2 = ServiceGroup()
            svc2.name = "g3" 
            svc2.protocol = AxAPI.PROTO_TCP
            svc2.lb_method = AxAPI.LB_LEAST_CONNECTED_ON_SERVICE_PORT
            svc2.member_list = [{"server":"1.1.1.2", "port": 80, "status": AxAPI.STATUS_ENABLED}, {"server":"1.1.1.3", "port": 80}]
            svc2.create()
            # disable g3 member 1.1.1.2:80
            svc2.member_list = [{"server":"1.1.1.2", "port": 80, "status": AxAPI.STATUS_DISABLED}]
            svc2.update()  
    """
    
    __display__ = ["name", "protocol", "lb_method"]
    __obj_name__ = 'service_group'
    __xml_convrt__ = {"service_group_list": "service_group", "member_list": "member"}

    @staticmethod
    def getAll():
        """ method :slb.service_group.getAll
            Returns a list of service groups in ServiceGroup instance.
        """
        try:
            res = method_call.call_api(ServiceGroup(), method = "slb.service_group.getAll", format = "json")
            svc_list = []
            for item in res["service_group_list"]:
                svc_list.append( ServiceGroup(**item) )
            return svc_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.service_group.search
            Search the service group by given name.
        """
        try:
            r = method_call.call_api(ServiceGroup(), method = "slb.service_group.search", name = name, format = "json")
            return ServiceGroup(**r[ServiceGroup.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.service_group.create
            Create the service group.
        """
        try:
            method_call.call_api(self, method = "slb.service_group.create", format = "json", post_data = self.getRequestPostDataJson())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.service_group.delete
            Delete the service group.
        """
        try:
            method_call.call_api(self, method = "slb.service_group.delete", format = "json", name = self.name) 
            return 0
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.service_group.update
            Update the service group.
        """
        try:
            method_call.call_api(self, method = "slb.service_group.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0 
        except AxAPIError, e:
            return e.code
        
class ServiceGroupStats(AxObject):
    """
        Implementation of the aXAPI slb.service_group.fetchAllStatistics/.fetchStatistics method to 
        collect the SLB service group statistics data 
        
        Usage:
            # Service group stats with following data fields: all read-only
            # name         service group name.
            # protocol     L4 protocol of this service group, TCP(2) or UDP(3)
            # status       member status
            #            disabled(0)
            #            all members up (1)
            #            partition up(2)
            #            functional up (3)
            #            down (4)
            #            unknown (5)  
            # cur_conns    total number of current connections
            # tot_conns    total number of connections, ulong64
            # req_pkts     total number of request packets received, ulong64
            # resp_pkts    total number of response packets sent, ulong64
            # req_bytes    total number of request bytes received, ulong64
            # resp_bytes   total number of response bytes sent, ulong64
            # cur_reqs     total number of current requests
            # tot_reqs      total number of requests, ulong64
            # tot_succ_reqs total number of successful requests, ulong64
            # member_stat_list  tag for service group members
            #     server        server IPv4 or IPv6 address
            #     port          server port number
            #     status        member status, up(1), down (4), unknown(5)
            #     cur_conns     total number of current connections
            #     tot_conns     total number of connections, ulong64
            #     req_pkts      total number of request packets received, ulong64
            #     resp_pkts     total number of response packets sent, ulong64
            #     req_bytes     total number of request bytes received, ulong64
            #     resp_bytes    total number of response bytes sent, ulong64
            #     cur_reqs      total number of current requests
            #     tot_reqs      total number of requests, ulong64
            #     tot_succ_reqs total number of successful requests, ulong64
            
            # Example: 
            all_group_stats = ServiceGroupStats.getAll()
            for grp in all_group_stats:
                # work grp for stats data
                print grp
            # get the stats data for g1
            aGroup = ServiceGroupStats.searchByName(name='g1')
            print aGroup

    """

    __display__ = ["name", "status", "protocol"]
    __obj_name__ = 'service_group_stat_list'
    __obj_readonly__ = True
    __xml_convrt__ = {"service_group_stat_list": "service_group_stat", "member_stat_list": "member_stat"}

    def __init__(self,**params):
        AxObject.__init__(self,**params)
    
    @staticmethod
    def getAll():
        """ method : slb.service_group.fetchAllStatistics
        """ 
        try:       
            res = method_call.call_api(ServiceGroupStats(), method = "slb.service_group.fetchAllStatistics", format = "json")
            svc_list = []
            for item in res[ServiceGroupStats.__obj_name__]:
                svc_list.append( ServiceGroupStats(**item) )
            return svc_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        try:
            r = method_call.call_api(ServiceGroupStats(), method = "slb.service_group.fetchAllStatistics", name = name, format = "json")
            if len(r[ServiceGroupStats.__obj_name__]) > 0:
                return ServiceGroupStats(**r[ServiceGroupStats.__obj_name__][0])
            else:
                return None
        except AxAPIError:
            return None
        
class RealServer(AxObject):
    """
        Implementation of the aXAPI slb.server.* method to 
        manage the SLB real servers as getAll/create/delete/update 
        
        Usage:
            # Server with parameters:
            # name                    (required) Server name
            # host                    (required) Server IP address or dns name
            # status                  Server status, enabled(1) or disabled(0), default is enabled
            # gslb_external_address   GSLB external IP address
            # health_monitor          Server health-monitor name, empty means the default
            # weight                  Server weight
            # conn_limit              Server connection limit
            # conn_limit_log          Server connection limit logging, enabled(1) or disabled(0)
            # conn_resume             Server connection resume
            # stats_data              Server stat data option, enabled(1) or disabled(0)
            # extended_stats          Server extended stats, enabled(1) or disabled(0)
            # slow_start              Server slow start option, enabled(1) or disabled(0)
            # spoofing_cache          Server spoofing cache option, enabled(1) or disabled(0)
            # template                Server template name, empty means the default
            # port_list        tag for the server ports
            #     port_num           (key) server port number
            #     protocol           (key) either TCP(2) or UDP(3) protocol type
            #     weight             server port weight
            #     no_ssl             server port no ssl, enabled(1) or disabled(0)
            #     conn_limit         server port connection limit
            #     conn_limit_log     server port connection limit logging, enabled(1) or disabled(0)
            #     conn_resume        server port connection resume
            #     template           server port template name, empty means the default
            #     stats_data         server port stat data option, enabled(1) or disabled(0)
            #     extended_stats     server port extended stats, enabled(1) or disabled(0)
            #     health_monitor     server port health monitor name, empty means the default. Only when follow port is not set
            #     follow_port        tag of follow port, only when health monitor is not set
            #         follow_port_num  follow port number
            #         follow_port_type follow port type
            
            # Example: 

    """
    
    __display__ = ["name", "host", "status"]
    __obj_name__ = 'server'
    __xml_convrt__ = {"server_list": "server", "port_list": "port"}

    def __init__(self,**params):
        AxObject.__init__(self,**params)
    
    @staticmethod
    def getAll():
        """ method :slb.server.getAll
            Returns a list of real servers in RealServer instance.
        """
        try:
            res = method_call.call_api(RealServer(), method = "slb.server.getAll", format = "json")
            rs_list = []
            for item in res["server_list"]:
                rs_list.append( RealServer(**item) )
            return rs_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.server.search
            Search the real server by given name.
        """
        try:
            r = method_call.call_api(RealServer(), method = "slb.server.search", name = name, format = "json")
            return RealServer(**r[RealServer.__obj_name__])
        except AxAPIError:
            return None

    @staticmethod    
    def searchByHost(host):
        """ method: slb.server.search
            Search the real server by given host IP or host name.
        """
        try:
            r = method_call.call_api(self, method="slb.server.search", host = host, format = "json")
            return RealServer(**r[RealServer.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.server.create
            Create the real server.
        """
        try:
            method_call.call_api(self, method="slb.server.create", format = "json", post_data = self.getRequestPostDataJson()) 
            return 0
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.server.delete
            Delete the real server.
        """
        try:
            if len(self.name) > 0:
                method_call.call_api(self, method = "slb.server.delete", format = "json", name = self.name) 
            else:
                method_call.call_api(self, method = "slb.server.delete", format = "json", host = self.host)
            return 0
        except AxAPIError, e:
            return e.code
        
    def update(self):
        """ method: slb.server.update
            Update the real server.
        """
        try:
            method_call.call_api(self, method = "slb.server.update", format = "json", post_data = self.getRequestPostDataJson()) 
            return 0
        except AxAPIError, e:
            return e.code
        
class RealServerStats(AxObject):
    """
        Implementation of the aXAPI slb.server.fetchAllStatistics/.fetchStatistics method to 
        collect the SLB server statistics data 
        
        Usage:
            # Server stats with following data fields: all read-only
            # name              Server name.
            # host              Server IP address (IPv4 or IPv6) or dns name
            # status            Server status, either enabled(1) or disabled(0)
            # cur_conns         total number of current connections
            # tot_conns         total number of connections, ulong64
            # req_pkts          total number of request packets received, ulong64
            # resp_pkts         total number of response packets sent, ulong64
            # req_bytes         total number of request bytes received, ulong64
            # resp_bytes        total number of response bytes sent, ulong64
            # cur_reqs          total number of current requests
            # total_reqs        total number of requests, ulong64
            # total _reqs_succ  total number of successful requests, ulong64
            # port_stat_list    tag for the server ports
            #    port_num         server port number
            #    protocol         L3 protocol. TCP(2) or UDP(3)
            #    status           member status either enabled(1) or disabled(0)
            #    cur_conns        total number of current connections
            #    tot_conns        total number of connections, ulong64
            #    req_pkts         total number of request packets received, ulong64
            #    resp_pkts        total number of response packets sent, ulong64
            #    req_bytes        total number of request bytes received, ulong64
            #    resp_bytes       total number of response bytes sent, ulong64
            #    cur_reqs         total number of current requests
            #    total_reqs       total number of requests, ulong64
            #    total_reqs_succ  total number of successful requests, ulong64
            
            # Example: 
            all_server_stats = RealServerStats.getAll()
            for srv in all_server_stats:
                # work srv for stats data
                print srv
            # get the stats data for s1
            s = RealServerStats.searchByName(name='s1')
            print s

    """

    __display__ = ["name", "host", "status"]
    __obj_name__ = 'server_stat_list'
    __obj_readonly__ = True
    __xml_convrt__ = {"server_stat_list": "server_stat", "port_stat_list": "port_stat"}

    def __init__(self,**params):
        AxObject.__init__(self,**params)
    
    @staticmethod
    def getAll():
        """ method : slb.server.fetchAllStatistics
        """      
        try:  
            res = method_call.call_api(RealServerStats(), method = "slb.server.fetchAllStatistics", format = "json")
            svc_list = []
            for item in res[RealServerStats.__obj_name__]:
                svc_list.append( RealServerStats(**item) )
            return svc_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        try:
            r = method_call.call_api(RealServerStats(), method = "slb.server.fetchAllStatistics", name = name, format = "json")
            if len(r[RealServerStats.__obj_name__]) > 0:
                return RealServerStats(**r[RealServerStats.__obj_name__][0])
            else:
                return None
        except AxAPIError:
            return None
    
class VirtualServer(AxObject):
    """
        Implementation of the aXAPI slb.virtual_server.* method to 
        manage the SLB virtual servers as getAll/create/delete/update 
        
        Usage:
            # Virtual server with parameters:
            # name         (required) virtual server name.
            #              Required one of the following token (address, subnet, acl_id, acl_name):
            # address        virtual server address, either IPv4 or IPv6
            # subnet         IPv4 subnet 
            #     address        address of subnet
            #     mask_len       the length of this subnet
            # acl_id         IPv4 ACL id
            # acl_name       IPv6 ACL name
            #
            # status         virtual server status, either enabled(1) or disabled(0)
            # arp_status     ARP disabled option, either disabled(0) or enabled(1)
            # stata_data     stats data option, either disabled(0) or enabled(1)
            # extended_stat  extended stat option, either disabled(0) or enabled(1)
            # disable_vserver_on_condition    disable vserver on conditions. Do not disable virtual server in any case(0), disable virtual server when any port down (1), disable virtual server when all ports down(2)
            # redistribution_flagged          redistribution flagged option, either disabled(0) or enabled(1)
            # ha_group       configured HA group
            #     group                  status of HA config
            #     ha_group_id            ha group id
            #     dynamic_server_weight  dynamic server weight
            # vip_template   virtual server template name
            # pbslb_template pbslb policy template name
            # vport_list     tag for virtual services
            #      protocol   (key) virtual service protocol with:
            #             TCP         2
            #             UDP         3
            #             Other       4
            #             RTSP        5
            #             FTP         6
            #             MMS         7
            #             SIP         8
            #             FAST-HTTP   9
            #             TCP-PROXY   10
            #             HTTP        11
            #             HTTPS       12
            #             SSL-PROXY   13
            #             SMTP        14
            #             SIP-TCP     15
            #             SIP-TLS     16
            #             DIAMETER    17
            #             DNS-UDP     18
            #             TFTP        19
            #      port       (key) virtual service port number
            #      service_group     service group assigned to the virtual service
            #      status            virtual service status either enabled(1) or disabled(0)
            #      connection_limit  connection limit of the virtual service
            #          status        connection limit status of the virtual service either enabled(1) or disabled(0)
            #          connection_limit           connection limit value
            #          connection_limit_action    connection limit action, either reset(1) or drop(0)
            #          connection_limit_log       connection limit logging, either enabled(1) or disabled(0)
            #      default_selection    use default server selection when preferred method fails, 
            #                           either enabled(1) or disabled(0) 
            #      received_hop         use received hop for response either enabled(1) or disabled(0)
            #      stats_data           stats data, either enabled(1) or disabled(0)
            #      extended_stats       extended stats, either enabled(1) or disabled(0)
            #      snat_against_vip     source nat traffic against vip either enabled(1) or disabled(0)
            #      vport_template       virtual server port template name
            #      port_acl_id          assigned access-list, ipv4 only
            #      pbslb_template       pbslb template
            #      aflex_list          aflex list
            #          aflex            name of aflex in aflex_list
            #      acl_natpool_binding_list    acl – natpool binding list
            #                    ***one of the follwing properties, acl_id or acl_name:
            #          acl_id                   ipv4 acl id
            #          acl_name                 IPv6 acl name
            #          nat_pool                 source nat pool name
            #
            #    protocol=HTTP:  vport has the following additional properties: 
            #      send_reset        send client reset when server selection fails, 
            #                        either enabled(1) or disabled(0)
            #      sync_cookie        syn cookie, either enabled(1) or disabled(0)
            #      source_nat            source NAT pool name
            #      http_template         HTTP template name
            #      ram_cache_template    RAM caching template name
            #      tcp_proxy_template    TCP-Proxy template name
            #      server_ssl_template   Server-SSL template name
            #      conn_reuse_template   Connection-Reuse template name
            #              ***one of the following properties, source_ip_persistence_template/cookie_persistence_template
            #      source_ip_persistence_template   Source-IP-Persistent template name
            #      cookie_persistence_template      cookie persistence template name
            #      
            #    protocol=HTTPS:  vport has the following additional properties:
            #      send_reset             send client reset when server selection fails, 
            #                             either enabled(1) or disabled(0)
            #      sync_cookie            syn cookie, either enabled(1) or disabled(0)
            #      source_nat             source NAT pool name
            #      http_template          HTTP template name
            #      ram_cache_template     RAM caching template name
            #      tcp_proxy_template     TCP-Proxy template name
            #      client_ssl_template    client ssl template
            #      server_ssl_template    Server-SSL template name
            #      conn_reuse_template    Connection-Reuse template name
            #              ***one of the following properties: source_ip_persistence_template/cookie_persistence_template
            #      source_ip_persistence_template  Source-IP-Persistent template name
            #      cookie_persistence_template     cookie persistence template name
            #
            #    protocol=FAST-HTTP:  vport has the following additional properties:
            #      send_reset              send client reset when server selection fails, 
            #                              either enabled(1) or disabled(0)
            #      sync_cookie             syn cookie, either enabled(1) or disabled(0)
            #      source_nat              source NAT pool name
            #      http_template           HTTP template name
            #      tcp_template            TCP template name
            #      conn_reuse_template     Connection-Reuse template name
            #              ***one of the following properties: source_ip_persistence_template/cookie_persistence_template
            #      source_ip_persistence_template   Source-IP-Persistent template name
            #      cookie_persistence_template      cookie persistence template name
            #
            #    protocol=TCP:  vport has the following additional properties:
            #      send_reset              send client reset when server selection fails, 
            #                              either enabled(1) or disabled(0)
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      direct_server_return    direct server return (no destination NAT) enabled (1) or disabled (0)
            #      sync_cookie             syn cookie, either enabled(1) or disabled(0)
            #      source_nat              source NAT pool name
            #      tcp_template            TCP template name
            #              ***one of the following properties: source_ip_persistence_template/cookie_persistence_template
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #      cookie_persistence_template       cookie persistence template name
            #
            #    protocol=UDP:  vport has the following additional properties:
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      direct_server_return    direct server return (no destination NAT) enabled (1) or disabled (0)
            #      source_nat              source NAT pool name
            #      udp_template            UDP template name
            #      dns_template            DNS template name
            #      source_ip_persistence_template   Source-IP-Persistent template name
            #
            #    protocol=RTSP:  vport has the following additional properties:
            #      send_reset        send client reset when server selection fails, 
            #      either enabled(1) or disabled(0)
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      direct_server_return    direct server return (no destination NAT) enabled (1) or disabled (0)
            #      sync_cookie        syn cookie, either enabled(1) or disabled(0)
            #      tcp_template        TCP template name
            #      rtsp_template    RTSP template name
            #
            #    protocol=FTP:  vport has the following additional properties:
            #      send_reset        send client reset when server selection fails, 
            #      either enabled(1) or disabled(0)
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      direct_server_return    direct server return (no destination NAT) enabled (1) or disabled (0)
            #      sync_cookie        syn cookie, either enabled(1) or disabled(0)
            #      source_nat        source NAT pool name
            #      tcp_template        TCP template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #
            #    protocol=MMS:  vport has the following additional properties:
            #      send_reset        send client reset when server selection fails, 
            #      either enabled(1) or disabled(0)
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      sync_cookie        syn cookie, either enabled(1) or disabled(0)
            #      tcp_template        TCP template name
            #
            #    protocol=SSL-PROXY:  vport has the following additional properties:
            #      send_reset        send client reset when server selection fails, 
            #      either enabled(1) or disabled(0)
            #      sync_cookie        syn cookie, either enabled(1) or disabled(0)
            #      source_nat        source NAT pool name
            #      tcp_proxy_template        TCP-Proxy template name
            #      client_ssl_template        client ssl template
            #      server_ssl_template        Server-SSL template name
            #      conn_reuse_template    Connection-Reuse template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #
            #    protocol=SMTP-PROXY: vport has the following additional properties:
            #      send_reset           send client reset when server selection fails, 
            #                           either enabled(1) or disabled(0)
            #      sync_cookie          syn cookie, either enabled(1) or disabled(0)
            #      source_nat           source NAT pool name
            #      tcp_proxy_template   TCP-Proxy template name
            #      client_ssl_template  client ssl template
            #      smtp_template        Server-SSL template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #
            #    protocol=SIP:  vport has the following additional properties:
            #      send_reset              send client reset when server selection fails, 
            #                              either enabled(1) or disabled(0)
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      udp_template            UDP template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #      sip_template            SIP template name
            #      dns_template            DNS template name
            #
            #    protocol=SIP-TCP:  vport has the following additional properties:
            #      send_reset                  send client reset when server selection fails, 
            #                                  either enabled(1) or disabled(0)
            #      sync_cookie                 syn cookie, either enabled(1) or disabled(0)
            #      source_nat                  source NAT pool name
            #      server_ssl_template         Server-SSL template name
            #      conn_reuse_template         Connection-Reuse template name
            #      tcp_proxy_template          TCP-Proxy template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #      sip_template                SIP template name
            #
            #    protocol=SIP-TLS:  vport has the following additional properties:
            #      send_reset                 send client reset when server selection fails, 
            #                                 either enabled(1) or disabled(0)
            #      sync_cookie                syn cookie, either enabled(1) or disabled(0)
            #      source_nat                 source NAT pool name
            #      client_ssl_template        client ssl template
            #      server_ssl_template        Server-SSL template name
            #      conn_reuse_template        Connection-Reuse template name
            #      tcp_proxy_template         TCP-Proxy template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #      sip_template               SIP template name
            #
            #    protocol=TCP-PROXY:  vport has the following additional properties:
            #      send_reset                send client reset when server selection fails, 
            #                                either enabled(1) or disabled(0)
            #      sync_cookie               syn cookie, either enabled(1) or disabled(0)
            #      source_nat                source NAT pool name
            #      tcp_proxy_template        TCP-Proxy template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #
            #    protocol=DNS-UDP:  vport has the following additional properties:
            #      send_reset                send client reset when server selection fails, 
            #                                either enabled(1) or disabled(0)
            #      source_nat                source NAT pool name
            #      udp_template              UDP template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #      dns_template              DNS template name
            #
            #     protocol=DIAMETER:  vport has the following additional properties:
            #      send_reset                  send client reset when server selection fails, 
            #                                  either enabled(1) or disabled(0)
            #      source_nat                  source NAT pool name
            #      udp_template                UDP template name
            #      source_ip_persistence_template    Source-IP-Persistent template name
            #      dns_template                DNS template name
            #
            #    protocol=TFTP:  vport has the following additional properties:
            #      ha_connection_mirror    HA connection mirror enabled(1) or disabled (0)
            #      direct_server_return    direct server return (no destination NAT) enabled (1)
            #      source_nat              source NAT pool name
            #      udp_template            UDP template name
            #
            #    protocol=OTHER:  vport has the following additional properties:
            #      direct_server_return   direct server return (no destination NAT) enabled (1)
            #      source_nat          source NAT pool name
            #      udp_template        UDP  template name
            #      l4_template_type    TCP (2) or UDP(3)
            #          ***one of the following properties: udp_template/tcp_template
            #      udp_template        UDP template name
            #      tcp_template        TCP template name
            
            # Example: 
            # create a virtual server, test_vip1, with address 100.10.10.1
            # and configure a HTTP service at port 80:
            vip1 = VirtualServer(name="test_vip1", address="100.10.10.1")
            vip1.vport_list = [{"port" : 80, "protocol": AxAPI.SVC_HTTP}]
            vip1.create()
            # disable the vip1 HTTP port 80:
            vip1.vport_list = [{"port" : 80, "protocol": AxAPI.SVC_HTTP, "status": AxAPI.STATUS_DISABLED}]
            vip1.update()
            # delete the vip1
            vip1.delete()

            # get all virtual server
            vip_list = VirtualServer.getAll()
            for avip in vip_list:
                # work on avip instance
                print avip
            # search a virtual server with name, vip2
            vip2 = VirtualServer.searchByName("vip2")
    """

    __display__ = ["name", "address", "status"]
    __obj_name__ = 'virtual_server'
    __xml_convrt__ = {"virtual_server_list": "virtual_server", "vport_list": "vport", "aflex_list": "aflex", "acl_natpool_binding_list": "acl_natpool_binding"}
    
    def __init__(self,**params):
        AxObject.__init__(self,**params)
    
    @staticmethod
    def getAll():
        """ method :slb.virtual_server.getAll
            Returns a list of virtual servers in VirtualServer instance.
        """
        try:
            res = method_call.call_api(VirtualServer(), method = "slb.virtual_server.getAll", format = "json")
            vip_list = []
            for item in res["virtual_server_list"]:
                vip_list.append( VirtualServer(**item) )
            return vip_list
        except AxAPIError:
            return None
    
    @staticmethod    
    def searchByName(name):
        """ method: slb.virtual_server.search
            Search the virtual server by given name.
        """
        try:
            r = method_call.call_api(VirtualServer(), method = "slb.virtual_server.search", name = name, format = "url")
            return VirtualServer(**r[VirtualServer.__obj_name__])
        except AxAPIError:
            return None

    def create(self):
        """ method: slb.virtual_server.create
            Create the virtual server.
        """
        try:
            method_call.call_api(self, method = "slb.virtual_server.create", format = "json", post_data = self.getRequestPostDataJson())
            return 0 
        except AxAPIError, e:
            return e.code
        
    def delete(self):
        """ method: slb.virtual_server.delete
            Delete the virtual server.
        """
        try:
            method_call.call_api(self, method = "slb.virtual_server.delete", format = "json", name = self.name)
            return 0 
        except AxAPIError, e:
            return e.code

    def update(self):
        """ method: slb.virtual_server.update
            Update the virtual server.
        """
        try:
            method_call.call_api(self, method = "slb.virtual_server.update", format = "json", post_data = self.getRequestPostDataJson())
            return 0
        except AxAPIError, e:
            return e.code 
        
class VirtualServerStats(AxObject):
    """
        Implementation of the aXAPI slb.virtual_server.fetchAllStatistics/.fetchStatistics method to 
        collect the SLB virtual server statistics data 
        
        Usage:
            # Virtual server stats with following data fields: all read-only
            # name          Virtual server name.
            #     ***One of the following token (address, subnet, acl_id, acl_name):
            # address       virtual server address, either IPv4 or IPv6
            # subnet        IPv4 subnet 
            #     address   address of subnet
            #     mask_len  the length of this subnet
            # acl_id        IPv4 ACL id
            # acl name      IPv6 ACL name
            # status        Virtual server status
            #     0:    disabled
            #     1:    all up
            #     2:    partition up
            #     3:    function up
            #     4:    down
            #     5:    unknown
            # cur_conns          total number of current connections
            # tot_conns          total number of connections, ulong64
            # req_pkts           total number of request packets received, ulong64
            # resp_pkts          total number of response packets sent, ulong64
            # req_bytes          total number of request bytes received, ulong64
            # resp_bytes         total number of response bytes sent, ulong64
            # cur_reqs           total number of current requests
            # total_reqs         total number of requests, ulong64
            # total _reqs_succ   total number of successful requests, ulong64
            # vport_stat_list    tag for the virtual server ports
            #      port        virtual server port number
            #      protocol    virtual port protocol
            #             TCP        2
            #             UDP        3
            #             Other      4
            #             RTSP       5
            #             FTP        6
            #             MMS        7
            #             SIP        8
            #             FAST-HTTP  9
            #             TCP-PROXY  10
            #             HTTP       11
            #             HTTPS      12
            #             SSL-PROXY  13
            #             SMTP       14
            #             SIP-TCP    15
            #             SIP-STL    16
            #             DIAMETER   17
            #             DNS-UDP    18
            #             TFTP       19
            #      status      virtual port status
            #             0:    disabled
            #             1:    all up
            #             2:    partition up
            #             3:    function up
            #             4:    down
            #             5:    unknown
            #      cur_conns         total number of current connections
            #      tot_conns         total number of connections, ulong64
            #      req_pkts          total number of request packets received, ulong64
            #      resp_pkts         total number of response packets sent, ulong64
            #      req_bytes         total number of request bytes received, ulong64
            #      resp_bytes        total number of response bytes sent, ulong64
            #      cur_reqs          total number of current requests
            #      total_reqs        total number of requests, ulong64
            #      total_reqs_succ   total number of successful requests, ulong64
            
            # Example: 
            all_vip_stats = VirtualServerStats.getAll()
            for vip in all_vip_stats:
                # work vip for stats data
                print vip
            # get the stats data for vip1
            avip = VirtualServerStats.searchByName(name='vip1')
            print avip
    """
    
    __display__ = ["name", "status", "protocol"]
    __obj_name__ = 'virtual_server_stat_list'
    __obj_readonly__ = True
    __xml_convrt__ = {"virtual_server_stat_list": "virtual_server_stat", "vport_stat_list": "vport_stat"}

    def __init__(self,**params):
        AxObject.__init__(self,**params)
    
    @staticmethod
    def getAll():
        """ method : slb.virtual_server.fetchAllStatistics
        """    
        try:    
            res = method_call.call_api(VirtualServerStats(), method = "slb.virtual_server.fetchAllStatistics", format = "json")
            vip_list = []
            for item in res[VirtualServerStats.__obj_name__]:
                vip_list.append( VirtualServerStats(**item) )
            return vip_list
        except AxAPIError:
            return None
        
    @staticmethod    
    def searchByName(name):
        try:
            r = method_call.call_api(VirtualServerStats(), method = "slb.virtual_server.fetchAllStatistics", name = name, format = "json")
            if len(r[VirtualServerStats.__obj_name__]) > 0:
                return VirtualServerStats(**r[VirtualServerStats.__obj_name__][0])
            else:
                return None
        except AxAPIError:
            return None





