# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from .meta import topocollections, geocollections, intersections
from .intersection import Intersection
from bw2data import DataStore, JsonWrapper


class Topography(DataStore):
    """A topographical description of a `geocollection`.

    A topography must be registered to exactly one geocollection.

    For example, the geocollection 'countries' could have the location 'Ghana', and include a spatial data file which defines 'Ghana'. The `Topography` 'countries-topo' would have two files:

        #. A mapping file that linked each location in the geocollection 'countries' to a set of topographical faces
        #. A spatial dataset which defines the topographical faces

    Topographies can make some calculations much quicker for two reasons:

        #. Large features are split into smaller faces, making GIS calculations easier and spatial index queries more efficient, as bounding boxes are smaller
        #. You only do GIS work on each topographical face once

    The LCA classes in `bw2regional` don't work directly with the `Topography` objects; rather, GIS calculations on topographies can be merged to the spatial features of the `geocollection`.

    TODO: What default topographies are installed, if any?

    The usual order of operations with a `geocollection` that has a `Topography` is the following:

        #. Create a `geocollection`, including defining a spatial dataset
        #. Create a new `topocollection` and specify the linked `geocollection`. You can also optionally define another spatial dataset, using the same format as for `geocollections`.
        #. Instantiate the new `Topography` object created in the earlier step, and write mapping data from spatial features in the `geocollection`(s) to face ids in the `Topography` spatial data set.

    The data format for mapping data is ``{feature field value: [list of topo field values (usually id numbers)]}``.

    Here is a code sample for using the test data in `bw2regional`:

    .. code-block:: python

        from bw2regional import Topography, geocollections
        from bw2regional.tests import data_dir
        import json

        geocollections['countries'] = {
            'filepath': os.path.join(data_dir, "test_countries.gpkg"),
            'field': 'name'
        }
        topocollections['countries-topo'] = {
            'geocollection': 'countries',
            'filepath': os.path.join(data_dir, "test_provinces.gpkg"),
            'field': 'OBJECTID_1'
        }
        topo = Topography('countries-topo')
        topo.write(json.load(open(os.path.join(data_dir, "test_topo_mapping.json"))))

    """
    _metadata = topocollections

    def write(self, data):
        self.metadata['empty'] = False
        self._metadata.flush()
        super(Topography, self).write(data)
