# 2023-01_Team8 CMPT395 Project - Scheduler  

# Table of Contents TODO: DOUBLECHECK ENTRIES.  

[Introduction](https://github.com/MacEwanCMPT395/2023-01_Team8/blob/main/README.md#introduction)  
[Installation](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#installation)  
[Basic UI Overview](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#basic-ui-overview)  
    [Sidebar](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#sidebar)  
    [File Import](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#file-import)    
        [Create Template](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#create-template)  
        [Import Template](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#import-template)   
    [Students per Term Menu](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#students-per-term-menu)  
    [Create Schedule](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#create-schedule)

# 1. Introduction
Scheduler is a standalone Windows-compatible application created for the Macewan School of Continuing Education. It allows the user to create timetables for the students, based on given courses, terms, classrooms, and enrollment numbers.  

# 2. Installation
Download the Scheduler.exe file from the dist folder onto a Windows machine. The executable can run without further installation by double-clicking on the icon.  

# 3. Basic UI Overview
Scheduler is broken into two main parts: the left sidebar with various user functions, and the right side with three main tabs. The default tab 'Schedule' shows any created schedules based on user input (see Section Schedule Tab for more information). Furthermore, there is also an 'Options' tab as well as the 'Instructions' tab in which the user can easily reference this guide in-app. 

## 3.1. Sidebar
On the left sidebar, the user can adjust the number of students either manually by program and term, or by uploading a pre-made template file to quickly populate predetermined enrollment numbers.

### 3.1.1. File Import
Optionally, the user can upload a file to populate enrollment numbers automatically. 

Scheduler will accept two types of templates to create the same kind of output:  
a) Template A (by program) <INSERT NAME INSERT NAME INSERT NAME>
b) Template B (by student ID) <INSERT NAME INSERT NAME INSERT NAME>

### 3.1.2. Create Template
If no file exists yet, click the 'Create Template' button to make a compatible .xlsx file that can be filled out with enrollment numbers via any available spreadsheet editor program (e.g. Microsoft Excel). 

### 3.1.3. Import Template
If a file with the correct template already exists, click the "Choose File" button and navigate to the correct file to upload. Once a file has been chosen, click the "Load Data" button to import the student enrollment data into Scheduler. 

### 3.1.4. Students per Term Menu
The number of students per program per term can be manually adjusted here, either by clicking on the box and typing in the desired value, or by clicking the up/down arrows to the right of the box.  

Note: Importing data via the Load Data function will overwrite previous input.   

### 3.1.5. Create Schedule
Once data has been entered, select the desired Term (Fall, Winter, or Spring / Summer) from the dropdown menu. Afterwards, click the "Create Schedule" button to generate the schedule. 

## 3.2. Tabs

### 3.2.1. Schedule

### 3.2.2. Options
The Options tab provides the means to do various 

### 3.2.3. Instructions
These instructions can be found in the Instructions tab for easy access without an internet connection. 
