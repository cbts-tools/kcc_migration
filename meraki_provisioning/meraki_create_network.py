from dotenv import load_dotenv
import os
from pprint import pprint
import json

from handler.merakihandler import MerakiCreateGoldenNetwork



def main():
    load_dotenv(dotenv_path='../../.env')
    MERAKI_DASHBOARD_API_KEY=os.getenv("MERAKI_DASHBOARD_API_KEY")

    org_name = "Kentuckiana Curb Company"
    new_network_name = 'Grassland'
    meraki = MerakiCreateGoldenNetwork(MERAKI_DASHBOARD_API_KEY, org_name)

    with open('../templates_tooele/KCC_networks.json', 'r') as old_network_file:
        old_network_data = json.load(old_network_file)


    for old_network in old_network_data:
        if new_network_name == new_network_name:
            # pprint(old_network)
            productTypes = old_network['productTypes']
            timeZone = old_network['timeZone']
            print(old_network['notes'])
            name = 'Kentuckian Curb Company - '+new_network_name

            print(name)

            # crm_number = '8085629'
            # new_network = meraki.create_new_network_kcc(name, crm_number, timeZone)
            # if new_network is None or 'Error' in new_network:
            #     print(new_network)
            #     exit()

            # print(meraki.update_network_settings(new_network))
            



            # with open("../templates_tooele/KCC_grouppolices.json", "r") as file:
            #     grps = json.load(file)
            # for grp in grps:
            #     if new_network_name in grp:
            #         if grp[new_network_name] != []:
            #             print(meraki.create_group_policies(new_network, grp[new_network_name]))

            # with open("../templates_tooele/KCC_ssids.json", "r") as file:
            #     ssids = json.load(file)
            # for ssid in ssids:
            #     if new_network_name in ssid:
            #         print(meraki.create_wireless_ssid(new_network, ssid[new_network_name]))

        
    # new_network = meraki.get_network_kcc('Kentuckian Curb Company - Grassland')
    # pprint(new_network)
    # with open("../templates_tooele/KCC_wirelessSetting.json", "r") as file:
    #     wirelesssettings = json.load(file)


    # for setting in wirelesssettings:
    #     if 'Electron' in setting:
    #         print(setting['Electron'])

    #         pprint(meraki.updateNetworkWirelessSettings(new_network, setting['Electron']))


    # with open("../templates_tooele/KCC_wirelessSsidTrafficShapingRules.json", "r") as file:
    #     rules = json.load(file)
    # for rule in rules:
    #     if rule['network'] == 'Grassland':
    #         print(rule['network'], rule['ssid']['name'], rule['ssid']['number'], rule['rule'])
    #         pprint(meraki.updateNetworkWirelessSsidTrafficShapingRules(new_network, rule['ssid'], rule['rule']))



        # print(meraki.create_vlans(new_network))
        # print(meraki.update_security_firewall(new_network))
        # print(meraki.update_switch_setting(new_network))
        # print(meraki.create_sensor_alertprofiles(new_network))


    
    
    
if __name__ == '__main__':
    main()