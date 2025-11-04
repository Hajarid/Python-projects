# Konstanten für das pyBalls Crush Spiel

# Fenster-Einstellungen
TITEL = "pyBalls Crush"
BREITE = 800      
HOEHE = 600
FPS = 60

# Spielfeld-Einstellungen
RASTER_GROESSE = 8  # 8x8 Spielfeld
ZELLEN_GROESSE = 50
# SPIELFELD_VERSATZ_X = 250
SPIELFELD_VERSATZ_X = 205

SPIELFELD_VERSATZ_Y = 80


# Farben (RGB)
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
HINTERGRUND_FARBE = (240, 220, 240)
RASTER_FARBE = (180, 180, 200)

# Süßigkeiten-Typen
SUESSIGKEITEN_TYPEN = 6 # Anzahl verschiedener Süßigkeiten

# Süßigkeiten-Farben
SUESSIGKEITEN_FARBEN = [
    (255, 60, 60),     # Rot
    (60, 255, 60),     # Grün
    (60, 60, 255),     # Blau
    (255, 255, 60),    # Gelb
    (255, 60, 255),    # Magenta
    (60, 255, 255),    # Cyan
]

# Spielsteuerung
MIN_MATCH = 3        # Mindestanzahl für ein Match
FALL_GESCHWINDIGKEIT = 8  # Pixel pro Frame beim Fallen
ANIMATION_DAUER = 15  # Frames für Tausch-Animation