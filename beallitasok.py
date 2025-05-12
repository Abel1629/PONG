import pygame
from pygame import mixer
import sys
import time
import math
import random
from datetime import datetime, timedelta

pygame.init()   #inicializaljuk a jatekot

KEPERNYO_SZELESSEG = 1920   #itt beallitjuk, hogy mekkora legyen a kepernyo szelessege
KEPERNYO_MAGASSAG = 1080    #itt beallitjuk, hogy mekkora legyen a kepernyo magassaga
FONT = pygame.font.Font("kepek/SHOWG.ttf", 50)    #itt megadjuk a font tipust
FONT2 = pygame.font.Font("kepek/SHOWG.ttf", 100)

#hatterek
KEZDO_HATTER = pygame.image.load("kepek/kezdo_oldal.jpg")  #megadjuk, hogy mi legyen a kezdo oldal hattere
KEZDO_HATTER = pygame.transform.scale(KEZDO_HATTER, (1920, 1080))   #megadjuk, hogy mekkora legyen a hatter

JATEK_HATTER = pygame.image.load("kepek/jatek_hatter.jpg")  #megadjuk, hogy mi legyen a jatek hattere
JATEK_HATTER = pygame.transform.scale(JATEK_HATTER, (1920, 1080))   #megadjuk, hogy mekkora legyen a hatter

BEALLITASOK_HATTER = pygame.image.load("kepek/beallitasok_hatter.jpg")
BEALLITASOK_HATTER = pygame.transform.scale(BEALLITASOK_HATTER, (1920, 1080))

VESZTETTEL_HATTER = pygame.image.load("kepek/vesztettel_hatter.jpg")
VESZTETTEL_HATTER = pygame.transform.scale(VESZTETTEL_HATTER, (1920, 1080))

RANGLISTA_HATTER = pygame.image.load("kepek/ranglista_hatter.jpg")
RANGLISTA_HATTER = pygame.transform.scale(RANGLISTA_HATTER, (1920, 1080))

NYERTEL_HATTER = pygame.image.load("kepek/nyertel_hatter.jpg")
NYERTEL_HATTER = pygame.transform.scale(NYERTEL_HATTER, (1920, 1080))

JATEK_HATTER2 = pygame.image.load("kepek/jatek_hatter2.jpg")
JATEK_HATTER2 = pygame.transform.scale(JATEK_HATTER2, (1920, 1080))

JATEK_HATTER3 = pygame.image.load("kepek/jatek_hatter3.jpg")
JATEK_HATTER3 = pygame.transform.scale(JATEK_HATTER3, (1920, 1080))

#gombok importalasa es meretre alakitasa
GOMB_JATEK_PIROS = pygame.image.load("kepek/jatek_gomb_piros.png")
GOMB_JATEK_PIROS = pygame.transform.scale(GOMB_JATEK_PIROS, (900, 255))

GOMB_JATEK_ZOLD = pygame.image.load("kepek/jatek_gomb_zold.png")
GOMB_JATEK_ZOLD = pygame.transform.scale(GOMB_JATEK_ZOLD, (900, 255))

GOMB_BEALLITASOK_PIROS = pygame.image.load("kepek/beallitasok_gomb_piros.png")
GOMB_BEALLITASOK_PIROS = pygame.transform.scale(GOMB_BEALLITASOK_PIROS, (900, 255))

GOMB_BEALLITASOK_ZOLD = pygame.image.load("kepek/beallitasok_gomb_zold.png")
GOMB_BEALLITASOK_ZOLD = pygame.transform.scale(GOMB_BEALLITASOK_ZOLD, (900, 255))

GOMB_RANGLISTA_PIROS = pygame.image.load("kepek/ranglista_gomb_piros.png")
GOMB_RANGLISTA_PIROS = pygame.transform.scale(GOMB_RANGLISTA_PIROS, (900, 255))

GOMB_RANGLISTA_ZOLD = pygame.image.load("kepek/ranglista_gomb_zold.png")
GOMB_RANGLISTA_ZOLD = pygame.transform.scale(GOMB_RANGLISTA_ZOLD, (900, 255))

GOMB_KILEPES_KEREK = pygame.image.load("kepek/kilepes_kerek.png")
GOMB_KILEPES_KEREK = pygame.transform.scale(GOMB_KILEPES_KEREK, (80, 80))

GOMB_KILEPES_PIROS = pygame.image.load("kepek/kilepes_piros.png")
GOMB_KILEPES_PIROS = pygame.transform.scale(GOMB_KILEPES_PIROS, (80, 80))

GOMB_VISSZANYIL_KEREK = pygame.image.load("kepek/visszanyil_kerek.png")
GOMB_VISSZANYIL_KEREK = pygame.transform. scale(GOMB_VISSZANYIL_KEREK, (80, 80))

GOMB_VISSZANYIL_FEHER = pygame.image.load("kepek/visszanyil_feher.png")
GOMB_VISSZANYIL_FEHER = pygame.transform. scale(GOMB_VISSZANYIL_FEHER, (80, 80))

