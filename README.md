# Places.xyz Google Maps Integration
## Overview
A quick script written in python to show off the global coverage of the __places.xyz__ project.

## Instructions
- Install requirements with `pip3 -r install requirements.txt` (Python 3.8.x required)
- Set environment variables in `settings.env` and run `source settings.env` before calling the main script
- If you want to change the theme, choose from supported themes in `data/themes.txt`
- `python3 places_mapper.py`
- Open your your generated HTML file in any web browser. Default save dir is `/tmp/map.html`

## Considerations:
- I haven't integrated the rest of the places.xyz metadata to the map as I overran on time I alloted for this project. Still, the data is pulled and formatted so rendering it is as simple as working Folium's [Marker API](https://python-visualization.github.io/folium/modules.html#folium.map.Marker, "link to documentation")
- Currently, the algo pulls data from chain every time. Caching could be added really easily but I'm lazy. 
- The current renderer will scale to keep all map points in view, no matter how geographically distance they are (the centre of the map at launch is the average latitude and average longitude of all places in the project). 
	- In the future, this behaviour might need to be changed as sufficiently distance places will eventually mean the map intitializes to a view of the whole world (though maybe this is desired?)
- I don't care to mess around with formal licensing, just assume this code is under the most permissing license possible. Do as you will.
