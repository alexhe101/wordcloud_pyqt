import sys
from main_ui import Ui_MainWindow
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox
import numpy as np
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image
import jieba
class Action(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.font_path = r'C:\\Windows\\fonts\\simsun.ttc'
        self.mask = None
        self.char_divide_flag = True
        self.color_from_mask_flag = False
        self.show()
        self.mask_flag= False
        self.width = 800
        self.height = 600
        QMessageBox.about(self,"read me",'github.com/alexhe101')

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self,'选择文件','','TxT files(*.txt)')
        if file_path!=('', ''):
            self.text = open(file_path[0],"r",encoding="utf-8").read()
        else:
            QMessageBox.about(self,'提示','文件未正常打开')

    def choose_font_path(self):
        file_path = QFileDialog.getOpenFileName(self, '选择字体文件', '', 'All files(*.*)')
        if file_path!=('', ''):
            self.font_path = file_path[0]
        else:
            QMessageBox.about(self, '提示', '字体未选择，使用默认字体')
    def choose_mask_path(self):
        file_path = QFileDialog.getOpenFileName(self, '选择蒙版文件', '', 'Png files(*.png)')
        if file_path!=('', ''):
            self.mask = np.array(Image.open(file_path[0]))
            self.mask_flag=True
        else:
            QMessageBox.about(self, '提示', '蒙版未选择，不使用蒙版')

    def show_image(self):
        if self.char_divide_flag==True:
            tmp =' '.join(jieba.cut(self.text))
        else:
            tmp = self.text
        self.width,self.height = eval(self.lineEdit.text())
        self.wc = WordCloud(mask=self.mask,font_path=self.font_path,background_color=None,width=self.width,height=self.height).generate(tmp)
        if self.color_from_mask_flag==True:
            if self.mask_flag==False:
                QMessageBox.about(self,'提示','蒙版文件不存在，无法生成背景色')
            else:
                image_colors = ImageColorGenerator(self.mask)
                self.wc.recolor(color_func=image_colors)
        img = np.array(self.wc)
        qimg = QImage(img,img.shape[1],img.shape[0],QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
    def character_divide(self):
        if self.char_divide_flag==True:
            self.char_divide_flag = False
        else:
            self.char_divide_flag=True

    def save_file(self):
        fold_path = QFileDialog.getSaveFileName(self,"文件保存","/","Image File(*.jpg *png)")
        self.wc.to_file(fold_path[0])
        QMessageBox.about(self, '消息提示', '保存成功')

    def generate_color_from_mask(self):
        if self.color_from_mask_flag==False:
            self.color_from_mask_flag=True
        else:
            self.color_from_mask_flag=False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    act = Action()
    sys.exit(app.exec_())
