from beallitasok import *

clock = pygame.time.Clock()
kepernyo = pygame.display.set_mode((KEPERNYO_SZELESSEG, KEPERNYO_MAGASSAG))
jatek_futas = False
hang_be = True
clock.tick(60)


class Gomb():
    def __init__(self, kep, kep1, kep2, x_pozicio, y_pozicio):
        self.kep = kep
        self.kep1 = kep1
        self.kep2 = kep2
        self.x_pozicio = x_pozicio
        self.y_pozicio = y_pozicio
        self.rect = self.kep.get_rect(center=(self.x_pozicio, self.y_pozicio))

    def frissites(self):   #itt ratesszuk a kepet a megadott koordinatakra
        kepernyo.blit(self.kep, self.rect)

    def check_for_input(self, pozicio):  #ez vizsgalja, hogyha az egeret a gombra visszuk
        if pozicio[0] in range(self.rect.left, self.rect.right) and pozicio[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def szin_csere(self, pozicio):  #ha az eger a gombon van, akkor megvaltozik a szoveg szine
        if pozicio[0] in range(self.rect.left, self.rect.right) and pozicio[1] in range(self.rect.top, self.rect.bottom):
            self.kep = self.kep2
        else:
            self.kep = self.kep1


class Platform():
    def __init__(self, kep, kep1, kep2, x_pozicio, y_pozicio):
        self.kep = kep
        self.kep1 = kep1
        self.kep2 = kep2
        self.x_pozicio = x_pozicio
        self.y_pozicio = y_pozicio
        self.rect = self.kep.get_rect(topleft=(self.x_pozicio, self.y_pozicio))
        self.loves = False
        self.kezdo_pontok = pontok

    def platform_pozicio(self, pozicio):
        if pozicio[0] > 200 and pozicio[0] < KEPERNYO_SZELESSEG - 200:  #igy nem tudjuk kivinni a platformot a kepernyon kivulre
            self.rect.x = int(pozicio[0]) - 200  #igy a mouse mindig a platform kozepet jelenti

    def frissites(self):

        if pontok - self.kezdo_pontok >= 5:  #ha a platform tud lezert loni
            self.kep = self.kep2
            self.loves = True

        else:                                #ha a platform nem tud lezert loni
            self.kep = self.kep1
            self.loves = False

        kepernyo.blit(self.kep, self.rect)


class Labda():
    SEBESSEG = 5

    def __init__(self, kep, x, y):
        self.kep = kep
        self.x = x
        self.y = y
        self.x_sebesseg = 0
        self.y_sebesseg = -self.SEBESSEG
        self.rect = self.kep.get_rect(topleft=(self.x, self.y))

    def mozgas(self):   #igy a labda folyamatosan mozog
        self.x += self.x_sebesseg
        self.y += self.y_sebesseg

        self.rect.x += self.x_sebesseg
        self.rect.y += self.y_sebesseg

    def sebesseg_beallitas(self, x_sebesseg, y_sebesseg):
        self.x_sebesseg = x_sebesseg
        self.y_sebesseg = y_sebesseg

    def frissites(self):
        kepernyo.blit(self.kep, self.rect)

    def pattogas_fal(labda):    #ha a labda falnak utkozik, derekszogben visszapattan
        if labda.x <= 0 or labda.x + labda_atmero >= KEPERNYO_SZELESSEG:
            if hang_be:
                hang_pattogas = mixer.Sound("hang_effektek/hang_pattanas.mp3")
                hang_pattogas.play()
            labda.sebesseg_beallitas(labda.x_sebesseg * -1, labda.y_sebesseg)

        if labda.y <= 0:
            if hang_be:
                hang_pattogas = mixer.Sound("hang_effektek/hang_pattanas.mp3")
                hang_pattogas.play()
            labda.sebesseg_beallitas(labda.x_sebesseg, labda.y_sebesseg * -1)

    def pattogas_platform(self, platform):  #ha a platformnak utkozik, akkor tobb fele modon pattanhat vissza
        utkozes_tolerancia = 10  # mivel a pixelek nagyon gyorsan mozognak, ezert meg kell adjuk, egy toleranciat, hogy ne fedjek at egymast

        if self.rect.colliderect(platform.rect):  # itt vizsgaljuk, ha a labda utkozik a platformmal
            if abs(platform.rect.top - self.rect.bottom) < utkozes_tolerancia:
                platform_kozepe = platform.rect.x + 200  # megnezzuk, hogy hol van a platform kozepe
                tavolsag_a_kozepeig = self.x - platform_kozepe  # ha ez az ertek pozitiv, akkor a labda a jobb, ha negativ,
                                                                # akkor a bal oldalan van a platformnak

                szazalekos_szelesseg = tavolsag_a_kozepeig / 400  # elosztjuk a platform hosszaval, hogy kapjunk egy szamot 1 es 0 kozott
                szog = szazalekos_szelesseg * 90  # atalakitjuk szogge
                szog_radian = math.radians(szog)  # atalakitjuk radianna

                # ket egyszeru keplet alapjan megvaltoztatjuk a labda iranyat
                self.x_sebesseg = math.sin(szog_radian) * labda.SEBESSEG
                self.y_sebesseg = math.cos(szog_radian) * labda.SEBESSEG * -1

                if hang_be:
                    hang_pattogas_platform = mixer.Sound("hang_effektek/hang_pattogas_platform.mp3")
                    hang_pattogas_platform.play()

                labda.sebesseg_beallitas(int(self.x_sebesseg), int(self.y_sebesseg))

            if abs(platform.rect.left - self.rect.right) < utkozes_tolerancia:
                if hang_be:
                    hang_pattogas_platform = mixer.Sound("hang_effektek/hang_pattogas_platform.mp3")
                    hang_pattogas_platform.play()
                self.x_sebesseg *= -1

            if abs(platform.rect.right - self.rect.left) < utkozes_tolerancia:
                if hang_be:
                    hang_pattogas_platform = mixer.Sound("hang_effektek/hang_pattogas_platform.mp3")
                    hang_pattogas_platform.play()
                self.x_sebesseg *= -1


class Zuhanas():
    SEBESSEG = 3

    def __init__(self, x, y, kep, kep2, bomba, allapot):
        self.x = x
        self.y = y
        self.kep = kep
        self.kep2 = kep2
        self.bomba = bomba
        self.rect = self.kep.get_rect(topleft=(self.x, self.y))
        self.allapot = allapot

    def frissites(self):
        kepernyo.blit(self.kep, self.rect)

    def utkozes(self):  #ha a lezuhano buborek utkozik a platformmal
        if self.rect.colliderect(platform.rect):
            if not self.bomba:
                if hang_be:
                    hang_sziv = mixer.Sound("hang_effektek/hang_sziv_felveves.mp3")
                    hang_sziv.play()
                self.kep = self.kep2
                eletcsik.sziv += 1

            else:
                if hang_be:
                    hang_robbanas = mixer.Sound("hang_effektek/hang_robbanas.mp3")
                    hang_robbanas.play()
                self.kep = self.kep2
                eletcsik.sziv -= 1

            self.allapot -= 1

        elif self.rect.colliderect(lezer.rect) and lezer.van and self.bomba:    #ha a lezer kilovi a bombat
            if hang_be:
                hang_robbanas = mixer.Sound("hang_effektek/hang_robbanas.mp3")
                hang_robbanas.play()
            self.kep = self.kep2
            lezer.van = False
            self.allapot -= 1

    def mozgas(self):
        self.y += self.SEBESSEG
        self.rect.y += self.SEBESSEG


class Eletcsik():
    def __init__(self, kep):
        self.kep = kep
        self.kep1 = ELETCSIK_1
        self.kep2 = ELETCSIK_2
        self.kep3 = ELETCSIK_3
        self.kep4 = ELETCSIK_4
        self.x = KEPERNYO_SZELESSEG - 210
        self.y = 10
        self.rect = self.kep.get_rect(topleft=(self.x, self.y))
        self.sziv = 3

    def frissites(self):
        if labda.y > KEPERNYO_MAGASSAG: #ha leesik a labda
            self.sziv -= 1
            return True

        if self.sziv == 0:
            return True

        elif self.sziv == 1:
            self.kep = self.kep1

        elif self.sziv == 2:
            self.kep = self.kep2

        elif self.sziv == 3:
            self.kep = self.kep3

        elif self.sziv == 4:
            self.kep = self.kep4

        elif self.sziv > 4:
            self.sziv = 4

        kepernyo.blit(self.kep, self.rect)

class Lezer():
    SEBESSEG = 5

    def __init__(self, kep, x, y, van):
        self.kep = kep
        self.x = x
        self.y = y
        self.van = van
        self.rect = self.kep.get_rect(center=(self.x, self.y))

    def frissites(self):
        kepernyo.blit(self.kep, self.rect)

    def mozgas(self):
        self.y -= self.SEBESSEG
        self.rect.y -= self.SEBESSEG

        if self.y + 100 < 0:
            self.van = False


class Tegla():
    def __init__(self, x, y, kep):
        self.x = x
        self.y = y
        self.kep = kep
        self.kep2 = TEGLA_PIROS_REPEDT
        self.kep3 = TEGLA_ZOLD_REPEDT
        self.szelesseg = TEGLA_SZELESSEG
        self.magassag = TEGLA_MAGASSAG
        self.allapot = 1
        self.rect = self.kep.get_rect(topleft=(self.x, self.y))

    def frissites(self):
        kepernyo.blit(self.kep, self.rect)

    def utkozes(self, labda):
        if lezer.van:   #ha a lezerrel utkozik
            if self.rect.colliderect(lezer.rect):
                lezer.van = False
                self.erintkezes()
                if hang_be:
                    hang_lezer_becsapodas = mixer.Sound("hang_effektek/lezer_becsapodas_hang.mp3")
                    hang_lezer_becsapodas.play()
                return True
        #ha nem utkozik a labdaval, akkor hamis erteket terit vissza
        if not ((labda.x <= self.x + self.szelesseg and labda.x >= self.x) or (
                labda.x + labda_atmero <= self.x + self.szelesseg and labda.x + labda_atmero >= self.x)):
            return False
        if not ((labda.y <= self.y + self.magassag and labda.y >= self.y) or (
                labda.y + labda_atmero <= self.y + self.magassag and labda.y + labda_atmero >= self.y)):
            return False

        utkozes_tolerancia = 10

        #ez vizsgalja, hogyha a labda erintkezik egy teglaval
        if abs(self.rect.top - labda.rect.bottom) < utkozes_tolerancia or abs(
                self.rect.bottom - labda.rect.top) < utkozes_tolerancia:
            labda.sebesseg_beallitas(labda.x_sebesseg, labda.y_sebesseg * -1)
            self.erintkezes()
            if hang_be:
                hang_pattogas = mixer.Sound("hang_effektek/hang_pattanas.mp3")
                hang_pattogas.play()
            return True

        if abs(self.rect.left - labda.rect.right) < utkozes_tolerancia or abs(
                self.rect.right - labda.rect.left) < utkozes_tolerancia:
            labda.sebesseg_beallitas(labda.x_sebesseg * -1, labda.y_sebesseg)
            self.erintkezes()
            if hang_be:
                hang_pattogas = mixer.Sound("hang_effektek/hang_pattanas.mp3")
                hang_pattogas.play()
            return True

    def erintkezes(self):
        self.allapot += 1

        if self.allapot == 2 and self.kep == TEGLA_PIROS:
            self.kep = self.kep2

        elif self.allapot == 2 and self.kep == TEGLA_ZOLD:
            self.kep = self.kep3


#letrehozzuk a gombokat
gomb_jatek = Gomb(GOMB_JATEK_PIROS, GOMB_JATEK_PIROS, GOMB_JATEK_ZOLD, KEPERNYO_SZELESSEG/2, 300)
gomb_beallitasok = Gomb(GOMB_BEALLITASOK_PIROS, GOMB_BEALLITASOK_PIROS, GOMB_BEALLITASOK_ZOLD, KEPERNYO_SZELESSEG/2, 572)
gomb_ranglista = Gomb(GOMB_RANGLISTA_PIROS, GOMB_RANGLISTA_PIROS, GOMB_RANGLISTA_ZOLD, KEPERNYO_SZELESSEG/2, 848)

gomb_kilepes = Gomb(GOMB_KILEPES_KEREK, GOMB_KILEPES_KEREK, GOMB_KILEPES_PIROS, 50, 50)
gomb_visszanyil = Gomb(GOMB_VISSZANYIL_KEREK, GOMB_VISSZANYIL_KEREK, GOMB_VISSZANYIL_FEHER, 50, 50)
gomb_menu = Gomb(GOMB_MENU_FEKETE, GOMB_MENU_FEKETE, GOMB_MENU_FEHER, 50, 50)
gomb_hang = Gomb(GOMB_HANG_BE, GOMB_HANG_BE, GOMB_HANG_KI, KEPERNYO_SZELESSEG/2, 50)

gomb_vissza_a_jatekba = Gomb(GOMB_VISSZA_A_JATEKBA_PIROS, GOMB_VISSZA_A_JATEKBA_PIROS, GOMB_VISSZA_A_JATEKBA_ZOLD, KEPERNYO_SZELESSEG/2, 1155)
gomb_jatek_beallitasok = Gomb(GOMB_JATEK_BEALLITASOK_PIROS, GOMB_JATEK_BEALLITASOK_PIROS, GOMB_JATEK_BEALLITASOK_ZOLD, KEPERNYO_SZELESSEG/2, 1325)
gomb_jatek_kilepes = Gomb(GOMB_JATEK_KILEPES_PIROS, GOMB_JATEK_KILEPES_PIROS, GOMB_JATEK_KILEPES_ZOLD, KEPERNYO_SZELESSEG/2, 1495)

gomb_labda_kosar = Gomb(GOMB_LABDA_KOSAR, GOMB_LABDA_KOSAR, GOMB_LABDA_KOSAR_KIVALASZTVA, 240, 900)
gomb_labda_foci = Gomb(GOMB_LABDA_FOCI, GOMB_LABDA_FOCI, GOMB_LABDA_FOCI_KIVALASZTVA, 720, 900)
gomb_labda_strand = Gomb(GOMB_LABDA_STRAND, GOMB_LABDA_STRAND, GOMB_LABDA_STRAND_KIVALASZTVA, 1200, 900)
gomb_labda_tenisz = Gomb(GOMB_LABDA_TENISZ, GOMB_LABDA_TENISZ, GOMB_LABDA_TENISZ_KIVALASZTVA, 1680, 900)
gomb_labda_volley = Gomb(GOMB_LABDA_VOLLEY, GOMB_LABDA_VOLLEY, GOMB_LABDA_VOLLEY_KIVALASZTVA, 480, 550)
gomb_labda_baseball = Gomb(GOMB_LABDA_BASEBALL, GOMB_LABDA_BASEBALL, GOMB_LABDA_BASEBALL_KIVALASZTVA, 1440, 550)

#alapbol a kosarlabda van kivalasztva, de ezt a beallitasoknal ki lehet cserelni
labda_atmero = 50
labda_kivalasztott = GOMB_LABDA_KOSAR
labda_kivalasztott = pygame.transform.scale(labda_kivalasztott, (labda_atmero, labda_atmero))
gomb_labda_kosar.kep = gomb_labda_kosar.kep2


def kezdokepernyo():    #letrehozzuk a kezdokepernyot. Gombok megnyomasaval ablakokat lehet megnyitni
    global jatek_futas, hang_be
    pygame.display.set_caption("Kezdőképernyő")
    jatek_futas = False
    uj_ablak_megnyitasa = 0

    while uj_ablak_megnyitasa == 0:

        kepernyo.blit(KEZDO_HATTER, (0, 0))
        kezdokepernyo_mouse_pozicio = pygame.mouse.get_pos()    #ez figyeli a mouse helyzetet

        billentyu = pygame.key.get_pressed()    #ez figyeli, ha le van nyomva egy billentyu

        for gomb in [gomb_jatek, gomb_beallitasok, gomb_ranglista, gomb_kilepes]:   #ha a gombon van az eger, akkor megvqaltozik a gomb szine
            gomb.szin_csere(kezdokepernyo_mouse_pozicio)
            gomb.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #igy tudjuk leallitani a jatekot
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or billentyu[pygame.K_ESCAPE]:
                if gomb_jatek.check_for_input(kezdokepernyo_mouse_pozicio) and not billentyu[pygame.K_ESCAPE]:  #ha a jatek gombra klikkelunk, elindul a jatek
                    uj_ablak_megnyitasa = 2
                    break

                if gomb_beallitasok.check_for_input(kezdokepernyo_mouse_pozicio) and not billentyu[pygame.K_ESCAPE]:    #ha a beallitasok gombra klikkelunk, elojonnek a beallitasok
                    uj_ablak_megnyitasa = 3
                    break

                if gomb_ranglista.check_for_input(kezdokepernyo_mouse_pozicio) and not billentyu[pygame.K_ESCAPE]:  #ha a ranglista gombra klikkelunk, elojon a ranglista
                    uj_ablak_megnyitasa = 4
                    break

                if gomb_kilepes.check_for_input(kezdokepernyo_mouse_pozicio) or billentyu[pygame.K_ESCAPE]: #masik modszer, hogy leallitsuk a jatekot
                    pygame.quit()
                    sys.exit()

        pygame.display.update()     #frissitjuk a kepernyot

    if uj_ablak_megnyitasa == 2:
        jatek()

        if masodik_palya:
            jatek2()

    elif uj_ablak_megnyitasa == 3:
        beallitasok()

    elif uj_ablak_megnyitasa == 4:
        ranglista()


def jatek():
    global jatek_futas, labda, platform, teglak, PALYA_FELEPITES, eletcsik, lezer, pontok, masodik_palya, kezdoido
    pygame.display.set_caption("Játék")
    jatek_futas = True  #ez arra kell, hogyha jatek kozben megnyitjuk a beallitasokat, akkor onnan kilepve tudjuk folytatni a jatekot
    pontok = 0
    masodik_palya = False
    teglak = []
    bombak = []
    szivek = []
    kezdoido = datetime.now()

    PALYA_FELEPITES = [
        '       XXXXX       ',
        '      XXXOXXX      ',
        '     XXXO OXXX     ',
        '   XXOO     OOXX   ',
        '  XXO         OXX  ',
        '  XXO         OXX  ',
        '   XXOO     OOXX   ',
        '     XXXO OXXX     ',
        '      XXXOXXX      ',
        '       XXXXX       ']

    # platform es labda deklaralasa
    platform = Platform(PLATFORM_UJ, PLATFORM_UJ, PLATFORM_UJ_PIROS,  KEPERNYO_SZELESSEG / 2 - 200, KEPERNYO_MAGASSAG - 50)
    labda = Labda(labda_kivalasztott, KEPERNYO_SZELESSEG / 2, platform.y_pozicio - labda_atmero)
    eletcsik = Eletcsik(ELETCSIK_3)

    palya_felepites()

    zuhanas_sziv = Zuhanas(0, 0, SZIV_BUBOREK, KIPUKKANAS_BUBOREK, False, 10)
    zuhanas_sziv.allapot = 0

    bomba = Zuhanas(0, 0, SZIV_BUBOREK, KIPUKKANAS_BUBOREK, False, 10)
    bomba.allapot = 0

    lezer = Lezer(LEZER, 0, 0, False)

    transition(JATEK_HATTER, JATEK_HATTER3, False)

    szoveg = FONT.render(f"Pontok: {pontok}", True, (255, 255, 255))  # ez kiirja, hogy hany pontunk van
    kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 120, 20))

    if hang_be:
        mixer.music.load("hang_effektek/hatter_zene.mp3")
        mixer.music.play(-1)

    while True:

        if pontok == 136:
            mixer.music.stop()
            transition(JATEK_HATTER2, JATEK_HATTER, True)
            masodik_palya = True

            return 0

        kepernyo.blit(JATEK_HATTER, (0, 0))
        jatek_mouse_pozicio = pygame.mouse.get_pos()

        platform.platform_pozicio(jatek_mouse_pozicio)
        platform.frissites()

        labda.mozgas()
        labda.pattogas_fal()
        labda.pattogas_platform(platform)
        labda.frissites()

        gomb_menu.szin_csere(jatek_mouse_pozicio)
        gomb_menu.frissites()

        if eletcsik.frissites():   #ha eletet veszitunk
            if eletcsik.sziv > 0:
                labda = Labda(labda_kivalasztott, KEPERNYO_SZELESSEG / 2, platform.y_pozicio - labda_atmero)

            elif eletcsik.sziv <= 0:
                mixer.music.stop()
                vesztettel(pontok)
                return 0

        #vizsgaljuk, hogy utkozunk- e a teglakkal
        tores = 0   #ha veletlenul egyszerre ket teglahoz er a labda fuggoleges iranyban, akkor abban a for ciklusban csak az egyiket erzekelje utkozesnek
        for tegla in teglak:
            if tores == 0:
                if tegla.utkozes(labda):
                    tores = 1
                    pontok += 1

                    szoveg = FONT.render(f"Pontok: {pontok}", True, (255, 255, 255))  # ez kiirja, hogy hany pontunk van

                    if tegla.allapot > 2:
                        random_szam = random.randint(0, 10)

                        if eletcsik.sziv < 4:
                            if random_szam == 10:
                                zuhanas_sziv = Zuhanas(tegla.x, tegla.y, SZIV_BUBOREK, KIPUKKANAS_BUBOREK, False, 10)
                                szivek.append(zuhanas_sziv)

                        if random_szam <= 7:
                            bomba = Zuhanas(tegla.x, tegla.y, BOMBA_BUBOREK, ROBBANAS_BUBOREK, True, 10)
                            bombak.append(bomba)

                        teglak.remove(tegla)

            tegla.frissites()

        kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 120, 20))

        for sziv in szivek:
            if sziv.allapot:
                sziv.mozgas()
                if sziv.allapot == 10:
                    sziv.utkozes()
                sziv.frissites()

                if bomba.allapot == 1:
                    bombak.remove(bomba)

        for bomba in bombak:
            if bomba.allapot:
                bomba.mozgas()
                if bomba.allapot == 10:
                    bomba.utkozes()
                bomba.frissites()

                if bomba.allapot == 1:
                    bombak.remove(bomba)

        if lezer.van:
            lezer.mozgas()
            lezer.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  #ha megnyomjuk a gombot, vagy az ESC karaktert
                if gomb_menu.check_for_input(jatek_mouse_pozicio):
                    menu_animacio(-10, szoveg, zuhanas_sziv, bombak)
                    uj_ablak_megnyitasa = menu_futas(szoveg, zuhanas_sziv, bombak)

                    if uj_ablak_megnyitasa == 1:
                        menu_animacio(10, szoveg, zuhanas_sziv, bombak)

                    elif uj_ablak_megnyitasa == 0:
                        mixer.music.stop()
                        return 0

                elif not lezer.van and pontok - platform.kezdo_pontok >= 5:
                    if hang_be:
                        hang_lezer = mixer.Sound("hang_effektek/lezer_hang.mp3")
                        hang_lezer.play()
                    lezer = Lezer(LEZER, platform.rect.x + 200, platform.rect.y, True)
                    platform.kezdo_pontok = pontok

            elif event.type == pygame.KEYDOWN:

                billentyu = pygame.key.get_pressed()  # vizsgalja, hogy milyen billentyu van lenyomva

                if billentyu[pygame.K_ESCAPE]:
                    menu_animacio(-10, szoveg, zuhanas_sziv, bombak)
                    uj_ablak_megnyitasa2 = menu_futas(szoveg, zuhanas_sziv, bombak)

                    if uj_ablak_megnyitasa2 == 1:
                        menu_animacio(10, szoveg, zuhanas_sziv, bombak)

                    elif uj_ablak_megnyitasa2 == 0:
                        mixer.music.stop()
                        return 0

        pygame.display.update() #frissitjuk a kepernyot


