import random
import pygame
from konstanten import RASTER_GROESSE, SUESSIGKEITEN_TYPEN, ZELLEN_GROESSE
from suessigkeit import Suessigkeit


#verwaltung das Spielfeld 

class Spielfeld:
    
    def __init__(self):
        self.raster = []
        self.ausgewaehlte_suessigkeit = None
        self.punkte = 0
        self.erstelle_spielfeld()
        self.klick_sound1 = pygame.mixer.Sound("source/click_1.wav")
        self.smash = pygame.mixer.Sound("source/smash1.wav")
        
 #eine Methode zur Erstellung ein neues Spielfeld 
 

    def erstelle_spielfeld(self):
        self.raster = []
        
        for zeile in range(RASTER_GROESSE):
            zeilen_liste = []
            for spalte in range(RASTER_GROESSE):
                # Wähle einen zufälligen Typ
                typ = self.waehle_gueltigen_typ(zeile, spalte, zeilen_liste)
                zeilen_liste.append(Suessigkeit(typ, zeile, spalte))
            self.raster.append(zeilen_liste)
            
            
            #zum Wählen einen Typ, der keine 3er-Matches erzeugt

    def waehle_gueltigen_typ(self, zeile, spalte, aktuelle_zeile):
        verbotene_typen = set()
        
        # horizontal Prüfen  (links)
        if spalte >= 2:
            if aktuelle_zeile[spalte-1].typ == aktuelle_zeile[spalte-2].typ:
                verbotene_typen.add(aktuelle_zeile[spalte-1].typ)
        
        # vertikal Prüfen  (oben)
        if zeile >= 2:
            if self.raster[zeile-1][spalte].typ == self.raster[zeile-2][spalte].typ:
                verbotene_typen.add(self.raster[zeile-1][spalte].typ)
        
        # einen erlaubten Typ Wählen
        erlaubte_typen = [t for t in range(SUESSIGKEITEN_TYPEN) if t not in verbotene_typen]
        return random.choice(erlaubte_typen) if erlaubte_typen else random.randint(0, SUESSIGKEITEN_TYPEN - 1)
    
        #zur Verarbeiteung von Klicks auf Süßigkeiten

    def suessigkeit_auswaehlen(self, zeile, spalte):
      
        self.klick_sound1.play()

        if not (0 <= zeile < RASTER_GROESSE and 0 <= spalte < RASTER_GROESSE):
            return False
        
        # Wenn bereits eine Süßigkeit ausgewählt ist
        if self.ausgewaehlte_suessigkeit:
            alte_zeile, alte_spalte = self.ausgewaehlte_suessigkeit
            
            #  benachbart Prüfen
            
            
            if self.sind_benachbart(alte_zeile, alte_spalte, zeile, spalte):
                
                # Versuchen zu tauschen
                if self.tausche_suessigkeiten(alte_zeile, alte_spalte, zeile, spalte):
                    self.raster[alte_zeile][alte_spalte].ausgewaehlt = False
                    self.raster[zeile][spalte].ausgewaehlt = False
                    self.ausgewaehlte_suessigkeit = None
                    return True
            
            # Neue Auswahl
            self.raster[alte_zeile][alte_spalte].ausgewaehlt = False
            self.raster[zeile][spalte].ausgewaehlt = True
            self.ausgewaehlte_suessigkeit = (zeile, spalte)
        else:
            # Erste Auswahl
            self.raster[zeile][spalte].ausgewaehlt = True
            self.ausgewaehlte_suessigkeit = (zeile, spalte)
        
        return False
        #zur Prüfung ob zwei Positionen direkt benachbart sind

    def sind_benachbart(self, z1, s1, z2, s2):
        return (abs(z1 - z2) == 1 and s1 == s2) or (abs(s1 - s2) == 1 and z1 == z2)
        #zum Tausch zwei Süßigkeiten wenn dadurch Matches entstehen

    def tausche_suessigkeiten(self, z1, s1, z2, s2):
        # temporär Tausche
        self.raster[z1][s1], self.raster[z2][s2] = self.raster[z2][s2], self.raster[z1][s1]
        
        #  auf Matches Prüfen
        matches = self.finde_matches()
        
        if matches:
            # Gültiger Zug - animieren den Tausch
            self.raster[z1][s1].setze_position(z1, s1)
            self.raster[z2][s2].setze_position(z2, s2)
            return True
        else:
            # Ungültiger Zug -  zurück tauschen
 
            self.raster[z1][s1], self.raster[z2][s2] = self.raster[z2][s2], self.raster[z1][s1]
            return False
        #alle 3er oder größere Matches finden

    def finde_matches(self):
        matches = set()
        
        # Horizontale Matches
        for zeile in range(RASTER_GROESSE):
            for start in range(RASTER_GROESSE - 2):
                typ = self.raster[zeile][start].typ
                if typ == -1:
                    continue
                    
                # Länge des Matches Finden
                ende = start
                while ende < RASTER_GROESSE and self.raster[zeile][ende].typ == typ:
                    ende += 1
                
                # Wenn 3 oder mehr
                if ende - start >= 3:
                    for spalte in range(start, ende):
                        matches.add((zeile, spalte))
        
        # Vertikale Matches
        for spalte in range(RASTER_GROESSE):
            for start in range(RASTER_GROESSE - 2):
                typ = self.raster[start][spalte].typ
                if typ == -1:
                    continue
                    
                # Länge des Matches Finden
                ende = start
                while ende < RASTER_GROESSE and self.raster[ende][spalte].typ == typ:
                    ende += 1
                
                # Wenn 3 oder mehr
                if ende - start >= 3:
                    for zeile in range(start, ende):
                        matches.add((zeile, spalte))
        
        return list(matches)
    
        #zur Entfernen gefundene Matches und gibt Punkte

    def entferne_matches(self):
        matches = self.finde_matches()
        
        if not matches:
            return False
        
        try:
            self.smash.play()
        except Exception as e:
            print(f"Sound-Fehler: {e}")
    
        #  Süßigkeiten Markiere zum Löschen
        for zeile, spalte in matches:
            self.raster[zeile][spalte].typ = -1
            self.raster[zeile][spalte].markiert_zum_loeschen = True
        
        # Punkte berechnen
        self.punkte += len(matches) * 10
        if len(matches) >= 4:
            self.punkte += (len(matches) - 3) * 20
        
        return True
        #Süßigkeiten in leere Felder fallen

    def lasse_suessigkeiten_fallen(self):
        bewegung = False
        
        # Von unten nach oben durch jede Spalte
        for spalte in range(RASTER_GROESSE):
            for zeile in range(RASTER_GROESSE - 1, -1, -1):
                if self.raster[zeile][spalte].typ == -1:
                    #  nächste Süßigkeit oben Finden
                    for obere_zeile in range(zeile - 1, -1, -1):
                        if self.raster[obere_zeile][spalte].typ != -1:
                            # Tausche
                            self.raster[zeile][spalte], self.raster[obere_zeile][spalte] = \
                                self.raster[obere_zeile][spalte], self.raster[zeile][spalte]
                            
                            #  Fall-Animation Starten
                            self.raster[zeile][spalte].starte_fallen(zeile)
                            bewegung = True
                            break
        
        return bewegung
    
        #zur Füllung leere Felder mit neuen Süßigkeiten von oben

    def fuelle_leere_felder(self):
        for spalte in range(RASTER_GROESSE):
            for zeile in range(RASTER_GROESSE):
                if self.raster[zeile][spalte].typ == -1:
                    # Neue Süßigkeit erstellen
                    neuer_typ = random.randint(0, SUESSIGKEITEN_TYPEN - 1)
                    self.raster[zeile][spalte] = Suessigkeit(neuer_typ, zeile, spalte)
                    
                    # von oben Starten
                    self.raster[zeile][spalte].y = -ZELLEN_GROESSE
                    self.raster[zeile][spalte].starte_fallen(zeile)
    
        #zur prüfung ob Animationen noch läuft

    def ist_animiert(self):
        for zeile in self.raster:
            for suess in zeile:
                if suess.ist_in_bewegung():
                    return True
        return False
        #Aktualisierung alle Süßigkeiten

    def update(self):
        for zeile in self.raster:
            for suess in zeile:
                suess.update()
    
        #Zeichnung das Spielfeld 

    def zeichne(self, screen, versatz_x, versatz_y):
        spielfeld_breite = RASTER_GROESSE * ZELLEN_GROESSE
        spielfeld_hoehe = RASTER_GROESSE * ZELLEN_GROESSE
        
        # eine Surface mit Alpha-Kanal für Transparenz Erstellen
        board_surface = pygame.Surface((spielfeld_breite + 20, spielfeld_hoehe + 20), pygame.SRCALPHA)
        
        # Hauptrahmen mit Transparenz und Farbverlauf
        # Äußerer Rahmen : dunkler, semi-transparent
        
        pygame.draw.rect(board_surface, (20, 10, 40, 180), 
                        (0, 0, spielfeld_breite + 20, spielfeld_hoehe + 20), 
                        border_radius=15)
        
        # Innerer Rahmen: heller, mehr transparent
        pygame.draw.rect(board_surface, (100, 50, 150, 120), 
                        (5, 5, spielfeld_breite + 10, spielfeld_hoehe + 10), 
                        border_radius=12)
        
        # Glanz-Effekt oben
        glanz_rect = pygame.Rect(10, 10, spielfeld_breite, 40)
        for i in range(20):
            alpha = 60 - i * 3
            if alpha > 0:
                pygame.draw.rect(board_surface, (255, 255, 255, alpha), 
                               (glanz_rect.x, glanz_rect.y + i, glanz_rect.width, 2))
        
        # zum Zeichnung einzelne Zellen
        for zeile in range(RASTER_GROESSE):
            for spalte in range(RASTER_GROESSE):
                x = 10 + spalte * ZELLEN_GROESSE
                y = 10 + zeile * ZELLEN_GROESSE
                
                # Zellen-Hintergrund : abwechselnde Farben wie ein Schachbrett
                if (zeile + spalte) % 2 == 0:
                    zellen_farbe = (80, 40, 100, 100)  # Dunkles Lila, transparent
                else:
                    zellen_farbe = (120, 60, 140, 100)  # Helleres Lila, transparent
                
                # Zelle mit abgerundeten Ecken
                zellen_rect = pygame.Rect(x + 2, y + 2, ZELLEN_GROESSE - 4, ZELLEN_GROESSE - 4)
                pygame.draw.rect(board_surface, zellen_farbe, zellen_rect, border_radius=8)
                
                # Innerer Schatten für Tiefe
                schatten_rect = pygame.Rect(x + 4, y + 4, ZELLEN_GROESSE - 8, ZELLEN_GROESSE - 8)
                pygame.draw.rect(board_surface, (0, 0, 0, 40), schatten_rect, border_radius=6)
                
                # Highlight am Rand der Zelle
                pygame.draw.rect(board_surface, (255, 255, 255, 30), zellen_rect, 1, border_radius=8)
        
        # Dekorative Elemente an den Ecken
        # Oben links
        pygame.draw.circle(board_surface, (255, 200, 100, 150), (15, 15), 8)
        pygame.draw.circle(board_surface, (255, 255, 255, 100), (13, 13), 4)
        
        # Oben rechts
        pygame.draw.circle(board_surface, (255, 200, 100, 150), (spielfeld_breite + 5, 15), 8)
        pygame.draw.circle(board_surface, (255, 255, 255, 100), (spielfeld_breite + 3, 13), 4)
        
        # Unten links
        pygame.draw.circle(board_surface, (255, 200, 100, 150), (15, spielfeld_hoehe + 5), 8)
        pygame.draw.circle(board_surface, (255, 255, 255, 100), (13, spielfeld_hoehe + 3), 4)
        
        # Unten rechts
        pygame.draw.circle(board_surface, (255, 200, 100, 150), (spielfeld_breite + 5, spielfeld_hoehe + 5), 8)
        pygame.draw.circle(board_surface, (255, 255, 255, 100), (spielfeld_breite + 3, spielfeld_hoehe + 3), 4)
        
        # Board auf Screen zeichnen
        screen.blit(board_surface, (versatz_x - 10, versatz_y - 10))
        
        # Süßigkeiten zeichnen
        for zeile in self.raster:
            for suess in zeile:
                suess.zeichne(screen, versatz_x, versatz_y)