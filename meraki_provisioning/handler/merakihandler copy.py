import meraki
import time
import json

class MerakiHandler:
    """
    A class to handle interactions with the Meraki Dashboard API using a specified API key.

    Args:
        api_key (str): The Meraki Dashboard API key used to authenticate requests.

    Attributes:
        dashboard (meraki.DashboardAPI): An instance of the Meraki DashboardAPI class.

    Example:
        To create an instance of MerakiHandler:

        handler = MerakiHandler(api_key="your_api_key_here")
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.log_path = '/Users/moshfequr.rahman/Documents/AutoProjects/meraki/KCC/meraki_provisioning/data/logs/'
        dashboard = meraki.DashboardAPI(api_key=self.api_key, print_console=False, output_log=True, log_path = self.log_path)
        self.dashboard = dashboard
        
        

class MerakiTestClass(MerakiHandler):
    """This is a test class to test the MerakiHandler class. It inherits from MerakiHandler.
    Call this class to test the MerakiHandler class.
    Example:
        api_key = os.getenv('MERAKI_API_KEY')
        meraki = MerakiTestClass(api_key)
        orgs = meraki.test_list_orgs()
    """
    def __init__(self, dashboard):
        super().__init__(dashboard)
    
    
    def test_list_orgs(self) -> None:
        """Test Method to list all organizations the user has access to."""
        orgs = self.dashboard.organizations.getOrganizations()
        return (f'The current amount of Orgs you have access too: {len(orgs)}')
    
    def test_list_org_networks(self, org_id) -> None:
        """Test Method to list all networks in an organization."""
        networks = self.dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
        return (f'The current amount of Networks in this Org: {len(networks)}')


class MerakiCreateOrganization(MerakiHandler):
    def __init__(self, dashboard):
        super().__init__(dashboard)
    
    
    def create_golden_organization(self, new_organization_name):
        organizations = self.dashboard.organizations.getOrganizations()

        golden_org = next((organization for organization in organizations if organization['name'] == "Golden Org"), None)

        if golden_org == None:
            return "Error: Golden Org not found!"

        check_new_org_exists = next((True for organization in organizations if organization['name'] == new_organization_name), False)

        if check_new_org_exists:
            return "Error: {} already exists.".format(new_organization_name)


        organization_id = golden_org['id']
        name = new_organization_name
        response = self.dashboard.organizations.cloneOrganization(organization_id, name)
        
        if response:
            print("Successfully created organization: {}".format(response['name']))
            return response
        else:
            return "Error: Failed to create organization {}".format(new_organization_name)

class MerakiCreateGoldenNetwork(MerakiHandler):
    def __init__(self, dashboard, new_organization):
        super().__init__(dashboard)
        self.new_organization = new_organization
        self.template_path = '/Users/moshfequr.rahman/Documents/AutoProjects/meraki/KCC/meraki_provisioning/templates/'
    
    
    def create_new_network_kcc(self, name, crm_number, timeZone='US/Eastern', notes='Additional description of the network'):
        try:
            orgs = self.dashboard.organizations.getOrganizations()
            cloned_org = [org for org in orgs if org['name'] == self.new_organization]

            if len(cloned_org) == 1:
                cloned_org = cloned_org[0]
            else:
                return "Error: organization {} not found!".format(self.new_organization)

            organization_id = cloned_org['id']
            networks = self.dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')
            check_new_network_exists = next((True for network in networks if network['name'] == name), False)

            if check_new_network_exists:
                return "Error: Network {} already exists!".format(name)
            crm = 'CRM:{}'.format(crm_number)
            print(crm)
            new_network = self.dashboard.organizations.createOrganizationNetwork(organization_id, name,
            tags=[str(crm)], 
            timeZone=timeZone, 
            notes=notes,
            productTypes= ['appliance','camera','cellularGateway','sensor','switch','wireless'])
            print("Successfully created golden network: {}".format(new_network['name']))
            return new_network
        except Exception as error:
            print("Error occurred while creating golden network: {}".format(error))
            return

    def get_network_kcc(self, name):
        try:
            orgs = self.dashboard.organizations.getOrganizations()
            cloned_org = [org for org in orgs if org['name'] == self.new_organization]

            if len(cloned_org) == 1:
                cloned_org = cloned_org[0]
            else:
                return "Error: organization {} not found!".format(self.new_organization)

            organization_id = cloned_org['id']
            networks = self.dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')
            if name == 'ALL':
                return [network['name'] for network in networks]
            check_new_network_exists = next((network for network in networks if network['name'] == name), False)

            if not check_new_network_exists:
                return "Error: Network {} already exists!".format(name)
            return check_new_network_exists
        except Exception as error:
            print("Error occurred while creating golden network: {}".format(error))
            return

    def clone_golden_network(self, name, crm_number, golden_network_name):
        try:
            orgs = self.dashboard.organizations.getOrganizations()
            cloned_org = [org for org in orgs if org['name'] == self.new_organization]

            if len(cloned_org) == 1:
                cloned_org = cloned_org[0]
            else:
                return "Error: organization {} not found!".format(self.new_organization)

            organization_id = cloned_org['id']
            networks = self.dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')
            check_new_network_exists = next((True for network in networks if network['name'] == name), False)

            if check_new_network_exists:
                return "Error: Network {} already exists!".format(name)

            check_golden_network_exists = next((network for network in networks if network['name'] == golden_network_name), None)

            if check_golden_network_exists is None:
                return "Error: Golden Network {} not found!".format(golden_network_name)

            crm = "CRM: {}".format(str(crm_number))
            print(crm)
            new_network = self.dashboard.organizations.createOrganizationNetwork(organization_id, name,
            tags=[crm], 
            timeZone='US/Eastern', 
            notes='Additional description of the network',
            copyFromNetworkId=check_golden_network_exists['id'],
            productTypes= ['appliance',
                          'camera',
                          'cellularGateway',
                          'sensor',
                          'switch',
                          'wireless'])
            print("Successfully created network: {}".format(new_network['name']))
            return new_network
        except Exception as error:
            print("Error occurred while creating network: {}".format(error))
            return
    
    # 1. network_setting -> General
    def update_network_settings(self, new_network):
        try:
            response = self.dashboard.networks.updateNetworkSettings(
                new_network['id'], 
                localStatusPageEnabled=False, 
                remoteStatusPageEnabled=False, 
                localStatusPage={'authentication': {'enabled': True, 'password': 'SDandM1!'}}, 
                securePort={'enabled': False})
            # print(response)

            response = self.dashboard.networks.updateNetworkFirmwareUpgrades(new_network['id'], upgradeWindow={'dayOfWeek': 'sun', 'hourOfDay': '2:00'})
            
            response = self.dashboard.networks.updateNetworkTrafficAnalysis(new_network['id'], 
                mode='detailed', 
                customPieChartItems=[])
            # print(response)


            # 1. network_setting -> Alerts -- Webhooks
            response = self.dashboard.networks.createNetworkWebhooksHttpServer(
                new_network['id'], name='CBTS-UAT-Listener-1', url='https://cbtscsmuat.service-now.com/api/global/em/meraki_event?source=merakiWebhook&service=NaaS', 
                sharedSecret='!29$Mda@_#)', 
                payloadTemplate={'payloadTemplateId': 'wpt_00001', 'name': 'Meraki (included)'}
            )
            # print(response)

            response = self.dashboard.networks.createNetworkWebhooksHttpServer(
                new_network['id'], name='CBTS-Listener-1', url='https://cbts.service-now.com/api/global/em/meraki_event?source=merakiWebhook&service=NaaS', 
                sharedSecret='!29$Mda@_#)', 
                payloadTemplate={'payloadTemplateId': 'wpt_00001', 'name': 'Meraki (included)'}
            )
            # print(response)

            time.sleep(3)
            webhooks = self.dashboard.networks.getNetworkWebhooksHttpServers(new_network['id'])

            cbts_listener = next(( webhook for webhook in webhooks if webhook['name'] == 'CBTS-Listener-1'), None)
            cbts_listener_uat = next(( webhook for webhook in webhooks if webhook['name'] == 'CBTS-UAT-Listener-1'), None)

            with open(self.template_path+'alerts.json', 'r') as alert_file:
                content = alert_file.read()
                content = content.replace('aHR0cHM6Ly9jYnRzY3NtdWF0LnNlcnZpY2Utbm93LmNvbS9hcGkvZ2xvYmFsL2VtL21lcmFraV9ldmVudD9zb3VyY2U9bWVyYWtpV2ViaG9vayZzZXJ2aWNlPU5hYVM=', cbts_listener['id'])
                content = content.replace('aHR0cHM6Ly9jYnRzLnNlcnZpY2Utbm93LmNvbS9hcGkvZ2xvYmFsL2VtL21lcmFraV9ldmVudD9zb3VyY2U9bWVyYWtpV2ViaG9vayZzZXJ2aWNlPU5hYVM=', cbts_listener_uat['id'])
                alert_settings = json.loads(content)

            response = self.dashboard.networks.updateNetworkAlertsSettings(new_network['id'], 
                defaultDestinations={'emails': [], 'allAdmins': True, 'snmp': False, 'httpServerIds': [cbts_listener_uat['id'], cbts_listener['id']]}, 
                alerts=alert_settings['alerts']
            )
            # print(response)

            return "Successfully updated network setting"
        except Exception as error:
            print("Error occurred while updating network settings: {}".format(error))
            self.delete_new_network(new_network)


    # 2. Secuirty & SD-WAN --> Addressing & Vlans and DHCP
    def create_vlans(self, new_network):
        try:
            response = self.dashboard.appliance.updateNetworkApplianceVlansSettings(new_network['id'], vlansEnabled=True)
            # print(response)

            with open(self.template_path+'vlans.json', 'r') as vlans_file:
                vlans_data = json.load(vlans_file)

            for vlan in vlans_data:
                vlan.pop('networkId')
                response = self.dashboard.appliance.createNetworkApplianceVlan(new_network['id'], **vlan)
                    # print(response)

            return "Successfully created vlans"
        except Exception as error:
            print("Error occurred while creating vlans: {}".format(error))
            self.delete_new_network(new_network)



    # 2. Secuirty & SD-WAN --> Firewall
    def update_security_firewall(self, new_network):
        try:
            response = self.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(new_network['id'], 
                rules=[{'comment': 'Deny Guest to RFC1918', 'policy': 'deny', 'protocol': 'any', 'srcPort': 'Any', 'srcCidr': 'VLAN(1000).*', 'destPort': 'Any', 'destCidr': 'VLAN(99).*,VLAN(100).*,VLAN(128).*', 'syslogEnabled': False}]
            )
            # print(response)

            # 2. Secuirty & SD-WAN --> SD-Wan & traffic shaping 
            # ----> no need
            return "Successfully updated security firewall"
        except Exception as error:
            print("Error occurred while updating security firewall: {}".format(error))
            self.delete_new_network(new_network)


    # 3. Switching -> Switch Setting
    def update_switch_setting(self, new_network):
        try:
            response = self.dashboard.switch.updateNetworkSwitchSettings(new_network['id'], vlan = 128)
            # print(response)

            response = self.dashboard.switch.createNetworkSwitchQosRule(new_network['id'], vlan=100, dscp = 46, protocol = 'ANY')
            # print(response)
            return "Successfully updated switch setting"
        except Exception as error:
            print("Error occurred while updating switch setting: {}".format(error))
            self.delete_new_network(new_network)



    # 4. Wirelsess -> SSIDs
    def create_wireless_ssid(self, new_network):
        try: 
            with open('/Users/moshfequr.rahman/Documents/AutoProjects/meraki/KCC/templates_tooele/Tooele_ssids.json', 'r') as ssids_file:
                ssids_data = json.load(ssids_file)

            for ssid in ssids_data:
                response = self.dashboard.wireless.updateNetworkWirelessSsid(new_network['id'], **ssid)
                # print(response)

            # number = 1
            # with open(self.template_path+'splace_welcomemessage.json', 'r') as splace_welcomemessage_file:
            #     welcomemessage = json.load(splace_welcomemessage_file)
            # response = self.dashboard.wireless.updateNetworkWirelessSsidSplashSettings(new_network['id'], number, splashLogo = {'extension': 'jpg', 'md5': 'c0f35e6ccf6e51f7a2384c7f1f90c946'}, welcomeMessage=welcomemessage)
            # print(response)
            return "Successfully created wireless ssid"
        except Exception as error:
            print("Error occurred while creating wireless ssid: {}".format(error))
            self.delete_new_network(new_network)


    # 5. Sensors - Alert Profiles
    def create_sensor_alertprofiles(self, new_network):
        try:
            webhooks = self.dashboard.networks.getNetworkWebhooksHttpServers(new_network['id'])
            cbts_listener = next(( webhook for webhook in webhooks if webhook['name'] == 'CBTS-Listener-1'), None)
            cbts_listener_uat = next(( webhook for webhook in webhooks if webhook['name'] == 'CBTS-UAT-Listener-1'), None)

            with open(self.template_path+'alert_profile.json', 'r') as alert_profile_file:
                content = alert_profile_file.read()
                alert_profile = json.loads(content)

            response = self.dashboard.sensor.createNetworkSensorAlertsProfile(new_network['id'],
                name= 'Environmental Alerts', conditions=alert_profile['conditions'],
                recipients = {'emails': [],
                            'httpServerIds': [cbts_listener_uat['id'], cbts_listener['id']],
                            'smsNumbers': []})
            # print(response)
            return "Successfully created sensor alertprofile"
        except Exception as error:
            print("Error occurred while creating sensor alertprofile: {}".format(error))
            self.delete_new_network(new_network)


    def create_group_policies(self, new_network):
        try:
            with open('/Users/moshfequr.rahman/Documents/AutoProjects/meraki/KCC/templates_tooele/Tooele_grouppolices.json', 'r') as alert_profile_file:
                content = alert_profile_file.read()
                group_policies = json.loads(content)
            for group_policy in group_policies:
                response = self.dashboard.networks.createNetworkGroupPolicy(new_network['id'], **group_policy)
                # print(response)
            return "Successfully created group_policies"
        except Exception as error:
            print("Error occurred while creating group_policies: {}".format(error))
            # self.delete_new_network(new_network)

    def update_switch_port(self, serial, port):
        try:
            print("\tUpdating switch port {} for serial no. {}".format(port['portId'], serial))
            response = self.dashboard.switch.updateDeviceSwitchPort(serial, **port)
            print(response)
            return "Successfully update_switch_port"
        except Exception as error:
            print("Error occurred while update_switch_ports: {}".format(error))
            # self.delete_new_network(new_network)

    def get_devices(self, new_network):
        try:
            devices = self.dashboard.networks.getNetworkDevices(new_network['id'])
            return devices
        except Exception as error:
            print("Error occurred getting devices: {}".format(error))
            # self.delete_new_network(new_network)

    def update_device(self, serial, device):
        try:
            print("Updating: serial {}, name {}".format(serial, device['name']))
            response = self.dashboard.devices.updateDevice(serial, **device)
            return response
        except Exception as error:
            print("Error occurred update_devices: {}".format(error))

    # delete network
    def delete_new_network(self, new_network):
        print("Deleting new network: {}".format(new_network['name']))
        # response = self.dashboard.networks.deleteNetwork(new_network['id'])
        # return response
