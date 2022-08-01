# -*- coding: utf-8 -*-
"""
Note: If you're going to try running this program, you'll need to pip install PySimpleGui and matplotlib

PySimpleGUI citations:
    https://www.pysimplegui.org/en/latest/
    https://www.pysimplegui.org/en/latest/cookbook/
    https://www.pysimplegui.org/en/latest/call%20reference/

Matplotlib citations:
    https://www.geeksforgeeks.org/matplotlib-tutorial/

Note: no code is directly implemented from any of these sources, but these tutorials/documentations
    were used to learn these libraries.

"""
import sys
sys.path.insert(0, './src')
import ls
import energy
import time
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import os
import subprocess
report = energy.get_report()

def reset():
    window['-STATE-'].update(disabled=False)
    window['-STATE-'].update(ls.USstates)
    window['-CAT1-'].update(ls.blankList)
    window['-CAT2-'].update(ls.blankList)
    window['-CAT3-'].update(ls.blankList)
    window['-CAT4-'].update(ls.blankList)
    window['-YEAR-'].update(ls.yearRange)
    values.clear()

def commandCleanup(string):
    string = string.replace("\'", "")
    string = string.replace("[", "")
    string = string.replace("]", "")
    return string

def writeToFile(data):
    if os.path.exists(".\\Intermediate_Files\\transferData.txt"):
        os.remove(".\\Intermediate_Files\\transferData.txt")
    f = open(".\\Intermediate_Files\\transferData.txt", "a")
    f.write(values['-CAT4-'][0])
    for x in range(0, len(data)):
        f.write('\n' + str(data[x]))
        
def timePopup(timeList):
    if values['-CAT4-'][0] == 'All':
        sg.popup('MergeSort: ' + timeList[0] + ' milliseconds', 'QuickSort: ' + timeList[1] + ' milliseconds', 'TimSort: ' +
                 timeList[2] + ' milliseconds',title='Timing Report',grab_anywhere=True, non_blocking=True)
    if values['-CAT4-'][0] == 'MergeSort':
        sg.popup('MergeSort: ' + timeList[0] + ' milliseconds',title='Timing Report',grab_anywhere=True, non_blocking=True)
    if values['-CAT4-'][0] == 'QuickSort':
        sg.popup('QuickSort: ' + timeList[0] + ' milliseconds',title='Timing Report',grab_anywhere=True, non_blocking=True)
    if values['-CAT4-'][0] == 'TimSort':
        sg.popup('TimSort: ' + timeList[0] + ' milliseconds',title='Timing Report',grab_anywhere=True, non_blocking=True)

