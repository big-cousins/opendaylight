'''
Created on 2016-5-14

@author: jeremy
'''
from opendaylight import Opendaylight
from opendaylight import OpendaylightFlow
from opendaylight import OpendaylightFlowOperate
import time
from sys import stdout

def count_time(n):
    for i in range(0,n):
        stdout.write("\r%d" % i)
        stdout.flush()
        time.sleep(1)
    


odl_obj=Opendaylight()                                                             #create a Opendaylight object
odl_flow_obj=OpendaylightFlow(odl_obj)                           #create a OpendaylightFlow object
odl_flow_ope_obj=OpendaylightFlowOperate()                #create a OpendaylightFlowOperate object
odl_flow_ope_obj.openflow_sw=['openflow:1']
odl_flow_ope_obj.xml_files_name=['template_1.xml']
odl_flow_ope_obj.get_flow_id()
odl_flow_ope_obj.get_flow_content()
actions={'in_port':['7','1','2','3','4','5','6','8'],'out_port':['1','7','3','2','5','4','8','6']}
print "****************************************************************"
print "****************You are about to add some new flow*****************"
for i in range(0,8):
    odl_flow_ope_obj.comple_flow(odl_flow_ope_obj.flow_content[0],actions['in-port'][i],actions['out-port'][i],odl_flow_ope_obj.flow_id[i],odl_flow_ope_obj.openflow_sw[0],odl_flow_obj)

print "****************************************************************"
answer=raw_input("Now , Do you wanna delete all the flows? Please answer  Y or N  >>  ")
for i in range(0,8):
    odl_flow_ope_obj.delete_flow(odl_flow_ope_obj.openflow_sw[0], odl_flow_ope_obj.flow_id[i], odl_flow_obj)
