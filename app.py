import sys
from PyQt6.QtWidgets import QApplication
from overlay_ui import Overlay

def main():
    app = QApplication(sys.argv)
    hud = Overlay()
    hud.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()