import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class FileObj(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        # self.initUI()

    # def initUI(self):
    #     self.setWindowTitle(self.title)
    #     self.setGeometry(self.left, self.top, self.width, self.height)
    #
    #     # self.openFileNameDialog()
    #     # self.openFileNamesDialog()
    #     self.saveFileDialog()
    #
    #     # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","*.csv", options=options)
        if fileName:
            print(fileName)
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","*.csv", options=options)
        if files:
            print(files)

    def saveFolderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select directory containing SunVox app',
        )
        if path:
            return path

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","*.csv", options=options)
        if fileName:
            print(fileName)
            return fileName

# pyuic5 -x main.ui -o ui.py
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileObj()
    sys.exit(app.exec_())
