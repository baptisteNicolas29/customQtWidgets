import sys
from Qt import QtWidgets

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    wdg = QtWidgets.QWidget()
    wdg.show()
    app.exec()
