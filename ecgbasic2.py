import sys
import os
import time
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import threading
import struct
import queue

class ECGRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("PythonECG - Simplified Visualization")
        self.root.geometry("1000x600")
        
        # Audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = None
        
        # ECG data
        self.ecg_data = []
        self.time_data = []
        self.is_tracing = False
        self.trace_thread = None
        self.data_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        
        # Setup plotting
        self.setup_plot()
        
    def setup_ui(self):
        # Create frame for control
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Single toggle button for tracing
        self.trace_btn = tk.Button(control_frame, text="Start Tracing", command=self.toggle_tracing)
        self.trace_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_plot(self):
        # Create matplotlib figure
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#ffe6e6')  # Light pink background
        self.fig.patch.set_facecolor('#ffe6e6')  # Light pink background
        
        self.line, = self.ax.plot([], [], 'k-', linewidth=1.5)  # Black line for ECG
        self.ax.grid(True, color='#ffcccc', linestyle='-', linewidth=0.5)  # Pale red grid
        
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('ECG Reading')
        
        # Show time in seconds at the bottom
        self.ax.set_xlim(0, 10)  # 10 seconds window initially
        self.ax.set_ylim(-32768, 32767)  # 16-bit audio range
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Setup animation
        self.update_plot()
        
    def update_plot(self):
        if not self.data_queue.empty():
            data_chunk = []
            # Get all available data from the queue
            while not self.data_queue.empty():
                data_chunk.extend(self.data_queue.get())
            
            # Update plot data
            self.ecg_data.extend(data_chunk)
            
            # Keep only the last 10 seconds of data
            max_points = 10 * self.RATE
            if len(self.ecg_data) > max_points:
                self.ecg_data = self.ecg_data[-max_points:]
            
            # Update time data
            self.time_data = np.linspace(0, len(self.ecg_data) / self.RATE, len(self.ecg_data))
            
            # Update plot
            self.line.set_data(self.time_data, self.ecg_data)
            self.ax.set_xlim(max(0, self.time_data[-1] - 10), max(10, self.time_data[-1]))
            self.canvas.draw()
        
        # Schedule the next update
        self.root.after(50, self.update_plot)  # Update every 50 ms
    
    def toggle_tracing(self):
        if self.is_tracing:
            self.stop_tracing()
        else:
            self.start_tracing()
    
    def start_tracing(self):
        if self.is_tracing:
            return
        
        self.trace_btn.config(text="Stop Tracing")
        self.status_var.set("Tracing ECG from sound input...")
        self.is_tracing = True
        
        # Clear existing data
        self.ecg_data = []
        self.time_data = []
        
        # Start the audio stream in a separate thread
        self.trace_thread = threading.Thread(target=self.trace_audio)
        self.trace_thread.daemon = True
        self.trace_thread.start()
    
    def stop_tracing(self):
        if not self.is_tracing:
            return
            
        self.is_tracing = False
        
        if self.trace_thread and self.trace_thread.is_alive():
            self.trace_thread.join(timeout=1.0)
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        self.trace_btn.config(text="Start Tracing")
        self.status_var.set("Ready")
    
    def trace_audio(self):
        try:
            # Open audio stream
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            while self.is_tracing:
                # Read audio data
                data = self.stream.read(self.CHUNK)
                audio_data = struct.unpack(f'{self.CHUNK}h', data)
                
                # Add to queue for plotting
                self.data_queue.put(audio_data)
                
                # Small delay to prevent thread from consuming too much CPU
                time.sleep(0.001)
                
        except Exception as e:
            print(f"Error in trace_audio: {e}")
            self.status_var.set(f"Error: {str(e)}")
            
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

def main():
    root = tk.Tk()
    app = ECGRecorder(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_tracing(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()