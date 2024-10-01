# Author: Anand Cheruvu
# Version: 1.2

# import the necessary libraries
import numpy as np
from scipy.signal import correlate
from cortex import Cortex
from collections import deque
from threading import Thread
import matplotlib.pyplot as plt

# Emotiv client credentials (replace with your actual client_id and client_secret)
emotiv_client_id = 'YOUR_EMOTIV_CLIENT_ID'
emotiv_client_secret = 'YOUR_EMOTIV_CLIENT_SECRET'

# EEG buffer length (in seconds)
BUFFER_LENGTH = 14
# Emotiv headset sampling rate
SAMPLING_RATE = 128 
# Number of EEG channels
NUM_CHANNELS = 11     
# Amplitude threshold to detect eye blink
AMP_THRESHOLD = 14

# Initialize buffers for each EEG channel
eeg_buffers = [deque([0] * SAMPLING_RATE * BUFFER_LENGTH, maxlen=SAMPLING_RATE * BUFFER_LENGTH) for _ in range(NUM_CHANNELS)]

# EEG channel labels
channel_names = ['FP1', 'FP2', 'AF3', 'AF4', 'T7', 'T8', 'Pz', 'O1', 'O2', 'Cz','CPz'] 

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

# Function to calculate and plot cross-correlation of the EEG signals
def calculate_cross_correlation():
    correlations = []
    for i in range(NUM_CHANNELS):
        for j in range(i + 1, NUM_CHANNELS):
            signal_1 = np.array(eeg_buffers[i])
            signal_2 = np.array(eeg_buffers[j])
            cross_corr = correlate(signal_1, signal_2, mode='full')
            correlations.append((channel_names[i], channel_names[j], cross_corr))

            # Plot cross-correlation for each pair of signals
            plt.figure()
            plt.plot(cross_corr)
            plt.title(f"Cross-Correlation: {channel_names[i]} vs {channel_names[j]}")
            plt.xlabel("Lag")
            plt.ylabel("Correlation")
            plt.grid(True)
            plt.show()

    return correlations

# Main function to start EEG streaming and cross-correlation calculation
def main():
    # Start the EEG streaming thread
    emotiv_thread = Thread(target=start_emotiv_stream)
    emotiv_thread.start()

    # Allow time for data collection
    print("Collecting EEG data for cross-correlation...")
    Thread(target=collect_data).start()

# Collect data over a fixed interval before calculating cross-correlation
def collect_data():
    time_to_collect = BUFFER_LENGTH  # Time in seconds to collect data
    Thread(target=calculate_cross_correlation).join()

# Start the Emotiv streaming
def start_emotiv_stream():
    client = EmotivStream(emotiv_client_id, emotiv_client_secret)
    client.do_prepare_steps()

if __name__ == "__main__":
    main()
