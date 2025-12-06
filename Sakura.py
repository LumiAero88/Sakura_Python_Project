import tkinter as tk
import random
import math

# --- Einstellungen ---
WIDTH, HEIGHT = 900, 550
N_BLOSSOMS = 28         # wie viele Blüten gleichzeitig
BG = "#142034"          # Abendhimmel
PINKS = ["#ffd1e0", "#ffc1d5", "#ffb3ce", "#ff9fc4", "#ff8bb8"]
CENTER_COLOR = "#ffe7f0"

# Hilfsfunktionen
def rot(x, y, angle_deg):
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    return x * ca - y * sa, x * sa + y * ca

class Blossom:
    """Eine fallende, rotierende Kirschblüte (5 Blätter)"""
    def __init__(self, canvas):
        self.cv = canvas
        # Startposition oben/über dem Bild
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(-HEIGHT, -20)
        # Größe der Blüte
        self.size = random.uniform(20, 42)
        # Physik
        self.fall = random.uniform(0.7, 1.6)       # Fallgeschwindigkeit
        self.drift = random.uniform(-0.5, 0.5)     # Grund-Drift
        self.sway_amp = random.uniform(8, 22)      # Amplitude der Pendelbewegung
        self.sway_speed = random.uniform(0.4, 0.9) # Geschwindigkeit des Pendelns
        self.spin = random.uniform(-1.2, 1.2)      # Rotationsgeschwindigkeit (°/Frame)
        self.angle = random.uniform(0, 360)        # Startwinkel
        self.t = random.uniform(0, 1000)           # Phase fürs Pendeln
        # Farbe je Blütenblatt
        self.colors = [random.choice(PINKS) for _ in range(5)]
        # Canvas-Objekte anlegen (5 Blätter + Zentrum)
        self.petals = []
        for _ in range(5):
            pid = self.cv.create_oval(0, 0, 0, 0, fill=random.choice(self.colors), outline="")
            self.petals.append(pid)
        self.center = self.cv.create_oval(0, 0, 0, 0, fill=CENTER_COLOR, outline="")

        self.draw()  # initiale Position

    def draw(self):
        # relative Geometrie einer Blüte:
        # 5 Blätter im Kreis, jedes Blatt eine "Ellipse" (Oval)
        r = self.size * 0.55            # Radius zum Blattmittelpunkt
        petal_w = self.size * 0.9       # Breite eines Blatts
        petal_h = self.size * 1.25      # Höhe eines Blatts

        # sanftes Pendeln für Drift
        sway = math.sin(self.t * self.sway_speed) * self.sway_amp

        # Mittelpunkt der Blüte verschieben
        cx = self.x + sway
        cy = self.y

        # Blätter setzen
        for i, pid in enumerate(self.petals):
            # Basiswinkel für Blatt i
            base = i * 72.0  # 360/5
            # Position des Blattmittelpunkts relativ zum Zentrum, rotiert
            px_rel, py_rel = rot(0, -r, base + self.angle)
            px, py = cx + px_rel, cy + py_rel

            # Die Ovale selbst lassen sich nicht drehen, aber wir "rotieren" die Position der Blätter.
            # Das wirkt wie eine rotierende Blüte.
            # Bounding-Box des Ovals:
            x1 = px - petal_w/2
            y1 = py - petal_h/2
            x2 = px + petal_w/2
            y2 = py + petal_h/2

            # leicht variierende Farben für lebendigeres Bild
            self.cv.itemconfig(pid, fill=self.colors[i])
            self.cv.coords(pid, x1, y1, x2, y2)

        # kleines Zentrum (Kelch)
        c = self.size * 0.28
        self.cv.coords(self.center, cx - c, cy - c, cx + c, cy + c)

    def update(self):
        # Bewegung
        self.t += 0.02
        self.y += self.fall
        self.x += self.drift
        self.angle = (self.angle + self.spin) % 360

        # Neu zeichnen
        self.draw()

        # Wenn unten raus -> oben neu spawnen
        if self.y - self.size > HEIGHT + 30:
            self.x = random.uniform(0, WIDTH)
            self.y = random.uniform(-HEIGHT*0.5, -20)
            self.angle = random.uniform(0, 360)
            self.drift = random.uniform(-0.5, 0.5)
            self.fall = random.uniform(0.7, 1.6)
            self.sway_amp = random.uniform(8, 22)
            self.sway_speed = random.uniform(0.4, 0.9)

class SakuraScene:
    def __init__(self, root):
        self.root = root
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.cv.pack()

        # dezente "Bokeh"-Lichter im Hintergrund
        for _ in range(90):
            x = random.uniform(0, WIDTH)
            y = random.uniform(0, HEIGHT)
            r = random.uniform(2, 5)
            col = "#1b2946"
            self.cv.create_oval(x-r, y-r, x+r, y+r, fill=col, outline="")

        # stilisierte dunkle Äste links/unten
        self.draw_branches()

        # Blüten erstellen
        self.blossoms = [Blossom(self.cv) for _ in range(N_BLOSSOMS)]

        # Loop starten
        self.tick()

    def draw_branches(self):
        branch_color = "#0d172b"
        # Einige dickere Pfade als Äste
        for _ in range(5):
            x1 = random.randint(-80, 120)
            y1 = random.randint(int(HEIGHT*0.55), HEIGHT+40)
            x2 = random.randint(int(WIDTH*0.25), int(WIDTH*0.55))
            y2 = random.randint(int(HEIGHT*0.35), int(HEIGHT*0.6))
            w = random.randint(6, 12)
            self.cv.create_line(x1, y1, x2, y2, fill=branch_color, width=w, smooth=True)

        # Feine Zweige
        for _ in range(18):
            x1 = random.randint(0, int(WIDTH*0.5))
            y1 = random.randint(int(HEIGHT*0.3), HEIGHT)
            x2 = x1 + random.randint(30, 120)
            y2 = y1 - random.randint(20, 90)
            self.cv.create_line(x1, y1, x2, y2, fill=branch_color, width=2, smooth=True)

    def tick(self):
        for b in self.blossoms:
            b.update()
        self.root.after(16, self.tick)  # ~60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sakura – fallende Kirschblüten 🌸")
    SakuraScene(root)
    root.mainloop()

