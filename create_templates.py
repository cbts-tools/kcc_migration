import meraki, os, json
from pprint import pprint
from dotenv import load_dotenv
from pandas import pandas
from geopy.geocoders import Nominatim

load_dotenv(dotenv_path='../.env')

MERAKI_DASHBOARD_API_KEY=os.getenv("MERAKI_DASHBOARD_API_KEY")
geolocator = Nominatim(user_agent="fasdfasfdasfas")
org_name = 'Axcess Financial'
dashboard = meraki.DashboardAPI(MERAKI_DASHBOARD_API_KEY, suppress_logging=True)#, print_console=False, output_log=True, log_path = 'output/')



try:
    orgs = dashboard.organizations.getOrganizations()
except meraki.exceptions.APIError as e:
    print(e)
    exit()

geolocator = Nominatim(user_agent="fasdfasfdasf1111as")

country_list = []
org_id =''
for org in orgs:
    if 'KCC'.lower() == str(org['name']).lower():#Kentuckiana Curb Company
        print(org)
        print('Working on organization: {}'.format(org['name']))
        print('*'*100)
        break

orgs_networks = dashboard.organizations.getOrganizationNetworks(organizationId=org['id'], total_pages='all')
group_policies = []
ssids = []
wirelessSettings = []
wirelessSsidTrafficShapingRules = []
switch_stacks_list = []
switchport_agg = []
for network in orgs_networks:
    if 'switch' in network['productTypes']:
        switch_stacks = dashboard.switch.getNetworkSwitchStacks(network['id'])

        print(switch_stacks)
        if switch_stacks != []:
            switch_stacks_list.append({'network': network, 'switch_stack': switch_stacks})
        for switch_stack in switch_stacks:
            switch_stack_id = switch_stack['id']
            response = dashboard.switch.getNetworkSwitchStackRoutingInterfaces(network['id'], switch_stack_id)
            print(response)
            response = dashboard.switch.getNetworkSwitchStackRoutingStaticRoutes(network['id'], switch_stack_id)
            print(response)


        response = dashboard.switch.getNetworkSwitchLinkAggregations(network['id'])
        print(response)
        if response != []:
            switchport_agg.append({'network': network, 'aggregations': response})

   


    # response = dashboard.networks.getNetworkGroupPolicies(network['id'])
    # group_policies.append({network['name']: response})

    # if 'wireless' in network['productTypes']:
    #     ssids_config = dashboard.wireless.getNetworkWirelessSsids(network['id'])
    #     ssids.append({network['name']: ssids_config})

    #     for ssid in ssids_config:
    #         if 'Unconfigured' not in ssid['name']:
    #             response = dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(network['id'], ssid['number'])
    #             rule = {}
    #             rule['network'] = network['name']
    #             rule['ssid'] =  ssid
    #             rule['rule'] = response
    #             print(network['name'], ssid['name'], response)
    #             wirelessSsidTrafficShapingRules.append(rule)

#         response = dashboard.wireless.getNetworkWirelessSettings(network['id'])
#         wirelessSettings.append({network['name']: response})

        # response = dashboard.switch.getNetworkSwitchAccessControlLists(network['id'])

        # print(response)
        # with open("templates/"+network['name']+"_network.json", "w") as file:
        #     json.dump(network, file, indent=4)

        # response = dashboard.networks.getNetworkAlertsSettings(network['id'])
        # with open("templates/"+network['name']+"_alerts.json", "w") as file:
        #     json.dump(response, file, ensure_ascii=False, indent=4)

        # response = dashboard.networks.getNetworkGroupPolicies(network['id'])
        # with open("templates/"+network['name']+"_grouppolices.json", "w") as file:
        #     json.dump(response, file, ensure_ascii=False, indent=4)

        # group_policies.append({network['name']: response})




    devices = dashboard.networks.getNetworkDevices(network['id'])
    # with open("templates/"+network['name']+"_devices.json", "w") as file:
    #     json.dump(devices, file, ensure_ascii=False, indent=4)
    for device in devices:
        # print(device['model'], device['name'])

        if 'MS' in device['model']:
            response = dashboard.switch.getDeviceSwitchPorts(device['serial'])
            df = pandas.DataFrame(response)
            df.to_excel("templates/"+network['name']+'_'+device['name']+".xlsx", index=False)

                # with open("templates/"+network['name']+"_"+device['name']+"_switch.json", "w") as file:
                #     json.dump(response, file, ensure_ascii=False, indent=4)
        # if 'wireless' in network['productTypes']:
        #     response = dashboard.wireless.getNetworkWirelessSsids(network['id'])
        #     with open("templates/"+network['name']+"_ssids.json", "w") as file:
        #         json.dump(response, file, ensure_ascii=False, indent=4)

        #     response = dashboard.wireless.getNetworkWirelessSettings(network['id'])
        #     with open("templates/"+network['name']+"_wirelessSetting.json", "w") as file:
        #         json.dump(response, file, ensure_ascii=False, indent=4)

