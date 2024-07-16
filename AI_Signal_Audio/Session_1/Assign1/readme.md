# Audio Signal Processing for Bird Sound Isolation

## Objective:

The goal of this project is to analyze an audio recording to identify and isolate the sounds of birds and a plane. This involves plotting time and frequency representations of the signal, applying filtering techniques to isolate the bird sounds, and removing the bird sounds to isolate the plane sounds.

## Analysis and Discussion:

For this assignment, I applied two filters with 3 orders to filter bird and plane sounds from the original audio.
 
### 🕊️ Bird sound: 

The filter used here is bandpass. It will remain the audio between the lowcut and upcut which means it will extract the signal within the frequency range of 1kHz to 8kHz.

The different order of filters shows a different steepness of the curve around the cutoff frequencies, as the following graphs:

* order = 3
![](AI_Signal_Audio/Session_1/Assign1/img/bf_3.png)
  
* order = 5
* order = 7

### ✈️ Plane sound: 
