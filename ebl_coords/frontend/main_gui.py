# Form implementation generated from reading ui file './ebl_coords/frontend/ui_files/main_gui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1186, 955)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.map_tab = QtWidgets.QWidget()
        self.map_tab.setObjectName("map_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.map_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.map_splitter = QtWidgets.QSplitter(parent=self.map_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map_splitter.sizePolicy().hasHeightForWidth())
        self.map_splitter.setSizePolicy(sizePolicy)
        self.map_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.map_splitter.setObjectName("map_splitter")
        self.map_left = QtWidgets.QWidget(parent=self.map_splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map_left.sizePolicy().hasHeightForWidth())
        self.map_left.setSizePolicy(sizePolicy)
        self.map_left.setMinimumSize(QtCore.QSize(200, 0))
        self.map_left.setMaximumSize(QtCore.QSize(600, 16777215))
        self.map_left.setObjectName("map_left")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.map_left)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.map_weichen_list = QtWidgets.QListWidget(parent=self.map_left)
        self.map_weichen_list.setObjectName("map_weichen_list")
        self.verticalLayout_5.addWidget(self.map_weichen_list)
        self.map_left_form = QtWidgets.QWidget(parent=self.map_left)
        self.map_left_form.setObjectName("map_left_form")
        self.formLayout = QtWidgets.QFormLayout(self.map_left_form)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(parent=self.map_left_form)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5
        )
        self.map_zonename_txt = QtWidgets.QLineEdit(parent=self.map_left_form)
        self.map_zonename_txt.setObjectName("map_zonename_txt")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.map_zonename_txt
        )
        self.map_zone_speichern_btn = QtWidgets.QPushButton(parent=self.map_left_form)
        self.map_zone_speichern_btn.setObjectName("map_zone_speichern_btn")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.map_zone_speichern_btn
        )
        self.label_6 = QtWidgets.QLabel(parent=self.map_left_form)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6
        )
        self.label_7 = QtWidgets.QLabel(parent=self.map_left_form)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7
        )
        self.map_zone_width = QtWidgets.QSpinBox(parent=self.map_left_form)
        self.map_zone_width.setObjectName("map_zone_width")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.map_zone_width
        )
        self.map_zone_height = QtWidgets.QSpinBox(parent=self.map_left_form)
        self.map_zone_height.setObjectName("map_zone_height")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.map_zone_height
        )
        self.label_8 = QtWidgets.QLabel(parent=self.map_left_form)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8
        )
        self.map_zone_select_combo_box = QtWidgets.QComboBox(parent=self.map_left_form)
        self.map_zone_select_combo_box.setObjectName("map_zone_select_combo_box")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.map_zone_select_combo_box
        )
        self.map_zone_neu_btn = QtWidgets.QPushButton(parent=self.map_left_form)
        self.map_zone_neu_btn.setObjectName("map_zone_neu_btn")
        self.formLayout.setWidget(
            6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.map_zone_neu_btn
        )
        self.verticalLayout_5.addWidget(self.map_left_form)
        self.map_right = QtWidgets.QWidget(parent=self.map_splitter)
        self.map_right.setObjectName("map_right")
        self.map_right_layout = QtWidgets.QVBoxLayout(self.map_right)
        self.map_right_layout.setContentsMargins(0, 0, 0, 0)
        self.map_right_layout.setObjectName("map_right_layout")
        self.verticalLayout_4.addWidget(self.map_splitter)
        self.tabWidget.addTab(self.map_tab, "")
        self.weichen_tab = QtWidgets.QWidget()
        self.weichen_tab.setObjectName("weichen_tab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.weichen_tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.weichen_splitter = QtWidgets.QSplitter(parent=self.weichen_tab)
        self.weichen_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.weichen_splitter.setObjectName("weichen_splitter")
        self.weichen_left = QtWidgets.QWidget(parent=self.weichen_splitter)
        self.weichen_left.setMinimumSize(QtCore.QSize(200, 0))
        self.weichen_left.setMaximumSize(QtCore.QSize(600, 16777215))
        self.weichen_left.setObjectName("weichen_left")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.weichen_left)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.weichen_list = QtWidgets.QListWidget(parent=self.weichen_left)
        self.weichen_list.setObjectName("weichen_list")
        self.verticalLayout.addWidget(self.weichen_list)
        self.weichen_new_btn = QtWidgets.QPushButton(parent=self.weichen_left)
        self.weichen_new_btn.setObjectName("weichen_new_btn")
        self.verticalLayout.addWidget(self.weichen_new_btn)
        self.weichen_right = QtWidgets.QWidget(parent=self.weichen_splitter)
        self.weichen_right.setObjectName("weichen_right")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.weichen_right)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.weichen_widget = QtWidgets.QWidget(parent=self.weichen_right)
        self.weichen_widget.setObjectName("weichen_widget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.weichen_widget)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.weichen_widget)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2
        )
        self.weichen_weichenname_txt = QtWidgets.QLineEdit(parent=self.weichen_widget)
        self.weichen_weichenname_txt.setObjectName("weichen_weichenname_txt")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.weichen_weichenname_txt
        )
        self.label_3 = QtWidgets.QLabel(parent=self.weichen_widget)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3
        )
        self.weichen_dcc_txt = QtWidgets.QLineEdit(parent=self.weichen_widget)
        self.weichen_dcc_txt.setObjectName("weichen_dcc_txt")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.weichen_dcc_txt
        )
        self.label_4 = QtWidgets.QLabel(parent=self.weichen_widget)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(
            2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4
        )
        self.weichen_einmessen_btn = QtWidgets.QPushButton(parent=self.weichen_widget)
        self.weichen_einmessen_btn.setObjectName("weichen_einmessen_btn")
        self.formLayout_2.setWidget(
            4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.weichen_einmessen_btn
        )
        self.weichen_speichern_btn = QtWidgets.QPushButton(parent=self.weichen_widget)
        self.weichen_speichern_btn.setObjectName("weichen_speichern_btn")
        self.formLayout_2.setWidget(
            5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.weichen_speichern_btn
        )
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.formLayout_2.setItem(
            3, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem
        )
        self.weichen_bhf_txt = QtWidgets.QLineEdit(parent=self.weichen_widget)
        self.weichen_bhf_txt.setObjectName("weichen_bhf_txt")
        self.formLayout_2.setWidget(
            2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.weichen_bhf_txt
        )
        self.verticalLayout_2.addWidget(self.weichen_widget)
        self.horizontalLayout_4.addWidget(self.weichen_splitter)
        self.tabWidget.addTab(self.weichen_tab, "")
        self.strecken_tab = QtWidgets.QWidget()
        self.strecken_tab.setObjectName("strecken_tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.strecken_tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.strecken_splitter = QtWidgets.QSplitter(parent=self.strecken_tab)
        self.strecken_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.strecken_splitter.setObjectName("strecken_splitter")
        self.strecken_left = QtWidgets.QWidget(parent=self.strecken_splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.strecken_left.sizePolicy().hasHeightForWidth()
        )
        self.strecken_left.setSizePolicy(sizePolicy)
        self.strecken_left.setMinimumSize(QtCore.QSize(200, 0))
        self.strecken_left.setMaximumSize(QtCore.QSize(600, 16777215))
        self.strecken_left.setObjectName("strecken_left")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.strecken_left)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.strecken_list = QtWidgets.QListWidget(parent=self.strecken_left)
        self.strecken_list.setObjectName("strecken_list")
        self.verticalLayout_3.addWidget(self.strecken_list)
        self.strecken_new_btn = QtWidgets.QPushButton(parent=self.strecken_left)
        self.strecken_new_btn.setObjectName("strecken_new_btn")
        self.verticalLayout_3.addWidget(self.strecken_new_btn)
        self.strecken_right = QtWidgets.QWidget(parent=self.strecken_splitter)
        self.strecken_right.setObjectName("strecken_right")
        self.formLayout_5 = QtWidgets.QFormLayout(self.strecken_right)
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label = QtWidgets.QLabel(parent=self.strecken_right)
        self.label.setObjectName("label")
        self.formLayout_5.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label
        )
        self.strecken_comboBox_a = QtWidgets.QComboBox(parent=self.strecken_right)
        self.strecken_comboBox_a.setObjectName("strecken_comboBox_a")
        self.formLayout_5.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.strecken_comboBox_a
        )
        self.label_10 = QtWidgets.QLabel(parent=self.strecken_right)
        self.label_10.setObjectName("label_10")
        self.formLayout_5.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_10
        )
        self.strecken_comboBox_b = QtWidgets.QComboBox(parent=self.strecken_right)
        self.strecken_comboBox_b.setObjectName("strecken_comboBox_b")
        self.formLayout_5.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.strecken_comboBox_b
        )
        self.strecken_speichern_btn = QtWidgets.QPushButton(parent=self.strecken_right)
        self.strecken_speichern_btn.setObjectName("strecken_speichern_btn")
        self.formLayout_5.setWidget(
            3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.strecken_speichern_btn
        )
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.formLayout_5.setItem(
            2, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem1
        )
        self.horizontalLayout.addWidget(self.strecken_splitter)
        self.tabWidget.addTab(self.strecken_tab, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1186, 22))
        self.menubar.setObjectName("menubar")
        self.menuZonen = QtWidgets.QMenu(parent=self.menubar)
        self.menuZonen.setObjectName("menuZonen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionneue_Zone = QtGui.QAction(parent=MainWindow)
        self.actionneue_Zone.setObjectName("actionneue_Zone")
        self.actionZone_laden = QtGui.QAction(parent=MainWindow)
        self.actionZone_laden.setObjectName("actionZone_laden")
        self.menuZonen.addAction(self.actionneue_Zone)
        self.menuZonen.addAction(self.actionZone_laden)
        self.menubar.addAction(self.menuZonen.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EBL"))
        self.label_5.setText(_translate("MainWindow", "Zonename"))
        self.map_zone_speichern_btn.setText(
            _translate("MainWindow", "Speichern und Generieren")
        )
        self.label_6.setText(_translate("MainWindow", "Zonenbreite"))
        self.label_7.setText(_translate("MainWindow", "Zonenhöhe"))
        self.label_8.setText(_translate("MainWindow", "Zone"))
        self.map_zone_neu_btn.setText(_translate("MainWindow", "Neue Zone"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.map_tab), _translate("MainWindow", "Karte")
        )
        self.weichen_new_btn.setText(_translate("MainWindow", "Neue Weiche"))
        self.label_2.setText(_translate("MainWindow", "Weichename"))
        self.label_3.setText(_translate("MainWindow", "DCC"))
        self.label_4.setText(_translate("MainWindow", "Bahnhof"))
        self.weichen_einmessen_btn.setText(_translate("MainWindow", "Einmessen"))
        self.weichen_speichern_btn.setText(_translate("MainWindow", "Speichern"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.weichen_tab),
            _translate("MainWindow", "Weichen"),
        )
        self.strecken_new_btn.setText(_translate("MainWindow", "Neue Strecke"))
        self.label.setText(_translate("MainWindow", "Weiche A"))
        self.label_10.setText(_translate("MainWindow", "Weiche B"))
        self.strecken_speichern_btn.setText(_translate("MainWindow", "Speichern"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.strecken_tab),
            _translate("MainWindow", "Strecken"),
        )
        self.menuZonen.setTitle(_translate("MainWindow", "Zonen"))
        self.actionneue_Zone.setText(_translate("MainWindow", "Neue Zone"))
        self.actionZone_laden.setText(_translate("MainWindow", "Zone laden"))
