from csv import reader
from lxml import etree
from tkinter import Tk, ttk

class sprawdz():

    def SprawdzSumePESEL(pesel):
        wagi = '1379137913'
        suma = 0
        for i in range(len(wagi)):
            suma += int(pesel[i]) * int(wagi[i]) % 10
        suma = 10 - suma % 10
        if int(pesel[len(wagi)]) != suma:
            return False
        else:
            return True

    def PobierzDanePESEL(pesel):
        rok = 1900 + int(pesel[0:2])
        miesiac = int(pesel[2:4])
        dzien = int(pesel[4:6])
        plec = int(pesel [9:10])
        if miesiac > 80:
            rok -= 100
            miesiac -= 80
        while miesiac > 20:
            rok += 100
            miesiac -= 20
        plec %= 2
        if plec:
            tekst = 'PESEL należy do mężczyzny urodzonego w dniu '
        else:
            tekst = 'PESEL należy do kobiety urodzonej w dniu '
        tekst += str(dzien).zfill(2) + "." + str(miesiac).zfill(2) + "." + str(rok) + ' r.'
        return tekst

    def SprawdzSumeNIP(nip):
        wagi = '657234567'
        suma = 0
        for i in range(len(wagi)):
            suma += int(nip[i]) * int(wagi[i])
        suma = suma % 11
        if int(nip[len(wagi)]) != suma:
            return False
        else:
            return True

    def PobierzModuloUS(modulo):
        plik_csv = 'US_NIP.csv'
        with open(plik_csv, encoding='UTF-8') as f:
            dane = reader(f, delimiter=';')
            for wiersz in dane:
                if modulo == wiersz[0]:
                    return f'NIP nadany przez {wiersz[1]}'
        return 'Nieprawidłowe modulo US'

    def SprawdzSumeNRB(kraj,nrb):
        modulo = nrb[2:10]
        wagi = '3971397'
        suma = 0
        for i in range(len(wagi)):
            suma += int(modulo[i]) * int(wagi[i])
        suma = suma % 10
        if suma != 0:
            suma = 10 - suma
        if int(modulo[len(wagi)]) != suma:
            return False
        iban = kraj + nrb
        iban = iban[4:] + iban[:4]
        for i in range(10,36):
            iban = iban.replace(chr(i+55), str(i))
        if int(iban) % 97 == 1:
            return True
        else:
            return False

    def PobierzDaneBanku(modulo):
        plik_xml = 'plewiba.xml'
        parser = etree.XMLParser(ns_clean=True, encoding='UTF-8')
        tree = etree.parse(plik_xml,parser)
        instytucje = tree.getroot()
        nrrozliczeniowe = instytucje.findall('.//NrRozliczeniowy')
        for nrrozliczeniowy in nrrozliczeniowe:
            if nrrozliczeniowy.text == modulo:
                numerrozliczeniowy = nrrozliczeniowy.getparent()
                jednostka = numerrozliczeniowy.getparent()
                daneadresowe = jednostka.find('DaneAdresowe')
                instytucja = jednostka.getparent()
                wynik = f"Rachunek prowadzony przez {instytucja.find('NazwaInstytucji').text}\n"
                wynik += jednostka.find('NazwaJednostki').text + '\n'
                wynik += f"{daneadresowe.find('kraj').text.capitalize()}, województwo {daneadresowe.find('wojewodztwo').text.lower()}\n"
                wynik += f"{daneadresowe.find('ulica').text} {daneadresowe.find('numerBudynku').text}\n"
                wynik += f"{daneadresowe.find('kodPocztowy').text} {daneadresowe.find('poczta').text}\n"
                for bic in numerrozliczeniowy.findall('KodyBIC'):
                    wynik += bic.text + '\n'
        return wynik[:-1]

