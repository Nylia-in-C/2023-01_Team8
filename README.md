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
Scheduler has tabs for the classroom schedules ('Schedule'), room and course adjustments ('Options'), and a copy of this ReadMe ('Instructions').

### 3.2.1. Schedule
The schedule of the first room in the list is displayed from Monday to Thursday of the relevant week (starting at Week 1), from 8:00am to 5:00pm. 
Each lecture is represented by a coloured block; matching colours denote lectures of the same course. 

To view a different week, click on the left and right arrow navigation buttons above the schedule.

To view a different classroom, select it from the dropdown menu below the "Create Schedule button". <CHANGE IF NECESSARY>

Note: The Full-Stack Development program has its own <INSERT TO FINISH THIS POINT ONCE FS IMPLEMENTED>

### 3.2.2. Options  
The Options tab provides the ability to add/delete rooms and courses.   

#### 3.2.2.1 Room Options  
Rooms can be added or deleted here.  
a) To add a room, the following needs to be entered:    
    i)      Classroom Name:     The room code. (e.g. 5-261)    
    ii)     Room Capacity:      The number of seats in the room  
    iii)    Room Type:          Lecture hall or Laboratory room  

Once this data has been entered for the room, click the 'Add' button to add the room to the list of available classrooms. 

b) To delete a room, select the room to be deleted from the dropdown menu, and then click the 'Remove' button to complete the process.  

#### 3.2.2.2 Course Options  
Courses can be added or edited here. 
a) To add a course:  
    i)      Select "New Course".  
    ii)     Enter the Course Name (e.g. PCOM101).  
    iii)    Optional: Check off if the course to be added is a core course, online, and/or has a lab component.  
    iv)     Enter the total number of course hours, the Term (1 for Fall, 2 for Winter, 3 for Spring/Summer) and the lecture duration in hours. 
    v)      Optional: To add prerequisite courses, select the relevant prerequisite from the dropdown menu and click the 'Add Pre-Req' button. 
    vi)     Optional: To clear previously assigned prerequisite courses, click the 'Clear Pre-Reqs' button.  
    vii)    When finished, click the 'Save Course' button to add the course to the course list. 

b) To edit an existing course:
    i)      Select "Edit Course".    
    ii)     Select the course name from the drop down menu (e.g. PCOM101).  
    iii)    Optional: Check off if the course to be edited is a core course, online, and/or has a lab component.  
    iv)     Enter the total number of course hours, the Term (1 for Fall, 2 for Winter, 3 for Spring/Summer) and the lecture duration in hours. 
    v)      Optional: To add prerequisite courses, select the relevant prerequisite from the dropdown menu and click the 'Add Pre-Req' button.   
    vi)     Optional: To clear previously assigned prerequisite courses, click the 'Clear Pre-Reqs' button.  
    vii)    When finished, click the 'Save Course' button to finish editing the course.  


### 3.2.3. Instructions
These instructions can be found in the Instructions tab for easy access without an internet connection. 
