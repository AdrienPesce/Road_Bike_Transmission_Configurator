# ----------------------------------------------------------------
#       Import all the libraries for exactra functions      
# ----------------------------------------------------------------
# General librarie for operating system parameters
import sys
import os
# General librarie for Graphic User Interface
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc



# -------------------------------------------------- #
# ---------------- ConfigurationPignonsWindow ---------------- #
# -------------------------------------------------- #
class ConfigurationPignonsWindow(qtw.QDialog):
    def __init__(self, recWidth, recHeight, nbPignons, parent = None):
        super().__init__(parent)
        self.title = 'Configurateur des pignons'
        self.setWindowTitle(self.title)
        
        self.nbPignons = nbPignons

        self.etagement = []

        self.recWidth, self.recHeight = recWidth, recHeight
        self.width, self.height = 230, 60+self.nbPignons*30
        
        self.update_geometry()
        self.create()
        self.setFixedSize(self.size())
        self.show()


    def update_geometry(self):
        self.left, self.top = (self.recWidth - self.width)/2, (self.recHeight - self.height)/2
        self.setGeometry(self.left, self.top, self.width, self.height)


    def create(self):
        self.comboBox_list = []

        label = qtw.QLabel('(petit)', self)
        label.move(10,14)

        for i in range(0, self.nbPignons):
            label = qtw.QLabel(str(i+1), self)
            label.move(60,14+i*30)
            
            comboBox = qtw.QComboBox(self)
            comboBox.addItems([str(j) for j in range(11+i,32-(self.nbPignons-i-2))])
            comboBox.move(80,10+i*30)
            self.comboBox_list.append(comboBox)

            label = qtw.QLabel('(dents)', self)
            label.move(170,14+i*30)

        label = qtw.QLabel('(grand)', self)
        label.move(10,14+(self.nbPignons-1)*30)

        self.pushButton_valider = qtw.QPushButton('Valider', self)
        self.pushButton_valider.clicked.connect(self.valider)
        self.pushButton_valider.move(70, 20+(self.nbPignons)*30)


    def valider(self):
        erreur = False

        for i in range(1, len(self.comboBox_list)):
            if int(self.comboBox_list[i-1].currentText()) >= int(self.comboBox_list[i].currentText()):
                self.popup = Popup_Info("Le nombre de dents du pignon {} doit être inférieur à celui du {}".format(i, i+1), recWidth=self.recWidth/2, recHeight=self.recHeight)
                erreur = True

        if not erreur:
            for comboBox in self.comboBox_list:
                self.etagement.append(int(comboBox.currentText()))

            self.close()


    def get_value(self):
        return self.etagement
        


# -------------------------------------------------- #
# ---------------- ConfigurationPlateauxWindow ---------------- #
# -------------------------------------------------- #
class ConfigurationPlateauxWindow(qtw.QDialog):
    def __init__(self, recWidth, recHeight, nbPlateaux, parent = None):
        super().__init__(parent)
        self.title = 'Configurateur des plateaux'
        self.setWindowTitle(self.title)
        
        self.nbPlateaux = nbPlateaux

        self.etagement = []

        self.recWidth, self.recHeight = recWidth, recHeight
        self.width, self.height = 230, 60+self.nbPlateaux*30
        
        self.update_geometry()
        self.create()
        self.setFixedSize(self.size())
        self.show()


    def update_geometry(self):
        self.left, self.top = (self.recWidth - self.width)/2, (self.recHeight - self.height)/2
        self.setGeometry(self.left, self.top, self.width, self.height)


    def create(self):
        self.comboBox_list = []

        for i in range(0, self.nbPlateaux):
            label = qtw.QLabel(str(i+1), self)
            label.move(60,14+i*30)
            
            comboBox = qtw.QComboBox(self)
            comboBox.addItems([str(j) for j in range(24+i,58-(self.nbPlateaux-i)+2)])
            comboBox.move(80,10+i*30)
            self.comboBox_list.append(comboBox)

            label = qtw.QLabel('(dents)', self)
            label.move(170,14+i*30)
        
        if self.nbPlateaux > 1:
            label = qtw.QLabel('(petit)', self)
            label.move(10,14)

            label = qtw.QLabel('(grand)', self)
            label.move(10,14+(self.nbPlateaux-1)*30)

        self.pushButton_valider = qtw.QPushButton('Valider', self)
        self.pushButton_valider.clicked.connect(self.valider)
        self.pushButton_valider.move(70, 20+(self.nbPlateaux)*30)


    def valider(self):
        erreur = False

        for i in range(1, len(self.comboBox_list)):
            if int(self.comboBox_list[i-1].currentText()) >= int(self.comboBox_list[i].currentText()):
                self.popup = Popup_Info("Le nombre de dents du plateau {} doit être inférieur à celui du {}".format(i, i+1), recWidth=self.recWidth/2, recHeight=self.recHeight)
                erreur = True

            if int(self.comboBox_list[i].currentText()) - int(self.comboBox_list[i-1].currentText()) > 14:
                self.popup = Popup_Info("La différence de nombre de dents entre les plateaux {} et {} doit être inférieure ou égale à 14".format(i, i+1), recWidth=self.recWidth/2, recHeight=self.recHeight)
                erreur = True


        if not erreur:
            for comboBox in self.comboBox_list:
                self.etagement.append(int(comboBox.currentText()))

            self.close()


    def get_value(self):
        return self.etagement



# -------------------------------------------- #
# ---------------- Popup_Info ---------------- #
# -------------------------------------------- #
class Popup_Info(qtw.QWidget):
    def __init__(self, text, recWidth=None, recHeight=None):
        super(Popup_Info, self).__init__()
        # width for 1 char = 9 (capital) or 7 (low); height for 1 char = 19
        # width for the button = 80; height for the button = 28
        self.width, self.height = 100, 77

        label = qtw.QLabel(text, self)
        buttonOk = qtw.QPushButton('OK', self)
        buttonOk.clicked.connect(self.close_window)
        
        self.widthText = label.fontMetrics().boundingRect(label.text()).width()
        
        if self.widthText > 100:
            self.width = self.widthText + 20
        
        label.move(10 + (self.width - self.widthText -20)/2, 10)
        buttonOk.move(10 + (self.width - 100)/2, 39)

        if not recWidth:
            left = 0
        else:
            left = (recWidth - self.width)/2

        if not recHeight:
            top = 0
        else:
            top = (recHeight - self.height)/2

        self.setWindowTitle('Erreur')
        self.setGeometry(left, top, self.width, self.height)

        self.show()

    def close_window(self):
        self.close()
             