'''
Final Project for PSYCH 403 - Experimental design for the Stroop Test 

strooptest.py 

Sasha Schneider, 1598633

- Expriment is intended to measure executive processing abilities, specifically selective attention capacity,by pairing names of words and colours of ink
- Experiment has 2 stages: congruent, and incongruent, with 6 trials of each (12 trials/block total) - first 6 congruent, followed by 6 incongruent in each block 
- Experiment stimuli include various instructional/informative text, a fixation cross (shown for 250 ms), followed by a word either matching the ink colour (shown until their keypress is recorded), or not matching the ink colour - depending on where in the block they are  
- At the presentation of the stimuli (colour word), participant is required to press either 'r', 'g', or 'b' according to what colour of ink the word is shown in

- Experiment runs 3 blocks of trials - per trial recording their responses, accuracy & average accuracy, colour of ink, word presented, reaction time & average reaction time, and block/trial numbers
- This data is saved to a CSV file in a folder called Stroop Data, creating a filename of the participant name and number, and saving all recorded data #=============================
''' 

#=====================
#IMPORT MODULES
#=====================
import random
from psychopy import visual, monitors, core, event, gui
import os 
import time 
import csv
import pandas as pd
from datetime import datetime

#=====================
#PATH SETTINGS
#=====================
directory = os.getcwd() 
path = os.path.join(directory, 'Stroop Data') #create path to save file in
   
#=====================
#COLLECT PARTICIPANT INFO
#=====================
dlg = gui.Dlg(title='Participant info')  #collect info in dialog box
dlg.addField('Name:') 
dlg.addField('Participant number:') 
dlg.addField('Age:') 
dlg.addField('Gender:') #user can type whatever gender they prefer 
dlg.addField('Handedness:', choices=['Left','Right','Ambidextrous'])
info = dlg.show() 

date = datetime.now() 
print(date) 

filename=path + '\\' +'participant_%s_name_%s.csv'%(info[1],info[0])  #set filename 

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
nTrials = 12 #12 trials
nBlocks = 3 #3 blocks
instr = 'Stoop task: respond by pressing "r","g", or "b" corresponding to ink colour of word.' #experiment instructions

#=====================
#PREPARE CONDITION LISTS
#=====================
#No files are used in the experiment

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
dataCollect = {"blockNumber": [], "trialNumber": [], "word":[], "color":[], "response": [],"accuracy": [], "reaction time": []} #create dict to save all data in empty lists within

#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
mon = monitors.Monitor('myMonitor', width=31.00, distance=60) 
mon.setSizePix([1920, 1080])
#initalize grey window of specified size 
win = visual.Window(
 fullscr=False, 
 monitor=mon, 
 size=(800,800), 
 color='grey', 
 units='pix'
)

#initialize all variables for text stimuli for all color/text combinations 
greenGreen = visual.TextStim(win,text='green',color='green')
greenRed = visual.TextStim(win,text='green',color='red') 
greenBlue = visual.TextStim(win,text='green',color='blue') 

redRed = visual.TextStim(win,text='red',color='red') 
redGreen = visual.TextStim(win,text='red',color='green') 
redBlue = visual.TextStim(win,text='red',color='blue') 

blueBlue = visual.TextStim(win, text='blue',color='blue') 
blueGreen = visual.TextStim(win,text='blue',color='green') 
blueRed = visual.TextStim(win,text='blue',color='red') 

#initalize text to be displayed 
cText = visual.TextStim(win,color='black') 
blockText = visual.TextStim(win,color='black') 
trialText = visual.TextStim(win,color='black') 

#initalize fixation cross 
fix = visual.TextStim(win,text='+',color='black') 

#initalize timer 
timer = core.Clock() 

#=====================
#START EXPERIMENT
#=====================
cText.text=instr #show instructions 
cText.draw() 
win.flip() 
core.wait(2) 

#=====================
#BLOCK SEQUENCE
#=====================
for block in range(nBlocks):
    
    #shuffle order of all 6 incongruent options in each block
    incongruentStims = [redBlue,redGreen,blueRed,blueGreen,greenRed,greenBlue]
    random.shuffle(incongruentStims)
    #shuffle order for all 6 congruent options in each block 
    congruentStims = [redRed,redRed,blueBlue,blueBlue,greenGreen,greenGreen] 
    random.shuffle(congruentStims) 

    #add lists together
    stimsList = congruentStims + incongruentStims
    
    counter = 0 #reset counter in each block 
    #show block text
    blockText.text='Block '+str(block+1) 
    blockText.draw() 
    win.flip() 
    core.wait(1) 
    
    #=====================s
    #TRIAL SEQUENCE
    #=====================    
    for trial in range(nTrials):
        dataCollect['blockNumber'].append(block+1) #record current block number
       
        dataCollect['trialNumber'].append(trial+1)  #record current trial number 
        trialInput = False #false until input is made 
        
        #=====================
        #START TRIAL
        #=====================   
        
        #show fixation cross 
        fix.draw() 
        win.flip() 
        core.wait(0.25) #250 ms 
        
        timer.reset() 
        
        cColor = stimsList[counter] #choose a stim according to trial run (counter) - 0-5 = congruent, 6-12 = incongruent 
        cColor.draw()
        win.flip()
        dataCollect['response'].append(event.waitKeys(keyList=['r','b','g'])[0]) #wait for keypress and collect it 
        
        dataCollect['word'].append(cColor.text) #collect word displayed
        
        correctColor = ''                      #initalize correct colour to avoid pandas error
        if cColor.color[0] > -1:               #check if 0th idex of rbg array of colour shown has red in it 
            dataCollect['color'].append('red') #append colour as red
            correctColor = 'r'                 #set this as the correct colour
        elif cColor.color[1] > -1:             #same rules follows for green/blue but with 1st/2nd index rbg array being checked 
            dataCollect['color'].append('green')
            correctColor = 'g'
        elif cColor.color[2] > -1:
            dataCollect['color'].append('blue')
            correctColor = 'b'
        else:
            dataCollect['color'].append('error!') #append error in case something goes wrong 
            
        # save accuracy data
        if dataCollect['response'][-1] == correctColor: #check if the correct colour == the key response 
            dataCollect['accuracy'].append(1) #1 is appended for correct
        else:
            dataCollect['accuracy'].append(0) #0 is appended for incorrect

        trialInput=True #response collected 
            
        if trialInput: #check if response was made 
            dataCollect['reaction time'].append(timer.getTime()) #record reaction time 
            
        counter+=1
        
#======================
# END OF EXPERIMENT
#======================

totalAccuracy = sum(dataCollect['accuracy'])/len(dataCollect['accuracy']) #calculate average accuracy 
avgRT = sum(dataCollect['reaction time'])/len(dataCollect['reaction time']) #calculate average reaction time 

dataCollect['blockNumber'].append('') #append an extra space to all lists to avoid pandas error for averages being appended to end of lists 
dataCollect['trialNumber'].append('')
dataCollect['word'].append('')
dataCollect['color'].append('')
dataCollect['response'].append('')
dataCollect['accuracy'].append(totalAccuracy) #append average accuracy 
dataCollect['reaction time'].append(avgRT) #append average RT

if not os.path.exists(path): #if the path doesn't exist, make it  
    os.mkdir(path)
dataframe = pd.DataFrame(dataCollect, index=None) #create a pandas dataframe of dict dataCollect
dataframe.to_csv(filename, index=False) #turn dataframe int csv file 

win.close() 

 