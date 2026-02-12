
# AB Puzzle Solver
## CMPT 355 - Group # 4
### Authors
- Alex Rasmussen
- Ethan Redmond
- Helen Ly
- Boden Smereka


## Overview
This project implements a solver for the AB circular‑board puzzle using the Iterative Deepening A* (IDA*) search algorithm. The solver explores the state space using a depth‑first strategy combined with a cost‑bounded iterative deepening loop, allowing it to find optimal solutions while using minimal memory.

The puzzle consists of:
- A circular arrangement of tiles  
- A single empty space (0)  
- A set of shift values determining how far the empty space can move  


## Filesystem Structure
The filesystem structure for this program is quite simple. The first directory you will see when unzipping the tarball is called '355G4' which is our main program directory. The '355G4' holds the following inside the directory: AB.py, README.md, Makefile, and a subdirectory called test_files. The test_files subdirectory holds a number of .txt files that we used when testing our program, these files are meant to replicate initial board states for the small and large disks that the program will attempt to solve. The README.md (which you are currently reading) holds our names, basic overview, filesystem structure as well as how to run our program. The Makefile is used for executing our Python script in accordance with the project specification sheet. The last file within the 355G4 directory is AB.py which is our main program and holds the code for the AB Puzzle Solver. 

---

## How to Run Our Program
There are two ways to run our program since it is a Python script. Regardless of which approach you use, you must be in the '355G4' directory when attempting to run the program

### Option 1: Using the Makefile
Step 1: Make sure you are in the '355G4' directory by using the following bash command (if the last directory listed is not '355G4', you must navigate to that directory)
```bash
pwd
```
Step 2: Create an executable file by using the Makefile via the following bash command
```bash
make 
```
Step 3: Execute the executable file created in Step 2 by using the following command.
The < number of disks > parameter is an integer that represents the number of large disks on the board. It is equivalent to the the 'n' value in the assignment specification sheet
```bash
./AB <number_of_disks>
```
After this point, you will have to enter a series of values for the large disks. This must match the number of disks entered into the command line during Step 3. After that, you must enter the series of values for the small disks, which also must match the number of disks entered into the command line during Step 3. Once both series of numbers have been entered, the program will start looking for a solution. 

### Option 2: Using the Interpreter Directly
Step 1: Make sure you are in the '355G4' directory by using the following bash command (if the last directory listed is not '355G4', you must navigate to that directory)
```bash
pwd
```
Step 2: Invoke the interpreter and the python script directly. The < number of disks > parameter is an integer that represents the number of large disks on the board. It is equivalent to the the 'n' value in the assignment specification sheet
```bash
python3 AB.py <number_of_disks>
```
After this point, you will have to enter a series of values for the large disks. This must match the number of disks entered into the command line during Step 3. After that, you must enter the series of values for the small disks, which also must match the number of disks entered into the command line during Step 3. Once both series of numbers have been entered, the program will start looking for a solution. 
