# Author: Anand Cheruvu
# Version: 1.4
# Purpose: Read the streaming EEG signal from 11 channels and plot them in real time.

# import the necessary libraries
import time
import matplotlib.pyplot as plt
import numpy as np
from cortex import Cortex
from collections import deque
from threading import Thread

# Emotiv client credentials (replace with your actual client_id and client_secret)
emotiv_client_id = 'xxxx'
emotiv_client_secret = 'yyyy'

# EEG buffer length (in seconds)
BUFFER_LENGTH = 5
SAMPLING_RATE = 128  # Emotiv headset sampling rate
NUM_CHANNELS = 11     # Number of EEG channels

# Initialize buffers for plotting
eeg_buffers = [deque([0] * SAMPLING_RATE * BUFFER_LENGTH, maxlen=SAMPLING_RATE * BUFFER_LENGTH) for _ in range(NUM_CHANNELS)]
channel_names = ['FP1', 'FP2', 'CPz','AF3', 'AF4', 'T7', 'T8', 'Pz', 'O1', 'O2', 'Cz']  # EEG channel labels

# Set up the live plot
fig, axs = plt.subplots(NUM_CHANNELS, 1, figsize=(10, 10))
plt.subplots_adjust(hspace=0.5)

for i in range(NUM_CHANNELS):
    axs[i].set_title(channel_names[i])
    axs[i].set_ylim(-100, 100)  # Adjust based on the signal range
    axs[i].set_xlim(0, BUFFER_LENGTH)
    axs[i].grid(True)

# Class for streaming EEG data from Emotiv
class EmotivStream(Cortex):
    def __init__(self, client_id, client_secret):
        Cortex.__init__(self, {
            "client_id": client_id,
            "client_secret": client_secret,
            "debit": 100,
        })

    def on_create_session(self, *args, **kwargs):
        print("Emotiv session created, subscribing to EEG data...")
        self.sub(['eeg'])

    def on_eeg_data(self, *args, **kwargs):
        eeg_data = args[0]['eeg']
        self.update_eeg_buffers(eeg_data)

    def update_eeg_buffers(self, eeg_data):
        """Update the EEG buffers with new data."""
        for i, data_point in enumerate(eeg_data[2:10]):  # Only select 8 channels
            eeg_buffers[i].append(data_point)

# Function to update the plot
def update_plot():
    while True:
        for i in range(NUM_CHANNELS):
            axs[i].cla()
            axs[i].set_ylim(-100, 100)  # Adjust signal range as needed
            axs[i].set_xlim(0, BUFFER_LENGTH)
            axs[i].grid(True)
            axs[i].plot(np.linspace(0, BUFFER_LENGTH, SAMPLING_RATE * BUFFER_LENGTH), list(eeg_buffers[i]))
            axs[i].set_title(channel_names[i])
        plt.pause(0.01)  # Small delay to keep the plot updating smoothly

# Main function to start streaming and plotting
def main():
    # Start the EEG streaming thread
    emotiv_thread = Thread(target=start_emotiv_stream)
    emotiv_thread.start()

    # Start the plot updating loop
    update_plot()

# Start the Emotiv streaming
def start_emotiv_stream():
    client = EmotivStream(emotiv_client_id, emotiv_client_secret)
    client.do_prepare_steps()

if __name__ == "__main__":
    main()
