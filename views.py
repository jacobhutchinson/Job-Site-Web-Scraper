# views.py: contains class for viewing given job information in various ways
import pandas as pd
import numpy as np
import geoviews as gv
import geoviews.tile_sources as gvts
from geoviews import dim, opts

""" Class for viewing job data in various forms """
class Views():
    # Initialize the class
    def __init__(self):
        super(Views, self).__init__()

    """ Converts data into pandas dataframe """
    def __convert_to_df(self, data):
        for table in data:
            data = data[table]
        data_list = []
        for row in data:
            data_list.append(list(row))
        df = pd.DataFrame(data_list, columns=['Source', 'Search Term', 'ID', 'Title', \
                'Link', 'Remote', 'Location', 'Company', 'Summary', 'Date', 'Lat', 'Long'])
        return df

    """ View given data in map format """
    def map_view(self, data):
        gv.extension('matplotlib')
        job_df = self.__convert_to_df(data)
        job_gv_points = gv.Points(job_df, ['Lat', 'Long'], ['Title', 'Summary', 'Link'])
        #gvts.CartoDark * job_gv_points
        gv.save(job_gv_points, 'output.html')
