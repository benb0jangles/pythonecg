# PythonECG - Simplified ECG Visualization

A lightweight Python application for real-time ECG (Electrocardiogram) signal visualization from audio input.

![PythonECG Screenshot](https://github.com/benb0jangles/pythonecg/raw/main/screenshot.png)

## Overview

PythonECG is a simple desktop application that allows you to visualize ECG-like signals captured from your computer's audio input. It's designed to be minimalist and focuses solely on real-time visualization.

This tool can be used for:
- Educational demonstrations of signal processing
- Testing audio input devices
- Visualizing audio waveforms in a medical-style display
- Prototyping ECG-related applications

## Features

- Real-time audio signal visualization with ECG-like display
- Simple toggle button to start/stop signal tracing
- Automatic scaling to show the last 10 seconds of data
- Clean, medical-inspired interface with grid lines

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- PyAudio
- Tkinter (usually comes with Python)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pythonecg.git
   cd pythonecg
   ```

2. Install required dependencies:
   ```
   pip install numpy matplotlib pyaudio
   ```

3. Run the application:
   ```
   python ecgbasic.py
   ```

## Usage

1. Connect an audio input device to your computer (microphone, line-in, etc.)
2. Launch the application
3. Click "Start Tracing" to begin visualizing the audio signal
4. Click "Stop Tracing" to halt the visualization

## How It Works

The application captures audio from your system's input device at a sampling rate of 44.1kHz. This raw audio data is then plotted in real-time to create an ECG-like visualization. The display shows a 10-second window that automatically scrolls as new data comes in.

## Technical Details

- Sampling rate: 44.1kHz
- Bit depth: 16-bit
- Single channel (mono) input
- Window size: 10 seconds

## Extending the Application

This is a simplified version of a more comprehensive ECG application. If you need additional features such as recording, file operations, or settings adjustment, you can extend this codebase as needed.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- This project was inspired by medical visualization tools
- Thanks to the PyAudio, NumPy, and Matplotlib communities for their excellent libraries
