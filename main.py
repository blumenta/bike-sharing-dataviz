import pandas as pd
import holoviews as hv
import bokeh
hv.extension('bokeh')
import param
import panel
import geoviews as gv, cartopy.crs as crs
from geoviews.tile_sources import EsriImagery
from geoviews import dim, opts
import utils


names = utils.get_contract_names()
stations = utils.get_all_bike_data()
topts = dict(width=1000, height=700, bgcolor='black', xaxis=None, yaxis=None, show_grid=False)
tiles = EsriImagery.clone(crs=crs.GOOGLE_MERCATOR).options(**topts)

class BikeStandExplorer(param.Parameterized):
    city_name = param.ObjectSelector(default="lyon", objects=names.to_list())
    def make_view(self):
        dfc = stations[stations['contractName'] == self.city_name]
        gv_df = gv.Dataset(dfc[['longitude', 'latitude', 'name', 'bikes_available_total']])
        points = gv_df.to(gv.Points, ['longitude', 'latitude'], ['name', 'bikes_available_total'])
        return (tiles * points).opts(opts.Points(tools=['hover'],
                                                 size=dim('bikes_available_total'),
                                                 color='bikes_available_total',
                                                 cmap='viridis'))
explorer = BikeStandExplorer(name="Bike Stand Explorer: streaming live from JCDecaux API")
panel.Column(explorer, explorer.make_view).servable()
