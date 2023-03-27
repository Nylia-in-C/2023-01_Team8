# 2023-01_Team8 CMPT395 Project - Scheduler  
&nbsp; 
# Table of Contents  
&nbsp; 
[1. Introduction](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#1-introduction)  
[2. Installation](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#2-installation)  
[3. Basic UI Overview](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#3-basic-ui-overview)  
    [3.1. Sidebar](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#31-sidebar)  
        [3.1.1. File Import](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#311-file-import)    
        [3.1.2. Create Template](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#312-create-template)  
        [3.1.3. Import Template](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#313-import-template)   
        [3.1.4. Students per Term Menu](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#314-students-per-term-menu)  
        [3.1.5. Create Schedule](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#315-create-schedule)  
    [3.2. Tabs](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#32-tabs)  
        [3.2.1. Schedule](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#321-schedule)  
        [3.2.2. Options](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#322-options)  
            [3.2.2.1. Room Options](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#3221-room-options)  
            [3.2.2.2. Course Options](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#3222-course-options)  
        [3.2.3. Instructions](https://github.com/Nylia-in-C/2023-01_Team8/blob/main/README.md#323-instructions)  
&nbsp;   
  
# 1. Introduction
*Scheduler* is a standalone Windows-compatible application created for the Macewan School of Continuing Education. It allows the user to create timetables for the students, based on given courses, terms, classrooms, and enrollment numbers.  
&nbsp;   
# 2. Installation
Download the *Scheduler.exe* file from the *dist* folder onto a Windows machine. The executable can run without further installation by double-clicking on the icon.  
&nbsp;   
# 3. Basic UI Overview
*Scheduler* is broken into two main parts: the left sidebar with various user functions, and the right side with three main tabs. The default tab *Schedule* shows any created schedules based on user input (see Section Schedule Tab for more information). Furthermore, there is also an *Options* tab as well as the *Instructions* tab in which the user can easily reference this guide in-app.  
&nbsp; 
&nbsp; 
## 3.1. Sidebar
On the left sidebar, the user can adjust the number of students either manually by program and term, or by uploading a pre-made template file to quickly populate predetermined enrollment numbers.  
&nbsp;   
### 3.1.1. File Import
Optionally, the user can upload a file to populate enrollment numbers automatically.  
&nbsp; 
*Scheduler* will accept two types of templates to create the same kind of output:  
a) Template A (by program) <!INSERT NAME INSERT NAME INSERT NAME>  
b) Template B (by student ID) <!INSERT NAME INSERT NAME INSERT NAME>  
&nbsp; 
### 3.1.2. Create Template
If no file exists yet, click the *Create Template* button to make a compatible .xlsx file that can be filled out with enrollment numbers via any available spreadsheet editor program *(e.g. Microsoft Excel)*.  
&nbsp;   
### 3.1.3. Import Template
If a file with the correct template already exists, click the *Choose File* button and navigate to the correct file to upload. Once a file has been chosen, click the *Load Data* button to import the student enrollment data into *Scheduler*.  
&nbsp;   
### 3.1.4. Students per Term Menu
The number of students per program per term can be manually adjusted here, either by clicking on the box and typing in the desired value, or by clicking the up/down arrows to the right of the box.  

Note: Importing data via the *Load Data* function will overwrite previous input.   
&nbsp;   
### 3.1.5. Create Schedule
Once data has been entered, select the desired Term (Fall, Winter, or Spring / Summer) from the dropdown menu. Afterwards, click the *Create Schedule* button to generate the schedule. 
&nbsp;   
&nbsp; 
## 3.2. Tabs  
Scheduler has tabs for the classroom schedules (*Schedule*), room and course adjustments (*Options*), and a copy of this ReadMe (*Instructions*).
&nbsp;   
&nbsp; 
### 3.2.1. Schedule
The schedule of the first room in the list is displayed from Monday to Thursday of the relevant week (starting at Week 1), from 8:00am to 5:00pm. 
Each lecture is represented by a coloured block; matching colours denote lectures of the same course. 
&nbsp;   
To view a different week, click on the left and right arrow navigation buttons above the schedule.
&nbsp;   
To view a different classroom, select it from the dropdown menu below the *Create Schedule button*. <!CHANGE IF NECESSARY>
&nbsp;   
Note: The Full-Stack Development program has its own <!INSERT TO FINISH THIS POINT ONCE FS IMPLEMENTED>  
&nbsp;   
### 3.2.2. Options  
The *Options* tab provides the ability to add/delete rooms and courses.  
&nbsp;   
#### 3.2.2.1 Room Options  
Rooms can be added or deleted here.  
- To add a room, the following needs to be entered:    
    1.    Classroom Name:     The room code. (e.g. 5-261)    
    2.    Room Capacity:      The number of seats in the room  
    3.    Room Type:          Lecture hall or Laboratory room  
    4.    Once this data has been entered for the room, click the 'Add' button to add the room to the list of available classrooms. 
&nbsp;   
- To delete a room, select the room to be deleted from the dropdown menu, and then click the 'Remove' button to complete the process.  

&nbsp;   
#### 3.2.2.2 Course Options  
Courses can be added or edited here. 
&nbsp; 
- To add a course:  
    1.  Select "New Course".  
    2.  Enter the Course Name (e.g. PCOM101).  
    3.  Optional: Check off if the course to be added is a core course, online, and/or has a lab component.  
    4.  Enter the total number of course hours, the Term (1 for Fall, 2 for Winter, 3 for Spring/Summer) and the lecture duration in hours. 
    5.  Optional: To add prerequisite courses, select the relevant prerequisite from the dropdown menu and click the 'Add Pre-Req' button. 
    6.  Optional: To clear previously assigned prerequisite courses, click the 'Clear Pre-Reqs' button.  
    7.  When finished, click the 'Save Course' button to add the course to the course list. 
&nbsp;   
- To edit an existing course:  
    1.  Select "Edit Course".    
    2.  Select the course name from the drop down menu (e.g. PCOM101).  
    3.  Optional: Check off if the course to be edited is a core course, online, and/or has a lab component.  
    4.  Enter the total number of course hours, the Term (1 for Fall, 2 for Winter, 3 for Spring/Summer) and the lecture duration in hours.   
    5.  Optional: To add prerequisite courses, select the relevant prerequisite from the dropdown menu and click the 'Add Pre-Req' button.   
    6.  Optional: To clear previously assigned prerequisite courses, click the 'Clear Pre-Reqs' button.  
    7.  When finished, click the 'Save Course' button to finish editing the course.  
 
&nbsp;   
### 3.2.3. Instructions
These instructions can be found in the *Instructions* tab for easy access without an internet connection. 
&nbsp;   