def jatek2():
    global jatek_futas, labda, platform, teglak, PALYA_FELEPITES, eletcsik, lezer, pontok
    pygame.display.set_caption("Játék")

    idobonusz = 0
    teglak = []
    bombak = []
    szivek = []

    if hang_be:
        mixer.music.load("hang_effektek/hatter2_zene.mp3")
        mixer.music.play(-1)

    PALYA_FELEPITES = [
        ' O               O ',
        'OXO             OXO',
        ' O  X         X  O ',
        '   XOX  OOO  XOX   ',
        '    X  XOOOX  X    ',
        '      XX   XX      ',
        '      XX   XX      ',
        '    X  XOOOX  X    ',
        '   XOX  OOO  XOX   ',
        ' O  X         X  O ',
        'OXO             OXO',
        ' O               O ']

    palya_felepites()

    platform = Platform(PLATFORM_UJ, PLATFORM_UJ, PLATFORM_UJ_PIROS, KEPERNYO_SZELESSEG / 2 - 200, KEPERNYO_MAGASSAG - 50)
    labda = Labda(labda_kivalasztott, KEPERNYO_SZELESSEG / 2, platform.y_pozicio - labda_atmero)

    szoveg = FONT.render(f"Pontok: {pontok}", True, (255, 255, 255))  # ez kiirja, hogy hany pontunk van
    kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 120, 20))

    zuhanas_sziv = Zuhanas(0, 0, SZIV_BUBOREK, KIPUKKANAS_BUBOREK, False, 10)
    zuhanas_sziv.allapot = 0

    bomba = Zuhanas(0, 0, SZIV_BUBOREK, KIPUKKANAS_BUBOREK, False, 10)
    bomba.allapot = 0

    lezer = Lezer(LEZER, 0, 0, False)

    while True:

        if pontok == 264:
            mixer.music.stop()

            #idobonusz jar, ha a jatekos 7 perc alatt kiuti az osszes teglat
            mostido = datetime.now()
            if mostido < kezdoido + timedelta(minutes=7):
                idobonusz = 420 - int(mostido.second)

            osszes_pont = pontok + idobonusz + eletcsik.sziv * 10

            nyertel(pontok, idobonusz, osszes_pont)
            return 0

        kepernyo.blit(JATEK_HATTER2, (0, 0))
        jatek_mouse_pozicio = pygame.mouse.get_pos()

        platform.platform_pozicio(jatek_mouse_pozicio)
        platform.frissites()

        labda.mozgas()
        labda.pattogas_fal()
        labda.pattogas_platform(platform)
        labda.frissites()

        gomb_menu.szin_csere(jatek_mouse_pozicio)
        gomb_menu.frissites()

        if eletcsik.frissites():
            if eletcsik.sziv > 0:
                labda = Labda(labda_kivalasztott, KEPERNYO_SZELESSEG / 2, platform.y_pozicio - labda_atmero)

            elif eletcsik.sziv <= 0:
                mixer.music.stop()
                vesztettel(pontok)
                return 0

            else:
                mixer.music.stop()
                vesztettel(pontok)
                return 0

        #vizsgaljuk, hogy utkozunk- e a teglakkal
        tores = 0   #ha veletlenul egyszerre ket teglahoz er a labda fuggoleges iranyban, akkor abban a for ciklusban csak az egyiket erzekelje utkozesnek
        for tegla in teglak:
            if tores == 0:
                if tegla.utkozes(labda):
                    tores = 1
                    pontok += 1

                    szoveg = FONT.render(f"Pontok: {pontok}", True, (255, 255, 255))  # ez kiirja, hogy hany pontunk van

                    if tegla.allapot > 2:
                        random_szam = random.randint(0, 10)
                        print(random_szam)

                        if eletcsik.sziv < 4:
                            if random_szam == 10:
                                zuhanas_sziv = Zuhanas(tegla.x, tegla.y, SZIV_BUBOREK, KIPUKKANAS_BUBOREK, False, 10)
                                szivek.append(zuhanas_sziv)

                        if random_szam <= 7:
                            bomba = Zuhanas(tegla.x, tegla.y, BOMBA_BUBOREK, ROBBANAS_BUBOREK, True, 10)
                            bombak.append(bomba)

                        teglak.remove(tegla)

            tegla.frissites()

        kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 120, 20))

        for sziv in szivek:
            if sziv.allapot:
                sziv.mozgas()
                if sziv.allapot == 10:
                    sziv.utkozes()
                sziv.frissites()

                if bomba.allapot == 1:
                    bombak.remove(bomba)

        for bomba in bombak:
            if bomba.allapot:
                bomba.mozgas()
                if bomba.allapot == 10:
                    bomba.utkozes()
                bomba.frissites()

                if bomba.allapot == 1:
                    bombak.remove(bomba)

        if lezer.van:
            lezer.mozgas()
            lezer.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  #ha megnyomjuk a gombot, vagy az ESC billentyut
                if gomb_menu.check_for_input(jatek_mouse_pozicio):
                    menu_animacio(-10, szoveg, zuhanas_sziv, bombak)
                    uj_ablak_megnyitasa = menu_futas(szoveg, zuhanas_sziv, bombak)

                    if uj_ablak_megnyitasa == 1:
                        menu_animacio(10, szoveg, zuhanas_sziv, bombak)

                    elif uj_ablak_megnyitasa == 0:
                        mixer.music.stop()
                        return 0

                elif not lezer.van and pontok - platform.kezdo_pontok >= 5:
                    if hang_be:
                        hang_lezer = mixer.Sound("hang_effektek/lezer_hang.mp3")
                        hang_lezer.play()
                    lezer = Lezer(LEZER, platform.rect.x + 200, platform.rect.y, True)
                    platform.kezdo_pontok = pontok

            elif event.type == pygame.KEYDOWN:

                billentyu = pygame.key.get_pressed()  # vizsgalja, hogy milyen billentyu van lenyomva

                if billentyu[pygame.K_ESCAPE]:
                    menu_animacio(-10, szoveg, zuhanas_sziv, bombak)
                    uj_ablak_megnyitasa2 = menu_futas(szoveg, zuhanas_sziv, bombak)

                    if uj_ablak_megnyitasa2 == 1:
                        menu_animacio(10, szoveg, zuhanas_sziv, bombak)

                    elif uj_ablak_megnyitasa2 == 0:
                        mixer.music.stop()
                        return 0

        pygame.display.update() #frissitjuk a kepernyot


