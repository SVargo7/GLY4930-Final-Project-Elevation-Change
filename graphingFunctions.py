# imports
import pandas as pd
import numpy as np
import rioxarray as rxr

import cartopy.crs as ccrs
from cartopy.io import srtm
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cmocean
from matplotlib.colors import LightSource
import matplotlib.colors as colors
from matplotlib.colors import TwoSlopeNorm
import pyvista as pv



# ----------------------------------------------------------------------------------------------



# 2d graphing function

def twoDGraphing(filePathOld, filePathNew, north, south, east, west, oldDataYear, newDataYear):
    
    # open up data files
    oldData = rxr.open_rasterio(filePathOld, masked = True)
    newData = rxr.open_rasterio(filePathNew, masked = True)

    # gather values for each
    elevationOld = oldData.squeeze().values
    longitudeOld = oldData.x.values
    latitudeOld = oldData.y.values
    
    elevationNew = newData.squeeze().values
    longitudeNew = newData.x.values
    latitudeNew = newData.y.values

    # ------------------------------------------------------------------------------------------
    
    # plot old data
    oldFig = plt.figure(figsize=(7, 7), layout='constrained')
    
    # set map location 
    ax = plt.axes(projection=ccrs.LambertConformal(
        central_longitude= (west+east) / 2.0,       
        central_latitude = (north+south) / 2.0,         
        standard_parallels=(south + ((north-south)/4.0), north - ((north-south)/4.0)), 
        cutoff=0
    ))
    
    ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())
    
    # add map features
    ax.coastlines(color='black', linewidth=1)
    
    left, bottom, right, top = oldData.rio.bounds()

    # create map
    topo = ax.imshow(elevationOld, 
                     cmap='cmo.ice', 
                     extent=[left, right, bottom, top], 
                     origin='upper',
                     transform=ccrs.PlateCarree()
                    )
    
    # hillshade
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(elevationOld, vert_exag=1.0)
    
    ax.imshow(hillshade,
              cmap='gray',
              alpha=0.35,
              extent=[left, right, bottom, top],
              origin='upper',
              transform=ccrs.PlateCarree())
    
    # color bar
    cbar = oldFig.colorbar(topo, ax=ax, location='right', shrink=0.7)
    cbar.set_label('Elevation above/below Sea Level (m)', fontsize=11, fontweight='bold')
    
    # include gridlines and title
    ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, color = 'gray') 
    ax.set_title(f"Old Data: {oldDataYear} 2D Model", fontweight='bold')
    
    # longitude label
    ax.text(0.5, -0.22, 'Longitude', 
            va='bottom', ha='center', 
            rotation='horizontal', 
            transform=ax.transAxes, 
            fontsize=12, fontweight='bold')
    
    # latitude label 
    ax.text(-0.16, 0.5, 'Latitude', 
            va='center', ha='left', 
            rotation='vertical', 
            transform=ax.transAxes, 
            fontsize=12, fontweight='bold')

    # show plot 
    plt.show()

    # ------------------------------------------------------------------------------------------
    
    # plot new data
    newFig = plt.figure(figsize=(7, 7), layout='constrained')

    # set map location 
    ax = plt.axes(projection=ccrs.LambertConformal(
        central_longitude= (west+east) / 2.0,       
        central_latitude = (north+south) / 2.0,         
        standard_parallels=(south + ((north-south)/4.0), north - ((north-south)/4.0)), 
        cutoff=0
    ))
    
    ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())
    
    # add map features
    ax.coastlines(color='black', linewidth=1)
    
    left, bottom, right, top = newData.rio.bounds()

     # create map
    topo = ax.imshow(elevationNew, 
                     cmap='cmo.ice', 
                     extent=[left, right, bottom, top], 
                     origin='upper',
                     transform=ccrs.PlateCarree()
                    )
    
    # color bar
    cbar = newFig.colorbar(topo, ax=ax, location='right', shrink=0.7)
    cbar.set_label('Elevation above/below Sea Level (m)', fontsize=11, fontweight='bold')
    
    # hillshade
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(elevationNew, vert_exag=1.0)
    
    ax.imshow(hillshade,
              cmap='gray',
              alpha=0.35,
              extent=[left, right, bottom, top],
              origin='upper',
              transform=ccrs.PlateCarree())
    
    # include gridlines and title
    ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, color = 'gray') 
    ax.set_title(f"New Data: {newDataYear} 2D Model", fontweight='bold')
    
    # longitude label
    ax.text(0.5, -0.22, 'Longitude', 
            va='bottom', ha='center', 
            rotation='horizontal', 
            transform=ax.transAxes, 
            fontsize=12, fontweight='bold')
    
    # latitude label 
    ax.text(-0.16, 0.5, 'Latitude', 
            va='center', ha='left', 
            rotation='vertical', 
            transform=ax.transAxes, 
            fontsize=12, fontweight='bold')

    # show plot
    plt.show()

    # ------------------------------------------------------------------------------------------

    # calculate difference between old and new data
    rows, cols = elevationOld.shape
    elevationDifference = np.zeros((rows, cols))
    
    for i in range(rows):
        for j in range(cols):
            oldElevationPoint = elevationOld[i][j]
            newElevationPoint = elevationNew[i][j]
    
            elevationDifference[i][j] = newElevationPoint - oldElevationPoint

    # gather greatest positive and greatest negative differences
    greatestPosDifference = elevationDifference.max()
    greatestNegDifference = elevationDifference.min()

    # scale for building color bar - have color bar maxes at 30th % for additional color emphasis 
    topScale = .3 * greatestPosDifference  
    bottomScale = .3 * greatestNegDifference
    
    if (topScale > abs(bottomScale)):
        colorBarScale = topScale
    else:
        colorBarScale = abs(bottomScale)

    # ------------------------------------------------------------------------------------------

    # plot the elevation difference 
    diffFig = plt.figure(figsize=(7, 7), layout='constrained')
    
    # set map location 
    ax = plt.axes(projection=ccrs.LambertConformal(
        central_longitude= (west+east) / 2.0,       
        central_latitude = (north+south) / 2.0,         
        standard_parallels=(south + ((north-south)/4.0), north - ((north-south)/4.0)), 
        cutoff=0
    ))
    
    ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())
    
    # add map features
    ax.coastlines(color='black', linewidth=1)
    
    left, bottom, right, top = newData.rio.bounds()

    # color bar scaling
    norm = colors.TwoSlopeNorm(vmin=-colorBarScale, vcenter=0, vmax=colorBarScale) 

    # create map
    topo = ax.imshow(elevationDifference, 
                     cmap='seismic', 
                     norm=norm,
                     extent=[left, right, bottom, top], 
                     origin='upper',
                     transform=ccrs.PlateCarree()
                    )
    
    # color bar
    cbar = diffFig.colorbar(topo, ax=ax, location='right', shrink=0.7, extend='both')
    cbar.set_label('Elevation above/below Sea Level (m)', fontsize=11, fontweight='bold')
    
    # hillshade
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(elevationDifference, vert_exag=1.0)
    
    ax.imshow(hillshade,
              cmap='gray',
              alpha=0.35,
              extent=[left, right, bottom, top],
              origin='upper',
              transform=ccrs.PlateCarree())
    
    # include gridlines and title
    ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, color = 'gray') 
    ax.set_title(f"Elevation Difference from {oldDataYear} to {newDataYear} (2D Model)", fontweight='bold')
    
    # longitude label
    ax.text(0.5, -0.22, 'Longitude', 
            va='bottom', ha='center', 
            rotation='horizontal', 
            transform=ax.transAxes, 
            fontsize=12, fontweight='bold')
    
    # latitude label 
    ax.text(-0.16, 0.5, 'Latitude', 
            va='center', ha='left', 
            rotation='vertical', 
            transform=ax.transAxes, 
            fontsize=12, fontweight='bold')

    # show plot
    plt.show()



