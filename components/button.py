import pygame
from pygame import Surface, Color
from pygame.event import Event
from pygame.font import Font, SysFont

from .component import Component


# Init the font module to allow the font property to have a default value
pygame.font.init()


class Button(Component):
    def __init__(
        self,
        screen: Surface,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 20,
        border_radius: int = 0,
        fg_color: Color = (0, 0, 0),
        bg_color: Color = (255, 255, 255),
        hover_bg_color: Color = (200, 200, 200),
        active_bg_color: Color = (100, 100, 100),
        text: str | None = None,
        font: Font = SysFont("Calibri", 18)
    ) -> None:
        super().__init__(screen)
        self._screen = screen
        # Properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.active_bg_color = active_bg_color
        self.text = text
        self.font = font
        # State
        self._is_pressed = False

    def _render_font(self) -> Surface:
        return None if self.text is None or self.font is None else self.font.render(self.text, True, self.fg_color)

    def _is_mouse_hover(self) -> bool:
        m_x, m_y = pygame.mouse.get_pos()
        return (
            (self.x <= m_x <= (self.x + self.width)) and
            (self.y <= m_y <= (self.y + self.height))
        )

    def update_events(self, events: list[Event]) -> None:
        for e in events:
            match e.type:
                case pygame.MOUSEBUTTONDOWN:
                    self._is_pressed = self._is_mouse_hover()
                case pygame.MOUSEBUTTONUP:
                    self._is_pressed = False

    def draw(self) -> None:
        bg_color: Color = self.bg_color
        if self._is_pressed:
            bg_color = self.active_bg_color
        elif self._is_mouse_hover():
            bg_color = self.hover_bg_color
        pygame.draw.rect(
            self._screen,
            bg_color,
            (self.x, self.y, self.width, self.height),
            border_radius=self.border_radius
        )
        text_surf = self._render_font()
        if text_surf is not None:
            txt_w, txt_h = text_surf.get_size()
            self._screen.blit(text_surf, (
                self.x + self.width / 2 - txt_w / 2,
                self.y + self.height / 2 - txt_h / 2
            ))