# with open("templates/KCC_networks.json", "w") as file:
#     json.dump(orgs_networks, file, ensure_ascii=False, indent=4)

# with open("templates/KCC_grouppolices.json", "w") as file:
#     json.dump(group_policies, file, ensure_ascii=False, indent=4)

# with open("templates/KCC_ssids.json", "w") as file:
#     json.dump(ssids, file, ensure_ascii=False, indent=4)

# with open("templates/KCC_wirelessSetting.json", "w") as file:
#     json.dump(wirelessSettings, file, ensure_ascii=False, indent=4)

# with open("templates/KCC_wirelessSsidTrafficShapingRules.json", "w") as file:
#     json.dump(wirelessSsidTrafficShapingRules, file, ensure_ascii=False, indent=4)


# with open("templates/KCC_switch_stacks.json", "w") as file:
#     json.dump(switch_stacks_list, file, ensure_ascii=False, indent=4)


# with open("templates/KCC_switch_ports_agg.json", "w") as file:
#     json.dump(switchport_agg, file, ensure_ascii=False, indent=4)


# with open("templates/KCC_wirelessSsidTrafficShapingRules.json", "r") as file:
#     rules = json.load(file)
# for rule in rules:
#     if rule['network'] == 'Grassland':
#         print(rule['network'], rule['ssid']['name'], rule['ssid']['number'], rule['rule'])


# with open("templates/KCC_grouppolices.json", "r") as file:
#     grps = json.load(file)
# for grp in grps:





# devices_list = []
# switches_list = []
# for network in orgs_networks:
#     devices = dashboard.networks.getNetworkDevices(network['id'])
#     devices_dict = {}
#     devices_dict['network'] = network
#     devices_dict['devices'] = devices
#     devices_list.append(devices_dict)
#     for device in devices:
#         if 'MS' in device['model']:
#             switchports_config_dict = {}
#             response = dashboard.switch.getDeviceSwitchPorts(device['serial'])
#             switchports_config_dict['network'] = network
#             switchports_config_dict['device'] = device
#             switchports_config_dict['switch_ports'] = response
#             switches_list.append(switchports_config_dict)



# with open("templates/KCC_devices.json", "w") as file:
#     json.dump(devices_list, file, ensure_ascii=False, indent=4)
# with open("templates/KCC_switches.json", "w") as file:
#     json.dump(switches_list, file, ensure_ascii=False, indent=4)





# with open("templates/KCC_devices.json", "r") as file:
#     devices = json.load(file)

# with open("templates/KCC_switches.json", "r") as file:
#     switch_ports_configs = json.load(file)


# grassland_devices = [d['devices'] for d in devices if d['network']['name'] == 'Grassland'][0]

# switches = [d['serial'] for d in grassland_devices if 'MS' in d['model']]


# switch_ports = [switch_ports_config['switch_ports'] for switch_ports_config in switch_ports_configs if switch_ports_config['device']['serial'] == 'Q2LP-UNFS-Z7ZS'][0]
# pprint(switch_ports)


# pprint(grassland_devices)














