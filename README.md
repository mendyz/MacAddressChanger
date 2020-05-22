# MacAddressChanger
Linux mac address changer using primarily ifconfig allows for manual changes to any device.

Can pull all devices and loop through them creating random MAC addresses that adhere to the last 6 in ':' colon based mac address systems.

Allows for default of eth0 and a random MAC, but also allows for manually changing to any mac you want, including other systems using -'s.

Allows control from command line with option parameters as well. Using optparse, will change to ArgParse over time. -i, -m, -r, -a, 

-i --interface Interface to change it's MAC address add things like wlan0 or eth0 after the option. like this: --interface wlan0 "
-m --mac new MAC address. like this: --mac 00:11:22:33:44:55 
-r --random random new MAC address. use as the option like this: -r random
-a --all change_all_macs automatically, changes all macs except for 'lo' which it strips out as there is no ether mac address in it. use as: -a all or --all all

Written in Python 3. 

Will update optparse to argparse. 

Will update to quite and verbose modes. 

MACS are created using Join, Hex and lambda/map functions.

Matches MACs before and after via regex to ensure changes were made.

Uses subprocess calls with safe list comprehension, and check_output with and without shell visualizations.

ToDo: refactor, remove clunky console logs and print statements remnants from debugging.
ToDo: fix menu system so that it's easier to navigate when others use it
ToDO: continue removing things to functions so they are isolated tasks
ToDo: remove internal
ToDo: Create better Readme markdown, and more informed instructions