GOMB_HANG_KI = pygame.image.load("kepek/hang_ki.png")
GOMB_HANG_KI = pygame.transform. scale(GOMB_HANG_KI, (80, 80))

GOMB_HANG_BE = pygame.image.load("kepek/hang_be.png")
GOMB_HANG_BE = pygame.transform. scale(GOMB_HANG_BE, (80, 80))

#labdak
GOMB_LABDA_KOSAR = pygame.image.load("kepek/labda_kosar.png")
GOMB_LABDA_KOSAR = pygame.transform.scale(GOMB_LABDA_KOSAR, (300, 300))

GOMB_LABDA_KOSAR_KIVALASZTVA = pygame.image.load("kepek/labda_kosar_kivalasztva.png")
GOMB_LABDA_KOSAR_KIVALASZTVA = pygame.transform.scale(GOMB_LABDA_KOSAR_KIVALASZTVA, (300, 300))

GOMB_LABDA_BASEBALL = pygame.image.load("kepek/labda_baseball.png")
GOMB_LABDA_BASEBALL = pygame.transform.scale(GOMB_LABDA_BASEBALL, (300, 300))

GOMB_LABDA_BASEBALL_KIVALASZTVA = pygame.image.load("kepek/labda_baseball_kivalasztva.png")
GOMB_LABDA_BASEBALL_KIVALASZTVA = pygame.transform.scale(GOMB_LABDA_BASEBALL_KIVALASZTVA, (300, 300))

GOMB_LABDA_FOCI = pygame.image.load("kepek/labda_foci.png")
GOMB_LABDA_FOCI = pygame.transform.scale(GOMB_LABDA_FOCI, (300, 300))

GOMB_LABDA_FOCI_KIVALASZTVA = pygame.image.load("kepek/labda_foci_kivalasztva.png")
GOMB_LABDA_FOCI_KIVALASZTVA = pygame.transform.scale(GOMB_LABDA_FOCI_KIVALASZTVA, (300, 300))

GOMB_LABDA_STRAND = pygame.image.load("kepek/labda_strand.png")
GOMB_LABDA_STRAND = pygame.transform.scale(GOMB_LABDA_STRAND, (300, 300))

GOMB_LABDA_STRAND_KIVALASZTVA = pygame.image.load("kepek/labda_strand_kivalasztva.png")
GOMB_LABDA_STRAND_KIVALASZTVA = pygame.transform.scale(GOMB_LABDA_STRAND_KIVALASZTVA, (300, 300))

GOMB_LABDA_TENISZ = pygame.image.load("kepek/labda_tenisz.png")
GOMB_LABDA_TENISZ = pygame.transform.scale(GOMB_LABDA_TENISZ, (300, 300))

GOMB_LABDA_TENISZ_KIVALASZTVA = pygame.image.load("kepek/labda_tenisz_kivalasztva.png")
GOMB_LABDA_TENISZ_KIVALASZTVA = pygame.transform.scale(GOMB_LABDA_TENISZ_KIVALASZTVA, (300, 300))

GOMB_LABDA_VOLLEY = pygame.image.load("kepek/labda_volley.png")
GOMB_LABDA_VOLLEY = pygame.transform.scale(GOMB_LABDA_VOLLEY, (300, 300))

GOMB_LABDA_VOLLEY_KIVALASZTVA = pygame.image.load("kepek/labda_volley_kivalasztva.png")
GOMB_LABDA_VOLLEY_KIVALASZTVA = pygame.transform.scale(GOMB_LABDA_VOLLEY_KIVALASZTVA, (300, 300))

#jatek gombok:
GOMB_VISSZA_A_JATEKBA_PIROS = pygame.image.load("kepek/vissza_a_jatekba_gomb_piros.png")
GOMB_VISSZA_A_JATEKBA_PIROS = pygame.transform.scale(GOMB_VISSZA_A_JATEKBA_PIROS, (450, 150))

GOMB_VISSZA_A_JATEKBA_ZOLD = pygame.image.load("kepek/vissza_a_jatekba_gomb_zold.png")
GOMB_VISSZA_A_JATEKBA_ZOLD = pygame.transform.scale(GOMB_VISSZA_A_JATEKBA_ZOLD, (450, 150))

GOMB_JATEK_BEALLITASOK_PIROS = pygame.image.load("kepek/jatek_beallitasok_gomb_piros.png")
GOMB_JATEK_BEALLITASOK_PIROS = pygame.transform.scale(GOMB_JATEK_BEALLITASOK_PIROS, (450, 150))

GOMB_JATEK_BEALLITASOK_ZOLD = pygame.image.load("kepek/jatek_beallitasok_gomb_zold.png")
GOMB_JATEK_BEALLITASOK_ZOLD = pygame.transform.scale(GOMB_JATEK_BEALLITASOK_ZOLD, (450, 150))

