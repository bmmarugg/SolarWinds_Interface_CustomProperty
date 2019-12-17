import requests
from orionsdk import SwisClient
from pprint import pprint


requests.packages.urllib3.disable_warnings()

server = 'SERVER IP ADDRESS'
username = 'USERNAME'
password = 'PASSWORD'

swis = SwisClient(server, username, password)


def main():
    # Prompts user to select either adding the custom property or removing it from a single device or list of devices

    def single_device():
        # Defines filter for Cisco devices ONLY
        filter = swis.query("SELECT NodeID,Caption FROM Orion.Nodes WHERE vendor='Cisco'")

        for row in filter.items():
            device_list = row[1]
            for device in device_list:
                device_name = device['Caption']
                node_id = device['NodeID']
                pprint(f"Device: {device_name} | Node ID: {node_id}")
            print("\n")

        mode = input("""
        (1) Adding **CUSTOM PROPERTY** custom property to UP interfaces
        (2) Removing **CUSTOM PROPERTY** custom property from ALL interfaces
        """)

        if "adding" in mode.lower() or "1" in mode:
            node_choice = input("Enter the Node ID of the device(s) you need to edit separated by commas: ")
            # Allows user to define a single or multiple Node IDs to configure
            node_list = node_choice.split(",")

            for entry in node_list:
                node_choice = entry
                query = """
                        SELECT InterfaceID, Caption, Status, InterfaceAlias FROM Orion.NPM.Interfaces WHERE NodeID={}
                    """.format(node_choice)
                interfaces = swis.query(query)

                for interface in interfaces['results']:
                    int_status = interface['Status']
                    int_desc = interface['InterfaceAlias']

                    if int_status == 1 and "CONDITION 1" and "CONDITION 2" not in int_desc.lower():
                        # Filters on interfaces in the UP/UP state and with user-defined condition(s) in the description
                        int_id = interface['InterfaceID']
                        uri = \
                            f"swis:/**SERVER IP**:17778/Orion/Orion.Nodes/NodeID={node_choice}/Interfaces/" \
                            f"InterfaceID={int_id}/CustomProperties"
                        swis.update(uri, CUSTOM_PROPERTY=True)

                    else:
                        int_id = interface['InterfaceID']
                        int_desc = interface['InterfaceAlias']
                        uri = \
                            f"swis://**SERVER IP**:17778/Orion/Orion.Nodes/NodeID={node_choice}/Interfaces/" \
                            f"InterfaceID={int_id}/CustomProperties"
                        swis.update(uri, CUSTOM_PROPERTY=False)

        elif "removing" in mode.lower() or "2" in mode:
        # Removes the custom property from all interfaces on the node EXCEPT FOR some condition, which can be removed
            node_choice = input("Enter the Node ID of the device(s) you need to edit separated by commas: ")
            # Allows user to define a single or multiple Node IDs to configure
            node_list = node_choice.split(",")

            for entry in node_list:
                node_choice = entry
                query = """
                        SELECT InterfaceID, Caption, Status, InterfaceAlias FROM Orion.NPM.Interfaces WHERE NodeID={}
                        """.format(node_choice)
                interfaces = swis.query(query)

                for interface in interfaces['results']:
                    int_id = interface['InterfaceID']
                    int_desc = interface['InterfaceAlias']
                    int_status = interface['Status']

                    if "CONDITION 1" in int_desc.lower():
                        uri = \
                            f"swis://**SERVER IP**:17778/Orion/Orion.Nodes/NodeID={node_choice}/Interfaces/" \
                            f"InterfaceID={int_id}/CustomProperties"
                        swis.update(uri, CUSTOM_PROPERTY=True)

                    else:
                        uri = \
                            f"swis://**SERVER IP**:17778/Orion/Orion.Nodes/NodeID={node_choice}/Interfaces/" \
                            f"InterfaceID={int_id}/CustomProperties"
                        swis.update(uri, CUSTOM_PROPERTY=False)


    def inventory():
        filter = swis.query("SELECT NodeID,Caption FROM Orion.Nodes WHERE vendor='Cisco'")

        for row in filter.items():
            device_list = row[1]

            for device in device_list:
                print("Now working on configuring interfaces for: {}".format(device['Caption']))
                node_id = device['NodeID']
                device_name = device['Caption']
                query = """
                        SELECT InterfaceID, Caption, Status, InterfaceAlias FROM Orion.NPM.Interfaces WHERE NodeID={}
                        """.format(node_id)

                interfaces = swis.query(query)
                for interface in interfaces['results']:
                    int_status = interface['Status']
                    int_desc = interface['InterfaceAlias']

                    if int_status == 1 and "CONDITION 1" and "CONDITION 2" not in int_desc.lower():
                        int_id = interface['InterfaceID']
                        uri = \
                            f"swis://**SERVER IP**:17778/Orion/Orion.Nodes/NodeID={node_id}/Interfaces/" \
                            f"InterfaceID={int_id}/CustomProperties"
                        swis.update(uri, CUSTOM_PROPERTY=True)

                    else:
                        int_id = interface['InterfaceID']
                        int_desc = interface['InterfaceAlias']
                        uri = \
                            f"swis://**SERVER IP**:17778/Orion/Orion.Nodes/NodeID={node_id}/Interfaces/" \
                            f"InterfaceID={int_it}/CustomProperties"
                        swis.update(uri, CUSTOM_PROPERTY=False)

    user_choice = input(
        """Choose the following: \n
        (1) - Single Device
        (2) - Entire Cisco Inventory
        """)

    if "1" in user_choice or "single" in user_choice.lower():
        single_device()

    elif "2" in user_choice or "entire" in user_choice.lower() or "inventory" in user_choice.lower():
        inventory()


if __name__ == "__main__":
    main()
