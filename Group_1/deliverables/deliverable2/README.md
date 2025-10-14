# Deliverable 2 - Complete by 10/27/25

Upcoming: <b>11/3/25 - Project Updates</b>

For the project updates, we are requesting a short presentation on the progress you have made on your projects. Whether that is the research and development, sensors integration, or meeting style - we want to know. (Will update this in more detail later.)

## Group Deliverable
Edit the main `README.md` in the `2026_FYC_Projects` repository with the title and basic description of the group's project.

In the `Group_1` directory, add a title and a detailed description in the `README.md`.

## Hardware Deliverable

I'm making this deliverable with a longer timeline because I want you guys to do some research for passive filters. Passive filters are the easiest way to filter out any unnecessary noise in a circuit. Look into Texas Instruments' filter design tool <b>AFTER</b> you read up on passive filters as it will not make ANY sense. 

Resource: https://www.electronics-tutorials.ws/filter/filter_2.html

1. Work to build a band-pass filter with a center frequency of 1591 Hz. Test using the equipment in the lab (please utilize the function generator and oscilloscope and make sure the BNC cable is set to 10x). Show me photos!

When completing the task, set the function generator at 10Hz, with a V_pp = 1V to start the experiment. Then, use the BNC cables to read the input and a second BNC cable connected to a different channel on the oscilloscope to read the V_out. Keep repeating this until you reach 100kHz on the function generator, so make sure to take the data points.

<img width="1630" height="488" alt="image" src="https://github.com/user-attachments/assets/bd4a202a-c324-475e-bae5-8610e9c34ead" />
Example of how this should be done. 

2. Simulate the band-pass on Multisim to obtain a similar graph.

<img width="770" height="393" alt="image" src="https://github.com/user-attachments/assets/35f7803b-b9b1-46f5-97ac-ba72f4482a43" />

Example of graph developed after exporting from Multisim.

3. Build a low-pass filter with a center frequency of your choice. I want to see results, so make calculations and insert photos.
4. Now, design a filter of your choice using TI's filter design tool. Make it a passive filter.

## Software Deliverable

1. Keep familiarizing yourself with the pinouts of the Raspberry Pi 5. Using the Raspberry Pi, build a simple LED circuit (ask the hardware friends how to do that and make sure there is a resistor) to control the state of the LED (on/off).

2. Research the idea behind a Kalman filter. This is one of the best ways to accomplish software filtering for sensors. Hint: it is a recursive method. 
3. Find a dataset of your choice, and write a program to manipulate the dataset and print it out to a `.csv` file. This could involve adding values from datasets, subtracting, removing - whatever it may be, it is up to you. This will be helpful when different forms of data may need to be written to another file for analysis. You can opt to use different packages of your choice to help with this. Bonus: generate graphs from the datasets!

4. Complete 5 LeetCode problems of your choice by the end of this deliverable date. 
