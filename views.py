# views.py: contains class for viewing given job information in various ways
import pandas as pd
import numpy as np
import geoviews as gv
import geoviews.tile_sources as gvts
from geoviews import dim, opts
from bokeh.models import HoverTool
import panel as pn

""" Class for viewing job data in various forms """
class Views():
    # Initialize the class
    def __init__(self):
        super(Views, self).__init__()
        gv.extension('bokeh')

    """ Converts data into pandas dataframe """
    def __convert_to_df(self, data):
        data_list = []
        for row in data:
            data_list.append(list(row))
        df = pd.DataFrame(data_list, columns=['Source', 'Search Term', 'ID', 'Title', \
                'Link', 'Remote', 'Location', 'Company', 'Summary', 'Date', 'Lat', \
                'Long', 'Num', 'Color', 'Desc'])
        return df

    """ Returns a formatted description of the given job data as a string """
    def job_desc(self, job_row):
        output = ''
        title = job_row[3]
        link = job_row[4]
        company = job_row[7]
        summary = job_row[8]
        output += title.upper() + '<br>'
        output = output + company + '<br><br>' if company is not None else output
        output = output + summary + '<br><br>' if summary is not None else output
        output = output + link + '<br>' if link is not None else output
        output += '----------------------------------------------'
        return output

    """ Lists out jobs with formatting """
    def list_jobs(self, data):
        for term in data:
            term_data = data[term]
            for job_row in term_data:
                print(self.job_desc(job_row).replace('<br>','\n'))

    """ View given data in map format """
    def map_view(self, data):
        locs = []
        final_data = []
        colors = ['#fc4f30', '#30a2da', '#4e9258', '#ede275', '#6f4e37']
        k = 0
        tooltips = """
                @Desc{safe}
                """
        hover = HoverTool(tooltips=tooltips)
        for term in data:
            term_color = colors[k]
            if k < len(colors) - 1:
                k += 1
            new_data = data[term]
            for job_row in new_data:
                job_row = list(job_row)
                new_latlong = []
                new_latlong.append(job_row[10])
                new_latlong.append(job_row[11])
                if [term, new_latlong] not in locs:
                    locs.append([term, new_latlong])
                    job_row.append(1)
                    job_row.append(term_color)
                    job_row.append(self.job_desc(job_row))
                    final_data.append(job_row)
                else:
                    for new_job_row in final_data:
                        if new_job_row[10] == new_latlong[0] and new_job_row[11] == new_latlong[1] \
                                and str(new_job_row[1]) == str(term):
                            new_job_row[12] += 1
                            new_job_row[14] += '<br>' + self.job_desc(job_row)
                            if type(new_job_row[3]) == list:
                                new_job_row[3].append(job_row[3])
                            else:
                                mt = []
                                mt.append(new_job_row[3])
                                new_job_row[3] = mt
                                new_job_row[3].append(job_row[3])
                            if type(new_job_row[4]) == list:
                                new_job_row[4].append(job_row[4])
                            else:
                                mt = []
                                mt.append(new_job_row[4])
                                new_job_row[4] = mt
                                new_job_row[4].append(job_row[4])
                            if type(new_job_row[8]) == list:
                                new_job_row[8].append(job_row[8])
                            else:
                                mt = []
                                mt.append(new_job_row[8])
                                new_job_row[8] = mt
                                new_job_row[8].append(job_row[8])
        final_df = self.__convert_to_df(final_data)
        final_df = final_df[final_df.Lat.notnull()]
        final_df = final_df.astype({'Lat': 'float64'})
        final_df = final_df.astype({'Long': 'float64'})
        final_df = final_df.astype({'Num': 'int64'})
        job_gv_points = gv.Points(final_df, ['Long', 'Lat'], ['Num', 'Color', 'Desc'])
        bokeh_server = pn.Row((gvts.CartoDark * job_gv_points).opts(opts.Points(
                width = 1400, height=800, alpha=0.3, hover_line_color='black',
                line_color='black', xaxis=None, yaxis=None, hover_fill_color=None,
                hover_fill_alpha=0.5, size=np.sqrt(dim('Num'))*10, tools = [hover], 
                color = dim('Color')))).show(port=12345)
        input()
        bokeh_server.stop()
        
