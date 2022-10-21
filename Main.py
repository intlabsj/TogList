import sys
import pandas as pd
from PyQt5.QtWidgets import *
from GatchaData import GatchaData

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setWindowTitle("신의탑M 뽑기 기록")
        self.success = False

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)
        self.viewstate = [True, True, True, True, True, True]

        groupBox = QGroupBox("검색 옵션")
        self.checkBox_LC = QCheckBox("전설캐릭")
        self.checkBox_LC.setChecked(True)
        self.checkBox_LC.clicked.connect(self.checkBoxState)

        self.checkBox_LW = QCheckBox("전설무기")
        self.checkBox_LW.setChecked(True)
        self.checkBox_LW.clicked.connect(self.checkBoxState)

        self.checkBox_HC = QCheckBox("영웅캐릭")
        self.checkBox_HC.setChecked(True)
        self.checkBox_HC.clicked.connect(self.checkBoxState)

        self.checkBox_HW = QCheckBox("영웅무기")
        self.checkBox_HW.setChecked(True)
        self.checkBox_HW.clicked.connect(self.checkBoxState)

        self.checkBox_RW = QCheckBox("희귀무기")
        self.checkBox_RW.setChecked(True)
        self.checkBox_RW.clicked.connect(self.checkBoxState)

        self.checkBox_AW = QCheckBox("고급무기")
        self.checkBox_AW.setChecked(True)
        self.checkBox_AW.clicked.connect(self.checkBoxState)

        self.tableWidget = QTableWidget()

        upper_left_innerlayout = QVBoxLayout()
        upper_left_innerlayout.addWidget(self.checkBox_LC)
        upper_left_innerlayout.addWidget(self.checkBox_LW)
        upper_left_innerlayout.addWidget(self.checkBox_HC)
        upper_left_innerlayout.addWidget(self.checkBox_HW)
        upper_left_innerlayout.addWidget(self.checkBox_RW)
        upper_left_innerlayout.addWidget(self.checkBox_AW)
        groupBox.setLayout(upper_left_innerlayout)

        upper_left_layout = QVBoxLayout()
        upper_left_layout.addWidget(groupBox)

        upper_right_layout = QVBoxLayout()
        # upper_right_layout.addWidget(self.tableWidget)

        tabs = QTabWidget()
        tabs.addTab(self.make_tab1(), '전체 통계')
        tabs.addTab(self.make_tab2(), '세부 통계')
        upper_right_layout.addWidget(tabs)

        upper_layout = QHBoxLayout()
        upper_layout.addLayout(upper_left_layout)
        upper_layout.addLayout(upper_right_layout)

        self.LabelID = QLabel("계정번호: ")
        self.TextID = QLineEdit(" ", self)
        self.ButtonSerach = QPushButton("검색")
        self.ButtonSerach.clicked.connect(self.ID_Search)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.LabelID)
        middle_layout.addWidget(self.TextID)
        middle_layout.addWidget(self.ButtonSerach)

        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addLayout(middle_layout)

        self.setLayout(layout)

    def make_tab1(self):
        self.TotalTable = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.TotalTable)

        tab = QWidget()
        tab.setLayout(vbox)

        return tab

    def make_tab2(self):
        self.DetailTable = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.DetailTable)

        tab = QWidget()
        tab.setLayout(vbox)

        return tab

    def checkBoxState(self):
        self.viewstate[0] = True if self.checkBox_LC.isChecked() else False
        self.viewstate[1] = True if self.checkBox_LW.isChecked() else False
        self.viewstate[2] = True if self.checkBox_HC.isChecked() else False
        self.viewstate[3] = True if self.checkBox_HW.isChecked() else False
        self.viewstate[4] = True if self.checkBox_RW.isChecked() else False
        self.viewstate[5] = True if self.checkBox_AW.isChecked() else False

        self.update_table()

    def update_totalTable(self, cls_cnt):
        val = list(cls_cnt.values())
        tot = sum(val)

        df_dict = {"등장 횟수": [tot], "등장 확률": ["100.00%"]}
        index = ["뽑기 횟수"]
        for idx, cls in enumerate(val):
            percent = "{0:.2f}%".format((cls / tot) * 100)
            df_dict["등장 횟수"].append(cls)
            df_dict["등장 확률"].append(percent)
            index.append(self.cls_list[idx])

        temp_df = pd.DataFrame(df_dict, columns=df_dict.keys(), index=index)
        self.TotalTable.setRowCount(len(temp_df.index))
        self.TotalTable.setColumnCount(len(temp_df.columns))
        self.TotalTable.setHorizontalHeaderLabels(temp_df.columns)
        self.TotalTable.setVerticalHeaderLabels(temp_df.index)

        for row_idx, row in enumerate(temp_df.index):
            for col_idx, col in enumerate(temp_df.columns):
                value = temp_df.iloc[row_idx, col_idx]
                item = QTableWidgetItem(str(value))
                self.TotalTable.setItem(row_idx, col_idx, item)

    def update_table(self):
        if not self.success: return

        search_list = list()
        for state_idx, state in enumerate(self.viewstate):
            if state:
                search_list.append(self.cls_list[state_idx])

        temp_df = self.df.loc[search_list]
        self.DetailTable.setRowCount(len(temp_df.index))
        self.DetailTable.setColumnCount(len(temp_df.columns))
        self.DetailTable.setHorizontalHeaderLabels(temp_df.columns)
        self.DetailTable.setVerticalHeaderLabels(temp_df.index)

        for row_idx, row in enumerate(temp_df.index):
            for col_idx, col in enumerate(temp_df.columns):
                value = temp_df.iloc[row_idx, col_idx]
                item = QTableWidgetItem(str(value))
                self.DetailTable.setItem(row_idx, col_idx, item)

    def ID_Search(self):
        ID = self.TextID.text()
        GD = GatchaData(ID)
        if GD.trigger == False:
            QMessageBox.information(self, "안내", "없는 계정입니다.")
            self.success = False
        elif GD.trigger == -1:
            QMessageBox.information(self, "안내", "뽑기 기록이 없습니다.")
            self.success = False
        else:
            QMessageBox.information(self, "안내", "검색 완료.")
            self.df = GD.print_from_gatcha()
            self.success = True
            self.cls_list = list(GD.cls_list.values())
            self.update_table()
            self.update_totalTable(GD.class_cnt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
