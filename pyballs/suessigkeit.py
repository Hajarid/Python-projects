import pygame
from konstanten import ZELLEN_GROESSE, SUESSIGKEITEN_FARBEN, FALL_GESCHWINDIGKEIT
   
class Suessigkeit:
   
   
          # Initialisiert eine neue Süßigkeit (Typ/Farbe ,Zeilenindex , Spaltenindex )

    def __init__(self, typ, zeile, spalte):
     
        self.typ = typ
        self.zeile = zeile
        self.spalte = spalte
        
        # Position auf dem Bildschirm (in Pixeln)
        
        self.x = spalte * ZELLEN_GROESSE
        self.y = zeile * ZELLEN_GROESSE
        
        # Zielposition für Animationen
        
        self.ziel_x = self.x
        self.ziel_y = self.y
        
        # Status
        
        self.faellt = False
        self.ausgewaehlt = False
        self.markiert_zum_loeschen = False
    
    
         #eine neue Position im Raster setzen

    def setze_position(self, zeile, spalte):
        
        self.zeile = zeile
        self.spalte = spalte
        self.ziel_x = spalte * ZELLEN_GROESSE
        self.ziel_y = zeile * ZELLEN_GROESSE
    
    #die Fall-Animation zu einer neuen Zeile Starten

    def starte_fallen(self, neue_zeile):
        self.zeile = neue_zeile
        self.ziel_y = neue_zeile * ZELLEN_GROESSE
        self.faellt = True
    
    #zur Aktualisierung die Süßigkeit (für Animationen)
    def update(self):
      
        # Horizontale Bewegung (beim Tauschen)
        
        if self.x != self.ziel_x:
            diff = self.ziel_x - self.x
            if abs(diff) < 5:
                self.x = self.ziel_x
            else:
                self.x += diff / 5
        
        # Vertikale Bewegung (beim Fallen)
        
        if self.y < self.ziel_y:
            self.y += FALL_GESCHWINDIGKEIT
            if self.y >= self.ziel_y:
                self.y = self.ziel_y
                self.faellt = False
        elif self.y > self.ziel_y:
            diff = self.ziel_y - self.y
            if abs(diff) < 5:
                self.y = self.ziel_y
            else:
                self.y += diff / 5
    
    #zur Prüfung, ob die Süßigkeit sich noch bewegt
    
    def ist_in_bewegung(self):
        return self.x != self.ziel_x or self.y != self.ziel_y
    
         # die Süßigkeit auf den Bildschirm Zeichnen

    def zeichne(self, screen, versatz_x, versatz_y):
       
        if self.typ == -1:  # Leere Zelle
            
            return
            
        # Position auf dem Bildschirm
        
        pos_x = int(self.x) + versatz_x
        pos_y = int(self.y) + versatz_y
        
        # Farbe basierend auf Typ
        
        farbe = SUESSIGKEITEN_FARBEN[self.typ]
        
        #Süßigkeit als Kreis Zeichnen
        
        radius = ZELLEN_GROESSE // 2 - 5
        zentrum_x = pos_x + ZELLEN_GROESSE // 2
        zentrum_y = pos_y + ZELLEN_GROESSE // 2
        
        # Hauptkreis
        pygame.draw.circle(screen, farbe, (zentrum_x, zentrum_y), radius)
        
        # Glanzeffekt
        glanz_x = zentrum_x - radius // 3
        glanz_y = zentrum_y - radius // 3
        pygame.draw.circle(screen, (255, 255, 255), (glanz_x, glanz_y), radius // 4)
        
        # Umrandung für ausgewählte Süßigkeiten
        if self.ausgewaehlt:
            pygame.draw.circle(screen, (255, 255, 255), 
                             (zentrum_x, zentrum_y), 
                             radius + 3, 3)