# 🛡️ HomeGuard Network Mapper

A professional-grade **Layer 2 Network Scanner** built with Python. 

Unlike standard ICMP (Ping) scanners which are often blocked by firewalls, HomeGuard utilizes **ARP (Address Resolution Protocol)** broadcasting to map the physical network layer, ensuring 100% device discovery on local subnets.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Scapy](https://img.shields.io/badge/Networking-Scapy-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

## 🚀 Features

* **Layer 2 Discovery:** Uses raw ARP packets to bypass Windows/Linux firewalls.
* **Vendor Identification:** Resolves MAC addresses to manufacturers (Apple, Intel, etc.).
* **Privacy Detection:** Algorithms to detect **Randomized/Private MAC addresses** used by modern iOS/Android devices.
* **Hostname Resolution:** Performs reverse DNS lookups to find device names (e.g., `iPhone-12`, `Desktop-PC`).
* **GUI Dashboard:** Modern dark-mode interface built with CustomTkinter.
* **Standalone Executable:** Compiled to `.exe` for portable deployment.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/HomeGuard.git](https://github.com/YOUR_USERNAME/HomeGuard.git)
    cd HomeGuard
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Npcap (Windows Only):**
    * Download [Npcap](https://npcap.com/#download).
    * **Critical:** Check *"Install Npcap in WinPcap API-compatible Mode"* during installation.

## 💻 Usage

### Running the Source Code
Because this tool accesses the network card to send raw packets, it requires **Administrator/Root** privileges.

**Windows (PowerShell as Admin):**
```powershell
python gui.py
