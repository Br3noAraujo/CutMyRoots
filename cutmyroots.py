#!/bin/python3
#! coding: utf-8

"""CODED BY Br3noAraujo"""

import os, time, subprocess, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry





#color_list
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
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
        # Check if 'tor' command exists by running 'tor --version'
        result = subprocess.run(['tor', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            #print("Tor is already installed.")
            return True
        else:
            #print("Tor is not installed.")
            return False
    except FileNotFoundError:
        # 'tor' command not found
        #print("Tor is not installed.")
        return False
def install_tor():
    try:
        print(f"{BLUE}Installing Tor...{RESET}")
        # Update package list and install Tor using apt (for Ubuntu/Debian systems)
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], check=True)
        print(f"{GREN}Tor has been installed successfully.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error during installation: {e}{RESET}")
        return False
    return True
def get_public_ip_through_tor():
    session = requests.Session()
    
    # Set the SOCKS5 proxy for Tor (default on localhost:9050 or 9150)
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    # Retry logic (optional)
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        # Send request through Tor to get the public IP
        response = session.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Raise exception for HTTP errors
        ip_info = response.json()
        return ip_info['ip']
    except requests.RequestException as e:
        print(f"{RED}Error fetching public IP through Tor: {e}{RESET}")
        return None


def main():
    if not check_tor():
            install_tor()
            
    banner()
    delay = int(input(f'{BLUE}INSERT DELAY IN SECONDS: {RESET}'))
            
    while True:
        
        os.system('sudo service tor restart')
        print(f"{BLUE}Restarting Tor...{RESET}")
        public_ip = get_public_ip_through_tor()
        if public_ip:
            print(f"{GREEN}My public IP through Tor is: {public_ip}{RESET}")
        else:
            print(f"{RED}Could not fetch public IP through Tor.{RESET}")
        time.sleep(delay)  # Check IP every minute
        
        
        



if __name__ == "__main__":
    main()

    