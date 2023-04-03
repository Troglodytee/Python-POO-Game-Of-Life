from tkinter import *

class Window :
    def __init__ (self) :
        self.window = Tk()
        self.window.title("Jeu de la Vie")
        self.window.resizable(width = False, height = False)

        self.canvas = Canvas(self.window, width = 500, height = 500, bg = "#fff")
        self.canvas.pack(side = TOP, anchor = "w", padx = 0, pady = 0)
        self.canvas.bind("<Button-1>", self.birth)
        self.canvas.bind("<B1-Motion>", self.birth)
        self.canvas.bind("<Button-2>", self.change_pause)
        self.canvas.bind("<Button-3>", self.die)
        self.canvas.bind("<B3-Motion>", self.die)
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.grid = [[Window.Pixel(0, self.canvas.create_rectangle(x * size + 2, y * size + 2, (x + 1) * size + 1, (y + 1) * size + 1, fill = "#fff", outline = "#fff")) for x in range (500 // size)] for y in range (500 // size)]
        self.pause = Window.Pause(0, 0)

        self.window.mainloop()

    def zoom (self, event) :
        if event.delta > 0 :
            del self.grid[0]
            del self.grid[-1]
            for y in range (len(self.grid)) :
                del self.grid[y][0]
                del self.grid[y][-1]
                for x in range (len(self.grid[y])) :
                    self.show(x, y)
        else : "zoom_out"

    def birth (self, event) :
        if 0 <= event.x < len(self.grid) * size and 0 <= event.y < len(self.grid[0]) * size :
            self.grid[event.y // size][event.x // size].state = 1
            self.show(event.x // size, event.y // size)

    def die (self, event) :
        if 0 <= event.x < len(self.grid) * size and 0 <= event.y < len(self.grid[0]) * size :
            self.grid[event.y // size][event.x // size].state = 0
            self.show(event.x // size, event.y // size)

    def show (self, x, y) :
        self.canvas.delete(self.grid[y][x].rectangle)
        self.grid[y][x].rectangle = self.canvas.create_rectangle(x * size + 2, y * size + 2, (x + 1) * size + 1, (y + 1) * size + 1, fill = ["#fff", "#000"][self.grid[y][x].state], outline = ["#fff", "#000"][self.grid[y][x].state])

    def change_pause (self, event) :
        self.pause.state = 1 - self.pause.state
        if self.pause.state : self.pause.object = self.canvas.create_text(22, 10, text = "PAUSE", font="Consolas 10", fill="#f00")
        else :
            self.canvas.delete(self.pause.object)
            self.increment()

    def increment (self) :
        grid = [[Window.Pixel(self.grid[y][x].state,0) for x in range (500 // size)] for y in range (500 // size)]
        for y in range (len(grid)) :
            for x in range (len(grid[y])) :
                total = sum([1 if not (i == 0 and j == 0) and 0 <= x + j < len(grid[y]) and 0 <= y + i < len(grid) and grid[y + i][x + j].state == 1 else 0 for i in [-1,0,1] for j in [-1,0,1]])
                if grid[y][x].state == 0 and total == 3 : self.birth(self.Event(x * size, y * size))
                elif grid[y][x].state == 1 and not (total == 2 or total == 3) : self.die(self.Event(x * size, y * size))
        if self.pause.state == 0 : self.canvas.after(50, self.increment)

    class Pixel :
        def __init__ (self, state, rectangle) :
            self.state = state
            self.rectangle = rectangle

    class Pause :
        def __init__ (self, state, object) :
            self.state = 0
            self.object = object

    class Event :
        def __init__ (self, x, y) :
            self.x = x
            self.y = y

size = 10
window = Window()