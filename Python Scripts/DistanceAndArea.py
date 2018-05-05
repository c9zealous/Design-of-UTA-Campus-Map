from PyQt4 import QtCore, QtGui
import sqlite3
from PyQt4.QtCore import *
from PyQt4. QtGui import *
from qgis. core import *
from qgis. gui import *
from qgis.utils import *
from qgis.networkanalysis import *

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
        Dialog.resize(800, 372)
        self.areaTitle = QtGui.QLabel(Dialog)
        self.areaTitle.setGeometry(QtCore.QRect(180, 20, 200, 16))
        self.areaTitle.setObjectName(_fromUtf8("label"))
        self.distanceTitle = QtGui.QLabel(Dialog)
        self.distanceTitle.setGeometry(QtCore.QRect(550, 20, 200, 16))
        self.distanceTitle.setObjectName(_fromUtf8("label"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(160, 70, 200, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.slabel = QtGui.QLabel(Dialog)
        self.slabel.setGeometry(QtCore.QRect(530, 70, 200, 16))
        self.slabel.setObjectName(_fromUtf8("label"))
        
        self.dlabel = QtGui.QLabel(Dialog)
        self.dlabel.setGeometry(QtCore.QRect(530, 140, 200, 16))
        self.dlabel.setObjectName(_fromUtf8("label"))
        
        self.submitButton = QtGui.QPushButton(Dialog)
        self.submitButton.setGeometry(QtCore.QRect(160, 160, 93, 28))
        self.submitButton.setObjectName(_fromUtf8("submitButton"))
        self.submitButton.clicked.connect(lambda : self.areaQuery(comboBox.currentText()))
        
        self.areaResult = QtGui.QLabel(Dialog)
        self.areaResult.setGeometry(QtCore.QRect(120, 200, 200, 16))
        self.areaResult.setObjectName(_fromUtf8("label"))
        
        self.distanceResult = QtGui.QLabel(Dialog)
        self.distanceResult.setGeometry(QtCore.QRect(520, 270, 400, 16))
        self.distanceResult.setObjectName(_fromUtf8("label"))
        
       
        comboBox = QtGui.QComboBox(Dialog)
        comboBox.setGeometry(QtCore.QRect(100, 100, 220, 28))
        
        comboBox1 = QtGui.QComboBox(Dialog)
        comboBox1.setGeometry(QtCore.QRect(470, 100, 220, 28))
        
        comboBox2 = QtGui.QComboBox(Dialog)
        comboBox2.setGeometry(QtCore.QRect(470, 170, 220, 28))
        
        self.distanceSubmitButton = QtGui.QPushButton(Dialog)
        self.distanceSubmitButton.setGeometry(QtCore.QRect(540, 220, 93, 28))
        self.distanceSubmitButton.setObjectName(_fromUtf8("submitButton"))
        self.distanceSubmitButton.clicked.connect(lambda : self.distanceQuery(comboBox1.currentText(),comboBox2.currentText()))
        
        
        
        conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select name from Polygons order by name')
        entrances = []
        for row in c.fetchall():
            entrances.append(row[0])
        print entrances
        comboBox.addItems(entrances)
        comboBox1.addItems(entrances)
        comboBox2.addItems(entrances)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Distance and Area", None))
        self.label.setText(_translate("Dialog", "Select Polygon", None))
        self.areaTitle.setText(_translate("Dialog", "<b>Area</b>", None))
        self.distanceTitle.setText(_translate("Dialog", "<b>Distance</b>", None))
        self.slabel.setText(_translate("Dialog", "Select Source", None))
        self.dlabel.setText(_translate("Dialog", "Select Destination", None))
        self.submitButton.setText(_translate("Dialog", "Submit", None))
        self.distanceSubmitButton.setText(_translate("Dialog", "Submit", None))
    
    def areaQuery(self,buildingName):
        conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select id,st_numpoints(st_boundary(geom)) from Polygons where name="'+buildingName+'"')
        layer =  QgsVectorLayer('Polygon', 'Area' , "memory")
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
        qgis.utils.iface.messageBar().clearWidgets()     
        c.execute('select st_area(st_transform(geom,2163)) as area from Polygons where name="'+str(buildingName)+'"')
        for row in c.fetchall():
            print row[0]
            self.areaResult.setText(_translate("Dialog", "<b>Area: </b>"+str(row[0])+' sq. meters', None))

    def distanceQuery(self,src,dest):
            conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
            c = conn.cursor()
            conn.enable_load_extension(True)
            c.execute("select load_extension('mod_spatialite')")
            c.execute('select id,st_numpoints(st_boundary(geom)) from Polygons where name="'+src+'" or name="'+dest+'"')
            layer =  QgsVectorLayer('Polygon', 'Distance' , "memory")
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
            qgis.utils.iface.messageBar().clearWidgets()     
            c.execute('select st_distance(st_transform(st_centroid(p.geom),2163),st_transform(st_centroid(e.geom),2163)) as distance from Polygons p, Polygons e where p.name="'+src+'" and e.name="'+dest+'"')
            for row in c.fetchall():
                print row[0]
                self.distanceResult.setText(_translate("Dialog", "<b>Distance : </b>"+str(row[0])+' meters', None))


import sys
Dialog = QtGui.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

