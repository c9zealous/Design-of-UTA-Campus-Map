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
        Dialog.resize(518, 372)
        
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(220, 70, 200, 16))
        self.label.setObjectName(_fromUtf8("label"))
        
        self.submitButton = QtGui.QPushButton(Dialog)
        self.submitButton.setGeometry(QtCore.QRect(220, 200, 93, 28))
        self.submitButton.setObjectName(_fromUtf8("submitButton"))
        self.submitButton.clicked.connect(lambda : self.ab(comboBox.currentText()))
        
       
        comboBox = QtGui.QComboBox(Dialog)
        comboBox.setGeometry(QtCore.QRect(160, 100, 220, 28))
        
        
        
        conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select distinct(gtype) from Polygons')
        entrances = []
        for row in c.fetchall():
            entrances.append(row[0])
        print entrances
        comboBox.addItems(entrances)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Select Polygons", None))
        self.submitButton.setText(_translate("Dialog", "Submit", None))
    
    def ab(self,buildingType):
        conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select id,st_numpoints(st_boundary(geom)) from Polygons where gtype="'+buildingType+'"')
        layer =  QgsVectorLayer('Polygon', buildingType , "memory")
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
   


import sys
Dialog = QtGui.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

