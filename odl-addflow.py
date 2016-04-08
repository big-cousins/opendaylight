import httplib2
import xml

#add-flow to make that two host can not ping each other 
baseUrl='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:$$$/table/0/flow/1'
headers = {
    'Content-type': 'application/xml',
    'Accept': 'application/xml',
}

h=httplib2.Http(".cache")
h.add_credentials('admin','admin')   #认证
body="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <strict>false</strict>
    <instructions>
       <instruction>
         <order>0</order>
         <apply-actions>
            <action>
                 <order>0</order>
                 <drop-action/>
           </action>
        </apply-actions>
      </instruction>
    </instructions>
    <table_id>0</table_id>
    <id>2</id>
    <cookie_mask>255</cookie_mask>
    <installHw>false</installHw>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>2048</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-source>10.0.0.14/32</ipv4-source>
        <ipv4-destination>10.0.0.15/32</ipv4-destination>
        <ip-match>
           <ip-protocol>1</ip-protocol>
        </ip-match>
        <in-port>1</in-port>
    </match>
    <hard-timeout>60</hard-timeout>
    <cookie>1</cookie>
    <idle-timeout>34</idle-timeout>
    <flow-name>lihao</flow-name>
    <priority>105</priority>
    <barrier>false</barrier>
</flow>
"""
resp,content=h.request(baseUrl,"PUT",body,headers)
