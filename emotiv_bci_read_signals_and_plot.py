
import time
import matplotlib.pyplot as plt
from collections import deque
from threading import Thread
from cortex import Cortex

# Parameters
client_id = 'YOUR_EMOTIV_CLIENT_ID'
client_secret = 'YOUR_EMOTIV_CLIENT_SECRET'

# Graphing setup
buffer_size = 100  # Number of points to show on the graph
channels = 4  # Adjust according to your headset (e.g., 4 or 14 channels)

# Initialize deque for each channel to store data points
data_buffer = [deque([0]*buffer_size, maxlen=buffer_size) for _ in range(channels)]

# Initialize a figure and axes for plotting
fig, ax = plt.subplots(channels, 1, figsize=(10, 8))

# Emotiv Stream Class
class EmotivStream(Cortex):
    def __init__(self, client_id, client_secret):
        Cortex.__init__(self, {
            "client_id": client_id,
            "client_secret": client_secret,
            "debit": 100,
        })

    def on_create_session(self, *args, **kwargs):
        print("Emotiv session created, subscribing to data...")
        self.sub(['eeg'])

    def on_eeg_data(self, *args, **kwargs):
        eeg_data = args[0]['eeg']
        for i, channel_data in enumerate(eeg_data[2:2+channels]):
            data_buffer[i].append(channel_data)

# Thread function to update graphs
def plot_graph():
    while True:
        for i in range(channels):
            ax[i].cla()  # Clear the previous plot
            ax[i].plot(data_buffer[i])  # Plot new data
            ax[i].set_title(f'Channel {i + 1}')
        plt.pause(0.1)  # Update rate for the graph

# Main function to start data streaming and plotting
def main():
    # Start Emotiv streaming in a separate thread
    client = EmotivStream(client_id, client_secret)
    client_thread = Thread(target=client.do_prepare_steps)
    client_thread.start()

    # Start plotting in the main thread
    plot_graph()

if __name__ == "__main__":
    main()