def transition(hatter_be, hatter_ki, hang):

    kepernyo.blit(hatter_ki, (0, 0))

    if hang_be and hang:
        hang_transition = mixer.Sound("hang_effektek/transition.mp3")
        hang_transition.play()

    y1 = -1080
    y2 = 0

    repul_animacio = 1

    while y1 < 0:

        kepernyo.blit(hatter_be, (0, y1))
        kepernyo.blit(hatter_ki, (0, y2))

        if repul_animacio == 1:
            kepernyo.blit(PLATFORM_REPULO, (KEPERNYO_SZELESSEG / 2 - 200, KEPERNYO_MAGASSAG - 150))
            repul_animacio = 2

        elif repul_animacio == 2:
            kepernyo.blit(PLATFORM_REPULO2, (KEPERNYO_SZELESSEG / 2 - 200, KEPERNYO_MAGASSAG - 150))
            repul_animacio = 3

        else:
            kepernyo.blit(PLATFORM_REPULO3, (KEPERNYO_SZELESSEG / 2 - 200, KEPERNYO_MAGASSAG - 150))
            repul_animacio = 1

        y1 += 2
        y2 += 2

        pygame.display.update()

    return 0


def beallitasok():
    global jatek_futas, labda_kivalasztott, hang_be, masodik_palya   #ez figyeli, hogy melyik labdat valasztottuk a beallitasoknal
    pygame.display.set_caption("Beállítások")

    if not jatek_futas:
        if hang_be:
            mixer.music.load("hang_effektek/beallitasok_zene.mp3")
            mixer.music.play(-1)

    while True:
        kepernyo.blit(BEALLITASOK_HATTER, (0, 0))
        beallitasok_mouse_pozicio = pygame.mouse.get_pos()

        billentyu = pygame.key.get_pressed()

        gomb_visszanyil.szin_csere(beallitasok_mouse_pozicio)
        gomb_visszanyil.frissites()

        for gomb in [gomb_labda_kosar, gomb_labda_baseball, gomb_labda_foci, gomb_labda_strand, gomb_labda_tenisz, gomb_labda_volley, gomb_hang]:
            gomb.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or billentyu[pygame.K_ESCAPE]:
                if (gomb_visszanyil.check_for_input(beallitasok_mouse_pozicio) or billentyu[pygame.K_ESCAPE]) and not jatek_futas:
                    mixer.music.stop()
                    return 1

                if (gomb_visszanyil.check_for_input(beallitasok_mouse_pozicio) or billentyu[pygame.K_ESCAPE]) and jatek_futas:
                    return 0

                if gomb_labda_kosar.check_for_input(beallitasok_mouse_pozicio):
                    gomb_labda_kosar.kep = gomb_labda_kosar.kep2
                    gomb_labda_baseball.kep = gomb_labda_baseball.kep1
                    gomb_labda_foci.kep = gomb_labda_foci.kep1
                    gomb_labda_strand.kep = gomb_labda_strand.kep1
                    gomb_labda_tenisz.kep = gomb_labda_tenisz.kep1
                    gomb_labda_volley.kep = gomb_labda_volley.kep1
                    labda_kivalasztott = GOMB_LABDA_KOSAR

                if gomb_labda_baseball.check_for_input(beallitasok_mouse_pozicio):
                    gomb_labda_kosar.kep = gomb_labda_kosar.kep1
                    gomb_labda_baseball.kep = gomb_labda_baseball.kep2
                    gomb_labda_foci.kep = gomb_labda_foci.kep1
                    gomb_labda_strand.kep = gomb_labda_strand.kep1
                    gomb_labda_tenisz.kep = gomb_labda_tenisz.kep1
                    gomb_labda_volley.kep = gomb_labda_volley.kep1
                    labda_kivalasztott = GOMB_LABDA_BASEBALL

                if gomb_labda_foci.check_for_input(beallitasok_mouse_pozicio):
                    gomb_labda_kosar.kep = gomb_labda_kosar.kep1
                    gomb_labda_baseball.kep = gomb_labda_baseball.kep1
                    gomb_labda_foci.kep = gomb_labda_foci.kep2
                    gomb_labda_strand.kep = gomb_labda_strand.kep1
                    gomb_labda_tenisz.kep = gomb_labda_tenisz.kep1
                    gomb_labda_volley.kep = gomb_labda_volley.kep1
                    labda_kivalasztott = GOMB_LABDA_FOCI

                if gomb_labda_strand.check_for_input(beallitasok_mouse_pozicio):
                    gomb_labda_kosar.kep = gomb_labda_kosar.kep1
                    gomb_labda_baseball.kep = gomb_labda_baseball.kep1
                    gomb_labda_foci.kep = gomb_labda_foci.kep1
                    gomb_labda_strand.kep = gomb_labda_strand.kep2
                    gomb_labda_tenisz.kep = gomb_labda_tenisz.kep1
                    gomb_labda_volley.kep = gomb_labda_volley.kep1
                    labda_kivalasztott = GOMB_LABDA_STRAND

                if gomb_labda_tenisz.check_for_input(beallitasok_mouse_pozicio):
                    gomb_labda_kosar.kep = gomb_labda_kosar.kep1
                    gomb_labda_baseball.kep = gomb_labda_baseball.kep1
                    gomb_labda_foci.kep = gomb_labda_foci.kep1
                    gomb_labda_strand.kep = gomb_labda_strand.kep1
                    gomb_labda_tenisz.kep = gomb_labda_tenisz.kep2
                    gomb_labda_volley.kep = gomb_labda_volley.kep1
                    labda_kivalasztott = GOMB_LABDA_TENISZ

                if gomb_labda_volley.check_for_input(beallitasok_mouse_pozicio):
                    gomb_labda_kosar.kep = gomb_labda_kosar.kep1
                    gomb_labda_baseball.kep = gomb_labda_baseball.kep1
                    gomb_labda_foci.kep = gomb_labda_foci.kep1
                    gomb_labda_strand.kep = gomb_labda_strand.kep1
                    gomb_labda_tenisz.kep = gomb_labda_tenisz.kep1
                    gomb_labda_volley.kep = gomb_labda_volley.kep2
                    labda_kivalasztott = GOMB_LABDA_VOLLEY

                if gomb_hang.check_for_input(beallitasok_mouse_pozicio) and hang_be:
                    gomb_hang.kep = gomb_hang.kep2
                    mixer.music.stop()
                    hang_be = False

                elif gomb_hang.check_for_input(beallitasok_mouse_pozicio) and not hang_be:
                    gomb_hang.kep = gomb_hang.kep1

                    if jatek_futas and not masodik_palya:
                        mixer.music.load("hang_effektek/hatter_zene.mp3")
                        mixer.music.play(-1)

                    elif jatek_futas and masodik_palya:
                        mixer.music.load("hang_effektek/hatter2_zene.mp3")
                        mixer.music.play(-1)

                    else:
                        mixer.music.load("hang_effektek/beallitasok_zene.mp3")
                        mixer.music.play(-1)

                    hang_be = True

            labda_kivalasztott = pygame.transform.scale(labda_kivalasztott, (labda_atmero, labda_atmero))

        pygame.display.update()


