# CutMyRoots

![CutMyRoots Banner](https://i.imgur.com/TiJB3ha.png)

A Python tool for automatic IP rotation using Tor network.

## Description

CutMyRoots is a command-line tool that automatically rotates your IP address using the Tor network. It provides a simple interface to:
- Rotate IP addresses at specified intervals
- Check connection speed through Tor
- Save IP history
- Monitor Tor connection status

## Requirements

- Python 3.x
- Tor
- torify
- requests
- pysocks

## Installation

1. Install Tor:
```bash
sudo apt update
sudo apt install tor
```

2. Install Python dependencies:
```bash
pip install requests pysocks
```

3. Make sure torify is available:
```bash
sudo apt install torify
```

## Usage

Run the script:
```bash
python3 cutmyroots.py
```

### Menu Options

1. **Start IP rotation**
   - Set the delay between IP changes (in seconds)
   - Choose whether to save IP history
   - Press Ctrl+C to stop rotation

2. **Check connection speed**
   - Tests the current connection speed through Tor

3. **View IP history**
   - Shows all previously used IPs (if history was saved)

4. **Exit**
   - Closes the program

## Features

- Automatic IP rotation through Tor network
- Connection speed testing
- IP history logging
- Tor connection verification
- Clean and simple interface

## Security Note

This tool requires sudo privileges to:
- Install Tor
- Restart Tor service
- Clear Tor cache
- Force new Tor identities

## Author

Created by Br3noAraujo

## License

This project is open source and available under the MIT License. 
