from scapy.all import ARP, Ether, srp, get_if_hwaddr, conf
from mac_vendor_lookup import MacLookup
import socket

class NetworkScanner:
    def __init__(self):
        # Initialize Vendor Database
        try:
            self.mac_lookup = MacLookup()
            self.mac_lookup.update_vendors()
        except Exception as e:
            print(f"Warning: Could not update MAC database. {e}")

    def get_local_ip(self):
        """Finds the local IP address of this computer."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to public DNS to find the active interface
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            # Fallback if offline
            return "192.168.2.101" 
        return ip

    def get_hostname(self, ip):
        """Tries to find the device name (e.g., 'iPhone-12')."""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown Name"

    def is_private_mac(self, mac):
        """Checks if the MAC address is randomized (Private Wi-Fi)."""
        if len(mac) > 1:
            # Check the second character: if it's 2, 6, A, or E, it's random.
            second_char = mac[1].lower()
            return second_char in ['2', '6', 'a', 'e']
        return False

    def scan(self, ip_range=None):
        """
        Scans the network using ARP requests.
        """
        # 1. Determine Network Range
        if not ip_range:
            local_ip = self.get_local_ip()
            # If your IP is 192.168.1.15, this makes it 192.168.1.1/24
            ip_range = f"{local_ip.rsplit('.', 1)[0]}.1/24"
        
        # Override: If your scan fails, UNCOMMENT the line below and put your real range:
        # ip_range = "192.168.1.1/24" 

        print(f"Scanning range: {ip_range}...")

        # 2. Build Packet
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        # 3. Send & Receive
        # timeout=4 and retry=2 helps find sleepy mobile devices
        result = srp(packet, timeout=4, retry=2, verbose=0)[0]

        devices = []
        
        # 4. Process Results
        for sent, received in result:
            mac = received.hwsrc
            ip = received.psrc
            
            # Identify Vendor
            try:
                vendor = self.mac_lookup.lookup(mac)
            except:
                if self.is_private_mac(mac):
                    vendor = "Private/Randomized Device"
                else:
                    vendor = "Unknown Vendor"

            # Identify Hostname
            hostname = self.get_hostname(ip)

            # Flag Suspicious Devices
            is_suspicious = True if vendor == "Unknown Vendor" else False

            devices.append({
                'ip': ip,
                'mac': mac,
                'vendor': vendor,
                'hostname': hostname,
                'is_suspicious': is_suspicious
            })

        # 5. MANUALLY ADD THE HOST COMPUTER (Yourself)
        # Because you can't "ping" yourself via ARP, we add this manually.
        try:
            my_ip = self.get_local_ip()
            my_mac = get_if_hwaddr(conf.iface)
            
            # Check if I am already in the list
            found_ips = [d['ip'] for d in devices]
            
            if my_ip not in found_ips:
                devices.append({
                    'ip': my_ip,
                    'mac': my_mac,
                    'vendor': "This Computer (Host)",
                    'hostname': socket.gethostname(),
                    'is_suspicious': False
                })
        except Exception as e:
            print(f"Could not add host: {e}")

        return devices