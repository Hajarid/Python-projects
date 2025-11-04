import os
import sys
import pygame
import json
import suessigkeit
from konstanten import TITEL, BREITE, HOEHE, FPS, WEISS, SCHWARZ, HINTERGRUND_FARBE
from konstanten import SPIELFELD_VERSATZ_X, SPIELFELD_VERSATZ_Y, ZELLEN_GROESSE, RASTER_GROESSE
from spielfeld import Spielfeld
from button import Button


# Ensure working directory is correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class pyBallsSpiel:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((BREITE, HOEHE))
        pygame.display.set_caption(TITEL)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.punkte_font = pygame.font.Font(None, 48)
        self.save_file = "savegame.json"
        self.btn_back = Button(
            rect=(675, 20, 100, 30),
            text="Menu",
            font=self.font,
            # idle_color=(255,200,255),
            idle_color=HINTERGRUND_FARBE,

            # hover_color=(235,130,130),
            hover_color=(230,180,235),

            text_color=(0,0,0)
        )
        self.btn_play = Button(
            rect=(BREITE//2 - 100, HOEHE//2 - 25, 200, 50),
            text="Play",
            font=self.font,
            idle_color=(200,200,255),
            hover_color=(180,180,235),
            text_color=(0,0,0)
        )
        self.btn_continue = Button(
            rect=(BREITE//2 - 100, HOEHE//2 +35, 200, 50),
            text="Continue",
            font=self.font,
            idle_color=(200,255,200),
            hover_color=(180,235,180),
            text_color=(0,0,0)
        )
        self.btn_exit = Button(
            rect=(BREITE//2 - 100, HOEHE//2 + 95, 200, 50),
            text="Exit",
            font=self.font,
            idle_color=(255,150,150),
            hover_color=(235,130,130),
            text_color=(0,0,0)
        )


        # Spielfeld & Spielzustand
        self.spielfeld = Spielfeld()
        self.zustand = "bereit"

        # Menü
        self.im_menü = True
        self.menu_musik_geladen = False
        self.menu_hintergrund = pygame.image.load("source/background.jpg").convert()
        self.klick_sound = pygame.mixer.Sound("source/click.wav")
        


    def zeige_menü(self):
    # Menü-Musik nur einmal laden
        if not self.menu_musik_geladen:
            pygame.mixer.music.load("source/menu_music.mp3")
            pygame.mixer.music.play(-1)
            self.menu_musik_geladen = True

        # Stelle sicher, dass self.im_menü=True ist, wenn Methode aufgerufen wird
        while self.im_menü:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Prüfe Klicks auf Buttons
                if self.btn_play.is_clicked(event):
                    self.klick_sound.play()
                    pygame.time.delay(200)
                    pygame.mixer.music.stop()
                    self.spielfeld = Spielfeld()
                    self.zustand = "bereit"
                    self.zeige_anleitung_und_countdown()
                    self.im_menü = False
                    # Sobald im_menü=False, wird die Schleife verlassen
                    break
                elif self.btn_continue.is_clicked(event):
                    self.klick_sound.play()
                    pygame.time.delay(200)
                    pygame.mixer.music.stop()
                    loaded = self.load_game()
                    if not loaded:
                        # Falls Laden fehlschlägt, starte ein neues Spiel
                        self.spielfeld = Spielfeld()
                        # Timer neu initialisieren:
                        self.start_ticks = pygame.time.get_ticks()
                    self.im_menü = False
                    # Sobald im_menü=False, wird die Schleife verlassen
                    break
                elif self.btn_exit.is_clicked(event):
                    self.klick_sound.play()
                    pygame.time.delay(200)
                    pygame.quit()
                    sys.exit()

            # Zeichnen
            self.screen.blit(pygame.transform.scale(self.menu_hintergrund, (BREITE, HOEHE)), (0, 0))
            # Buttons zeichnen
            self.btn_play.draw(self.screen)
            self.btn_exit.draw(self.screen)
            self.btn_continue.draw(self.screen)


            pygame.display.flip()
            self.clock.tick(FPS)


    def save_game(self):
    # """Speichert aktuellen Spielzustand in JSON."""
        data = {}
        # Raster speichern: nur Typen
        grid = []
        for zeile in self.spielfeld.raster:
            row = [suess.typ if hasattr(suess, "typ") else -1 for suess in zeile]
            grid.append(row)
        data["grid"] = grid
        # Score
        data["score"] = self.spielfeld.punkte
        # Timer: falls du start_ticks führst:
        if hasattr(self, "start_ticks"):
            elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
            data["elapsed_seconds"] = elapsed
        # In Datei schreiben
        try:
            with open(self.save_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def load_game(self):
        """Lädt Spielzustand aus JSON, baut Spielfeld und Timer neu auf."""
        if not os.path.exists(self.save_file):
            return False
        try:
            with open(self.save_file, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
            return False

        grid = data.get("grid")
        if not grid:
            return False
        # Erzeuge neues Spielfeld-Objekt, aber überschreibe Raster
        self.spielfeld = Spielfeld.__new__(Spielfeld)
        # Initialisiere die restlichen Attribute minimal:
        # Wenn Spielfeld.__init__ wichtige Dinge macht, kannst du erst aufrufen und dann überschreiben raster:
        try:
            # Rufe __init__ auf, um evt. Mixer oder andere Dinge einzurichten
            Spielfeld.__init__(self.spielfeld)
        except:
            # Falls __init__ Spielfeld komplett zufällig initialisiert, wir setzen danach raster neu.
            pass

        # Jetzt Raster überschreiben:
        new_raster = []
        for ze, row in enumerate(grid):
            new_row = []
            for sp, typ in enumerate(row):
                # Erzeuge neue Suessigkeit mit Typ:
                obj = suessigkeit.Suessigkeit(typ, ze, sp)
                new_row.append(obj)
            new_raster.append(new_row)
        self.spielfeld.raster = new_raster
        # Punkte setzen
        self.spielfeld.punkte = data.get("score", 0)
        # Zustand auf „bereit“, damit beim Fortsetzen sofort Klicken möglich
        self.zustand = "bereit"
        return True



    def zeige_anleitung_und_countdown(self):
        anweisungen = [
            "Swipe balls in any direction",
            
            "Create sets of 3 or more matching balls",
            
               "     enjoy"
            
        ]

        countdown_font = pygame.font.Font(None, 72)
        info_font = pygame.font.Font(None, 32)
        start_time = pygame.time.get_ticks()

        while True:
            self.screen.fill((240, 240, 255))

            for i, zeile in enumerate(anweisungen):
                text_surface = info_font.render(zeile, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(BREITE // 2, 100 + i * 40))
                self.screen.blit(text_surface, text_rect)

            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            
            if elapsed < 0.5:
                count_text = "3"
            elif elapsed < 2.0:
                count_text = "2"
            elif elapsed < 3.0:
                count_text = "1"
            elif elapsed < 4.0:
                count_text = "Go!"
            else:
                break

            count_surface = countdown_font.render(count_text, True, (0, 0, 0))
            count_rect = count_surface.get_rect(center=(BREITE // 2, HOEHE - 100))
            self.screen.blit(count_surface, count_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def verarbeite_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Prüfe Back-Button:
            if self.btn_back.is_clicked(event):
                self.klick_sound.play()
                self.save_game()
                pygame.time.delay(100)
                # zurück ins Menü
                self.im_menü = True
                pygame.mixer.music.stop()
                # self.spielfeld = Spielfeld()
                # self.zustand = "bereit"
                self.zeige_menü()
                return True
            # Rest der Logik:
            elif event.type == pygame.MOUSEBUTTONDOWN and self.zustand == "bereit":

                maus_x, maus_y = pygame.mouse.get_pos()
                rel_x = maus_x - SPIELFELD_VERSATZ_X
                rel_y = maus_y - SPIELFELD_VERSATZ_Y
                if 0 <= rel_x < RASTER_GROESSE * ZELLEN_GROESSE and \
                   0 <= rel_y < RASTER_GROESSE * ZELLEN_GROESSE:
                    zeile = rel_y // ZELLEN_GROESSE
                    spalte = rel_x // ZELLEN_GROESSE
                    if self.spielfeld.suessigkeit_auswaehlen(zeile, spalte):
                        self.zustand = "tausch"
                    ...

        return True


    def update(self):
        self.spielfeld.update()
        if self.zustand == "tausch":

            if not self.spielfeld.ist_animiert():
                if self.spielfeld.entferne_matches():
                    self.zustand = "fallen"
                else:
                    self.zustand = "bereit"
        elif self.zustand == "fallen":
            if not self.spielfeld.ist_animiert():
                if self.spielfeld.lasse_suessigkeiten_fallen():
                    pass
                else:
                    self.zustand = "nachfuellen"
        elif self.zustand == "nachfuellen":
            self.spielfeld.fuelle_leere_felder()
            self.zustand = "warten_auf_nachfuellen"
        elif self.zustand == "warten_auf_nachfuellen":
            if not self.spielfeld.ist_animiert():
                if self.spielfeld.finde_matches():
                    self.spielfeld.entferne_matches()
                    self.zustand = "fallen"
                else:
                    self.zustand = "bereit"

    def zeichne(self):
        self.screen.fill(HINTERGRUND_FARBE)
        self.spielfeld.zeichne(self.screen, SPIELFELD_VERSATZ_X, SPIELFELD_VERSATZ_Y)

        punkte_text = self.punkte_font.render(f"Score: {self.spielfeld.punkte}", True, SCHWARZ)
        # punkte_rect = punkte_text.get_rect(centerx=BREITE // 2, y=20)
        punkte_rect = punkte_text.get_rect(centerx=100, y=20)
       
        self.screen.blit(punkte_text, punkte_rect)

        anleitung = "swipe and match"
        anleitung_text = self.font.render(anleitung, True, SCHWARZ)
        anleitung_rect = anleitung_text.get_rect(centerx=BREITE // 2, bottom=HOEHE - 20)
        self.screen.blit(anleitung_text, anleitung_rect)

        self.btn_back.draw(self.screen)

        pygame.display.flip()

    def run(self):
        self.zeige_menü()
        laeuft = True
        while laeuft:
            laeuft = self.verarbeite_events()
            self.update()
            self.zeichne()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


# Hauptprogramm
if __name__ == "__main__":
    spiel = pyBallsSpiel()
    spiel.run()