def ranglista():
    if hang_be:
        mixer.music.load("hang_effektek/ranglista_zene.mp3")
        mixer.music.play()

    file = open("ranglista.txt", "r")   #beolvassuk a filet
    file_olvasas = file.readlines()     #felosztjuk sorokra
    szortalt_adat = sorted(file_olvasas, reverse=True)  #rendezzuk a sorokat a pontok alapjan

    while True:
        kepernyo.blit(RANGLISTA_HATTER, (0, 0))

        kezdokepernyo_mouse_pozicio = pygame.mouse.get_pos()

        gomb_visszanyil.szin_csere(kezdokepernyo_mouse_pozicio)
        gomb_visszanyil.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #igy tudjuk leallitani a jatekot
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gomb_visszanyil.check_for_input(kezdokepernyo_mouse_pozicio):
                    mixer.music.stop()
                    return 0

        koz = 25    #ez segit szimmetrikusan elhelyezni a sorokat a kepernyon
        for i in range(min(8, len(szortalt_adat))): #a legjobb nyolcat iratjuk ki
            if szortalt_adat[i][0] == '0' and szortalt_adat[i][1] != '0':   #kiiratjuk a szoveget a nullak es a \n nelkul
                szoveg = FONT2.render(f"{i + 1}) {szortalt_adat[i][1:-1]}", True, (255, 255, 255))

            elif szortalt_adat[i][0] == '0' and szortalt_adat[i][1] == '0':
                szoveg = FONT2.render(f"{i + 1}) {szortalt_adat[i][2:-1]}", True, (255, 255, 255))

            else:
                szoveg = FONT2.render(f"{i + 1}) {szortalt_adat[i][:-1]}", True, (255, 255, 255))

            kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 350, koz))
            koz += 135

        pygame.display.update()


