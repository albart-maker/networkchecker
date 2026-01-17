import customtkinter as ctk
import threading
from scanner import NetworkScanner  # Importing your existing engine

# Configuration for the modern look
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NetworkMapperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Setup the Window
        self.title("HomeGuard Network Mapper")
        self.geometry("900x600")
        
        # Initialize the scanner engine
        self.scanner = NetworkScanner()

        # 2. Define the Layout (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- LEFT SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🛡️ HomeGuard", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.scan_button = ctk.CTkButton(self.sidebar, text="Start Scan", command=self.start_scan_thread)
        self.scan_button.grid(row=1, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Ready", text_color="gray")
        self.status_label.grid(row=2, column=0, padx=20, pady=10)

        # --- TOP STATS BAR ---
        self.stats_frame = ctk.CTkFrame(self, height=60, fg_color="transparent")
        self.stats_frame.grid(row=0, column=1, sticky="ew", padx=20, pady=10)
        
        self.total_devices_label = ctk.CTkLabel(self.stats_frame, text="Devices Found: 0", font=("Arial", 16))
        self.total_devices_label.pack(side="left", padx=20)

        # --- MAIN LIST AREA (Scrollable) ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Network Devices")
        self.scrollable_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        
        # Configure columns for the list headers
        self.scrollable_frame.grid_columnconfigure(0, weight=1) # IP
        self.scrollable_frame.grid_columnconfigure(1, weight=2) # Name
        self.scrollable_frame.grid_columnconfigure(2, weight=2) # Vendor
        self.scrollable_frame.grid_columnconfigure(3, weight=1) # MAC

    def start_scan_thread(self):
        """Runs the scan in a background thread so the GUI doesn't freeze."""
        self.scan_button.configure(state="disabled", text="Scanning...")
        self.status_label.configure(text="Status: Scanning...", text_color="orange")
        
        # Start the thread
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        """The actual heavy lifting."""
        try:
            results = self.scanner.scan()
            # Once done, update GUI (must be done on main thread usually, but CTK handles simple calls well)
            self.after(0, self.update_ui, results)
        except Exception as e:
            print(f"Error: {e}")
            self.after(0, self.reset_ui_error)

    def update_ui(self, devices):
        """Clears the list and adds new items."""
        
        # 1. Clear previous items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 2. Headers (Re-add them)
        headers = ["IP Address", "Hostname", "Vendor", "MAC Address"]
        for i, h in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=h, text_color="cyan", font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, sticky="w", padx=10, pady=5)

        # 3. Populate List
        row_idx = 1
        for dev in devices:
            # Color logic
            color = "white"
            if dev['is_suspicious']: color = "#ff5555" # Red
            elif "Private" in dev['vendor']: color = "#ffb86c" # Orange
            
            # Create labels for each column
            ctk.CTkLabel(self.scrollable_frame, text=dev['ip'], text_color=color).grid(row=row_idx, column=0, sticky="w", padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=dev['hostname'], text_color=color).grid(row=row_idx, column=1, sticky="w", padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=dev['vendor'], text_color=color).grid(row=row_idx, column=2, sticky="w", padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=dev['mac'], font=("Consolas", 11), text_color="gray").grid(row=row_idx, column=3, sticky="w", padx=10)
            
            row_idx += 1

        # 4. Update Stats and Button
        self.total_devices_label.configure(text=f"Devices Found: {len(devices)}")
        self.scan_button.configure(state="normal", text="Start Scan")
        self.status_label.configure(text="Status: Idle", text_color="gray")

    def reset_ui_error(self):
        self.status_label.configure(text="Status: Error", text_color="red")
        self.scan_button.configure(state="normal", text="Start Scan")

if __name__ == "__main__":
    app = NetworkMapperApp()
    app.mainloop()