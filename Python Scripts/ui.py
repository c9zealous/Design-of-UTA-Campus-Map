from PyQt4 import QtCore, QtGui
import sqlite3
from PyQt4.QtCore import *
from PyQt4. QtGui import *
from qgis. core import *
from qgis. gui import *
from qgis.utils import *
from qgis.networkanalysis import *
import math
import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(518, 372)
        self.source = QtGui.QPushButton(Dialog)
        self.source.setGeometry(QtCore.QRect(120, 100, 93, 28))
        self.source.setObjectName(_fromUtf8("source"))
        self.destination = QtGui.QPushButton(Dialog)
        self.destination.setGeometry(QtCore.QRect(330, 100, 93, 28))
        self.destination.setObjectName(_fromUtf8("destination"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 70, 53, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(340, 70, 71, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(220, 150, 100, 16))
        self.label_3.setObjectName(_fromUtf8("label_2"))
        self.submitButton = QtGui.QPushButton(Dialog)
        self.submitButton.setGeometry(QtCore.QRect(220, 220, 93, 28))
        self.submitButton.setObjectName(_fromUtf8("submitButton"))
        self.submitButton.clicked.connect(lambda : self.sp(comboBox.currentText(),comboBox2.currentText(),comboBox3.currentText()))
        
        self.distanceLabel = QtGui.QLabel(Dialog)
        self.distanceLabel.setGeometry(QtCore.QRect(120, 270, 300, 16))
        self.distanceLabel.setObjectName(_fromUtf8("label"))
        self.timeLabel = QtGui.QLabel(Dialog)
        self.timeLabel.setGeometry(QtCore.QRect(120, 290, 350, 16))
        self.timeLabel.setObjectName(_fromUtf8("label"))
        self.errorLabel = QtGui.QLabel(Dialog)
        self.errorLabel.setGeometry(QtCore.QRect(210, 310, 350, 16))
        self.errorLabel.setObjectName(_fromUtf8("label"))
       
        comboBox = QtGui.QComboBox(Dialog)
        comboBox.setGeometry(QtCore.QRect(40, 100, 200, 28))
        
        comboBox2 = QtGui.QComboBox(Dialog)
        comboBox2.setGeometry(QtCore.QRect(300, 100, 200, 28))
        
        comboBox3 = QtGui.QComboBox(Dialog)
        comboBox3.setGeometry(QtCore.QRect(230, 170, 70, 28))
        comboBox3.addItems(['1','2','3','4','5','6','7','8','9','10'])
        conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select name from Points order by name')
        entrances = []
        for row in c.fetchall():
            entrances.append(row[0])
        print entrances
        comboBox.addItems(entrances)
        comboBox2.addItems(entrances)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Shortest Path", None))
        self.source.setText(_translate("Dialog", "Source", None))
        self.destination.setText(_translate("Dialog", "Destination", None))
        self.label.setText(_translate("Dialog", "Source", None))
        self.label_2.setText(_translate("Dialog", "Destination", None))
        self.label_3.setText(_translate("Dialog", "Speed (miles/hr)", None))
        self.submitButton.setText(_translate("Dialog", "Submit", None))
        
    def sp(self,src,dst,spd):
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
            self.errorLabel.setText(_translate("Dialog",'<b>No Available Path</b> ' , None))
            self.timeLabel.setText(_translate("Dialog",'' , None))
            self.distanceLabel.setText(_translate("Dialog",'' , None))
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
            tseconds = (miles*60*60)/int(spd)
            
            self.distanceLabel.setText(_translate("Dialog",'<b>Distance :</b> '+str(m*100000)+' m' , None))
            self.timeLabel.setText(_translate("Dialog",'<b>Time taken on the basis of '+spd+' miles/hour:</b> '+str(datetime.timedelta(seconds=tseconds)) , None))
            self.errorLabel.setText(_translate("Dialog",'' , None))
            print 'Time taken on the basis of '+spd+' miles/hour: '+str(datetime.timedelta(seconds=tseconds))
            layer =  QgsVectorLayer('LineString', 'ShortestPath' , "memory")
            pr = layer.dataProvider() 
            line = QgsFeature()
            line.setGeometry(QgsGeometry.fromPolyline(points))
            pr.addFeatures([line])
            layer.updateExtents()
            QgsMapLayerRegistry.instance().addMapLayers([layer])
            qgis.utils.iface.messageBar().clearWidgets()    
   


import sys
Dialog = QtGui.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