def menu_animacio(ertek, szoveg, zuhanas_sziv, bombak):
    while True:
        if (gomb_vissza_a_jatekba.rect.y > 300 and ertek < 0) or (gomb_vissza_a_jatekba.rect.y < 1155 and ertek > 0):

            for gomb in [gomb_vissza_a_jatekba, gomb_jatek_beallitasok, gomb_jatek_kilepes]:
                gomb.rect.y += ertek

            if not masodik_palya:
                kepernyo.blit(JATEK_HATTER, (0, 0))
            else:
                kepernyo.blit(JATEK_HATTER2, (0, 0))

            kepernyo.blit(labda.kep, labda.rect)
            kepernyo.blit(platform.kep, platform.rect)

            kepernyo.blit(eletcsik.kep, eletcsik.rect)
            kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 120, 20))

            for tegla in teglak:
                tegla.frissites()

            if zuhanas_sziv.allapot:
                kepernyo.blit(zuhanas_sziv.kep, zuhanas_sziv.rect)

            for bomba in bombak:
                bomba.frissites()

            gomb_vissza_a_jatekba.frissites()
            gomb_jatek_beallitasok.frissites()
            gomb_jatek_kilepes.frissites()

            pygame.display.update()  # frissitjuk a kepernyot
        else:
            break


