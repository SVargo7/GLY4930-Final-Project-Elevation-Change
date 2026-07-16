# GLY4930-Final-Project-Elevation-Change

## Description
This project automates visual representation of differences in elevation over time. It takes two different sets of data from different times over the same coordinate area and creates a visual of the elevation changes. 

## Packages & Dependencies 
discuss yml etc 

## Installation
up through opening jupyter lab

### Data Collection & Recommended Data Resource:
The two example sets in this repository include 2020 and 2026 Mid Ocean Ridge data, as well as 2020 and 2026 Great Barrier Reef data. The coordinates for these sites are as follows:

Mid Ocean Ridge:   
North: 43.131    
West: -33.299   
East: -23.434    
South: 35.663 

Great Barrier Reef:    
North: 9.08    
West: 143.52   
South: 24.06    
East: 152.42 

These sites were both selected off of [GEBCO's Grid Subsetting Application](https://download.gebco.net/). This application contains several years worth of topography data, and can specifically select an exact coordinate box to pull data from. For this program to function properly, the old data and new data should be downloaded using the exact same coordinates; the code relies on the old and new data matching in size, and therefore requires identical subsections for comparison. 

### User To-Do
1) create environment using GLY4930FinalProject.yml file
2) open jupyter lab, and open FinalProject.ipynb
3) cell 3 requires user input; user must update and include
   - file path to old data
   - file path to new data
   - year of old data
   - year of new data
   - 4 coordinates from the data's location

### NOTE: 
The color maps chosen were specifically selected for underwater areas, and will therefore will appear misleading above sea level.

## Author
The project was authored by Sydney Vargo. 