def executeProgram():
    unsortedList = []
    sortedList = []
    
    #There are two types of graphs we will display in this program:
    #The first displays all years for a state, the second displays all states for one year
    
    #if the user selects 'None' for the year, the list is filled with 60 years of data for one state
    if values['-YEAR-'] == ['None'] and values['-CAT4-'][0] == 'None':
        for x in range(ls.statesToInt[values['-STATE-'][0]]*60, ls.statesToInt[values['-STATE-'][0]]*60 + 60):
            unsortedList.append(report[x][values['-CAT1-'][0]][values['-CAT2-'][0]][values['-CAT3-'][0]])
        plt.plot(ls.yearRange2, unsortedList)
        plt.xlabel('Years')
        
        if values['-CAT1-'][0] == 'Consumption':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (billion BTU)')
            plt.title(values['-CAT1-'][0] + ' of ' + values['-CAT3-'][0] + ' in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      values['-STATE-'][0] + ' from 1960 to 2019')
            
        if values['-CAT1-'][0] == 'Expenditure':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (million USD)')
            plt.title(values['-CAT3-'][0] + ' Expenditures in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      values['-STATE-'][0] + ' from 1960 to 2019')
            
        if values['-CAT1-'][0] == 'Price':
            plt.ylabel('Price of ' + values['-CAT3-'][0] + ' per million BTU')
            plt.title(values['-CAT3-'][0] + ' price in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      values['-STATE-'][0] + ' from 1960 to 2019')
        plt.figure()
        return
    #end
    
    
    #Sorted variant of above
    if values['-YEAR-'] == ['None'] and values['-CAT4-'][0] != 'None':
        for x in range(ls.statesToInt[values['-STATE-'][0]]*60, ls.statesToInt[values['-STATE-'][0]]*60 + 60):
            unsortedList.append(report[x][values['-CAT1-'][0]][values['-CAT2-'][0]][values['-CAT3-'][0]])
    
    
        for x in range(len(unsortedList)):
            print(unsortedList[x])
        print("--------------")
        #map years to data values in the unsorted list, this way we can rematch when data is sorted later
        valMap = {}
        for x in range(0, len(unsortedList)):
            valMap[ls.yearRange2[x]] = unsortedList[x]
        tempValMap = valMap.copy()
        #write the unsorted list to a txt file, this way we can exchange data between programming languages
        writeToFile(unsortedList)
        
        #here is where we run the C++ executable
        subprocess.run(".\\src\\sortData.exe")
        
        #wait to make sure the C++ code finishes executing and writing
        time.sleep(1.5)
        
        f = open(".\\Intermediate_Files\\returnData.txt", "r")
        
        timeList = []
        if values['-CAT4-'] == ['All']:
            f.readline() #first line is always blank
            timeList.append(f.readline()) #Merge
            timeList.append(f.readline()) #Quick
            timeList.append(f.readline()) #Tim/Radix
        else:
            f.readline() #first line is blank
            timeList.append(f.readline()) #values['-CAT4-'][0]
        
        for x in range(60):
            sortedList.append(float(f.readline()))
        #finally, we have the sorted list. We have to remap it to the years.
        sortedYears = []
        
        tempYearRange = ls.yearRange2.copy()
        for x in range(len(sortedList)):
            for j in range(len(tempYearRange)):
                #print(tempValMap[tempYearRange[j]], sortedList[x])
                if tempValMap[tempYearRange[j]] == float(sortedList[x]):
                    sortedYears.append(tempYearRange[j])
                    tempValMap.pop(tempYearRange[j])
                    tempYearRange.pop(j)
                    break
        #we reverse the sorted list so that the graphs are more visually appealing.
        #it was necessary to have them in ascending order at first for mapping.
        sortedList.reverse()
        
        for x in range(len(sortedList)):
            print(sortedList[x])
        
        #this function creates an abbreviated list of years in line with the sortedYears list.
        #this makes it easier to read on the bar graph.
        ls.mapAbrevYears(sortedYears)
            
        """
        for x in range(len(sortedYears)):
            print(sortedYears[x])
        """
        
        if values['-CAT1-'][0] == 'Consumption':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (billion BTU)')
            plt.title(values['-CAT1-'][0] + ' of ' + values['-CAT3-'][0] + ' in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      values['-STATE-'][0] + ' in Descending Order')
            
        if values['-CAT1-'][0] == 'Expenditure':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (million USD)')
            plt.title(values['-CAT3-'][0] + ' Expenditures in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      values['-STATE-'][0] + ' in Descending Order')
            
        if values['-CAT1-'][0] == 'Price':
            plt.ylabel('Price of ' + values['-CAT3-'][0] + ' per million BTU')
            plt.title(values['-CAT3-'][0] + ' price in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      values['-STATE-'][0] + ' in Descending Order')
        ls.abrevYears.reverse()
        plt.xlabel('Years')
        plt.bar(ls.numRange2, sortedList, tick_label=ls.abrevYears, width = 0.5)
        plt.figure()
        timePopup(timeList)
        return
    
    #end
    
    
    #if the user selects a year, the list is filled with one year of data from all states
    if values['-YEAR-'] != ['None'] and values['-CAT4-'] == ['None']:
        for x in range((ls.yearsToIndex[values['-YEAR-'][0]] - 1), (ls.yearsToIndex[values['-YEAR-'][0]] - 1) + 3060, 60):
            unsortedList.append(report[x][values['-CAT1-'][0]][values['-CAT2-'][0]][values['-CAT3-'][0]])
        
        if values['-CAT1-'][0] == 'Consumption':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (billion BTU)')
            plt.title(values['-CAT1-'][0] + ' of ' + values['-CAT3-'][0] + ' in the ' + values['-CAT2-'][0] + ' sector of ' + 
                       'All States in the year ' + str(values['-YEAR-'][0]))
            
        if values['-CAT1-'][0] == 'Expenditure':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (million USD)')
            plt.title(values['-CAT3-'][0] + ' Expenditures in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      'All States in the year ' + str(values['-YEAR-'][0]))
            
        if values['-CAT1-'][0] == 'Price':
            plt.ylabel('Price of ' + values['-CAT3-'][0] + ' per million BTU')
            plt.title(values['-CAT3-'][0] + ' price in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      'All States in the year ' + str(values['-YEAR-'][0]))
        
        plt.xlabel('States')
        plt.bar(ls.numRange, unsortedList, tick_label=ls.USstatesAbrev, width = 0.8)
        plt.figure()
        return
    #end
    
    
    #Sorted variant of above
    if values['-YEAR-'] != ['None'] and values['-CAT4-'] != ['None']:
        for x in range((ls.yearsToIndex[values['-YEAR-'][0]] - 1), (ls.yearsToIndex[values['-YEAR-'][0]] - 1) + 3060, 60):
            unsortedList.append(report[x][values['-CAT1-'][0]][values['-CAT2-'][0]][values['-CAT3-'][0]])
        
        #map states to data values in the unsorted list, this way we can rematch when data is sorted later
        valMap = {}
        for x in range(0, len(unsortedList)):
            valMap[ls.USstatesAbrev[x]] = unsortedList[x]
        tempValMap = valMap.copy()
        #write the unsorted list to a txt file, this way we can exchange data between programming languages
        writeToFile(unsortedList)
        
        #here is where we run the C++ executable
        subprocess.run(".\\src\\sortData.exe")
        
        #wait to make sure the C++ code finishes executing and writing
        time.sleep(1.5)
        
        f = open(".\\Intermediate_Files\\returnData.txt", "r")
        
        timeList = []
        if values['-CAT4-'] == ['All']:
            f.readline() #first line is always blank
            timeList.append(f.readline()) #Merge
            timeList.append(f.readline()) #Quick
            timeList.append(f.readline()) #Tim/Radix
        else:
            f.readline() #first line is blank
            timeList.append(f.readline()) #values['-CAT4-'][0]
        
        for x in range(51):
            sortedList.append(float(f.readline()))
        
        #we have the sorted list. We have to remap it to the states.
        sortedStates = []
            
        tempAbrevStates = ls.USstatesAbrev.copy()
        for x in range(len(sortedList)):
            for j in range(len(tempAbrevStates)):
                if tempValMap[tempAbrevStates[j]] == float(sortedList[x]):
                    sortedStates.append(tempAbrevStates[j])
                    tempValMap.pop(tempAbrevStates[j])
                    tempAbrevStates.pop(j)
                    break
        #we reverse the sorted list so that the graphs are more visually appealing.
        #it was necessary to have them in ascending order at first for mapping.
        sortedList.reverse()
        if values['-CAT1-'][0] == 'Consumption':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (billion BTU)')
            plt.title(values['-CAT1-'][0] + ' of ' + values['-CAT3-'][0] + ' in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      'All States in the year ' + str(values['-YEAR-'][0]) + ' in Descending Order')
                
        if values['-CAT1-'][0] == 'Expenditure':
            plt.ylabel(values['-CAT3-'][0] + ' ' + values['-CAT1-'][0] + ' (million USD)')
            plt.title(values['-CAT3-'][0] + ' Expenditures in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      'All States in the year ' + str(values['-YEAR-'][0]) + ' in Descending Order')
                
        if values['-CAT1-'][0] == 'Price':
            plt.ylabel('Price of ' + values['-CAT3-'][0] + ' per million BTU')
            plt.title(values['-CAT3-'][0] + ' price in the ' + values['-CAT2-'][0] + ' sector of ' + 
                      'All States in the year ' + str(values['-YEAR-'][0]) + ' in Descending Order')
        sortedStates.reverse()
        plt.xlabel('States')
        plt.bar(ls.numRange, sortedList, tick_label=sortedStates, width = 0.5)
        plt.figure()
        timePopup(timeList)
        
    #end
        
        
#GUI STUFF!
sg.theme('DarkAmber')

layout = [
        [sg.Text('Select a State')],
        [sg.Listbox(ls.USstates, size=(15, 10), key='-STATE-', enable_events=True, no_scrollbar=False, 
                    tooltip='Select 1 US state. If a year is selected, this selection is ignored.')],
        [sg.Text('Select a Type')],
        [sg.Listbox(ls.blankList, size=(15, 3), key='-CAT1-', enable_events=True, no_scrollbar=True,
                    tooltip='Select which type of data you would like to see.'),
         ],
        [sg.Text('Select a Sector')],
        [sg.Listbox(ls.blankList, size=(15, 6), key='-CAT2-', enable_events=True, no_scrollbar=True,
                    tooltip='Select which sector you would like to see data from.')],
        [sg.Text('Select a Resource')],
        [sg.Listbox(ls.blankList, size=(15, 10), key='-CAT3-', enable_events=True, no_scrollbar=True,
                    tooltip='Select which resource you would like to see data about.')],
        [sg.Text('Select an Algorithm')],
        [sg.Listbox(ls.blankList, size=(15, 5), key='-CAT4-', enable_events=True, no_scrollbar=True,
                    tooltip='Select which algorithm should be used to sort the data.')],
        [sg.Text('Optional: Select a Year')],
        [sg.Listbox(ls.yearRange, size=(5, 5), key='-YEAR-', enable_events=True, no_scrollbar=False, default_values=['None'],
                    tooltip='Select a year to see data from. If a year is chosen, the State selection is ignored. Data will be displayed from all states.')],
        [sg.Button(button_text='Add', key='-Go-'), sg.Button(button_text='Show', key='-Show-'), sg.Button(button_text='Reset', key='-Reset-')]
          ]

window = sg.Window('Window Title', layout, enable_close_attempted_event=True,force_toplevel=True,
                   element_justification='left', grab_anywhere=True)

while True:  # Event Loop
    event, values = window.read()
    
    #Exit condition, also asks the user if they really want to quit
    if (event == 'Exit' or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT) and sg.popup_yes_no('Are you sure you want to exit?') == 'Yes':
        break
    
    #Reset condition
    if(event == '-Reset-'):
        reset()
        
    if(event == '-Show-'):
        plt.show()
    
    #if the user has not selected all categories, they can't go on. The popup notifies them of this
    if (event == '-Go-' and (values['-STATE-'] == [] or values['-CAT1-'] == [] or values['-CAT2-'] == [] or values['-CAT3-'] == [] or 
                             values['-CAT4-'] == [] or values['-YEAR-'] == [])):
        sg.popup('Please select an option from all categories first.', title='Error')
    elif event == '-Go-':
        executeProgram()
    
    if(event == '-STATE-' and values['-STATE-'] != []):
        window['-CAT1-'].update(ls.getList("Category1"))
    
    if(event == '-CAT1-' and values['-STATE-'] != [] and values['-CAT1-'] != []):
        command = str(values['-CAT1-']) + 'SubCats'
        command = commandCleanup(command)
        values['-CAT2-'] = []
        window['-CAT2-'].update(ls.getList(command))
        #the next 4 commands are there to reset the lists, a similar approach is done in the next event
        values['-CAT3-'] = []
        window['-CAT3-'].update(ls.blankList)
        values['-CAT4-'] = []
        window['-CAT4-'].update(ls.blankList)
    
    if(event == '-CAT2-' and values['-STATE-'] != [] and values['-CAT1-'] != [] and values['-CAT2-'] != []):
        command = str(values['-CAT1-']) + '_' + str(values['-CAT2-'])
        command = commandCleanup(command)
        values['-CAT3-'] = []
        window['-CAT3-'].update(ls.getList(command))
        #reset the cat4 list
        window['-CAT4-'].update(ls.blankList)
        values['-CAT4-'] = []
    
    if(event == '-CAT3-' and values['-STATE-'] != [] and values['-CAT1-'] != [] and values['-CAT2-'] != [] and values['-CAT3-'] != []):
        window['-CAT4-'].update(ls.getList('Sorting_Algos'))
    
    if(event == '-YEAR-' and values['-YEAR-'] != ['None']):
        window['-STATE-'].update(disabled=True)
        values['-STATE-'] = []
    elif event == '-YEAR-' and values['-YEAR-'] == ['None']:
        window['-STATE-'].update(disabled=False)
        #window['-STATE-'].update(ls.USstates)
        #values['-STATE-'] = []
    print(event, values)
    
window.close()