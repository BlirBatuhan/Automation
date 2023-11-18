import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from FINAL_ui import *






uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

#veri tabanı
import sqlite3

baglanti = sqlite3.connect("otopark.db")
islem =baglanti.cursor()
baglanti.commit()

table = islem.execute("create table if not exists otopark(ARAÇ_SAHİBİ text, PLAKA text, RENK text, TEKERLEK_SAYISI int, ARAÇ_TÜRÜ text )")
baglanti.commit()

def bilgi_ekle():
    isim = ui.lineEdit_ISIM.text()
    plaka = ui.lineEdit_PLAKA.text()
    renk = ui.lineEdit_RENK.text()
    tekerlek_sayisi = int(ui.lineEdit_TEKERLEK.text()) 
    oto = ui.comboBox_cesit.currentText()
    

    try:
        ekle = "insert into otopark (ARAÇ_SAHİBİ,PLAKA,RENK,TEKERLEK_SAYISI,ARAÇ_TÜRÜ) values(?,?,?,?,?)"
        islem.execute(ekle,(isim,plaka,renk,tekerlek_sayisi,oto))
        baglanti.commit()
        ui.statusbar.showMessage("KAYIT EKLENDİ!!",2000)
    except Exception as error:
        ui.statusbar.showMessage("!! İŞLEM GERÇEKLEŞEMEDİ !! " + str(error), 2000)


def listele():
    ui.tableWidget_tablo.clear()
    ui.tableWidget_tablo.setHorizontalHeaderLabels(("ARAÇ SAHİBİ","PLAKA","RENK","TEKERLEK SAYISI","ARAÇ TÜRÜ"))
    ui.tableWidget_tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgu = "select * from otopark"
    islem.execute(sorgu)

    for indexSatır, kayıtNumarası in enumerate(islem):
        for indexSutun, kayıtSutun in enumerate(kayıtNumarası):
            ui.tableWidget_tablo.setItem(indexSatır,indexSutun,QTableWidgetItem(str(kayıtSutun)))

    ui.tableWidget_tablo.update()


listele()


def kategorile():
    sıra = ui.comboBox_kategori.currentText()
    sorgu = "select * from otopark where ARAÇ_TÜRÜ = ?"
    islem.execute(sorgu,(sıra,))
    ui.tableWidget_tablo.clear()
    for indexSatır, kayıtNumarası in enumerate(islem):
        for indexSutun, kayıtSutun in enumerate(kayıtNumarası):
            ui.tableWidget_tablo.setItem(indexSatır,indexSutun,QTableWidgetItem(str(kayıtSutun)))

def sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Onayı","Silmek İstediğinizden Emin misiniz?",QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        kayit = ui.tableWidget_tablo.selectedItems()
        silinecek_kayit = kayit[0].text()

        sorgu = "delete from otopark where ARAÇ_SAHİBİ = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata!!"+ str(error))
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")


    


#BUTON
ui.pushButton_EKLE.clicked.connect(bilgi_ekle)
ui.pushButton_EKLE.clicked.connect(listele)
ui.pushButton_listele.clicked.connect(kategorile)
ui.pushButton_sil.clicked.connect(sil)
ui.pushButton_sil.clicked.connect(listele)






sys.exit(uygulama.exec_())