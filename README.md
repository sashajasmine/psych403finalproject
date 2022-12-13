Final Project for PSYCH 403 - Experimental design for the Stroop Test 

strooptest.py 

Sasha Schneider, 1598633

- Expriment is intended to measure executive processing abilities, specifically selective attention capacity,by pairing names of words and colours of ink
- Experiment has 2 stages: congruent, and incongruent, with 6 trials of each (12 trials/block total) - first 6 congruent, followed by 6 incongruent in each block 
- Experiment stimuli include various instructional/informative text, a fixation cross (shown for 250 ms), followed by a word either matching the ink colour or not matching the ink colour (shown until their keypress is recorded)
- At the presentation of the stimuli (colour word), participant is required to press either a 'r', 'g', or 'b' key according to what colour of ink the word is shown in

- Experiment runs 3 blocks of trials - per trial recording their responses, accuracy & average accuracy, colour of ink, word presented, reaction time & average reaction time, and block/trial numbers
- This data is saved to a CSV file in a folder called Stroop Data, creating a filename of the participant name and number, and saving all recorded data 


