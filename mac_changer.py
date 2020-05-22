#!/usr/bin/env python3

import subprocess
import argparse
import optparse
import re
import random


# ToDo: add to github so I don't lose this as I'm on a virtual machine


def get_mac(ethernet_interface):
    mac_ifconfig_results = subprocess.check_output(["ifconfig", ethernet_interface])
    # print(mac_ifconfig_results)
    mac_ifconfig_results = mac_ifconfig_results.decode('utf-8')
    # print(mac_ifconfig_results)
    returned_mac_re_obj = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_ifconfig_results)
    if returned_mac_re_obj:
        current_mac = returned_mac_re_obj.group()
        # print("Current MAC is: " + str(current_mac))
    else:
        # ToDo check if we are stripping lo out as we make the device array when we pull it from ifconfig
        print("Could not find any mac addressed in the results, such as an lo adapter")
    return current_mac


def get_arguments():
    # use these if we want the user to have a default option and not need to put something in.
    # will be used if I ever make the mac become a random generated one on eth0 as the default
    ethernet_interface_default = "eth0"
    new_mac_address_default = random_mac()

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change it's MAC address add things like wlan0 or eth0 after the option. like this: --interface wlan0 ")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address. like this: --mac 00:11:22:33:44:55 ")
    parser.add_option("-r", "--random", dest="random_mac_val", help="random new MAC address. use as the option random")
    parser.add_option("-a", "--all", dest="change_all_macs",
                      help="changes all macs except for 'lo'. use as: -a all or --all all")
    # options holds the values that are added by the user in the command line i.e. wlan0 or eth0 and 00:11:22:33:44:55)
    # arguments are what I added above i.e. --interface and --mac
    (options, arguments) = parser.parse_args()
    # print("What's different?")
    # print(options.new_mac)
    # print(options.interface)
    print("\n")
    print("Mac for eth0 is: " + get_mac("eth0"))
    print("\n")
    if not options.interface:
        # parser will show the warning then exit gracefully if we let this check if the user added any values
        # parser.error("Please specify an ethernet interface such as eth0 or lan0 alongside -i or --interface")
        ethernet_interface = input("Which ethernet interface would you like to change? ")
        if not ethernet_interface:
            ethernet_interface = ethernet_interface_default
            print("default assigned as if " + ethernet_interface)
    else:
        ethernet_interface = options.interface
        # print(type(ethernet_interface))
        # parser will show the warning then exit gracefully if we let this check if the user added any values
        # parser.error("Please specify an ethernet interface such as eth0 or lan0 alongside -i or --interface")

    if not options.new_mac:
        if options.random_mac_val == "random":
            new_mac_address = random_mac()
            print("You've been assigned a random mac.")
        elif not options.random_mac_val:
            new_mac_address = input(
                "What is the new MAC address would you like to change to? \n(You may skip this to be assigned a random MAC address) ")
            if not new_mac_address:
                new_mac_address = random_mac()
                print("random MAC assigned as " + new_mac_address_default)
    else:
        new_mac_address = options.new_mac
        # print(type(new_mac_address))

    if not options.change_all_macs:
        if options.change_all_macs == "all":
            change_all_macs = options.change_all_macs
        else:
            change_all_macs = "do_not_change_all"

    return new_mac_address, ethernet_interface, random_mac, change_all_macs


# print("="*20)
# print(ethernet_interface)
# print(new_mac_address)
# print("="*20)

# print("="*10 + "changed start" + "="*10)
# print(ethernet_interface)
# print(new_mac_address)
# print("="*10 + "changed end" + "="*10)

# subprocess.call(["ifconfig"], shell=True)

# print("="*10 + "fully changed now" + "="*10)
# print("Changing Mac address for " + ethernet_interface + " with a mac address of " + new_mac_address)
# print("="*10 + "fully changed now" + "="*10)


def change_mac(ethernet_interface, new_mac_address):
    # using a list to make input safe for suppresses called in a terminal
    subprocess.call(["ifconfig", ethernet_interface, "down"])
    # print("down")
    subprocess.call(["ifconfig", ethernet_interface, "hw", "ether", new_mac_address])
    # print("changed")
    subprocess.call(["ifconfig", ethernet_interface, "up"])
    # print("up")

    # print("Mac address " + new_mac_address + " for " + ethernet_interface + " changed.")


def random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    random_mac = ':'.join(map(lambda x: "%02x" % x, mac))
    # print(random_mac)
    return random_mac


'''
print("+" * 20)
new_mac_address = "11:22:33:44:55:66"
subprocess.call("ifconfig " + ethernet_interface + " down")
subprocess.call("ifconfig " + ethernet_interface + " hw ether " + new_mac_address)
subprocess.call("ifconfig " + ethernet_interface + " up")
subprocess.call("ifconfig", shell=True)
'''



def ifconfig_devices():
    devices = subprocess.check_output(["ls", "/sys/class/net"])
    devices = devices.decode('utf-8')
    devices = devices.strip()
    device_list = [i for i in devices.split("\n")]
    # for device in device_list:
    #    print(device)
    # ToDo perhaps strip 'lo' as it can't get a ether mac address so when we iterate over this list it will not get stuck
    # ToDo if it's ALWAYS the last one it's easy with -1 pop, or a search exactly for 'lo'
    # ToDo although, check if we already do a check for not being able to change when it comes back as none from Regex Mac search
    while True:
        try:
            device_list.remove('lo')
        except ValueError:
            break
    # for device in device_list:
    #    print(device)
    return device_list


def change_all_macs(device_list, changes_all_macs):
    if changes_all_macs == "do_not_change_all":
        return
    else:
        for device in device_list:
            old_mac = get_mac(device)
            change_mac(device, random_mac())
            new_mac = get_mac(device)
            print("Running Change All Macs...Changed " + device + " from " + old_mac + " to " + new_mac)
        print("Stopped Changing All Macs.")


def check_if_changed(Old_Mac):
    current_mac = get_mac("eth0")
    if current_mac != Old_Mac:
        print("Mac address was changed Successfully. From " + Old_Mac + " to " + current_mac)
    else:
        print("Mac was not changed, Perhaps try: ifconfig eth0 up in order to reset it.")

# use pythex as the rules for regex

print("+" * 10 + "All Ethernet Adapters" + "+" * 10)
subprocess.call("ifconfig", shell=True)
print("+" * 30)
print("\n")

Old_Mac = get_mac("eth0")
(new_mac_address, ethernet_interface, random_mac, changes_all_macs) = get_arguments()
change_mac(ethernet_interface, new_mac_address)

device_list = ifconfig_devices()
change_all_macs(device_list, changes_all_macs)

check_if_changed(Old_Mac)
# subprocess.call("ifconfig eth0", shell=True)

print("\n")
print("The NEW MAC address has been changed to: " + get_mac(ethernet_interface))
