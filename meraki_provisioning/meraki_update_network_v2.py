from dotenv import load_dotenv
import os
from pprint import pprint
import json

from handler.merakihandler import MerakiCreateGoldenNetwork



def main():
    load_dotenv(dotenv_path='../../.env')
    MERAKI_DASHBOARD_API_KEY=os.getenv("MERAKI_DASHBOARD_API_KEY")

    org_name = "Kentuckiana Curb Company"
    meraki = MerakiCreateGoldenNetwork(MERAKI_DASHBOARD_API_KEY, org_name)

    old_network_name = 'Maintenance'
    new_network_name = 'Kentuckian Curb Company - Grassland'
    new_network = meraki.get_network_kcc(new_network_name)

    if new_network['name'] == new_network_name:
        print("Working on new network: '{}'".format(new_network['name']))
    else:
        exit()



    devices = meraki.get_devices(new_network)
    # print(devices)

    print("{}: has {} devices".format(new_network['name'], len(devices)))
    with open("../templates_tooele/KCC_devices.json", "r") as file:
        all_old_devices = json.load(file)
    for o in all_old_devices:
        if o['network']['name'] == old_network_name:
            old_network_devices = o['devices']
            old_devices = o['devices']
            for device in old_devices:
                if device['serial'] == 'Q2EX-XQM7-4QLK':
                    if 'MR' not in device['model']:
                        serail = device['serial']
                        print()
                        # print(meraki.update_device(serail, device))

    
    # with open("../templates_tooele/KCC_switch_stacks.json", "r") as file:
    #     all_switch_stacks = json.load(file)

    # for switch_stacks in all_switch_stacks:
    #     if switch_stacks['network']['name'] == old_network_name:
    #         # pprint(switch_stacks['switch_stack'])
    #         switch_stack = switch_stacks['switch_stack'][0]

    #         pprint(meraki.createNetworkSwitchStack(new_network, switch_stack))

    

    # print('-'*100)
    # switches = [device for device in old_network_devices if 'MS' in device['model']]
    # pprint(switches)
    # with open("../templates_tooele/KCC_switches.json", "r") as file:
    #     all_switch_config = json.load(file)
    # for switch in switches:
    #     # pprint(switch)
    #     print('*'*100)
    #     serial = switch['serial']
    #     print("Working on switch: {} with serial no. {}".format(switch['name'], serial))

    #     switch_ports_config = next(switch_config['switch_ports'] for switch_config in all_switch_config if switch_config['network']['name'] == old_network_name and switch_config['device']['serial'] == serial)
    #     for port in switch_ports_config:
    #         # pprint(port)
    #         # print(serial)
    #         print(meraki.update_switch_port(serial, port))


    

    # with open("../templates_tooele/KCC_switch_ports_agg.json", "r") as file:
    #     switch_ports_aggs = json.load(file)

    # for switch_ports_agg in switch_ports_aggs:
    #     # pprint(switch_ports_agg)
    #     if switch_ports_agg['network']['name'] == old_network_name:
    #         switchPorts = switch_ports_agg['aggregations']
    #         for switchPort in switchPorts:
    #             # print(switchPort['switchPorts'])
    #             pprint(meraki.createNetworkSwitchLinkAggregation(new_network, switchPort['switchPorts']))



if __name__ == '__main__':
    main()