def menu_futas(szoveg, zuhanas_sziv, bombak):
    while True:
        menu_mouse_pozicio = pygame.mouse.get_pos()  # megkapjuk a menuben a mouse poziciojat

        for gomb in [gomb_vissza_a_jatekba, gomb_jatek_beallitasok, gomb_jatek_kilepes]:  # ha a gombon van az eger, akkor megvqaltozik a gomb szine
            gomb.szin_csere(menu_mouse_pozicio)
            gomb.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gomb_vissza_a_jatekba.check_for_input(menu_mouse_pozicio):  # igy tudjuk folytatni a jatekot
                    return 1

                if gomb_jatek_beallitasok.check_for_input(menu_mouse_pozicio):  # megnyitjuk a beallitasokat es onnan kilepve folytatjuk a jatekot
                    beallitasok()

                    labda.kep = labda_kivalasztott  # miutan bezarjuk a beallitasokat, meg kell jelenitsuk a jatekot

                    if not masodik_palya:
                        kepernyo.blit(JATEK_HATTER, (0, 0))
                    else:
                        kepernyo.blit(JATEK_HATTER2, (0, 0))

                    kepernyo.blit(labda.kep, labda.rect)
                    kepernyo.blit(platform.kep, platform.rect)
                    kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG / 2 - 120, 20))
                    kepernyo.blit(eletcsik.kep, eletcsik.rect)

                    for tegla in teglak:
                        tegla.frissites()

                    if zuhanas_sziv.allapot:
                        kepernyo.blit(zuhanas_sziv.kep, zuhanas_sziv.rect)

                    for bomba in bombak:
                        bomba.frissites()

                if gomb_jatek_kilepes.check_for_input(menu_mouse_pozicio):  # visszavisz a kezdokepernyore
                    return 0

            elif event.type == pygame.KEYDOWN:
                billentyu = pygame.key.get_pressed()    #vizsgaljuk, hogy melyik gomb lett lenyomva

                if billentyu[pygame.K_ESCAPE]:  # igy tudjuk folytatni a jatekot
                    return 1

        pygame.display.update()  # frissitjuk a kepernyot


