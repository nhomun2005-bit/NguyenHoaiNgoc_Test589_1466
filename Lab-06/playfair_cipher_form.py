import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Giả sử bạn đã convert file .ui của Playfair thành playfair_ui.py
from ui.playfair import Ui_MainWindow 
import requests

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối các nút bấm với hàm xử lý
        # btn_En: Nút mã hóa, btn_De: Nút giải mã
        self.ui.btn_En.clicked.connect(self.call_api_encrypt)
        self.ui.btn_De.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        """Hàm gọi API để mã hóa văn bản"""
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        
        # Lấy dữ liệu từ txt_P (Plaintext) và txt_K (Key - nếu có)
        payload = {
            "plaintext": self.ui.txt_P.toPlainText(),
            "key": self.ui.txt_K.text() if hasattr(self.ui, 'txt_K') else "default_key"
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Hiển thị kết quả vào txt_C (Ciphertext)
                self.ui.txt_C.setPlainText(data["ciphertext"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Mã hóa thành công!")
                msg.setWindowTitle("Thông báo")
                msg.exec_()
            else:
                self.show_error("Lỗi API: Không thể mã hóa.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Lỗi kết nối: {str(e)}")

    def call_api_decrypt(self):
        """Hàm gọi API để giải mã văn bản"""
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        
        # Lấy dữ liệu từ txt_C (Ciphertext) để giải mã
        payload = {
            "ciphertext": self.ui.txt_C.toPlainText(),
            "key": self.ui.txt_K.text() if hasattr(self.ui, 'txt_K') else "default_key"
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Hiển thị kết quả ngược lại vào txt_P (Plaintext)
                self.ui.txt_P.setPlainText(data["plaintext"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Giải mã thành công!")
                msg.setWindowTitle("Thông báo")
                msg.exec_()
            else:
                self.show_error("Lỗi API: Không thể giải mã.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Lỗi kết nối: {str(e)}")

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Lỗi")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())