  

# KCC meraki migration

Meraki network migration from KCC to Kentuckiana Curb Company.

## Description

KCC is a meraki customer organization that recently signed on to be managed by CBTS. We had a single location for this company under the name - Kentuckiana Curb Company organization. We needed to migrate the networks from KCC into Kentuckiana Curb Company, where we kept the network names the way they are currently just an uplift and place into our organization. Along with the networks, all the devices and their configuration needs to be migrated.  

## Getting Started
1. backup all the configuration
2. create new network from old network
3. update new networks from old network backups

### Executing program

* create_templates.py - to create the templates - which are backups of old network

* meraki_provisioing/meraki_create_network.py - to create new network and update the config from the backups

