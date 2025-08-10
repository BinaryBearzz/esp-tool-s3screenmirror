import socket
import struct
import time
from io import BytesIO
from PIL import Image
import mss
import tkinter as tk
from tkinter import ttk, messagebox

class ScreenStreamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32-streammirror capture v.1.0.0 by BinaryBearx")
        
        self.sct = mss.mss()
        self.monitors = self.sct.monitors
        
        self.streaming = False
        self.stream_job = None
        
        # UI Elements
        self.create_widgets()
        self.refresh_screens()
        
    def create_widgets(self):
        pad = {'padx': 5, 'pady': 5}
        
        # Monitor dropdown
        ttk.Label(self.root, text="Select Monitor:").grid(row=0, column=0, sticky='e', **pad)
        self.monitor_var = tk.StringVar()
        self.monitor_combo = ttk.Combobox(self.root, textvariable=self.monitor_var, state='readonly')
        self.monitor_combo.grid(row=0, column=1, sticky='we', **pad)
        
        # IP:Port input
        ttk.Label(self.root, text="ESP32 IP:Port").grid(row=1, column=0, sticky='e', **pad)
        self.ip_port_var = tk.StringVar(value="192.168.1.142:8888")
        self.ip_port_entry = ttk.Entry(self.root, textvariable=self.ip_port_var, width=20)
        self.ip_port_entry.grid(row=1, column=1, sticky='we', **pad)
        
        # JPEG quality slider    
        ttk.Label(self.root, text="JPEG Quality(%)").grid(row=2, column=0, sticky='e', **pad)
        self.quality_var = tk.IntVar(value=70)

        # Create the scale, but no variable binding (ttk.Scale always returns float)
        self.quality_slider = ttk.Scale(self.root, from_=10, to=100, orient='horizontal',
                                        command=self.quality_slider_changed)
        self.quality_slider.set(self.quality_var.get())
        self.quality_slider.grid(row=2, column=1, sticky='we', **pad)

        self.quality_label = ttk.Label(self.root, text=str(self.quality_var.get()))
        self.quality_label.grid(row=2, column=2, sticky='w', **pad)
    
        
        # Interval ms input
        ttk.Label(self.root, text="Interval (ms)").grid(row=3, column=0, sticky='e', **pad)
        self.interval_var = tk.StringVar(value="50")
        self.interval_entry = ttk.Entry(self.root, textvariable=self.interval_var, width=10)
        self.interval_entry.grid(row=3, column=1, sticky='w', **pad)

        # Width input
        ttk.Label(self.root, text="Width").grid(row=4, column=0, sticky='e', **pad)
        self.width_var = tk.StringVar(value="320")
        self.width_entry = ttk.Entry(self.root, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=4, column=1, sticky='w', **pad)

        # Height input
        ttk.Label(self.root, text="Height").grid(row=5, column=0, sticky='e', **pad)
        self.height_var = tk.StringVar(value="170")
        self.height_entry = ttk.Entry(self.root, textvariable=self.height_var, width=10)
        self.height_entry.grid(row=5, column=1, sticky='w', **pad)
        
        # Buttons
        self.refresh_button = ttk.Button(self.root, text="Refresh Screens", command=self.refresh_screens)
        self.refresh_button.grid(row=6, column=0, **pad)
        
        self.clear_button = ttk.Button(self.root, text="Clear Fields", command=self.clear_fields)
        self.clear_button.grid(row=6, column=1, **pad)
        
        self.stream_button = ttk.Button(self.root, text="Start Streaming", command=self.toggle_streaming)
        self.stream_button.grid(row=7, column=0, columnspan=3, sticky='we', **pad)
        
        # Configure column weights for responsive layout
        self.root.columnconfigure(1, weight=1)

    def quality_slider_changed(self, val):
        # val comes as a string float, convert and round it to int
        int_val = int(round(float(val)))
        # update IntVar and label text
        self.quality_var.set(int_val)
        self.quality_label.config(text=str(int_val))
        
    def refresh_screens(self):
        self.monitors = self.sct.monitors
        options = []
        for i, mon in enumerate(self.monitors):
            desc = f"Monitor {i} ({mon['left']},{mon['top']},{mon['width']}x{mon['height']})"
            options.append(desc)
        self.monitor_combo['values'] = options
        if options:
            self.monitor_combo.current(1 if len(options) > 1 else 0)
        else:
            self.monitor_combo.set('')
    
    def clear_fields(self):
        self.ip_port_var.set("")
        self.quality_var.set(70)
        self.interval_var.set("50")
        self.width_var.set("320")
        self.height_var.set("170")
        if self.monitor_combo['values']:
            self.monitor_combo.current(0)
    
    def capture_screen_jpeg(self, monitor_index, quality, target_width, target_height):
        try:
            monitor = self.monitors[monitor_index]
        except IndexError:
            return None
        img = self.sct.grab(monitor)
        im = Image.frombytes('RGB', img.size, img.rgb)
        im = im.resize((target_width, target_height), Image.LANCZOS)
        buf = BytesIO()
        im.save(buf, format='JPEG', quality=quality)
        return buf.getvalue()
    
    def send_frame(self, jpeg_bytes, ip, port):
        try:
            s = socket.socket()
            s.settimeout(1.0)
            s.connect((ip, port))
            s.sendall(struct.pack("<I", len(jpeg_bytes)))
            s.sendall(jpeg_bytes)
            s.shutdown(socket.SHUT_WR)
            s.close()
        except Exception as e:
            print(f"Error sending frame: {e}")
            return False
        return True
    
    def stream_loop(self):
        if not self.streaming:
            return
        
        ip_port_str = self.ip_port_var.get().strip()
        if ':' not in ip_port_str:
            messagebox.showerror("Invalid IP:Port", "Please enter IP and port as ip:port")
            self.toggle_streaming(stop=True)
            return
        ip, port_str = ip_port_str.split(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Invalid Port", "Port must be an integer")
            self.toggle_streaming(stop=True)
            return
        
        monitor_idx = self.monitor_combo.current()
        if monitor_idx < 0:
            messagebox.showerror("No Monitor Selected", "Please select a monitor")
            self.toggle_streaming(stop=True)
            return
        
        quality = self.quality_var.get()
        
        try:
            interval_ms = int(self.interval_var.get())
            if interval_ms < 10:
                interval_ms = 10
        except ValueError:
            messagebox.showerror("Invalid Interval", "Interval must be an integer (ms)")
            self.toggle_streaming(stop=True)
            return
        
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Dimensions", "Width and Height must be positive integers")
            self.toggle_streaming(stop=True)
            return
        
        jpeg_bytes = self.capture_screen_jpeg(monitor_idx, quality, width, height)
        if jpeg_bytes is None:
            messagebox.showerror("Capture Error", "Failed to capture screen")
            self.toggle_streaming(stop=True)
            return
        
        print(f"Sending frame size: {len(jpeg_bytes)} bytes to {ip}:{port}")
        success = self.send_frame(jpeg_bytes, ip, port)
        if not success:
            messagebox.showwarning("Send Failed", "Failed to send frame, stopping stream")
            self.toggle_streaming(stop=True)
            return
        
        self.stream_job = self.root.after(interval_ms, self.stream_loop)
    
    def toggle_streaming(self, stop=False):
        if stop or self.streaming:
            self.streaming = False
            if self.stream_job:
                self.root.after_cancel(self.stream_job)
                self.stream_job = None
            self.stream_button.config(text="Start Streaming")
            print("Streaming stopped.")
        else:
            self.streaming = True
            self.stream_button.config(text="Stop Streaming")
            print("Streaming started.")
            self.stream_loop()

def main():
    root = tk.Tk()
    app = ScreenStreamerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