def palya_felepites():
    global teglak

    koz = 2
    kezdeti_magassag = 100

    for sor_index, sor in enumerate(PALYA_FELEPITES):
        for oszlop_index, oszlop in enumerate(sor):
            x = oszlop_index * TEGLA_SZELESSEG + koz * oszlop_index
            y = sor_index * TEGLA_MAGASSAG + kezdeti_magassag + koz * sor_index
            if oszlop == 'X':
                tegla = Tegla(x, y, TEGLA_PIROS)
                teglak.append(tegla)

            elif oszlop == 'O':
                tegla = Tegla(x, y, TEGLA_ZOLD)
                teglak.append(tegla)


def vesztettel(pontok):

    if hang_be:
        hang_vesztettel = mixer.Sound("hang_effektek/hang_vesztettel.mp3")
        hang_vesztettel.play()

    felhaszanalo_szoveg = ''

    input_rect = pygame.Rect(960, 710, 200, 90)
    aktiv_szin = (255, 255, 255)
    passziv_szin = (0, 0, 0)
    szin = aktiv_szin

    aktiv = False

    while True:
        kepernyo.blit(VESZTETTEL_HATTER, (0, 0))

        if aktiv:   #ha raclickeltunk a teglalapra
            szin = aktiv_szin

        else:
            szin = passziv_szin

        szoveg = FONT2.render(f"{pontok}", True, (255, 255, 255))   #elhelyezzuk a pontokat a kepernyon
        kepernyo.blit(szoveg, (1150, 495))

        kezdokepernyo_mouse_pozicio = pygame.mouse.get_pos()

        gomb_kilepes.szin_csere(kezdokepernyo_mouse_pozicio)
        gomb_kilepes.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #igy tudjuk leallitani a jatekot
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gomb_kilepes.check_for_input(kezdokepernyo_mouse_pozicio):
                    mixer.music.stop()
                    return 0

                if input_rect.collidepoint(event.pos):
                    aktiv = True

                else:
                    aktiv = False

            if event.type == pygame.KEYDOWN:
                if aktiv:
                    if event.key == pygame.K_BACKSPACE: #ha a backspace-t nyomjuk, akkor kitorlodik a betu
                        felhaszanalo_szoveg = felhaszanalo_szoveg[:-1]

                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:    #ha entert nyomunk, akkor elmenti a nevet egy fileba
                        if felhaszanalo_szoveg != '':
                            file = open("ranglista.txt", "a")
                            if pontok < 10:     #az egyjegyu szamok ele teszunk ket nullat, hogy ossze lehessen hasonlitani oket
                                pontok = str(pontok)
                                pontok = pontok.zfill(3)

                            elif 10 <= pontok < 100:    #a ketjegyu szamok ele teszunk egy nullat, hogy ossze lehessen hasonlitani oket
                                pontok = str(pontok)
                                pontok = pontok.zfill(3)

                            file.write(str(pontok) + "    " + felhaszanalo_szoveg + "\n")
                            file.close()
                            mixer.music.stop()
                            return 0

                    else:   #ha mas betuket nyomunk, akkor elmenti oket egy valtozoba
                        felhaszanalo_szoveg += event.unicode

        pygame.draw.rect(kepernyo, szin, input_rect, 2) #itt rajzoljuk meg a teglalapot

        szoveg_felulet = FONT2.render(felhaszanalo_szoveg, True, (255, 255, 255))   #itt iratjuk ki a kepernyore a beirt szoveget
        kepernyo.blit(szoveg_felulet, (input_rect.x + 4, input_rect.y + 5))

        input_rect.w = max(200, szoveg_felulet.get_width() + 10)    #megvaltoztatjuk a teglalap szelesseget, ha tul hosszu a szoveg

        pygame.display.update()


