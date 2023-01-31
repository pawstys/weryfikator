from weryfikator import sprawdz

# Przykład testowy ze strony: https://obywatel.gov.pl/pl/dokumenty-i-dane-osobowe/czym-jest-numer-pesel
def test_SprawdzSumePESEL():
    pesel = '02070803628'
    assert sprawdz.SprawdzSumePESEL(pesel)
# weryfikacja błędnego numeru PESEL - zmieniona ostatnia cyfra:
    pesel = '02070803629'
    assert sprawdz.SprawdzSumePESEL(pesel) == False

def test_PobierzDanePESEL():
    pesel = '02070803628'
    assert sprawdz.PobierzDanePESEL(pesel) == 'PESEL należy do kobiety urodzonej w dniu 08.07.1902 r.'

# Przykład testowy ze strony: http://www.krs-online.com.pl/urzedy-skarbowe-3.html
# Do weryfikacji użyto podany NIP Izby Skarbowej w Warszawie
def test_SprawdzSumeNIP():
    nip = '5251007278'
    assert sprawdz.SprawdzSumeNIP(nip)
# weryfikacja błędnego numeru NIP - zmieniona ostatnia cyfra:
    nip = '5251007279'
    assert sprawdz.SprawdzSumeNIP(nip) == False

def test_PobierzModuloUS():
    nip = '5251007278'
    assert sprawdz.PobierzModuloUS(nip[0:3]) == 'NIP nadany przez Pierwszy Urząd Skarbowy Warszawa-Śródmieście'

# Przykłady testowe ze strony: https://www.gov.pl/web/kas/rachunki-bankowe-urzedow-skarbowych-obowiazujace-od-1012020-r
def test_SprawdzSumeNRB():
    boleslawiec = ['71101000712223020245000000','32101000550200202000070000','34101000550200202001000000']
    brodnica = ['91101000712223040343000000','08101000550200403000070000','10101000550200403001000000']
    bilgoraj = ['35101000712223060330000000','29101000550200603000070000','31101000550200603001000000']
    for i in boleslawiec:
        assert sprawdz.SprawdzSumeNRB('PL', i)
    for i in brodnica:
        assert sprawdz.SprawdzSumeNRB('PL', i)
    for i in bilgoraj:
        assert sprawdz.SprawdzSumeNRB('PL', i)
# weryfikacja błędnych numerów NRB - zmienione ostatnie cyfry:
    boleslawiec = ['71101000712223020245000001','32101000550200202000070001','34101000550200202001000001']
    brodnica = ['91101000712223040343000001','08101000550200403000070001','10101000550200403001000001']
    bilgoraj = ['35101000712223060330000001','29101000550200603000070001','31101000550200603001000001']
    for i in boleslawiec:
        assert sprawdz.SprawdzSumeNRB('PL', i) == False
    for i in brodnica:
        assert sprawdz.SprawdzSumeNRB('PL', i) == False
    for i in bilgoraj:
        assert sprawdz.SprawdzSumeNRB('PL', i) == False
