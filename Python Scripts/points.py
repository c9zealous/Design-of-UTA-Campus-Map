import sqlite3
from PyQt4. QtCore import *
from PyQt4. QtGui import *
from qgis. core import *
from qgis. gui import *
from qgis. networkanalysis  import *

conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
c = conn.cursor()
conn.enable_load_extension(True)
c.execute("select load_extension('mod_spatialite')")
c.execute('select ST_X(geom),ST_Y(geom) from Points')
points = []
for row in c.fetchall():
    points.append(QgsPoint(row[0],row[1]))
print points
layer =  QgsVectorLayer('Point', 'PointQuery' , "memory")
dr = layer.dataProvider() 
for point in points: 
    pt=QgsFeature()
    pt.setGeometry(QgsGeometry.fromPoint(point))
    dr.addFeatures([pt])
    layer.updateExtents()
QgsMapLayerRegistry.instance().addMapLayers([layer])


