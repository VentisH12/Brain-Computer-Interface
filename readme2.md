Key components of the EEG signals cross correlation program:

a) EmotivStream Class: Streams EEG signals from the Emotiv headset.
b) Buffers: Signals from the EEG channels are stored in circular buffers using deque.
c) Cross-Correlation Calculation: The cross-correlation of the EEG signals from different channels is calculated using scipy.signal.correlate, and the results are plotted.
d) Real-Time Processing: The program collects data for a specified duration and then performs cross-correlation between different EEG channels.
