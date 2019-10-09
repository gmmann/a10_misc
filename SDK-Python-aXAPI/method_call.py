# -*- encoding: utf8 -*-
"""
    method_call module.
    
    This module is used to perform the calls to the AX RESTful interface.
    
    Author: Richard Zhang, A10 Networks (c)
    e-mail: rzhang@a10networks.com
    Date  : 03/04/2012
    
"""
import urllib2
import urllib
import json
from xml.etree.ElementTree import XML
from base import AxObject, AxError, AxAPIError

REST_URL = "/services/rest/V2/"
AXAPI_DEVICE = "192.168.210.239"
AXAPI_SESSION_ID = ""
AXAPI_LOGIN = 0

class AxApiContext(AxObject):    
    
    __display__ = ["session_id", "is_login", "device_ip", "username"]
    
    def __init__(self, device_ip, username, password):
        params = dict(device_ip=device_ip, username=username, password=password, is_login=False)
        AxObject.__init__(self, **params)

    def authentication(self):
        global AXAPI_SESSION_ID, AXAPI_DEVICE, AXAPI_LOGIN
        AXAPI_DEVICE = self.device_ip
        AXAPI_SESSION_ID = ""
        AXAPI_LOGIN = 0
        resp = call_api(self, method="authenticate", username=self.username, password=self.password)
        xml_s = XML(resp)
        for node in xml_s.findall('session_id'):
            self.session_id = node.text
            self.is_login = True
            _set_session_id(self.session_id, self.device_ip)
            break
        return self

    def switchContext(self):
        if self.is_login == False:
            self.authentication()
        else:
            _set_session_id(self.session_id, self.device_ip)

def call_api(axobjectinstance, **args):
    """
        Performs the GET/POST calls to the aXAPI REST interface.
        
        Arguments :
            method : The name of aXAPI call.
            format : (optional) Specify the aXAPI format, json/url.  The default is "url".
            post_data : (optional) The POST data for the REST create/update/delete transactions.
            args : the arguments to pass to the method.
    """

    if AXAPI_LOGIN == 1:
        args["session_id"] = AXAPI_SESSION_ID

    if args.has_key("post_data"):
        data = args["post_data"]
        del args["post_data"]
        url_str = _get_request_url()+"?"+urllib.urlencode(args)
    else:
        data = urllib.urlencode(args)
        url_str = _get_request_url()
    print data
    print url_str
    
    resp = _send_request(url_str, data)
    print resp
    if args.has_key("format"):
        fmt = args["format"]
        if fmt == "json":
            # handle the json response to build the dict
            resp = json.loads(resp)
        else:
            # handle the xml/url response into the dict
            resp = _XmlDict(XML(resp), axobjectinstance.__xml_convrt__)
            print resp
        
    return resp
            
def _set_session_id(session_id, device_ip):
    global AXAPI_SESSION_ID, AXAPI_DEVICE, AXAPI_LOGIN
    AXAPI_SESSION_ID = session_id
    AXAPI_DEVICE = device_ip
    AXAPI_LOGIN = 1

def _get_request_url() :
    return "https://" + AXAPI_DEVICE + ":443" + REST_URL 

def _send_request(url,data):
    req = urllib2.Request(url,data)
    try :
        return urllib2.urlopen(req).read()
    except urllib2.HTTPError , e:
        raise AxError( e.read().split('&')[0] )

class _XmlList(list):
    def __init__(self, aList, assistant_dict):
        for element in aList:
            if len(element):
                # treat like dict
                #if len(element) == 1 or element[0].tag != element[1].tag:
                #    self.append(XmlDictConfigWithAssistant(element, assistant_dict))
                # treat like list
                #elif element[0].tag == element[1].tag:
                #    self.append(XmlListConfigWithAssistant(element, assistant_dict))
                if assistant_dict.has_key(element.tag):
                    self.append( _XmlList(element, assistant_dict) )
                else:
                    self.append( _XmlDict(element, assistant_dict) )
            elif element.text:
                text = element.text.strip()
                if text.isdigit():
                    self.append(int(element.text))
                else:
                    self.append(text)

class _XmlDict(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = _XmlDictConvertWithAssistant(root, assistant_dict)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = _XmlDictConvertWithAssistant(root, assistant_dict)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element, assistant_dict):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #if len(element) == 1 or element[0].tag != element[1].tag:
                #    aDict = XmlDictConfigWithAssistant(element, assistant_dict)
                if assistant_dict.has_key(element.tag):
                    aDict = _XmlList(element, assistant_dict)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = _XmlDict(element, assistant_dict)
                # if the tag has attributes, add those to the dict
                if element.items():
                    #aDict.update(dict(element.items()))
                    aDict.update(element.items())
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                if assistant_dict.has_key(element.tag):
                    # add the empty list
                    self.update({element.tag: []})
                elif element.text == None:
                    self.update({element.tag: ''})
                elif element.text.isdigit():
                    self.update({element.tag: int(element.text)})
                else:
                    self.update({element.tag: element.text})


