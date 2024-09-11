# Description
This simple GUI application only shows you the time series and band power using OpenBCI's Ultracortex Mark IV EEG (https://docs.openbci.com/AddOns/Headwear/MarkIV/). The plastic of the helmet is 3D printed except for the electrodes. I use a 16-channel helmet but can also work with 8. The board(s) I use are Cyton and Daisy. There is no user interaction with this application. This project started on 11/18/23 to 8/17/24 with various stops and gos. I will periodically add or change the code so I can base my next version on this.
# Materials
- OpenBCI
  - 3D-Print-It-Yourself Neurotechnologist Bundle - (https://shop.openbci.com/products/print-it-yourself-neurotechnologist-bundle)
    -  Cyton+Daisy 16-channel with battery and charger	1
    -  EMG/ECG Snap Electrode Cables	1
    -  EMG/ECG Foam Solid Gel Electrodes	2
    -  EEG Dry Comb Electrodes 5 mm	1
# Sources
- OpenBCI
  - Documentation - https://docs.openbci.com/
  - Widget Guide - https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/
    - Also provided the wording of the widget descriptions.
- Brainflow
  - API - https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
  - Code Samples - https://brainflow.readthedocs.io/en/stable/Examples.html
- PyQt5 - https://www.pythonguis.com/pyqt5-tutorial/
- pyqtgraph API - https://pyqtgraph.readthedocs.io/en/latest/api_reference/index.html
- The Neurotech Primer - NeurotechX - https://www.amazon.com/Neurotech-Primer-Beginners-Everything-Neurotechnology/dp/B09CKP1D66/ref=sr_1_1?crid=34JY2M4Q4JXOI&dib=eyJ2IjoiMSJ9.dhvdwzw7WWUflQ8GYKlwvA.owT1u1lTqqq9MHZn8rRTPIla6iTTfD4Rl1YYZVRWDnA&dib_tag=se&keywords=neurotech+primer&qid=1723924906&sprefix=neurotech+prime%2Caps%2C112&sr=8-1
## Other Sources
- https://www.nti-audio.com/en/support/know-how/fast-fourier-transform-fft#:~:text=The%20%22Fast%20Fourier%20Transform%22%20(,frequency%20information%20about%20the%20signal.
- https://eepower.com/technical-articles/how-to-create-bandpass-filters/#
- https://en.wikipedia.org/wiki/Band-stop_filter
- https://www.izotope.com/en/learn/6-ways-to-use-a-high-pass-filter-when-mixing.html#:~:text=A%20high%2Dpass%20filter%20is,of)%20lower%2Dfrequency%20signals.
- https://www.sciencedirect.com/topics/computer-science/signal-denoising#:~:text=Signal%20denoising%20allows%20the%20removal,domain%20(Akay%2C%202012).
- https://numpy.org/doc/stable/reference/generated/numpy.transpose.html
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html 
- https://mne.tools/stable/index.html
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig 
- https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.plot_psd 
- https://mne.tools/stable/auto_tutorials/raw/40_visualize_raw.html 
- https://www.youtube.com/watch?v=eKGmoJOB-_0 
- https://info.tmsi.com/blog/the-10-20-system-for-eeg 
- https://upload.wikimedia.org/wikipedia/commons/f/fb/EEG_10-10_system_with_additional_information.svg
- https://www.youtube.com/watch?v=TMeJyrPmwwM 
- https://en.wikipedia.org/wiki/Mu_wave
- https://neurofeedbackalliance.org/understanding-brain-waves/ 
- https://arnauddelorme.com/ica_for_dummies/#:~:text=Independent%20Component%20Analysis%20is%20a,usually%20independent%20of%20each%20other).
- https://en.wikipedia.org/wiki/NumPy 
- https://en.wikipedia.org/wiki/Marker_interface_pattern#:~:text=The%20marker%20interface%20pattern%20is,explicit%20support%20for%20such%20metadata
# Python Packages
- PyQt5 - 5.15.10
- PyQt5-Qt5 - 5.15.2
- PyQt5-sip - 12.13.0
- PyQt5Designer - 5.14.1
- brainflow - 5.12.1
- nptyping - 1.4.4
- numpy - 1.26.4
- pip - 23.2.1
- pyqtgraph - 0.12.4
- setuptools - 70.2.0
- typish - 1.9.3
