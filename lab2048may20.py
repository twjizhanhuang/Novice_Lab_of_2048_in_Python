import tkinter as tk
from tkinter import messagebox
import random, sys

class Algorithms2048:

    def moveRowLeft(row: list[int]) -> list[int]:
        size = len(row)
        row = [x for x in row if x != 0]
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i+1]:
                row[i] += row[i+1]
                row.pop(i+1)
            i += 1
        while len(row) < size:
            row.append(0)
        return row

    def moveRowRight(row: list[int]) -> list[int]:
        row = [x for x in reversed(row)]
        row = Algorithms2048.moveRowLeft(row)
        row = [x for x in reversed(row)]
        return row
    
    def monteCarloTreeSearch(boarddata: list[list[int]]) -> str:
        return "To Be Implemented"

class Model2048:

    def __init__(self, size: int):
        self.size: int = size
        self.boarddata: list | None = None
        self.after: list | None = None
        self.before: list | None = None

    def setup(self):
        self.boarddata = list()
        for _ in range(0, self.size):
            row = list()
            for _ in range(0, self.size):
                row.append(0)
            self.boarddata.append(row)
        initialTwosPlaced = 0
        while initialTwosPlaced < 2:
            i, j = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.boarddata[i][j] == 0:
                self.boarddata[i][j] = 2
                initialTwosPlaced += 1
        return self
    
    def win2048(self):
        return any(2048 in row for row in self.boarddata)
    
    def loss2048(self):
        if not self.isFull():
            return False
        for i in range(0, self.size):
            for j in range(0, self.size-1):
                if self.boarddata[i][j] == self.boarddata[i][j+1]:
                    return False
        for j in range(0, self.size):
            for i in range(0, self.size-1):
                if self.boarddata[i][j] == self.boarddata[i+1][j]:
                    return False
        return True
    
    def isFull(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.boarddata[i][j] == 0:
                    return False
        return True

class View2048:
    
    def __init__(self, model2048: Model2048):
        self.model2048 = model2048
        self.size = len(self.model2048.boarddata)
        self.root: tk.Tk | None = None
        self.menubar: tk.Menu | None = None
        self.hintOption: tk.StringVar | None = None
        self.mainFrames: list | None = None
        self.mainButtons: list | None = None
        self.statusFrame: tk.Frame | None = None
        self.statusLabel: tk.Label | None = None
        self.moveCount = 0
        self.alreadyWin = False

    def setup(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.size*100}x{self.size*100+40}")
        self.root.resizable(False, False)
        self.root.title("Lab of 2048 in Python")
        self.setupMenubar()
        self.setupMainFrames()
        self.setupMainButtons()
        self.setupStatusFrame()
        self.setupStatusLabel()
        self.root.bind("<Key>", lambda event: Controller2048.keyPressed(event, self))
        Controller2048.updatetexts(self)
        return self
    
    def setupMenubar(self):

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        gameMenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Game", menu=gameMenu)
        gameMenu.add_command(label="New Game", command=lambda: Controller2048.newGame(self.size, self.model2048, self))

        settingsMenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Settings", menu=settingsMenu)

        self.hintOption = tk.StringVar(value="No Hint")
        settingsMenu.add_radiobutton(label="No Hint", variable=self.hintOption, value="No Hint", command=lambda: Controller2048.updatetexts(self))
        settingsMenu.add_radiobutton(label="Monte Carlo Tree Search Hint", variable=self.hintOption, value="Monte Carlo Tree Search Hint", command=lambda: Controller2048.updatetexts(self))
        settingsMenu.add_radiobutton(label="Auto Run", variable=self.hintOption, value="Auto Run", command=lambda: messagebox.showinfo(message="To Be Implemented"))

        return self
    
    def setupMainFrames(self):
        self.mainFrames = list()
        for _ in range(0, self.size):
            rowFrames = list()
            rowFrame = tk.Frame(self.root, borderwidth=0)
            rowFrame.pack(expand=True, fill="both", side="top")
            rowFrame.pack_propagate(False)
            for _ in range(0, self.size):
                frame = tk.Frame(rowFrame, borderwidth=2)
                frame.pack(expand=True, fill="both", side="left")
                frame.pack_propagate(False)
                rowFrames.append(frame)
            self.mainFrames.append(rowFrames)
        return self

    def setupMainButtons(self):
        self.mainButtons = list()
        for i in range(0, self.size):
            rowButtons = list()
            for j in range(0, self.size):
                button = tk.Button(self.mainFrames[i][j], font=('Tahoma', 14), anchor="center", borderwidth=2)
                button.pack(expand=True,fill="both",side="left")
                rowButtons.append(button)
            self.mainButtons.append(rowButtons)
        return self

    def setupStatusFrame(self):
        self.statusFrame = tk.Frame(self.root, width=self.size*100, height=40)
        self.statusFrame.pack(expand=False, fill="x", side="bottom")
        return self
    
    def setupStatusLabel(self):
        self.statusLabel = tk.Label(self.statusFrame, font=('Tahoma', 10), anchor="center", width=self.size*100)
        self.statusLabel.pack(expand=False, fill="x")
        return self
    
class Controller2048:

    def keyPressed(event: tk.Event, view: View2048):
        if view.model2048.loss2048():
            messagebox.showinfo(message="Game Over.")
            sys.exit()
        sym = event.keysym
        if sym == "space" and view.model2048.before != None:
            view.model2048.boarddata = view.model2048.before
            view.model2048.before = None
            view.moveCount -= 1
            Controller2048.updatetexts(view)
        if sym in ('w', 's', 'a', 'd', "Up", "Down", "Left", "Right"):
            Controller2048.attemptMoveData(view.model2048, sym)
            if view.model2048.after != view.model2048.boarddata:
                view.model2048.before = view.model2048.boarddata
                view.model2048.boarddata = view.model2048.after
                view.model2048.after = None
                Controller2048.updatetexts(view)
                view.moveCount += 1
                if not view.model2048.isFull():
                    Controller2048.attemptAddTwo(view.model2048)
                    Controller2048.updatetexts(view)
            if view.model2048.win2048() and not view.alreadyWin:
                if not messagebox.askyesno(message="You Win!\nContinue?"):
                    sys.exit()
                else:
                    view.alreadyWin = True
    
    def attemptMoveData(model: Model2048, move):
        if move in ('w', "Up"):
            transpose = list(map(list, zip(*model.boarddata)))
            temp = [Algorithms2048.moveRowLeft(row) for row in transpose]
            model.after = list(map(list, zip(*temp)))
        if move in ('s', "Down"):
            transpose = list(map(list, zip(*model.boarddata)))
            temp = [Algorithms2048.moveRowRight(row) for row in transpose]
            model.after = list(map(list, zip(*temp)))
        if move in ('a', "Left"):
            model.after = [Algorithms2048.moveRowLeft(row) for row in model.boarddata]
        if move in ('d', "Right"):
            model.after = [Algorithms2048.moveRowRight(row) for row in model.boarddata]
        return model
    
    def updatetexts(view: View2048):
        for i in range(0, view.size):
            for j in range(0, view.size):
                view.mainButtons[i][j].config(text=f"{view.model2048.boarddata[i][j]}" if view.model2048.boarddata[i][j] != 0 else str())
        if view.hintOption.get() == "No Hint":
            hintStr = str()
        if view.hintOption.get() == "Monte Carlo Tree Search Hint":
            hintStr = f", Hint:{Algorithms2048.monteCarloTreeSearch(view.model2048.boarddata)}"
        view.statusLabel.config(text=f"Move Count: {view.moveCount}"+hintStr)
        return view
 
    def attemptAddTwo(model: Model2048):
        while True:
            i, j = random.randint(0, model.size-1), random.randint(0, model.size-1)
            if model.boarddata[i][j] == 0:
                model.boarddata[i][j] = 2
                return model
    
    def newGame(boardsize: int, model: Model2048, view: View2048):
        view.root.destroy()
        model = Model2048(boardsize).setup()
        view = View2048(model).setup()
        view.root.mainloop()

def main():
    BOARDSIZE = 4
    model = Model2048(BOARDSIZE).setup()
    view = View2048(model).setup()
    view.root.mainloop()

if __name__ == "__main__":
    main()