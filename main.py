import os
import sys

import minimalmodbus
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor, QIntValidator
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QTextEdit, QPushButton, QMessageBox, QComboBox


def config(com):
    com = f"COM{com}"
    meter_type = 1  # or 1 # or 3
    instrument = minimalmodbus.Instrument(com, 1, debug=False)
    instrument.serial.baudrate = 9600
    instrument.serial.timeout = 0.3
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.close_port_after_each_call = True
    n = 0
    return instrument, meter_type


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass  # Необходимо для совместимости с sys.stdout


class FileUploader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.join(current_dir, 'libs', 'maket_clbr.ui')

        uic.loadUi(ui_path, self)

        self.number_com = self.findChild(QLineEdit, 'enter_com')
        self.number_com.setValidator(QIntValidator())

        self.type = self.findChild(QComboBox, 'type')

        self.start = self.findChild(QPushButton, 'start_button')
        self.start.clicked.connect(self.start_command)

        self.start = self.findChild(QPushButton, 'start_button_2')
        self.start.clicked.connect(self.start_command_2)

        self.text_edit = self.findChild(QTextEdit, 'textEdit')
        self.text_edit.setStyleSheet(
            "background-color: #1e1e1e; color: #ffffff; font-family: Consolas; font-size: 12px;")
        self.text_edit.setReadOnly(True)  # Запрещаем редактирование
        self.redirect_stdout()
        self.stream.textWritten.connect(self.on_text_written)

        self.applyDarkTheme()

    def start_command(self):
        self.text_edit.clear()
        if not self.number_com.text().strip():
            # Показываем предупреждение
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Введите COM соединения!",
                QMessageBox.Ok
            )
            return

        com = self.number_com.text()
        type = self.type.currentText()
        try:
            instrument, meter_type = config(com)
            if type == '1PH':
                print('Выбранный тип счетчика >> 1PH')
                instrument.write_register(registeraddress=147, value=170)
            elif type == '3PH':
                print('Выбранный тип счетчика >> 3PH')
                instrument.write_register(registeraddress=239, value=170)
            self.update_text("УСПЕХ!", "green")
            print()
            self.update_text("Перезапустите счетчик!", "green")
        except Exception as e:
            self.update_text(f"Ошибка {e}.", "red")
            print()
            self.update_text(f"Проверьте настройки.", "red")

    def start_command_2(self):
        self.text_edit.clear()
        if not self.number_com.text().strip():
            # Показываем предупреждение
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Введите COM соединения!",
                QMessageBox.Ok
            )
            return

        com = self.number_com.text()
        type = self.type.currentText()
        try:
            instrument, meter_type = config(com)
            if type == '1PH':
                print('Выбранный тип счетчика >> 1PH')
                instrument.write_register(registeraddress=147, value=85)
            elif type == '3PH':
                print('Выбранный тип счетчика >> 3PH')
                instrument.write_register(registeraddress=239, value=85)
            self.update_text("УСПЕХ!", "green")
            print()
            self.update_text("Перезапустите счетчик!", "green")
        except Exception as e:
            self.update_text(f"Ошибка {e}.", "red")
            print()
            self.update_text(f"Проверьте настройки.", "red")

    def applyDarkTheme(self):
        # Определяем стили для темной темы
        dark_stylesheet = """
        QWidget {
            background-color: #2c313c;
            color: #ffffff;
        }

        QLineEdit {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px;
        }

        QLineEdit:focus {
            border: 1px solid #61dafb;
        }

        QPushButton {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px 10px;
        }

        QPushButton:hover {
            background-color: #444950;
        }

        QPushButton:pressed {
            background-color: #2c313c;
        }
        """

        # Применяем стиль к приложению
        self.setStyleSheet(dark_stylesheet)

    def update_text(self, message, color):
        self.text_edit.append(f"\n<font color={color} size='5'>{message}</font>\n")

    def redirect_stdout(self):
        self.stream = EmittingStream()
        sys.stdout = self.stream
        sys.stderr = self.stream

    def on_text_written(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        QApplication.processEvents()


def main():
    app = QApplication(sys.argv)
    ex = FileUploader()
    ex.show()
    sys.exit(app.exec_())


def debug():
    com = '3'
    type = '1PH'
    try:
        instrument, meter_type = config(com)
        if type == '1PH':
            print('Выбранный тип счетчика >> 1PH')
            instrument.write_register(registeraddress=147, value=85)
        elif type == '3PH':
            print('Выбранный тип счетчика >> 3PH')
            instrument.write_register(registeraddress=239, value=85)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
