import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from utils.config import APP_NAME, PRIMARY


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setFont(QFont("Roboto", 11))
    app.setStyleSheet(f"""
        QToolTip {{
            background: #FFFFFF;
            color: #1E293B;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 13px;
            font-family: Roboto;
        }}
        QMessageBox {{
            background: #F0F4F8;
            color: #1E293B;
            font-family: Roboto;
        }}
        QMessageBox QLabel {{
            color: #1E293B;
            font-size: 14px;
            font-family: Roboto;
        }}
        QMessageBox QPushButton {{
            background: #2563EB;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 6px 18px;
            min-width: 80px;
            font-size: 13px;
            font-family: Roboto;
        }}
        QMessageBox QPushButton:hover {{
            background: #1D4ED8;
        }}
    """)

    main_win = None

    def on_login_success(user):
        nonlocal main_win
        login_win.close()
        from views.main_window import MainWindow
        main_win = MainWindow()
        main_win.show()

    from views.login_view import LoginView
    login_win = LoginView(on_success=on_login_success)
    login_win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()