class app_ui(Tk):
    def __init__(self):
        super().__init__()
        self.title('Weryfikator')
        self.karty = ttk.Notebook(self)

        self.karta_PESEL = ttk.Frame(self.karty)
        self.karta_NIP = ttk.Frame(self.karty)
        self.karta_NRB = ttk.Frame(self.karty)
        self.karta_about = ttk.Frame(self.karty)

        self.karty.add(self.karta_PESEL, text='PESEL')
        self.karty.add(self.karta_NIP, text='NIP')
        self.karty.add(self.karta_NRB, text='NRB')
        self.karty.add(self.karta_about, text='O programie')
        self.karty.pack(expand=1, fill='both')

        ttk.Label(self.karta_PESEL, text='Wprowadź PESEL: ').grid(column=0, row=0, pady=10)
        self.pesel = ttk.Entry(self.karta_PESEL)
        self.pesel.grid(column=1, row=0, ipadx=28)
        ttk.Button(self.karta_PESEL,text='Weryfikuj', command=self.sprawdz_pesel).grid(column=0, row=1, columnspan=2 ,pady=0, ipadx=30)
        self.pesel_wynik = ttk.Label(self.karta_PESEL)
        self.pesel_wynik.grid(column=0, row=2,columnspan=2, pady=10)

        ttk.Label(self.karta_NIP, text='Wprowadź NIP:   ').grid(column=0, row=0, pady=10)
        self.nip = ttk.Entry(self.karta_NIP)
        self.nip.grid(column=1, row=0, ipadx=28)
        ttk.Button(self.karta_NIP,text='Weryfikuj', command=self.sprawdz_nip).grid(column=0, row=1, columnspan=2 ,pady=0, ipadx=30)
        self.nip_wynik = ttk.Label(self.karta_NIP)
        self.nip_wynik.grid(column=0, row=2,columnspan=2, pady=10)

        ttk.Label(self.karta_NRB, text='Wprowadź NRB:   ').grid(column=0, row=0, pady=10)
        self.nrb = ttk.Entry(self.karta_NRB)
        self.nrb.grid(column=1, row=0, ipadx=28)
        ttk.Button(self.karta_NRB,text='Weryfikuj', command=self.sprawdz_nrb).grid(column=0, row=1, columnspan=2 ,pady=0, ipadx=30)
        self.nrb_wynik = ttk.Label(self.karta_NRB)
        self.nrb_wynik.grid(column=0, row=2,columnspan=2, pady=10)

        about = 'Program służy do weryfikacji sum kontrolnych\n'
        about += 'numerów PESEL, NIP oraz rachunków bankowych\n'
        about += 'Autorem tego programu jest Paweł Styś\n'
        about += 'Program jest rozpowszechniany na licencji GPL\n'
        about += 'Autor nie gwarantuje poprawności dziania programu\n'
        about += 'ani wydania jego aktualizacji w przyszłości'
        ttk.Label(self.karta_about, text=about).grid(column=0, row=0, pady=10)

    def sprawdz_pesel(self):
        pesel = self.pesel.get()
        komunikat = f'Wprowadzono PESEL: {pesel}\n' 
        try:
            if sprawdz.SprawdzSumePESEL(pesel):
                komunikat += 'Suma kontrolna poprawna\n'
                komunikat += sprawdz.PobierzDanePESEL(pesel)
            else:
                komunikat += 'Suma kontrolna niepoprawna'
        except:
            komunikat += 'Wartość nieprawidłowa'
        self.pesel_wynik.config(text=komunikat)

    def sprawdz_nip(self):
        nip = self.nip.get().replace('-','')
        komunikat = f'Wprowadzono NIP: {nip}\n'
        try:
            if sprawdz.SprawdzSumeNIP(nip):
                komunikat += 'Suma kontrolna poprawna\n'
                komunikat += sprawdz.PobierzModuloUS(nip[:3])
            else:
                komunikat += 'Suma kontrolna niepoprawna'
        except:
            komunikat += 'Wartość nieprawidłowa'
        self.nip_wynik.config(text=komunikat)

    def sprawdz_nrb(self):
        rachunek = self.nrb.get().replace(' ','')
        komunikat = f'Wprowadzono NRB: {rachunek[0:2]} {rachunek[2:6]} {rachunek[6:10]} {rachunek[10:14]} {rachunek[14:18]} {rachunek[18:22]} {rachunek[22:26]}\n'
        try:
            if sprawdz.SprawdzSumeNRB('PL', rachunek):
                komunikat += 'Suma kontrolna poprawna\n'
                komunikat += sprawdz.PobierzDaneBanku(rachunek[2:10])
            else:
                komunikat += 'Suma kontrolna niepoprawna'
        except:
            komunikat += 'Wartość nieprawidłowa'
        self.nrb_wynik.config(text=komunikat)

if __name__ == '__main__':

    aplikacja = app_ui()
    aplikacja.mainloop()