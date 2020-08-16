# Job Site Web Scraper
This tool will scrape the job listing sites Indeed, Monster and Flexjobs for jobs featuring specific configurable settings and keywords. After completion of scraping, that data can be presented in various manners. 

NOTE: No built in proxy settings, use at own risk. If searching for many terms, there is a good chance of having your IP be blocked from visiting one or more of the sites.

# Scraping and Parsing

Data will be scraped, according to settings setup in your configuration file. There, edit several options for each of the different job sites. Scraping is accomplished using URL generation and the grequests package, for asynchronous scraping requests. As stated above, there is no built in proxy, so it is very possible that one or more of the sites may block your IP with prolonged or frequent scraping.

HTML collected through scraping will be parsed using BeautifulSoup4, to collect various info from the job listings, including job titles, links, location, summaries, companies, date posted and even whether or not a job is remote, should the information be available. Then, for every job with a location, a Latitude and Longitude will be generated using the geopy package, with Nominatim. This process will take the most time.

Parsed Data is stored in a locally in a MySQL database instance. The MySQL database instance must be up and running before beginning scraping and parsing. Username and Password for your MySQL instance must be input in the configuration file, as well as a name for the database that will be created.

To create or update database, run the command ```./main.py --update_db --config_path config.cfg```

![Scraping Image](https://github.com/jacobhutchinson/Job-Site-Web-Scraper/blob/master/images/scraper.PNG)

# Viewing Options

## Map View

Map view allows you to select several search terms simultaneously from your database that you have previously scraped for, selects the most recent scrape results for each site and displays their locations on a map. The plotting is done using the Geoviews package, and the output is displayed in your browser using a bokeh server instance. Pan and zoom over the map and hover over job listings to get details. All job listings that do not have locations (such as remote jobs) are not shown. All identical job locations are scraped into one, larger circle on the map, so larger circles implies more jobs at that location.

To initiate map view, run ```./main.py --view_map --config_path config.cfg```

![Map Image](https://github.com/jacobhutchinson/Job-Site-Web-Scraper/blob/master/images/map.PNG)

## Location View

Location view allows to select several search terms simultaneously from your database that you have previously scraped for and view all jobs within a certain (geodesic) distance of a given location on a map. Geodesic distance calculated using geopy package and the plotting is done using the Geoviews package with the touput being displayed in your browser using a bokeh server instance. Pan and zoom over the map and hover over job listings to get details. All job listings that do not have locations (such as remote jobs) are not shown. All identical job locations are scraped into one, larger circle on the map, so larger circles implies more jobs at that location.

To initiate location view, run ```./main.py --view_loc --config_path config.cfg```

![Location Image](https://github.com/jacobhutchinson/Job-Site-Web-Scraper/blob/master/images/location.PNG)

## Remote Job Listings

You can also list all remote jobs from several search terms simultaneously from your database, displayed in your console with tiles, companies, summaries and links to the job listings.

![Remote Image](https://github.com/jacobhutchinson/Job-Site-Web-Scraper/blob/master/images/remote.PNG)

# Setup
1. Setup the environment using conda and the environment.yml file by running ```conda env create -f environment.yml``` and activate the environment using ```conda activate scraper```
2. Start your local MySQL server instace
3. Fill in config settings, including MySQL username and password and a name for the MySQL database that will be created
4. Run main.py file with various options. To see all configurations, run ```./main.py --help```
