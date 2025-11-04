import pygame

class Button:
    def __init__(self, rect, text, font, idle_color, hover_color, text_color):
     
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.text_color = text_color
        # Text-Oberfläche einmal anlegen
        self.text_surf = font.render(text, True, text_color)
        
        
        
#  Button Zeichnen , hover_color effect wenn maus drüber ist 

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.idle_color

        shadow_offset = 4
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=20)
        
        # Abgerundeter Button
        pygame.draw.rect(screen, color, self.rect, border_radius=20)

        # Glanz-Effekt (oberer Bereich halbtransparent weiß)
        
        gloss_rect = pygame.Rect(
            self.rect.left, self.rect.top, self.rect.width, self.rect.height // 2
        )
        gloss_surface = pygame.Surface((gloss_rect.width, gloss_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(gloss_surface, (255, 255, 255, 80), gloss_surface.get_rect(), border_radius=20)
        screen.blit(gloss_surface, gloss_rect.topleft)
        
        # Text zentriert zeichnen
        
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        screen.blit(self.text_surf, text_rect)
        
     # diese Methode Prüft, ob MOUSEBUTTONUP in diesem Button-Rect stattfindet

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            
            # event.pos statt pygame.mouse.get_pos(), um Klick-Position zum Event-Zeitpunkt zu nutzen
            
            if self.rect.collidepoint(event.pos):
                return True
        return False
