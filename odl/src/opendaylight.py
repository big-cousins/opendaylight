'''
Created on 2016-5-4

@author: jeremy
'''
import requests 
from requests.auth import HTTPBasicAuth
import json
import os
import xmltodict


class Opendaylight(object):
    '''
    An object holding details to talk to the opendaylight REST API 
    '''
    def __init__(self):
        '''
        Constructor: Set some mostly reasonable defaults
        '''
        self.setup={'path':'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/',  'table':'/table/','flow':'/flow/',\
                    'username':'admin','password':'admin' }
        self.url=None
        self.auth=None
        
    def prepare(self,openflow_id,flow_id):
        self.url=self.setup['path']+openflow_id+self.setup['table']+'0'+self.setup['flow']+flow_id
        self.auth=HTTPBasicAuth(self.setup['username'],self.setup['password'])


class OpendaylightFlow(object):
    
    def __init__(self,odl_obj):
        """Mandatory argument:
            odl  -an Opendaylight object
        """
        self.odl_obj=odl_obj
        self.request=None
        self.flows=None
        
    def add(self,openflow_sw,xml_to_dict_flow,flow_id):
        #clean out any remaining crud from previous calls
        if hasattr(self,'request'):
            del self.request
           
        self.odl_obj.prepare(openflow_sw, flow_id)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        body=json.dumps(xml_to_dict_flow)
        self.request=requests.put(url=self.odl_obj.url,auth=self.odl_obj.auth,data=body,headers=headers)
        if self.request.status_code != 200:
            raise OpendaylightError({'url':self.odl_obj.url,'http_code':self.request.status_code,'message':self.request.text})
            
    def delete(self,openflow_sw,flow_id):
        if hasattr(self, 'request'):
            del self.request
        self.odl_obj.prepare(openflow_sw,flow_id)
        self.request=requests.delete(url=self.odl_obj.url,auth=self.odl_obj.auth)
        if self.request.status_code!=200:
            raise OpendaylightError({'url':self.odl_obj.url,'http_code':self.request.status_code,'msg':self.request.text})
        
        
class OpendaylightFlowOperate(object):
    
    def __init__(self):
        """initialize the data members"""
        self.openflow_sw=[]
        self.flow_id=[]
        self.flow_content=[]
        self.xml_files_path=[]
        self.xml_files_name=[]
        
    def get_flow_id(self):
        """acquire n number for flow_id"""
        n=input("please input a number, which is number of flows >>  ")
        prompt="please input %d numbers >> " % n
        self.flow_id=raw_input(prompt).split()
    
    def get_xml_files_path(self):
        """ acquire main_path, the path of xmlfiles, and  the path of xml files
            eg:
            mian_path="/home/jeremy/workspace/odl/xmlfiles/"
            xml_files_path=/home/jeremy/workspace/odl/xmlfiles/template_1.xml
       """
        cur_dir=os.path.dirname(__file__)
        main_path=os.path.join(os.path.dirname(cur_dir) ,'xmlfiles/' )     
        for i in self.xml_files_name:
            self.xml_files_path.append(main_path+i)
    
    def get_flow_content(self):
        """read the xml file, and convert it to json format ,and add it to the flow list"""
        self.get_xml_files_path()
        for i in self.xml_files_path:
            f=open(i)
            xml_file=f.read() 
            namespaces={"urn:opendaylight:flow:inventory":None}
            flow_content_xmltodict=xmltodict.parse(xml_file, process_namespaces=True, namespaces=namespaces);
            self.flow_content.append(flow_content_xmltodict)
            f.close()
    
    def comple_flow(self,singe_flow_content,input_id,output_id,flow_id,openflow_sw,odl_flow_obj):
        singe_flow_content['flow']['match']['in-port']=input_id
        singe_flow_content['flow']['instructions']['instruction']['apply-actions']['action']['output-action']['output-node-connector']=output_id
        singe_flow_content['flow']['id']=flow_id
        odl_flow_obj.add(openflow_sw,singe_flow_content,flow_id)
    
    def delete_flow(self,openflow_sw,flow_id,odl_flow_obj):
        odl_flow_obj.delete(openflow_sw,flow_id)




class OpendaylightError(Exception):
        """Opendaylight Exception Class"""
        pass
