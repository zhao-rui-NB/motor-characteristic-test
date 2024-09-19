import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QTextEdit
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMenuBar Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件
        self.central_widget = QTextEdit()
        self.setCentralWidget(self.central_widget)

        # 创建菜单栏
        self.create_menu_bar()
        
        # # add manu bar
        # self.menu_bar = QMenuBar(self)
        # self.menu_bar.addAction("File")
        
        # self.setMenuBar(self.menu_bar)

    def create_menu_bar(self):
        # 创建菜单栏
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)

        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")

        undo_action = QAction("撤销", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = QAction("重做", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("剪切", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)

        copy_action = QAction("复制", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)

        paste_action = QAction("粘贴", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")

        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        # help_menu.addAction(about_action)

        # menu_bar.addAction(about_action)
        
        self.Q = menu_bar.addMenu('QQQ')
        self.Q.


    def show_about(self):
        self.central_widget.setText("这是一个QMenuBar示例程序。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())