GOMB_JATEK_KILEPES_PIROS = pygame.image.load("kepek/jatek_kilepes_gomb_piros.png")
GOMB_JATEK_KILEPES_PIROS = pygame.transform.scale(GOMB_JATEK_KILEPES_PIROS, (450, 150))

GOMB_JATEK_KILEPES_ZOLD = pygame.image.load("kepek/jatek_kilepes_gomb_zold.png")
GOMB_JATEK_KILEPES_ZOLD = pygame.transform.scale(GOMB_JATEK_KILEPES_ZOLD, (450, 150))

GOMB_MENU_FEKETE = pygame.image.load("kepek/menu_gomb_fekete.png")
GOMB_MENU_FEKETE = pygame.transform.scale(GOMB_MENU_FEKETE, (80, 80))

GOMB_MENU_FEHER = pygame.image.load("kepek/menu_gomb_feher.png")
GOMB_MENU_FEHER = pygame.transform.scale(GOMB_MENU_FEHER, (80, 80))

#jatek elemek:
PLATFORM = pygame.image.load("kepek/platform.png")
PLATFORM = pygame.transform.scale(PLATFORM, (400, 50))

PLATFORM_UJ = pygame.image.load("kepek/platform_uj.png")
PLATFORM_UJ = pygame.transform.scale(PLATFORM_UJ, (400, 50))

PLATFORM_UJ_PIROS = pygame.image.load("kepek/platform_uj_piros.png")
PLATFORM_UJ_PIROS = pygame.transform.scale(PLATFORM_UJ_PIROS, (400, 50))

PLATFORM_REPULO = pygame.image.load("kepek/platform_repulo.png")
PLATFORM_REPULO = pygame.transform.scale(PLATFORM_REPULO, (400, 150))

PLATFORM_REPULO2 = pygame.image.load("kepek/platform_repulo2.png")
PLATFORM_REPULO2 = pygame.transform.scale(PLATFORM_REPULO2, (400, 150))

PLATFORM_REPULO3 = pygame.image.load("kepek/platform_repulo3.png")
PLATFORM_REPULO3 = pygame.transform.scale(PLATFORM_REPULO3, (400, 150))

LEZER = pygame.image.load("kepek/lezer.png")
LEZER = pygame.transform.scale(LEZER, (20, 100))

#teglak
TEGLA_SZELESSEG = 100
TEGLA_MAGASSAG = 40

TEGLA_PIROS = pygame.image.load("kepek/tegla_piros.jpg")
TEGLA_PIROS = pygame.transform.scale(TEGLA_PIROS, (TEGLA_SZELESSEG, TEGLA_MAGASSAG))

TEGLA_PIROS_REPEDT = pygame.image.load("kepek/tegla_piros_repedt.jpg")
TEGLA_PIROS_REPEDT = pygame.transform.scale(TEGLA_PIROS_REPEDT, (TEGLA_SZELESSEG, TEGLA_MAGASSAG))

TEGLA_ZOLD = pygame.image.load("kepek/tegla_zold.jpg")
TEGLA_ZOLD = pygame.transform.scale(TEGLA_ZOLD, (TEGLA_SZELESSEG, TEGLA_MAGASSAG))

TEGLA_ZOLD_REPEDT = pygame.image.load("kepek/tegla_zold_repedt.jpg")
TEGLA_ZOLD_REPEDT = pygame.transform.scale(TEGLA_ZOLD_REPEDT, (TEGLA_SZELESSEG, TEGLA_MAGASSAG))

#eletcsikok

ELETCSIK_1 = pygame.image.load("kepek/eletcsik_1.png")
ELETCSIK_1 = pygame.transform.scale(ELETCSIK_1, (200, 50))

ELETCSIK_2 = pygame.image.load("kepek/eletcsik_2.png")
ELETCSIK_2 = pygame.transform.scale(ELETCSIK_2, (200, 50))

ELETCSIK_3 = pygame.image.load("kepek/eletcsik_3.png")
ELETCSIK_3 = pygame.transform.scale(ELETCSIK_3, (200, 50))

ELETCSIK_4 = pygame.image.load("kepek/eletcsik_4.png")
ELETCSIK_4 = pygame.transform.scale(ELETCSIK_4, (200, 50))

#buborekok

SZIV_BUBOREK = pygame.image.load("kepek/buborek_sziv.png")
SZIV_BUBOREK = pygame.transform.scale(SZIV_BUBOREK, (50, 50))

KIPUKKANAS_BUBOREK = pygame.image.load("kepek/kipukkanas.png")
KIPUKKANAS_BUBOREK = pygame.transform.scale(KIPUKKANAS_BUBOREK, (50, 50))

BOMBA_BUBOREK = pygame.image.load("kepek/buborek_bomba.png")
BOMBA_BUBOREK = pygame.transform.scale(BOMBA_BUBOREK, (50, 50))

ROBBANAS_BUBOREK = pygame.image.load("kepek/robbanas.png")
ROBBANAS_BUBOREK = pygame.transform.scale(ROBBANAS_BUBOREK, (50, 50))
