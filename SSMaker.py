from PyQt4 import QtGui, QtCore
import os
import sys
import os
from PIL import Image
import glob
import threading
import re
from math import sqrt
################################
path = r"D:\MyPython\alphamerge"
if path not in sys.path:
    sys.path.append(path)
import myUI
################################

app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
UI = myUI.Ui_SpriteExport()
UI.setupUi(window)

class rootProgram():
    def __init__(self):
        self.progressBar = 0
        self.refresh = QtCore.QTimer()
        self.refresh.timeout.connect(lambda: rootProgram.variables(self))
        self.refresh.start(1000)

    def variables(self):
        self.lineEdit_Sequence_Path = UI.lineEdit_Sequence_Path.text()
        self.lineEdit_Save_Path = UI.lineEdit_Save_Path.text()
        self.Width = int(UI.lineEdit_Width.text())
        self.Height = int(UI.lineEdit_Height.text())
        self.Size = int(UI.lineEdit_Size.text())
        UI.progressBar.setProperty("value", self.progressBar)

    def CreateSprite(self):
        files = os.listdir(self.lineEdit_Sequence_Path)
        for i in enumerate(files):
            if re.findall("Thumbs.db", i[1]):
                files.pop(i[0])

        self.sequence = [os.path.join(self.lineEdit_Sequence_Path,i) for i in files]
        self.image_amount = len(self.sequence)

        image_W,image_H  = Image.open(self.sequence[0]).size; print(image_W,image_H)




        self.sprite_image_size_W = int(self.Width/self.Size)
        self.sprite_image_size_H = int(image_H/(image_W/self.sprite_image_size_W))


        print(self.sprite_image_size_W, self.sprite_image_size_H)
        ####################################################
        ####################################################
        self.image_amount_Height = int(self.Height/self.sprite_image_size_H)
        self.image_amount_Width = int(self.Width / self.sprite_image_size_W)

####################################################
        self.matrix_position = []
        x = 0
        y = 0
        for i in self.sequence:
            print(x, y)
            self.matrix_position.append([i, x, y])
            x += self.sprite_image_size_W

            if x > self.sprite_image_size_W * self.image_amount_Width - 1:
                x = 0
                y += self.sprite_image_size_H

####################################################
        background = Image.new("RGBA", (int(self.Width), int(self.Height)), (0, 0, 0, 0))
        for image, x,y in self.matrix_position:
            print("image :", image,"position x:", x,"position y:", y)
            image = Image.open(image).convert('RGBA')
            background.paste(image.resize((self.sprite_image_size_W, self.sprite_image_size_H), Image.ANTIALIAS), (x,y))


        background.save(self.lineEdit_Save_Path, "PNG")
        UI.label_view_Sprite.setPixmap(QtGui.QPixmap(self.lineEdit_Save_Path))
##################################################

    def Threading(self):
        self.__running = True
        self.Thread = threading.Thread(target=lambda: self.CreateSprite())
        self.Thread.start()


    def Cancel(self):
        self.__running = False


    def Sequence_Path(self):
        fileName = QtGui.QFileDialog.getExistingDirectory()
        UI.lineEdit_Sequence_Path.setText(fileName)


    def Save_Path(self):
        fileName = QtGui.QFileDialog.getSaveFileName(filter="Images (*.png)")
        UI.lineEdit_Save_Path.setText(fileName)

Program = rootProgram()

UI.pushButton_Export.clicked.connect(lambda: Program.CreateSprite())

UI.toolButton_Sequence_Path.clicked.connect(lambda: Program.Sequence_Path())
UI.toolButton_Save_Path.clicked.connect(lambda: Program.Save_Path())

UI.pushButton_Cancel.clicked.connect(lambda: Program.Cancel())

if __name__ == "__main__":
    window.show()
    sys.exit(app.exec_())
