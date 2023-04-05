# SP DCN Champions FY23 Bootcamp: Automation NDFC/NXOS

## What's in this repo?

The files in this repo were either used, or referenced, during the SP DCN Champions bootcamp, specifically:

1. The postman directory contains:
a. The Demo collection used to add a fabric to an NDFC instance using REST
b. A minimal ND (Nexus Dashboard) collection (enough to login)
c. A more complete NDFC (Nexus Dashboard Fabric Controller) collection.
2. The ndfc_ansible directory contains playbooks to add a switch to the fabric created in 1a above, and add a vrf+network to the fabric; attaching them to the switch.
3. The nxos_ansible directory contains an example Ansible inventory, and a playbook which uses the cisco.nxos.nxos_interfaces module to add a description to a couple interfaces.
4. The nxapi directory contains an example python script (sandbox.py) generated by the NX-OS Sandbox (present on all NX-OS switches).  It also contains a more involved python script that manages cookies and can be modified to send configurations and retrieve command output.  Below is what the script outputs:

```bash
(py311) % ./simple_request.py 
cookies refreshed by DUT
  old cookies {}
  new cookies <RequestsCookieJar[<Cookie nxapi_auth=dzqnf:Yo+Tt1AqYP8UIDukCy5pvIeBmn8= for 10.1.1.1/>]>
old cookies are fresh
hostname cvd-1311-leaf
old cookies are fresh
Interface Ethernet1/11
  state: up
  description: aaa
  eth_outrate1_bits: 280
(py311) % 
```


