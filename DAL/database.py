import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.baglanti = sqlite3.connect("DB/library.db")
        self.imlec=self.baglanti.cursor()
        self.tablolari_olustur() #sınıf çağırılır çağırılmaz tabloları oluşturmak için

    def tablolari_olustur(self):
        #kitaplar tablosu
        self.imlec.execute("""
                           CREATE TABLE IF NOT EXISTS Kitaplar (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           ad TEXT NOT NULL,
                           yazar TEXT NOT NULL,
                           durum TEXT DEFAULT 'Rafta')
                           """)
        #kullanıcılar tablosu 
        self.imlec.execute("""
                           CREATE TABLE IF NOT EXISTS Kullanicilar (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           kullanici_adi TEXT NOT NULL UNIQUE,
                           sifre TEXT NOT NULL,
                           rol TEXT NOT NULL)
                        """)
        #commit atıyoruz ki, execucte ile oluşturduklarımız kalıcı olsun
        self.baglanti.commit()
        print("Bilgi Mesajı: Veritabanı bağlantısı kuruldu ve tablolar hazırlandı!")

    def _sifre_hashle(self, ham_sifre):
        #dışarıdan çağırırlmaması için encapsüle ettik, başına _ koyduk. 
        return hashlib.sha256(ham_sifre.encode('utf-8')).hexdigest()

    def kullanici_ekle(self, kullanici_adi, sifre, rol):
        try:
            guvenli_sifre = self._sifre_hashle(sifre)
            self.imlec.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre, rol) VALUES (?, ?, ?)",
                               (kullanici_adi, guvenli_sifre, rol))
            #commit atarak dbye kayediyoruz
            self.baglanti.commit()
            print(f"Bilgi Mesajı: Kullanıcı '{kullanici_adi}' eklendi.")
        except sqlite3.IntegrityError:
            print(f"Hata: Kullanıcı adı '{kullanici_adi}' zaten mevcut.")
    def sifre_dogrula(self, kullanici_adi, girilen_sifre):
        #login'de kullanılacak method
        hashli_giris=self._sifre_hashle(girilen_sifre)
        self.imlec.execute("SELECT rol FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, hashli_giris))
        #eşleşme bulursa fetchone rolü getirir, adfmin uye veya none. 
        kullanici = self.imlec.fetchone()
        if kullanici:
            print(f"Giriş Başarılı! Hoş geldin {kullanici_adi}.")
            return kullanici[0] #rolü döndürüyoruz
        else:
            print("Giriş Başarısız! Kullanıcı adı veya şifre yanlış.")
            return None

    def sifre_degistir(self, kullanici_adi, yeni_sifre):
        yeni_guvenli_sifre= self._sifre_hashle(yeni_sifre)
        self.imlec.execute("UPDATE Kullanicilar SET sifre=? WHERE kullanici_adi=?", (yeni_guvenli_sifre, kullanici_adi))
        self.baglanti.commit()
        print(f"Bilgi Mesajı: '{kullanici_adi}' adlı kullanıcının şifresi başarıyla güncellendi.")

    def kitap_ekle(self, ad, yazar):
        self.imlec.execute("INSERT INTO Kitaplar (ad, yazar) VALUES (?, ?)", (ad, yazar))
        self.baglanti.commit()
        print(f"Bilgi Mesajı: Kitap '{ad}' kütüphaneye eklendi.")

    def baglantiyi_kapat(self):
        self.baglanti.close()
        print("Bilgi Mesajı: Veritabanı bağlantısı kapatıldı!")

if __name__ == "__main__":    
    db = Database()
#örnek kullanıcılar ekleyelim, bir admin bir de üye uyduralım
    db.kullanici_ekle("Hazal", "hazal123", "Admin") #k.adı, şifre, rol parametrelerini giriyoruz
    db.kullanici_ekle("Ahmet", "ahmet123", "Üye")
#örnek birkaç kitap da seedleyelim
    db.kitap_ekle("Sefiller", "Victor Hugo")
    db.kitap_ekle("Suç ve Ceza", "Fyodor Dostoevsky")
    db.baglantiyi_kapat()