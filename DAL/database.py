import sqlite3

class Database:
    def __init__(self):
        self.baglanti = sqlite3.connect("kutuphane.db")
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
                           CREATE TABLE IF NOT EXISTS Kullanicilar 
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           kullanici_adi TEXT NOT NULL UNIQUE,
                           sifre TEXT NOT NULL,
                           rol TEXT NOT NULL)
                        """)
        #commit atıyoruz ki, execucte ile oluşturduklarımız kalıcı olsun
        self.baglanti.commit()
        print("Bilgi Mesajı: Veritabanı bağlantısı kuruldu ve tablolar hazırlandı!")

    def kullanici_ekle(self, kullanici_adi, sifre, rol):
        try:
            self.imlec.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre, rol) VALUES (?, ?, ?)",
                               (kullanici_adi, sifre, rol))
            #commit atarak dbye kayediyoruz
            self.baglanti.commit()
            print(f"Bilgi Mesajı: Kullanıcı '{kullanici_adi}' eklendi.")
        except sqlite3.IntegrityError:
            print(f"Hata: Kullanıcı adı '{kullanici_adi}' zaten mevcut.")

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