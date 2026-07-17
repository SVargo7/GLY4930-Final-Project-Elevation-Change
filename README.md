# GLY4930-Final-Project-Elevation-Change

## Description
This project automates visual representation of differences in elevation over time. It takes two different sets of data from different times over the same coordinate area and creates visuals of the elevation changes. The first visual is in 2D; it gives a flat map with color exaggeration of which areas increased or decreased in elevation. The second visual provides a moveable 3D representation of the increases and decreases. This program creates and uses two functions, twoDGraphing and threeDGraphing. 

## Installation
This project is built to operate in its own environment created from the GLY4930FinalProject.yml file. In order to create a new environment for the project's specifications, download the .yml file and run the following command in the terminal: 

    conda env create -f GLY4930FinalProject.yml

This will allow for all packages and dependencies to be included properly. Unless specified, the new environment will be called svFinalProj, and can be activated using:

    conda activate svFinalProj

and deactivated with:

    conda deactivate

## Packages & Dependencies 
The code uses the following dependencies to operate: 

- python=3.12

- jupyterlab
- ipykernel
- ipywidgets
  
- numpy
- pandas
- matplotlib

- cartopy
- rioxarray
  
- pyvista
- cmocean
  
- pip
- pip:
   - "pyvista[jupyter]"
   - gstatsim==1.1.5
 
These are all included in the .yml file, and will be automatically installed in the new environment. 

## Opening the Project
Once the environment is created and activated, run "jupyter lab" and move both code files in. The two code files are included in the "projectCode" folder. Download SVFinalProjUserFile.ipynb and graphingFunctions.py into your preferred folder (ensure that they are in the same folder, or adjust the import statements at the top of the .ipynb file). In the SVFinalProjUserFile.ipynb file, the example is structured to call the data within folders named "midOceanRidge" and "greatBarrierReef." When downloading, ensure to adjust the file paths in the function calls to the correct data to avoid errors. Downloadable data can be located in the "data" folder.

### Data Collection & Recommended Data Resource:
The two example data sets in this repository include 2020 and 2026 Mid Ocean Ridge data, as well as 2020 and 2026 Great Barrier Reef data. The coordinates for these sites are as follows:

Mid Ocean Ridge:   
North: 43.131    
West: -33.299   
East: -23.434    
South: 35.663 

Great Barrier Reef:    
North: -9.08    
West: 143.52   
South: -24.06    
East: 152.42 

These sites were both selected off of [GEBCO's Grid Subsetting Application](https://download.gebco.net/). This application contains several years worth of topography data, and can specifically select an exact coordinate box to pull data from. For this program to function properly, the old data and new data should be downloaded using the exact same coordinates; the code relies on the old and new data matching in size, and therefore requires identical subsections for comparison. 

### Note: 
1) The color maps chosen were specifically selected for underwater areas, and will therefore will appear misleading above sea level. Color maps can be manually changed within the graphingFunctions.py file.
2) This project was also built to act as a template for any data from any part of the world, so factors such as the scaling and vertical exaggeration may need to be adjusted depending on the location of the data. Once again, these can be manually altered in the graphingFunctions.py file. 

## Author
The project was authored by Sydney Vargo. 
