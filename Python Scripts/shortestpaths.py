from PyQt4. QtCore import *
from PyQt4. QtGui import *
from qgis. core import *
from qgis. gui import *
from qgis. networkanalysis  import *
import sqlite3
import math
import datetime

def sp(src,dst):
    print src
    print dst
    #vectorLayer = qgis.utils.iface.mapCanvas().currentLayer() 
    #vectorLayer = QgsProject.instance().mapLayersByName('Paths')
    vectorLayer=None
    for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
        if lyr.name() == "Paths":
            vectorLayer = lyr
            break
    director = QgsLineVectorLayerDirector (vectorLayer,-1,'1','-1','0',3) 


    conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
    c = conn.cursor()
    conn.enable_load_extension(True)
    c.execute("select load_extension('mod_spatialite')")
    c.execute('select st_x(geom),st_y(geom) from Points where name="'+src+'"')
    source=''
    dest=''
    for row in c.fetchall():
        source = QgsPoint(row[0],row[1])
    c.execute('select st_x(geom),st_y(geom) from Points where name="'+dst+'"')    
    for row in c.fetchall():
        dest = QgsPoint(row[0],row[1])

    properter = QgsDistanceArcProperter() 
    director.addProperter(properter) 
    crs = qgis.utils.iface . mapCanvas().mapRenderer().destinationCrs() 
    builder = QgsGraphBuilder(crs)


    tiedPoints = director. makeGraph ( builder ,  [ source ,dest ]  ) 
    graph = builder. graph ( )
     
    tSource = tiedPoints [0] 
    tDest = tiedPoints [1]
     
    idSource = graph. findVertex ( tSource ) 
    idDest = graph. findVertex ( tDest )
     
    (tree,cost)  = QgsGraphAnalyzer.dijkstra(graph,idSource,0)
     
    if tree [ idDest ]  == - 1 :
       print  "No Available Path" 
    else :
        points =  [ ]  
        curPos = idDest
        while curPos != idSource:
            points. append ( graph. vertex ( graph. arc ( tree [ curPos ]  ) . inVertex ( )  ) . point ( )  ) 
            curPos = graph. arc ( tree [ curPos ]  ) . outVertex ( ) ;
     
        points. append ( tSource )
        
        distance = QgsDistanceArea()
        
        i=1
        m=0
        while i<len(points):
            m += distance.measureLine(points[i-1],points[i])
            i += 1
        
        print 'Distance : '+str(m*100000)+' m'
        miles = 0.000621371 * m *100000
        tseconds = (miles*60*60)/(3.0)
        print 'Time taken on the basis of 3 miles/hour: '+str(datetime.timedelta(seconds=tseconds))
        layer =  QgsVectorLayer('LineString', 'ShortestPath' , "memory")
        pr = layer.dataProvider() 
        line = QgsFeature()
        line.setGeometry(QgsGeometry.fromPolyline(points))
        pr.addFeatures([line])
        layer.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayers([layer])
        qgis.utils.iface.messageBar().clearWidgets() 