# Accessibility Analysis of Health Care Facilities and Specialists

Health care access is one of the most important aspects of each society. Irrespective of the part of the world, each child and adolescence deserve equal access to primary health care (PHC) facilities. Demographic changes such as ageing population or a substantial increase in births can further stretch health care systems, deepening the inequities in accessing to essential health care. Armed conflicts cause migration of people, putting a strain on already stretched health systems, damages to the road network can substantially impede the access to essential health care. Targeted attacks on health facilities have occurred in Syria, Yemen or Iraq infringing upon the  International Humanitarian Law. To help to identify populations at risk for insufficient health care access we will create maps of health facilities and specialists, isolines and choropleths of the population with health care access, taking into account the driving distance to the nearest health facility or specialist. Those types of maps can pinpoint the areas most in need of development, either in health care and infrastructure.

The repository will walk you through the process of conducting health care accessibility analysis, 
which encompasses the gathering of indispensable data, preparing it for further analysis (clipping, reprojecting, filtering), and creating the following three types of maps:
- map of health care facilities,
- map of health care access isolines,
- choropleth of the population with health care access.

The second part of the project encompasses the extraction with `Scrapy spiders` data regarding health specialists and performing the analysis of that data by creating the map of health specialists, isolines and choropleth. For example, the specializations may be as follows (depending on the data source):
- medical oncology
- general surgery
- radiotherapy
- urologist, and others.

### Table of contents

* [Download and prepare data](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/1_data_processing.ipynb)
 	
	In this notebook, we are going to download and prepare the data that is required to conduct the analysis of the health facilities accessibility. The data includes the following:

    - Administrative boundaries of a country at level 2 (second sub-national level) from the <i>GADM Database of Global Administrative Areas</i>
    - Health care location data from <i>healthsites.io</i>
    - Distribution of the population as the spatial raster dataset from <i>European Commission Global Human Settlement GHS-POP</i> dataset


* [Openrouteservice health facilities access isolines](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/2_vocabulary.ipynb)
	
	In this notebook we will use the <i>Openrouteservice API</i> to compute the isolines for health facilities, we will also create the following maps:
	- Map of health care facilities
	- Map of health care access isolines
	- Choropleth of the population with health care access

 * [OSMNX health facilities access isolines](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/2_vocabulary.ipynb)

	This notebook covers the use of the `OSMNX` library to compute the isolines for health facilities, but also we will create the same types of maps as in the previous notebook.

 * [Health specialists access isolines](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/2_vocabulary.ipynb)

	In this notebook we are going to obtain the data regarding the health specialists. Depending on the country of interest the process of data retrieving will be different (for example using `Scrapy spiders` to scrap the data from the website)

	We will create the following three types of maps:
	- Map of health specialists
	- Map of health specialists access isolines
	- Choropleth of the population with access to health specialists

 * [Utilities](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/2_vocabulary.ipynb)

	Python file that includes the following:
	- Definitions of the `ORS` and `photon` geocoders
	- Definitions of the helper functions.
	- Your <i>Openrouteservice API</i> key.
	- <i>ISO 3166 alpha-3</i> country codes

 * [ven_health_spec_spider](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/2_vocabulary.ipynb)

	Implementation of the `Scrapy Spider` that extracts the health specialists data for Venezuela from <http://oncologia.org.ve/site/estructuras/>

 * [nam_health_spec_spider](https://nbviewer.jupyter.org/github/radoslawkrolikowski/sentiment-analysis-pytorch/blob/master/2_vocabulary.ipynb)

	Implementation of the `Scrapy Spider` that extracts the health specialists data for Namibia from <http://www.methealth.com.na/doctor_types.php>

### Map examples

You can find the maps in HTML format for Venezuela in `Venezuela` directory.

![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)

### Dataset

Datasets used in this project are listed in the <i>Download and prepare data</i> and <i>References</i> sections.

Data is going to be stored in a folder structure according to the following template:

   {Country_name}\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Administrative_boundaries/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Health_facilities/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Population/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Roads/

`World_population_data/` directory contains the global population data, downloaded from the <i>European Commission Global Human Settlement</i> website.


### Requirements

1. Create a virtual environment (conda, virtualenv etc.).

	`conda create -n <env_name> python=3.7`

2. Activate your environment.

	`conda activate <env_name>`

3. Create a new kernel.

	`pip install ipykernel`

	`python -m ipykernel install --user --name <env_name>`

4. Go to the directory: `.local/share/jupyter/kernels/<env_name>` and ensure that *kernel.json* file contains the path to your environment python interpreter (can be checked by `which python` command).

  ```
  {
   "argv": [
    "home/user/anaconda3/envs/<env_name>/bin/python",
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}"
   ],
   "display_name": "<env_name>",
   "language": "python"
  }
  ```
5. Install `GDAL`.

	- `conda install -c conda-forge gdal` 

6. Install requirements.

	- `pip install -r requirements.txt`

	- In case of issues with the `rasterio` library installation visit <https://rasterio.readthedocs.io/en/latest/installation.html> to find out more.

7. Install `ogr2osm`.

	To be able to convert shapefiles to OSM format we have to install the `ogr2osm`.
	- `git clone --recursive https://github.com/pnorman/ogr2osm`
	To update the repository:
	- `cd ogr2osm`
	- `git pull`
	- `git submodule update`

	For more information regarding the installation and required dependencies visit: <https://github.com/pnorman/ogr2osm>

8. Restart your environment.

	`conda deactivate`
    
	`conda activate <env_name>`

### References

* <https://gadm.org/>
* <https://healthsites.io/>
* GHS-POP Population dataset - <http://data.europa.eu/89h/0c6b9751-a71f-4062-830b-43c9f432370f>:
Dataset: Schiavina, Marcello; Freire, Sergio; MacManus, Kytt (2019): GHS population grid multitemporal (1975-1990-2000-2015), R2019A. European Commission, Joint Research Centre (JRC) [Dataset] doi:10.2905/0C6B9751-A71F-4062-830B-43C9F432370F PID: http://data.europa.eu/89h/0c6b9751-a71f-4062-830b-43c9f432370f
Concept & Methodology: Freire, Sergio; MacManus, Kytt; Pesaresi, Martino; Doxsey-Whitfield, Erin; Mills, Jane (2016): Development of new open and free multi-temporal global population grids at 250 m resolution. Geospatial Data in a Changing World; Association of Geographic Information Laboratories in Europe (AGILE). AGILE 2016.
* <http://oncologia.org.ve/site/estructuras/>
* <http://www.methealth.com.na/doctor_types.php>