# ----------------------------------------------------------------------------------------------



# 3d graphing function

def threeDGraphing(filePathOld, filePathNew, north, south, east, west, oldDataYear, newDataYear):

    # open up data files
    oldData = rxr.open_rasterio(filePathOld, masked = True)
    newData = rxr.open_rasterio(filePathNew, masked = True)

    # gather values for each
    elevationOld = oldData.squeeze().values
    longitudeOld = oldData.x.values
    latitudeOld = oldData.y.values
    
    elevationNew = newData.squeeze().values
    longitudeNew = newData.x.values
    latitudeNew = newData.y.values

    # ------------------------------------------------------------------------------------------

    # plot old data
    
    # create grid that steps (improves timing)
    step = 2
    
    elevationOldThreeD = elevationOld[::step, ::step]
    
    xOld = oldData.x.values[::step]
    yOld = oldData.y.values[::step]
    
    XOld, YOld = np.meshgrid(xOld, yOld)
    
    # specific math to convert latitude/longitude/coordinates that allow for better visualization
    latAvg = np.mean(yOld)
    x_m = (xOld - xOld.min()) * 111320 * np.cos(np.deg2rad(latAvg))
    y_m = (yOld - yOld.min()) * 111320
    XOld, YOld = np.meshgrid(x_m, y_m)
    
    # create grid w/ vertical exaggeration
    grid = pv.StructuredGrid(XOld, YOld, elevationOldThreeD)
    
    verticalExaggeration = 20
    grid.points[:, 2] *= verticalExaggeration
    
    grid["ElevationOld"] = elevationOldThreeD.ravel(order="F")
    
    # build figure and plot data 
    plotter = pv.Plotter(window_size=(800,800))
    
    plotter.add_mesh(
        grid,
        scalars = "ElevationOld",
        cmap = "cmo.ice",
        smooth_shading =True,
        lighting = True,
    )
    
    # add features
    plotter.add_axes()
    plotter.add_title(f"Old Data: {oldDataYear} 3D Model")
    
    plotter.show_grid(
        xtitle = "Longitude",
        ytitle = "Latitude",
        ztitle = "Elevation (m)"
    )
    
    # show plot & make moveable
    plotter.view_isometric()
    plotter.reset_camera()
    
    plotter.show()

    # ------------------------------------------------------------------------------------------

    # plot new data
    
    # create grid that steps (improves timing)
    elevationNewThreeD = elevationNew[::step, ::step]
    
    xOld = oldData.x.values[::step]
    yOld = oldData.y.values[::step]
   
    XOld, YOld = np.meshgrid(xOld, yOld)
    
    # specific math to convert latitude/longitude/coordinates that allow for better visualization
    # uses old data, but coordinates for all three maps are the same, so sizing is the same
    latAvg = np.mean(yOld)
    x_m = (xOld - xOld.min()) * 111320 * np.cos(np.deg2rad(latAvg))
    y_m = (yOld - yOld.min()) * 111320
    XOld, YOld = np.meshgrid(x_m, y_m)
    
    # create grid w/ vertical exaggeration
    grid = pv.StructuredGrid(XOld, YOld, elevationNewThreeD)
    
    verticalExaggeration = 20
    grid.points[:, 2] *= verticalExaggeration
    
    grid["ElevationNew"] = elevationNewThreeD.ravel(order="F")
    
    # build figure and plot data 
    plotter = pv.Plotter(window_size=(800,800))
    
    plotter.add_mesh(
        grid,
        scalars = "ElevationNew",
        cmap = "cmo.ice",
        smooth_shading = True,
        lighting = True,
    )
    
    # add features
    plotter.add_axes()
    plotter.add_title(f"New Data: {newDataYear} 3D Model")
    
    plotter.show_grid(
        xtitle = "Longitude",
        ytitle = "Latitude",
        ztitle = "Elevation (m)"
    )
    
    # show plot & make moveable
    plotter.view_isometric()
    plotter.reset_camera()
    
    plotter.show()

    # ------------------------------------------------------------------------------------------

    # calculate difference between old and new data
    rows, cols = elevationOld.shape
    elevationDifference = np.zeros((rows, cols))
    
    for i in range(rows):
        for j in range(cols):
            oldElevationPoint = elevationOld[i][j]
            newElevationPoint = elevationNew[i][j]
    
            elevationDifference[i][j] = newElevationPoint - oldElevationPoint

    # gather greatest positive and greatest negative differences
    greatestPosDifference = elevationDifference.max()
    greatestNegDifference = elevationDifference.min()

    # scale for building color bar - have color bar maxes at 30th % for additional color emphasis 
    topScale = .3 * greatestPosDifference  
    bottomScale = .3 * greatestNegDifference
    
    if (topScale > abs(bottomScale)):
        colorBarScale = topScale
    else:
        colorBarScale = abs(bottomScale)

    # ------------------------------------------------------------------------------------------

    elevationDifferenceThreeD = elevationDifference[::step, ::step]

    # set coordinates/grid with the old data values 
    xOld = oldData.x.values[::step]
    yOld = oldData.y.values[::step]
    
    XOld, YOld = np.meshgrid(xOld, yOld)
    
    # specific math to convert latitude/longitude/coordinates that allow for better visualization
    # uses old data, but coordinates for all three maps are the same, so sizing is the same
    latAvg = np.mean(yOld)
    x_m = (xOld - xOld.min()) * 111320 * np.cos(np.deg2rad(latAvg))
    y_m = (yOld - yOld.min()) * 111320
    XOld, YOld = np.meshgrid(x_m, y_m)
    
    # create grid w/ vertical exaggeration and map the difference
    grid = pv.StructuredGrid(XOld, YOld, elevationDifferenceThreeD)
    
    verticalExaggeration = 20
    grid.points[:, 2] *= verticalExaggeration
    
    grid["ElevationDifference"] = elevationDifferenceThreeD.ravel(order="F")
    
    # build figure and plot data 
    plotter = pv.Plotter(window_size=(800,800))
    
    plotter.add_mesh(
        grid,
        scalars = "ElevationDifference",
        cmap = "seismic",
        clim=(-colorBarScale, colorBarScale),
        smooth_shading =True,
        lighting = True,
    )
    
    # add features
    plotter.add_axes()
    plotter.add_title(f"Elevation Difference from {oldDataYear} to {newDataYear} (3D Model)")
    
    plotter.show_grid(
        xtitle = "Longitude",
        ytitle = "Latitude",
        ztitle = "Elevation (m)"
    )
    
    # show plot & make moveable
    plotter.view_isometric()
    plotter.reset_camera()
    
    plotter.show()