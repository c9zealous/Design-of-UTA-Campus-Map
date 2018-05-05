import sqlite3
from PyQt4.QtCore import *
from PyQt4. QtGui import *
from qgis. core import *
from qgis. gui import *
from qgis.utils import *
from qgis.networkanalysis import *

conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
c = conn.cursor()
conn.enable_load_extension(True)
c.execute("select load_extension('mod_spatialite')")
c.execute('select id,st_numpoints(st_boundary(geom)) from Polygons')
layer =  QgsVectorLayer('Polygon', 'PolygonQuery' , "memory")
dr = layer.dataProvider() 
for row in c.fetchall():
    points = []
    for x in range(1 , row[1]):
        c.execute('select st_x(st_pointn(st_boundary(geom),'+str(x)+')),st_y(st_pointn(st_boundary(geom),'+str(x)+')) from Polygons where id='+str(row[0]))
        for coord in c.fetchall():
            points.append(QgsPoint(coord[0],coord[1]))
    polygon = QgsFeature()
    polygon.setGeometry(QgsGeometry.fromPolygon([points]))
    dr.addFeatures([polygon])
    layer.updateExtents()        
   
QgsMapLayerRegistry.instance().addMapLayers([layer])


