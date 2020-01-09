import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from ui_4 import Ui_Form
import sqlite3
from ui_add import Ui_Form as Ui_add


class AddWidget(QMainWindow, Ui_add):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.con = sqlite3.connect("films.db")
        self.params = {}
        self.setupUi(self)
        self.selectGenres()
        self.pushButton.clicked.connect(self.add_elem)

    def selectGenres(self):
        req = "SELECT * from genres"
        cur = self.con.cursor()
        for value, key in cur.execute(req).fetchall():
            self.params[key] = value
        self.comboBox.addItems(list(self.params.keys()))

    def add_elem(self):
        cur = self.con.cursor()
        id_off = cur.execute("SELECT max(id) FROM films").fetchone()[0]
        new_data = (id_off + 1, self.title.toPlainText(), int(self.year.toPlainText()),
                    self.params.get(self.comboBox.currentText()), int(self.duration.toPlainText()))
        cur.execute("INSERT INTO films VALUES (?,?,?,?,?)", new_data)
        self.con.commit()
        self.close()


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.pushButton.clicked.connect(self.update_result)
        self.addButton.clicked.connect(self.adding)
        self.dialogs = list()

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        que = "SELECT * FROM Films WHERE " + self.textEdit.toPlainText()
        result = cur.execute(que).fetchall()

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def adding(self):
        dialog = AddWidget(self)
        dialog.show()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
