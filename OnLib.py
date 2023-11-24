import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (125, 125, 125)
LIGHT_GREY = (175, 175, 175)
DARK_GREY = (75, 75, 75)


def InCoord(Coord, X, Y):
    if X[0] < Coord[0] < X[1] and Y[0] < Coord[1] < Y[1]:
        return True
    return False


def PaintСapsule(sf, color, ops):
    r = round(min(ops[2], ops[3]) / 10)
    pygame.draw.rect(sf, color, (ops[0] + r, ops[1], ops[2] - (r * 2), ops[3]))
    pygame.draw.rect(sf, color, (ops[0], ops[1] + r, ops[2], ops[3] - (r * 2)))
    pygame.draw.circle(sf, color, (ops[0] + r, ops[1] + r), r)
    pygame.draw.circle(sf, color, (ops[0] + ops[2] - r, ops[1] + r), r)
    pygame.draw.circle(sf, color, (ops[0] + r, ops[1] + ops[3] - r), r)
    pygame.draw.circle(
        sf, color, (ops[0] + ops[2] - r, ops[1] + ops[3] - r), r)


def FindFont(ops):
    i = 50
    font = pygame.font.Font(None, i)
    font_height = font.get_linesize()
    while (font_height > min(ops[2], ops[3]) * 0.7):
        font = pygame.font.Font(None, i)
        font_height = font.get_linesize()
        i -= 1
    return font


class Button:
    def __init__(self, sf, ops, colors, string=''):
        self.sf = sf
        self.ops = ops
        self.colors = colors
        self.string = string
        if len(self.string):
            self.font = FindFont(ops)

    def PaintText(self):
        text_surface = self.font.render(self.string, True, self.colors[2])
        text_l = text_surface.get_width()
        text_w = self.font.get_linesize()
        self.sf.blit(
            text_surface, (self.ops[0] + (self.ops[2] - text_l) // 2, self.ops[1] + (self.ops[3] - text_w) // 2))

    def MouseTracking(self, event):
        if event.type == pygame.MOUSEMOTION:
            X = (self.ops[0], self.ops[0] + self.ops[2])
            Y = (self.ops[1], self.ops[1] + self.ops[3])
            self.PaintButton(self.colors[1 if InCoord(event.pos, X, Y) else 0])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            X = (self.ops[0], self.ops[0] + self.ops[2])
            Y = (self.ops[1], self.ops[1] + self.ops[3])
            if InCoord(event.pos, X, Y):
                return True

    def PaintButton(self, color=None):
        if color is None:
            color = self.colors[0]
        PaintСapsule(self.sf, color, self.ops)
        if len(self.string):
            self.PaintText()


class ButtonWithOutline(Button):
    def __init__(self, sf, ops, colors, string=''):
        super().__init__(sf, ops, colors, string)

    def PaintButton(self, color=None):
        if color is None:
            color = self.colors[0]
        size_line = (min(self.ops[2], self.ops[3]) * 0.02)
        Outline_ops = (self.ops[0] - size_line, self.ops[1] - size_line, self.ops[2] +
                       (size_line * 2), self.ops[3] + (size_line * 2))
        PaintСapsule(self.sf, self.colors[2], Outline_ops)
        super().PaintButton(color)


class TextField:
    def __init__(self, sf, ops, colors, filter=(0, 50)):
        self.sf = sf
        self.ops = ops
        size_line = (min(self.ops[2], self.ops[3]) * 0.02)
        self.inside_ops = (self.ops[0] + size_line, self.ops[1] + size_line, self.ops[2] -
                           (size_line * 2), self.ops[3] - (size_line * 2))
        self.colors = colors
        self.active = False
        self.text = ""
        self.filter_mod = filter[0]
        self.limit = filter[1]
        self.font = FindFont(self.ops)

    def MouseTracking(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            X = (self.ops[0], self.ops[0] + self.ops[2])
            Y = (self.ops[1], self.ops[1] + self.ops[3])
            self.active = True if InCoord(event.pos, X, Y) else False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif self.limit > len(self.text):
                if self.filter_mod == 0:
                    self.text += event.unicode
                elif self.filter_mod == 1:
                    self.text += event.unicode if event.unicode.isdigit() else ''
                elif self.filter_mod == 2:
                    self.text += event.unicode if event.unicode.isalpha() else ''
        PaintСapsule(self.sf, self.colors[1 if self.active else 2], self.ops)
        PaintСapsule(self.sf, self.colors[0], self.inside_ops)
        self.sf.blit(self.font.render(self.text, True, BLACK),
                     (self.ops[0] + 5, self.ops[1] + round(self.ops[3] * 0.2)))

    def GetText(self):
        return self.text

    def SetText(self, text):
        self.text = text

    def ClearText(self):
        self.text = ""


if __name__ == "__main__":
    sf = pygame.display.set_mode((1300, 1000))
    sf.fill(DARK_GREY)

    x = 100
    y = 100
    l = 150
    w = 100

    one = ButtonWithOutline(
        sf, (x, y, l, w), (GREY, LIGHT_GREY, BLACK), 'Hello')
    two = TextField(sf, (50, 220, 300, 50), (GREY, BLUE, BLACK), (0, 5))

    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
            if (one.MouseTracking(event)):
                print(two.GetText())
                two.ClearText()
            two.MouseTracking(event)
