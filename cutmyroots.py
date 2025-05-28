#!/bin/python3
#! coding: utf-8

"""CODED BY Br3noAraujo"""

import os
import time
import subprocess
import requests
import json
from datetime import datetime

#color_list
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'

def banner():
    print(f"""{GREEN}
 _____       _  ___  ___     ______            _       
/  __ \\     | | |  \\/  |     | ___ \\          | |      
| /  \\/_   _| |_| .  . |_   _| |_/ /___   ___ | |_ ___ 
| |   | | | | __| |\\/| | | | |    // _ \\ / _ \\| __/ __|
| \\__/\\ |_| | |_| |  | | |_| | |\\ \\ (_) | (_) | |_\\__ \\
 \\____/\\__,_|\\__\\_|  |_/\\__, \\_| \\_\\___/ \\___/ \\__|___/  {RED}By Br3noAraujo{GREEN}
                         __/ |                         
                        |___/                          {RESET}\n""")

def check_tor():
    try:
        result = subprocess.run(['tor', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_tor():
    try:
        print(f"{BLUE}Installing Tor...{RESET}")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], check=True)
        print(f"{GREEN}Tor has been successfully installed.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error during installation: {e}{RESET}")
        return False
    return True

def get_public_ip_through_tor():
    try:
        result = subprocess.run(['torify', 'curl', '-s', 'https://api.ipify.org?format=json'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            ip_info = json.loads(result.stdout)
            return ip_info['ip']
        return None
    except Exception as e:
        print(f"{RED}Error getting public IP through Tor: {e}{RESET}")
        return None

def force_new_tor_identity():
    """Force Tor to create a new identity more aggressively"""
    try:
        subprocess.run(['sudo', 'service', 'tor', 'stop'], check=True)
        time.sleep(2)
        subprocess.run(['sudo', 'rm', '-rf', '/var/lib/tor/data/*'], check=True)
        subprocess.run(['sudo', 'service', 'tor', 'start'], check=True)
        time.sleep(5)
        subprocess.run(['sudo', 'killall', '-HUP', 'tor'], check=True)
        time.sleep(2)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error forcing new identity: {e}{RESET}")
        return False

def check_tor_connection():
    """Check if Tor is working correctly"""
    try:
        result = subprocess.run(['torify', 'curl', '-s', 'https://check.torproject.org/'], 
                              capture_output=True, text=True)
        return 'Congratulations' in result.stdout
    except:
        return False

def check_connection_speed():
    """Check connection speed through Tor"""
    try:
        start_time = time.time()
        response = requests.get('https://api.ipify.org?format=json', 
                              proxies={'http': 'socks5h://127.0.0.1:9050',
                                     'https': 'socks5h://127.0.0.1:9050'})
        end_time = time.time()
        speed = end_time - start_time
        return speed
    except:
        return None

def save_ip_to_file(ip):
    """Save IP and additional information to a file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('tor_ips.txt', 'a') as f:
        f.write(f"{timestamp} - IP: {ip}\n")

def show_menu():
    """Display main menu"""
    print(f"\n{BLUE}=== Main Menu ==={RESET}")
    print(f"{GREEN}1. Start IP rotation")
    print(f"2. Check connection speed")
    print(f"3. View IP history")
    print(f"4. Exit{RESET}")
    return input(f"{YELLOW}Choose an option: {RESET}")

def main():
    if not check_tor():
        install_tor()
    
    banner()
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            delay = int(input(f'{BLUE}Enter delay in seconds: {RESET}'))
            save_history = input(f'{BLUE}Do you want to save IP history? (y/n): {RESET}').lower() == 'y'
            
            while True:
                try:
                    print(f"{BLUE}Restarting Tor...{RESET}")
                    
                    if not force_new_tor_identity():
                        print(f"{RED}Error forcing new Tor identity.{RESET}")
                        continue
                    
                    if not check_tor_connection():
                        print(f"{RED}Error: Tor is not working correctly.{RESET}")
                        continue
                    
                    time.sleep(3)
                    
                    public_ip = get_public_ip_through_tor()
                    if public_ip:
                        print(f"{GREEN}My public IP through Tor is: {public_ip}{RESET}")
                        if save_history:
                            save_ip_to_file(public_ip)
                    else:
                        print(f"{RED}Could not get public IP through Tor.{RESET}")
                    
                    time.sleep(delay)
                except KeyboardInterrupt:
                    print(f"\n{YELLOW}Operation interrupted by user.{RESET}")
                    break
                
        elif choice == '2':
            speed = check_connection_speed()
            if speed:
                print(f"{GREEN}Connection speed: {speed:.2f} seconds{RESET}")
            else:
                print(f"{RED}Could not check connection speed.{RESET}")
                
        elif choice == '3':
            try:
                with open('tor_ips.txt', 'r') as f:
                    print(f"\n{BLUE}=== IP History ==={RESET}")
                    print(f.read())
            except FileNotFoundError:
                print(f"{RED}No history found.{RESET}")
                
        elif choice == '4':
            print(f"{GREEN}Exiting...{RESET}")
            break
            
        else:
            print(f"{RED}Invalid option!{RESET}")

if __name__ == "__main__":
    main()

    
