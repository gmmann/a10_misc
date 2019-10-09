# -*- encoding: utf8 -*-
"""
    Some base objects for the aXAPI.
    
    Author : Richard Zhang (c)
    e-mail : rzhang@a10networks.com
    Date   : 03/05/2012

"""

from cStringIO import StringIO
import json

class AxAPI:
    """ Status:
    """
    STATUS_ENABLED = 1
    STATUS_DISABLED = 0
    
    """ Protocol Types in service group and real server:
    """
    PROTO_TCP = 2
    PROTO_UDP = 3

    """ Load-Balancer methods:
    """
    LB_ROUND_ROBIN = 0
    LB_WEIGHTED_ROUND_ROBIN = 1
    LB_LEAST_CONN = 2
    LB_WEIGHTED_LEAST_CONN = 3
    LB_LEAST_CONNECTED_ON_SERVICE_PORT = 4
    LB_WEIGHTED_LEAST_CONN_ON_SERVICE_PORT = 5
    LB_FAST_RESP_TIME = 6
    LB_LEAST_REQ = 7
    LB_STRICT_ROUND_ROBIN = 8
    LB_STATE_LESS_SOURCE_IP_HASH = 9
    LB_STATE_LESS_SOURCE_IP_HASH_ONLY = 10
    LB_STATE_LESS_DEST_IP_HASH = 11
    LB_STATE_LESS_SOURCE_DEST_IP_HASH = 12
    LB_STATE_LESS_PER_PACKAGE_ROUND_ROBIN = 13
    
    """ Virtual Service Types:
    """
    SVC_TCP = 2
    SVC_UDP = 3
    SVC_HTTP = 11
    SVC_HTTPS = 12
    SVC_FAST_HTTP = 9
    SVC_RTSP = 5
    SVC_FTP = 6
    SVC_MMS = 7
    SVC_TCP_PROXY = 10
    SVC_SSL_PROXY = 13
    SVC_SMTP = 14
    SVC_SIP = 8
    SVC_SIP_TCP = 15
    SVC_SIP_STL = 16
    SVC_DIAMETER = 17
    SVC_DNS_UDP = 18
    SVC_TFTP = 19
     
class AxError(Exception):
    pass

class AxAPIError(AxError):
    def __init__(self,code,message):
        AxError.__init__(self,"%i : %s"%(code,message))
        self.code = code
        self.message = message

class AxDictObject(object):
    """
        Transform recursively JSON dictionaries into objects
    """
    def __init__(self,name,obj_dict):
        self.__name__ = name
        for k,v in obj_dict.iteritems() :
            if isinstance(v,dict) :
                v = AxDictObject(k,v)
            if isinstance(v,list) :
                v = [ AxDictObject(k,vi) for vi in v ]
            self.__dict__[k] = v

class AxObject(object):
    """
        Base Object for aXAPI Objects
    """
    __display__ = []
    __obj_name__ = ""
    __obj_readonly__ = False
    __xml_convrt__ = []
    
    def __init__(self,**params):
        self._set_properties(**params)

    def _set_properties(self,**params):
        self.__dict__.update(params)
    
    def __getattr__(self,name):
        if name not in self.__dict__ :
            #if not self.loaded :
            #    self.load()
            return "UNKONWN"
        try :
            return self.__dict__[name]
        except KeyError :
            raise AttributeError("'%s' object has no attribute '%s'"%(self.__class__.__name__,name))
    
    def __setattr__(self,name,values):
        if self.__obj_readonly__:
            raise AxError("Read-only instance")
        else:
            self.__dict__[name] = values
    
    def get(self,key,*args,**kwargs):
        return self.__dict__.get(key,*args,**kwargs)
    
    def __getitem__(self,key):
        return self.__dict__[key]
    
    def __setitem__(self,key,value):
        if self.__obj_readonly__:
            raise AxError("Read-only instance")
        else:
            self.__dict__[key] = value

    def __str__(self):
        vals = []
        for k in self.__class__.__display__ :
            val_found = False
            try :
                value = self.__dict__[k]
                val_found = True
            except KeyError :
                #self.load()
                try :
                    value = self.__dict__[k]
                    val_found = True
                except KeyError : pass
            if not val_found : continue
            if isinstance(value,unicode):
                value = value.encode("utf8")
            if isinstance(value,str):
                value = "'%s'"%value
            else : value = str(value)
            if len(value) > 20: value = value[:20]+"..."
            vals.append("%s = %s"%(k,value))
        return "%s(%s)"%(self.__class__.__name__,", ".join(vals))
    
    def __repr__(self): return str(self)

    def getRequestPostDataJson(self):
        if len(self.__obj_name__) > 0 :
            data = dict()
            data[self.__obj_name__] = self.__dict__
        else :
            data = self.__dict__
        return json.dumps(data)

    def _generateListInUrl(self, key_name_str, val_name, aList):
        count = 1
        resp_key = key_name_str+"="
        resp = ""
        is_first = True
        for e in aList:
            if isinstance(e, dict):
                # it has to be a Dictionary!
                if not is_first:
                    resp_key += chr(2)
                    resp += "&"
                resp_key += val_name+str(count)
                resp += self._generateDictInUrl(val_name+str(count), e)
            else:
                # otherwise, don't know to handle
                raise AxAPIError(code=99, message="invalid dictionary object")
            count += 1
            is_first = False
        return resp_key+"&"+resp
    
    def _generateDictInUrl(self, key_name_str, aDict):
        resp = key_name_str+"="
        is_first = True
        for k, v in aDict.iteritems():
            if type(v) == int:
                if not is_first:
                    resp += chr(2)
                resp += k+chr(3)+str(v)
                is_first = False
            elif len(v) > 0:
                if not is_first:
                    resp += chr(2)
                resp += k+chr(3)+v
                is_first = False
        return resp
    
    def _appendString(self, file_str, is_first, string):
        if is_first:
            file_str.write(string)
        else:
            file_str.write("&"+string)
            
    def getObjectDict(self):
        return self.__dict__
    
    def getRequestPostDataXml(self):
        file_str = StringIO()
        is_first = True
        for k, v in self.__dict__.iteritems():
            if self.__xml_convrt__.has_key(k):
                # a list value, v
                if len(v) > 0:
                    self._appendString(file_str, is_first, self._generateListInUrl(k, self.__xml_convrt__[k], v))
                    is_first = False
            elif isinstance(v, dict):
                #  key_name: { k1: v1, k2: v2, ..., }
                if len(v) > 0:
                    self._appendString(file_str, is_first, self._generateDictInUrl(k, v))
                    is_first = False
            elif type(v) == int:
                #  key_name: value
                self._appendString(file_str, is_first, k+"="+str(v))
                is_first = False
            elif len(v) > 0:
                #  key_name: value
                self._appendString(file_str, is_first, k+"="+v)
                is_first = False
        print file_str.getvalue()
        return file_str.getvalue()
    
    def dump(self):
        """
            Debug purpose to print out the AX object internal data.
        """
        print (self.__dict__)
        
    def getInfo(self):
        """
            Returns object information as a dictionary.
            Should be overridden.
        """
        return {}

