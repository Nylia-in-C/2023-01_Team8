# 2023-01_Team8 CMPT395 Project - Scheduler

# Table of Contents TODO: ADD EXTRA ENTRIES TO TABLE OF CONTENTS.

[Introduction](https://github.com/MacEwanCMPT395/2023-01_Team8/blob/main/README.md#introduction)  
[Installation](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#installation)  
[Basic UI Overview](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#basic-ui-overview)    
[File Import](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#file-import)    
    [Create Template](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#create-template)  
    [Import Template](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#import-template)   

# Introduction
Scheduler is a standalone Windows-compatible application created for the Macewan School of Continuing Education. It allows the user to create timetables for the students, based on given courses, terms, classrooms, and enrollment numbers.  

# Installation
Download the Scheduler.exe file from the dist folder onto a Windows machine. The executable can run without further installation by double-clicking on the icon.  

# Basic UI Overview
Scheduler is broken into two main parts: the left sidebar with various user functions, and the right side with three main tabs. The default tab 'Schedule' shows any created schedules based on user input (see Section Schedule Tab for more information). Furthermore, there is also an 'Options' tab as well as the 'Instructions' tab in which the user can easily reference this guide in-app. 

## Sidebar
On the left sidebar, the user can adjust the number of students either manually by program and term, or by uploading a pre-made template file to quickly populate predetermined enrollment numbers.

## Students per Term Menu
The number of students per program per term can be manually adjusted here, either by clicking on the box and typing in the desired value, or by clicking the up/down arrows to the right of the box.  

Note: Importing data via the Load Data function will overwrite previous input.   

## Enrollment by Program File Import
Optionally, the user can upload a file to populate enrollment numbers automatically. 

### Create Template
If no file exists yet, click the 'Create Template' button to make a compatible .xlsx file that can be filled out with enrollment numbers via any available spreadsheet editor program (e.g. Microsoft Excel). 

### Import Template
If a file with the correct template already exists, click the "Choose File" button and navigate to the correct file to upload. Once a file has been chosen, click the "Load Data" button to import the student enrollment data into Scheduler. 

## Create Schedule
Once data has been entered, select the desired Term (Fall, Winter, or Spring / Summer) from the dropdown menu. Afterwards, click the "Create Schedule" button to generate the schedule. 

<<<<<<< Updated upstream
Note: If there are insufficient rooms available, Scheduler will give a warning. To add more rooms, see ADDDDDD SECTION HERE   

=======
Note: If there are insufficient rooms available, Scheduler will give a warning. To add more rooms, see ADDDDDD SECTION HERE   
>>>>>>> Stashed changes