def nyertel(pontok, idobonusz, osszes_pont):

    if hang_be:
        mixer.music.load("hang_effektek/hang_nyertel.mp3")
        mixer.music.play()

    felhaszanalo_szoveg = ''

    input_rect = pygame.Rect(320, 405, 200, 90)
    aktiv_szin = (255, 255, 255)
    passziv_szin = (0, 255, 0)
    szin = aktiv_szin

    aktiv = False

    while True:
        kepernyo.blit(NYERTEL_HATTER, (0, 0))

        if aktiv:  # ha raclickeltunk a teglalapra
            szin = aktiv_szin

        else:
            szin = passziv_szin

        szoveg = FONT2.render(f"{pontok}", True, (255, 255, 255))  # elhelyezzuk a pontokat a kepernyon
        kepernyo.blit(szoveg, (610, 570))

        szoveg2 = FONT2.render(f"{idobonusz}", True, (255, 255, 255))  # elhelyezzuk a pontokat a kepernyon
        kepernyo.blit(szoveg2, (820, 745))

        szoveg3 = FONT2.render(f"{osszes_pont}", True, (255, 255, 255))  # elhelyezzuk a pontokat a kepernyon
        kepernyo.blit(szoveg3, (890, 910))

        kezdokepernyo_mouse_pozicio = pygame.mouse.get_pos()

        gomb_kilepes.szin_csere(kezdokepernyo_mouse_pozicio)
        gomb_kilepes.frissites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #igy tudjuk leallitani a jatekot
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gomb_kilepes.check_for_input(kezdokepernyo_mouse_pozicio):
                    mixer.music.stop()
                    return 0

                if input_rect.collidepoint(event.pos):
                    aktiv = True

                else:
                    aktiv = False

            if event.type == pygame.KEYDOWN:
                if aktiv:
                    if event.key == pygame.K_BACKSPACE: #ha a backspace-t nyomjuk, akkor kitorlodik a betu
                        felhaszanalo_szoveg = felhaszanalo_szoveg[:-1]

                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:    #ha entert nyomunk, akkor elmenti a nevet egy fileba
                        if felhaszanalo_szoveg != '':
                            file = open("ranglista.txt", "a")
                            if pontok < 10:     #az egyjegyu szamok ele teszunk ket nullat, hogy ossze lehessen hasonlitani oket
                                pontok = str(pontok)
                                pontok = pontok.zfill(3)

                            elif 10 <= pontok < 100:    #a ketjegyu szamok ele teszunk egy nullat, hogy ossze lehessen hasonlitani oket
                                pontok = str(pontok)
                                pontok = pontok.zfill(3)

                            file.write(str(osszes_pont) + "    " + felhaszanalo_szoveg + "\n")
                            file.close()
                            mixer.music.stop()
                            return 0

                    else:   #ha mas betuket nyomunk, akkor elmenti oket egy valtozoba
                        felhaszanalo_szoveg += event.unicode

        pygame.draw.rect(kepernyo, szin, input_rect, 2) #itt rajzoljuk meg a teglalapot

        szoveg_felulet = FONT2.render(felhaszanalo_szoveg, True, (255, 255, 255))   #itt iratjuk ki a kepernyore a beirt szoveget
        kepernyo.blit(szoveg_felulet, (input_rect.x + 4, input_rect.y + 5))

        input_rect.w = max(200, szoveg_felulet.get_width() + 10)    #megvaltoztatjuk a teglalap szelesseget, ha tul hosszu a szoveg

        pygame.display.update()


def main():
    while True:
        kezdokepernyo()


main()
