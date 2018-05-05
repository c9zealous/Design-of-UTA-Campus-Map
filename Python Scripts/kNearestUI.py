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
        self.label.setGeometry(QtCore.QRect(140, 70, 100, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(340, 70, 100, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 150, 150, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(340, 150, 150, 16))
        self.label_4.setObjectName(_fromUtf8("label_3"))
        self.submitButton = QtGui.QPushButton(Dialog)
        self.submitButton.setGeometry(QtCore.QRect(220, 220, 93, 28))
        self.submitButton.setObjectName(_fromUtf8("submitButton"))
        self.submitButton.clicked.connect(lambda : self.nearest(comboBox.currentText(),comboBox2.currentText(),comboBox3.currentText(),textBox.text()))
        
       
        comboBox = QtGui.QComboBox(Dialog)
        comboBox.setGeometry(QtCore.QRect(80, 100, 200, 28))
        
        comboBox2 = QtGui.QComboBox(Dialog)
        comboBox2.setGeometry(QtCore.QRect(300, 100, 200, 28))
        
        comboBox3 = QtGui.QComboBox(Dialog)
        comboBox3.setGeometry(QtCore.QRect(80, 180, 200, 28))
        
        textBox = QtGui.QLineEdit(Dialog)
        textBox.setGeometry(QtCore.QRect(300, 180, 200, 28))
        
        
        conn = sqlite3.connect('C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite')
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select name from Polygons')
        entrances = []
        for row in c.fetchall():
            entrances.append(row[0])
        print entrances
        comboBox.addItems(entrances)
        
        c.execute('select distinct(gtype) from Polygons')
        gtype = []
        for row in c.fetchall():
            gtype.append(row[0])
        print gtype
        
        comboBox2.addItems(gtype)
        
        comboBox3.addItems(['100','200','300','400','500','600','700','800','900','1000'])
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "k Nearest Neighbor", None))
        self.label.setText(_translate("Dialog", "Select Polygon", None))
        self.label_2.setText(_translate("Dialog", "Select Category", None))
        self.label_3.setText(_translate("Dialog", "Select Distance (meters) ", None))
        self.label_4.setText(_translate("Dialog", "Enter Limit k ", None))
        self.submitButton.setText(_translate("Dialog", "Submit", None))
        
    def nearest(self,building, gtype, distance,k):
        conn = sqlite3.connect("C:\Users\Shubham\Desktop\DATABASE_SPATIALITE\DBSPatiaLite.sqlite")
        c = conn.cursor()
        conn.enable_load_extension(True)
        c.execute("select load_extension('mod_spatialite')")
        c.execute('select e.id, st_numpoints(st_boundary(e.geom)),st_distance(st_transform(st_centroid(p.geom),2163),st_transform(st_centroid(e.geom),2163)) as dist from Polygons as p, Polygons as e where dist <'+distance+' and p.Name="'+building+'" and e.gtype="'+gtype+'" order by dist Limit '+k)
        layer =  QgsVectorLayer('Polygon', 'nearest distance' , "memory")
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

