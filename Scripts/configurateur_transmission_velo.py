#!/usr/bin/python3.5

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

# Custom libraries for Graphical User Interfaces (see file vibrations_resultsWindow.py)
from configuration_window import ConfigurationPignonsWindow, ConfigurationPlateauxWindow, Popup_Info
from dataBase import DataBase_cassettes, DataBase_pedalier



# -------------------------------------------------- #
# ---------------- MainWindow ---------------- #
# -------------------------------------------------- #
class MainWindow(qtw.QWidget):
    def __init__(self, recWidth, recHeight, parent = None):
        super().__init__(parent)
        self.title = 'Configurateur de transmission de vélo'
        self.setWindowTitle(self.title)
        
        self.recWidth, self.recHeight = recWidth, recHeight
        self.width, self.height = 800, 480
        
        self.update_geometry()
        self.init_lists()
        self.create()
        self.setFixedSize(self.size())
        self.update_CB_pignons()
        self.update_CB_plateaux()
        self.show()


    def update_geometry(self):
        self.left, self.top = (self.recWidth - self.width)/2, (self.recHeight - self.height)/2
        self.setGeometry(self.left, self.top, self.width, self.height)
    

    def init_lists(self):
        self.zb_list = ['11', '12']

        self.l_chape = {}
        self.l_chape['Courte'] = 60
        self.l_chape['Moyenne'] = 80
        self.l_chape['Longue'] = 100

        self.etagementPignonsSurMesure = []
        self.etagementPlateauxSurMesure = []


    def create(self):
        pal = self.palette()
        pal.setColor(self.backgroundRole(), qtc.Qt.white)
        self.setPalette(pal)

        boldFont = qtg.QFont()
        boldFont.setBold(True)

        # Sélection de l'entre-axe
        self.label_entreAxe = qtw.QLabel("Longueur de l'entre-axe", self)
        self.label_entreAxe.setFont(boldFont)
        self.label_entreAxe.move(210,10)

        self.lineEdit_entreAxe = qtw.QLineEdit(self)
        self.lineEdit_entreAxe.move(220,40)
        regex = qtc.QRegExp("[0-9][0-9][0-9]")
        validator = qtg.QRegExpValidator(regex)
        self.lineEdit_entreAxe.setValidator(validator)

        self.label_limitesEntreAxe = qtw.QLabel("[390 - 450]", self)
        self.label_limitesEntreAxe.move(220,70)

        # Sélection de la taille des roues
        self.label_tailleRoue = qtw.QLabel('Taille de roue', self)
        self.label_tailleRoue.setFont(boldFont)
        self.label_tailleRoue.move(10,10)

        self.radioButton_tailleRoue_650 = qtw.QRadioButton("650", self)
        self.radioButton_tailleRoue_650.toggled.connect(lambda:self.btnstateRoue())
        self.radioButton_tailleRoue_650.move(20,40)

        self.radioButton_tailleRoue_700 = qtw.QRadioButton("700", self)
        self.radioButton_tailleRoue_700.toggled.connect(lambda:self.btnstateRoue())
        self.radioButton_tailleRoue_700.setChecked(True)
        self.radioButton_tailleRoue_700.move(20,70)

        self.buttonGroup_tailleRoue = qtw.QButtonGroup(self)
        self.buttonGroup_tailleRoue.addButton(self.radioButton_tailleRoue_650)
        self.buttonGroup_tailleRoue.addButton(self.radioButton_tailleRoue_700)

        # Sélection du nombre de pignons
        self.label_nombrePignons = qtw.QLabel("Nombre de pignons", self)
        self.label_nombrePignons.setFont(boldFont)
        self.label_nombrePignons.move(10,100)

        self.comboBox_nombrePignons = qtw.QComboBox(self)
        self.comboBox_nombrePignons.addItems([str(i) for i in range(7, 13)])
        self.comboBox_nombrePignons.currentTextChanged.connect(self.update_CB_pignons)
        self.comboBox_nombrePignons.move(20,130)

        # Sélection du nombre de plateaux
        self.label_nombrePlateaux = qtw.QLabel("Nombre de plateaux", self)
        self.label_nombrePlateaux.setFont(boldFont)
        self.label_nombrePlateaux.move(210,100)

        self.comboBox_nombrePlateaux = qtw.QComboBox(self)
        self.comboBox_nombrePlateaux.addItems(['1', '2', '3'])
        self.comboBox_nombrePlateaux.currentTextChanged.connect(self.update_CB_plateaux)
        self.comboBox_nombrePlateaux.move(220,130)

        # Sélection de la marque
        self.label_choixMarque = qtw.QLabel("Choix de la marque", self)
        self.label_choixMarque.setFont(boldFont)
        self.label_choixMarque.move(10,160)
        
        self.radioButton_shimano = qtw.QRadioButton("Shimano", self)
        self.radioButton_shimano.setChecked(True)
        self.radioButton_shimano.toggled.connect(lambda:self.btnstateMarque())
        self.radioButton_shimano.move(20,190)

        self.radioButton_campagnolo = qtw.QRadioButton("Campagnolo", self)
        self.radioButton_campagnolo.toggled.connect(lambda:self.btnstateMarque())
        self.radioButton_campagnolo.move(100,190)

        self.buttonGroup_marquePignons = qtw.QButtonGroup(self)
        self.buttonGroup_marquePignons.addButton(self.radioButton_shimano)
        self.buttonGroup_marquePignons.addButton(self.radioButton_campagnolo)

        # Sélection des pignons
        self.label_choixPignons = qtw.QLabel("Choix des pignons", self)
        self.label_choixPignons.setFont(boldFont)
        self.label_choixPignons.move(10,220)
        
        self.radioButton_pignons_standard = qtw.QRadioButton("Standard", self)
        self.radioButton_pignons_standard.setChecked(True)
        self.radioButton_pignons_standard.toggled.connect(lambda:self.btnstatePignons())
        self.radioButton_pignons_standard.move(20,250)

        self.radioButton_pignons_surMesure = qtw.QRadioButton("Sur mesure", self)
        self.radioButton_pignons_surMesure.toggled.connect(lambda:self.btnstatePignons())
        self.radioButton_pignons_surMesure.move(100,250)

        self.buttonGroup_pignons = qtw.QButtonGroup(self)
        self.buttonGroup_pignons.addButton(self.radioButton_pignons_standard)
        self.buttonGroup_pignons.addButton(self.radioButton_pignons_surMesure)

        self.comboBox_pignonsStandard = qtw.QComboBox(self)
        self.comboBox_pignonsStandard.currentTextChanged.connect(self.update_capacite)
        self.comboBox_pignonsStandard.setFixedWidth(170)
        self.comboBox_pignonsStandard.move(20,280)

        self.pushButton_configurerPignons = qtw.QPushButton('Configuer',self)
        self.pushButton_configurerPignons.clicked.connect(self.configurer_pignons)
        self.pushButton_configurerPignons.move(20,280)
        self.pushButton_configurerPignons.hide()

        # Sélection des plateaux
        self.label_choixPlateaux = qtw.QLabel("Choix des plateaux", self)
        self.label_choixPlateaux.setFont(boldFont)
        self.label_choixPlateaux.move(210,220)

        self.radioButton_plateaux_standard = qtw.QRadioButton("Standard", self)
        self.radioButton_plateaux_standard.setChecked(True)
        self.radioButton_plateaux_standard.toggled.connect(lambda:self.btnstatePlateaux())
        self.radioButton_plateaux_standard.move(220,250)

        self.radioButton_plateaux_surMesure = qtw.QRadioButton("Sur mesure", self)
        self.radioButton_plateaux_surMesure.toggled.connect(lambda:self.btnstatePlateaux())
        self.radioButton_plateaux_surMesure.move(300,250)

        self.buttonGroup_plateaux = qtw.QButtonGroup(self)
        self.buttonGroup_plateaux.addButton(self.radioButton_plateaux_standard)
        self.buttonGroup_plateaux.addButton(self.radioButton_plateaux_surMesure)

        self.comboBox_plateauxStandard = qtw.QComboBox(self)
        self.comboBox_plateauxStandard.currentTextChanged.connect(self.update_capacite)
        self.comboBox_plateauxStandard.setFixedWidth(170)
        self.comboBox_plateauxStandard.move(220,280)
        
        self.pushButton_configurerPlateaux = qtw.QPushButton('Configuer',self)
        self.pushButton_configurerPlateaux.clicked.connect(self.configurer_plateaux)
        self.pushButton_configurerPlateaux.move(220,280)
        self.pushButton_configurerPlateaux.hide()

        # Sélection de la dimension de la chape
        self.label_dimensionChape = qtw.QLabel("Dimension de la chape", self)
        self.label_dimensionChape.setFont(boldFont)
        self.label_dimensionChape.move(10,310)

        self.comboBox_dimensionChape = qtw.QComboBox(self)
        self.comboBox_dimensionChape.move(20,340)

        # Sélection du nombre de dents du galet
        self.label_nombreDentsGalet = qtw.QLabel("Nombre de dents du galet", self)
        self.label_nombreDentsGalet.setFont(boldFont)
        self.label_nombreDentsGalet.move(210,310)
        
        self.label_nombreDentsGaletHaut = qtw.QLabel("Haut", self)
        self.label_nombreDentsGaletHaut.move(220,340)

        self.comboBox_nombreDentsGaletHaut = qtw.QComboBox(self)
        self.comboBox_nombreDentsGaletHaut.addItems(self.zb_list)
        self.comboBox_nombreDentsGaletHaut.move(260,340)

        self.label_nombreDentsGaletBas = qtw.QLabel("Bas", self)
        self.label_nombreDentsGaletBas.move(220,370)

        self.comboBox_nombreDentsGaletBas = qtw.QComboBox(self)
        self.comboBox_nombreDentsGaletBas.addItems(self.zb_list)
        self.comboBox_nombreDentsGaletBas.move(260,370)

        # Sélection de la configuration de la chaine
        self.label_configurationChaine = qtw.QLabel("Configuration de la chaine", self)
        self.label_configurationChaine.setFont(boldFont)
        self.label_configurationChaine.move(10,370)
        
        self.comboBox_configurationChaine = qtw.QComboBox(self)
        self.comboBox_configurationChaine.addItems(['petite', 'moyenne', 'grande'])
        self.comboBox_configurationChaine.move(20,400)

        # Image logo
        self.logoInsa = qtg.QPixmap('Images/insalogo.png')
        self.logoInsa = self.logoInsa.scaledToWidth(370)
        self.label_logoInsa = qtw.QLabel(self)
        self.label_logoInsa.setPixmap(self.logoInsa)
        self.label_logoInsa.move(410, 10)

        self.logoMarque = qtg.QPixmap('Images/shimanologo.jpg')
        self.logoMarque = self.logoMarque.scaledToWidth(370)
        self.label_logo = qtw.QLabel(self)
        self.label_logo.setPixmap(self.logoMarque)
        self.label_logo.move(410, 120)

        # Image transmission
        self.transmission = qtg.QPixmap('Images/transmission_shimano.png')
        self.transmission = self.transmission.scaledToWidth(370)
        self.label_trasmission = qtw.QLabel(self)
        self.label_trasmission.setPixmap(self.transmission)
        self.label_trasmission.move(410, 220)

        # Button valider
        self.pushButton_valider = qtw.QPushButton('Valider', self)
        self.pushButton_valider.clicked.connect(self.valider)
        self.pushButton_valider.move(170,440)

        
    def btnstateMarque(self):
        if self.radioButton_shimano.isChecked():
            self.logoMarque = qtg.QPixmap('Images/shimanologo.jpg')
            self.logoMarque = self.logoMarque.scaledToWidth(370)
            self.transmission = qtg.QPixmap('Images/transmission_shimano.png')
            self.transmission = self.transmission.scaledToWidth(370)
        else:
            self.logoMarque = qtg.QPixmap('Images/campagnolologo.jpeg')
            self.logoMarque = self.logoMarque.scaledToWidth(370)
            self.transmission = qtg.QPixmap('Images/transmission_campagnolo.jpg')
            self.transmission = self.transmission.scaledToWidth(370)
        self.label_logo.setPixmap(self.logoMarque)
        self.label_trasmission.setPixmap(self.transmission)
        self.update_CB_pignons()
        self.update_CB_plateaux()
        self.update_capacite()
    

    def btnstatePignons(self):
        if self.radioButton_pignons_standard.isChecked():
            self.comboBox_pignonsStandard.show()
            self.pushButton_configurerPignons.hide()
        else:
            self.comboBox_pignonsStandard.hide()
            self.pushButton_configurerPignons.show()
        self.update_CB_pignons()
        self.update_capacite()


    def btnstatePlateaux(self):
        if self.radioButton_plateaux_standard.isChecked():
            self.comboBox_plateauxStandard.show()
            self.pushButton_configurerPlateaux.hide()
        else:
            self.comboBox_plateauxStandard.hide()
            self.pushButton_configurerPlateaux.show()
        self.update_CB_plateaux()
        self.update_capacite()


    def btnstateRoue(self):
        if self.radioButton_tailleRoue_700.isChecked():
            minEntreAxe = 390
        else:
            minEntreAxe = 350

        self.label_limitesEntreAxe.setText("[{} - 450]".format(minEntreAxe))


    def update_CB_pignons(self):
        self.comboBox_pignonsStandard.clear()
        comboList = []
        if self.radioButton_shimano.isChecked():
            crl = 'shimano'
        else:
            crl = 'campagnolo'
        key = '{}v'.format(self.comboBox_nombrePignons.currentText())
        if key in DataBase_cassettes[crl].keys():
            for etagement in DataBase_cassettes[crl][key].keys():
                comboList.append(etagement)
            comboList.sort()

        self.comboBox_pignonsStandard.addItems(comboList)
        self.update_capacite()


    def update_CB_plateaux(self):
        self.comboBox_plateauxStandard.clear()
        comboList = []
        if self.radioButton_shimano.isChecked():
            crl = 'shimano'
        else:
            crl = 'campagnolo'
        key = '{}p'.format(self.comboBox_nombrePlateaux.currentText())
        if key in DataBase_pedalier[crl].keys():
            for etagement in DataBase_pedalier[crl][key].keys():
                comboList.append(etagement)
            comboList.sort()

        self.comboBox_plateauxStandard.addItems(comboList)
        self.update_capacite()


    def configurer_pignons(self):
        recWidth = self.recWidth
        recHeight = self.recHeight
        nbPignons = int(self.comboBox_nombrePignons.currentText())
        self.winPignons = ConfigurationPignonsWindow(recWidth, recHeight, nbPignons)
        self.winPignons.exec_()
        self.etagementPignonsSurMesure = self.winPignons.get_value()
        self.update_capacite()


    def configurer_plateaux(self):
        recWidth = self.recWidth
        recHeight = self.recHeight
        nbPlateaux = int(self.comboBox_nombrePlateaux.currentText())
        self.winPlateaux = ConfigurationPlateauxWindow(recWidth, recHeight, nbPlateaux)
        self.winPlateaux.exec_()
        self.etagementPlateauxSurMesure = self.winPlateaux.get_value()
        self.update_capacite()


    def update_capacite(self):
        self.comboBox_dimensionChape.clear()

        if self.radioButton_shimano.isChecked():
            crl = 'shimano'
        else:
            crl = 'campagnolo'
        
        if self.radioButton_pignons_standard.isChecked():
            key_nb_pignons = '{}v'.format(self.comboBox_nombrePignons.currentText())
            key_etagement_pignons = self.comboBox_pignonsStandard.currentText()
            if key_nb_pignons in DataBase_cassettes[crl]:
                if key_etagement_pignons in DataBase_cassettes[crl][key_nb_pignons]:
                    etagement_pignons = DataBase_cassettes[crl][key_nb_pignons][key_etagement_pignons]
                else:
                    etagement_pignons = []
            else:
                etagement_pignons = []
        else: 
            etagement_pignons = self.etagementPignonsSurMesure
        
        if self.radioButton_plateaux_standard.isChecked():
            key_nb_plateaux = '{}p'.format(self.comboBox_nombrePlateaux.currentText())
            key_etagement_plateaux = self.comboBox_plateauxStandard.currentText()
            if key_nb_plateaux in DataBase_pedalier[crl]:
                if key_etagement_plateaux in DataBase_pedalier[crl][key_nb_plateaux]:
                    etagement_plateaux = DataBase_pedalier[crl][key_nb_plateaux][key_etagement_plateaux]
                else:
                    etagement_plateaux = []
            else:
                etagement_plateaux = []
        else: 
            etagement_plateaux = self.etagementPlateauxSurMesure
            
        if etagement_pignons != [] and etagement_plateaux != []:
            capacite = (etagement_pignons[-1] - etagement_pignons[0]) + (etagement_plateaux[-1] - etagement_plateaux[0])
            
            if capacite <= 29:
                self.comboBox_dimensionChape.addItems(['Courte', 'Moyenne', 'Longue'])
            elif capacite <= 37:
                self.comboBox_dimensionChape.addItems(['Moyenne', 'Longue'])
            elif capacite <= 45:
                self.comboBox_dimensionChape.addItem('Longue')


    def valider(self): 
        erreur = False

        if self.lineEdit_entreAxe.text() == '':
            self.popup = Popup_Info("La longueur de l'entre axe n'a pas été définie", recWidth=self.recWidth, recHeight=self.recHeight)
            erreur = True
        else:
            entreAxe = float(self.lineEdit_entreAxe.text())

            if entreAxe != int(entreAxe):
                self.popup = Popup_Info("La longueur de l'entre axe doit être un nombre entier", recWidth=self.recWidth, recHeight=self.recHeight)
                erreur = True
            else:
                if self.radioButton_tailleRoue_700.isChecked():
                    minEntreAxe = 390
                else:
                    minEntreAxe = 350

                if int(self.lineEdit_entreAxe.text()) < minEntreAxe:
                    self.popup = Popup_Info("La longueur de l'entre axe doit être suppérieure ou égale à {}".format(minEntreAxe), recWidth=self.recWidth, recHeight=self.recHeight)
                    erreur = True
                elif int(self.lineEdit_entreAxe.text()) > 450:
                    self.popup = Popup_Info("La longueur de l'entre axe doit être inférieure ou égale à 450", recWidth=self.recWidth, recHeight=self.recHeight)
                    erreur = True

        if self.radioButton_pignons_standard.isChecked() and self.comboBox_pignonsStandard.currentText() == '':
            self.popup = Popup_Info("L'étagement de la cassette n'a pas été défini", recWidth=self.recWidth, recHeight=self.recHeight)
            erreur = True
        elif not self.radioButton_pignons_standard.isChecked():
            if self.etagementPignonsSurMesure == []:
                self.popup = Popup_Info("L'étagement de la cassette n'a pas été défini", recWidth=self.recWidth, recHeight=self.recHeight)
                erreur = True
            elif len(self.etagementPignonsSurMesure) != int(self.comboBox_nombrePignons.currentText()):
                self.popup = Popup_Info("L'étagement de la cassette ne correspond pas au nombre de pignons sélectionné", recWidth=self.recWidth, recHeight=self.recHeight)
                erreur = True
        
        if self.radioButton_plateaux_standard.isChecked() and self.comboBox_plateauxStandard.currentText() == '':
            self.popup = Popup_Info("L'étagement du pédalier n'a pas été défini", recWidth=self.recWidth, recHeight=self.recHeight)
            erreur = True
        elif not self.radioButton_plateaux_standard.isChecked():
            if self.etagementPlateauxSurMesure == []:
                self.popup = Popup_Info("L'étagement du pédalier n'a pas été défini", recWidth=self.recWidth, recHeight=self.recHeight)
                erreur = True
            elif len(self.etagementPlateauxSurMesure) != int(self.comboBox_nombrePlateaux.currentText()):
                self.popup = Popup_Info("L'étagement du pédalier ne correspond pas au nombre de plateaux sélectionné", recWidth=self.recWidth, recHeight=self.recHeight)
                erreur = True
        
        if self.comboBox_dimensionChape.currentText() == '':
            self.popup = Popup_Info("La transmission choisie ne convient avec aucune chape", recWidth=self.recWidth, recHeight=self.recHeight)
            erreur = True

        if self.radioButton_shimano.isChecked():
            crl = 'shimano'
        else:
            crl = 'campagnolo'
        
        if self.radioButton_pignons_standard.isChecked():
            key_nb_pignons = '{}v'.format(self.comboBox_nombrePignons.currentText())
            key_etagement_pignons = self.comboBox_pignonsStandard.currentText()
            if key_nb_pignons in DataBase_cassettes[crl]:
                if key_etagement_pignons in DataBase_cassettes[crl][key_nb_pignons]:
                    etagement_pignons = DataBase_cassettes[crl][key_nb_pignons][key_etagement_pignons]
                else:
                    etagement_pignons = []
            else:
                etagement_pignons = []
        else: 
            etagement_pignons = self.etagementPignonsSurMesure
        
        if self.radioButton_plateaux_standard.isChecked():
            key_nb_plateaux = '{}p'.format(self.comboBox_nombrePlateaux.currentText())
            key_etagement_plateaux = self.comboBox_plateauxStandard.currentText()
            if key_nb_plateaux in DataBase_pedalier[crl]:
                if key_etagement_plateaux in DataBase_pedalier[crl][key_nb_plateaux]:
                    etagement_plateaux = DataBase_pedalier[crl][key_nb_plateaux][key_etagement_plateaux]
                else:
                    etagement_plateaux = []
            else:
                etagement_plateaux = []
        else: 
            etagement_plateaux = self.etagementPlateauxSurMesure
            
        if etagement_pignons != [] and etagement_plateaux != []:
            capacite = (etagement_pignons[-1] - etagement_pignons[0]) + (etagement_plateaux[-1] - etagement_plateaux[0])
            configuration = self.comboBox_configurationChaine.currentText()
            if capacite >= 40 and configuration == 'petite':
                self.popup = Popup_Info("La configuration petite n'est pas possible pour une capacité supérieure ou égale à 40", recWidth=self.recWidth, recHeight=self.recHeight)
                erreur = True

        if not erreur:
            self.write_outputFile()


    def write_outputFile(self):
        txtFile = open('INPUT_PROGRAMME.txt', 'w')
        txtFile.write('ENTRAXE = {}\n'.format(self.lineEdit_entreAxe.text()))
        txtFile.write('CONFIG = "{}"\n'.format(self.comboBox_configurationChaine.currentText()))
        txtFile.write('VITESSE = "{}"\n'.format(self.comboBox_nombrePignons.currentText()))
        txtFile.write('NB_PLAT = "{}"\n'.format(self.comboBox_nombrePlateaux.currentText()))
        
        if self.radioButton_shimano.isChecked():
            crl = 'shimano'
        else:
            crl = 'campagnolo'
        txtFile.write('CRL = "{}"\n'.format(crl))
        
        if self.radioButton_pignons_standard.isChecked():
            key_nb_pignons = '{}v'.format(self.comboBox_nombrePignons.currentText())
            key_etagement_pignons = self.comboBox_pignonsStandard.currentText()
            etagement_pignons = DataBase_cassettes[crl][key_nb_pignons][key_etagement_pignons]
            for i in range(0, len(etagement_pignons)):
                txtFile.write('Z{}_ = {}.000000\n'.format(i+1, etagement_pignons[i]))
        else: 
            for i in range(0, len(self.etagementPignonsSurMesure)):
                txtFile.write('ZP{}_ = {}.000000\n'.format(i+1, self.etagementPignonsSurMesure[i]))
        
        if self.radioButton_plateaux_standard.isChecked():
            key_nb_plateaux = '{}p'.format(self.comboBox_nombrePlateaux.currentText())
            key_etagement_plateaux = self.comboBox_plateauxStandard.currentText()
            etagement_plateaux = DataBase_pedalier[crl][key_nb_plateaux][key_etagement_plateaux]
            for i in range(0, len(etagement_plateaux)):
                txtFile.write('ZP{}_ = {}.000000\n'.format(i+1, etagement_plateaux[i]))
        else: 
            for i in range(0, len(self.etagementPlateauxSurMesure)):
                txtFile.write('ZP{}_ = {}.000000\n'.format(i+1, self.etagementPlateauxSurMesure[i]))
        
        txtFile.write('ZGH_ = {}.000000\n'.format(self.comboBox_nombreDentsGaletHaut.currentText()))
        txtFile.write('ZGB_ = {}.000000\n'.format(self.comboBox_nombreDentsGaletBas.currentText()))
        txtFile.write('L_CHAPE = {}.000000\n'.format(self.l_chape[self.comboBox_dimensionChape.currentText()]))
        txtFile.close()
        self.close()



# ----------------------------------------------------------------
#       Main function      
# ----------------------------------------------------------------
def main():
    '''
    Function : main
    Description : Create an application and open the GUI for the project
    Parameters : None
    Returns : None
    '''
    app = qtw.QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    _ = MainWindow(rect.width(), rect.height())
    sys.exit(app.exec_())



# ----------------------------------------------------------------
#       Main part      
# ----------------------------------------------------------------
if __name__ == '__main__':
    main()

