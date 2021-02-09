import tkinter as tk
from tkinter.ttk import *
import os
import cv2

class MainWindow():
    SHIPS_PATH = "data/global_ships/"

    X0_CORD = 5.3818480
    Y0_CORD = 59.5011267
    X1_CORD = 13.8625297
    Y1_CORD = 53.1910957

    RASTER_XSIZE = 1000
    RASTER_YSIZE = 1000

    def __init__(self):
        self.window=tk.Tk()
        self.label1 = tk.Label()
        self.label2 = tk.Label()
        self.img = tk.PhotoImage()
        self.refreshButton = tk.Button()
        self.progress = Progressbar()
        self.frameButtons = tk.Frame(self.window)
        self.frameMap = tk.Frame(self.window)


    #main window
    def mainWindow(self):
        self.window.geometry("1600x1250")
        self.window.title("aplikacjaV1.0")

        #labelZmapa
        self.frameButtons = tk.Frame(self.window, width=100, height =800)
        self.frameButtons.place(x=2220,y=0,)
        self.frameButtons.pack()

        self.frameMap = tk.Frame(self.window, width=700, height=800)
        self.frameMap.place(x=100, y=0, )
        self.frameMap.pack()

        self.img = tk.PhotoImage(file="mapa.png")

        self.label1 = tk.Label(self.frameButtons,text="test")
        self.label1.place(x=0, y=0)
        self.label1.pack()

        self.label2 = tk.Label(self.frameMap, image=self.img)
        self.label2.place(x=0,y=100)
        self.label2.pack()

        self.var = tk.IntVar()
        self.progress = Progressbar(self.frameButtons, maximum=100, variable=self.var, orient='horizontal', mode='determinate')

        self.progress.place(x=100, y=0)
        self.progress.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.refreshButton = tk.Button(self.label1, text="Detekcja statków", command=lambda:self.refreshImage())
        self.refreshButton.place(x=0,y=0)
        self.refreshButton.pack()

        self.window.mainloop()

    def getTabShips(self, filname):
        tabShips = []
        f = open(self.SHIPS_PATH +filname, 'r')
        counter = 1
        x= 0.0
        for i in f:
            if counter%2 == 1:
                x = float(i)
            else:
                y = float(i)
                tabShips.append((x,y))
            counter += 1
        f.close()
        return tabShips

    def countingFiles(self):
        counter = 0
        for i in os.listdir(self.SHIPS_PATH):
            counter += 1
        return counter

    def calculatingProgress(self):
        n = self.countingFiles()
        step = 100/n
        return step

    def refreshImage(self):
        img_file = 'mapa.png'
        imgChanged = cv2.imread(img_file, cv2.IMREAD_COLOR)
        step = self.calculatingProgress()
        counter = step
        for infile in os.listdir(self.SHIPS_PATH):
            tabShips = self.getTabShips(infile)
            for t in tabShips:
                x,y=t
                xp, yp = self.coordsToPixel(x, y)
                if(xp > 0 and xp < self.RASTER_XSIZE-2  and yp > 0 and yp < self.RASTER_YSIZE-2):
                    imgChanged[int(xp), int(yp)] = [0, 0, 255]
                    imgChanged[int(xp) + 1, int(yp) + 1] = [0, 0, 255]
                    imgChanged[int(xp) + 2, int(yp) + 2] = [0, 0, 255]
                    imgChanged[int(xp) - 1, int(yp) - 1] = [0, 0, 255]
                    imgChanged[int(xp) - 2, int(yp) - 2] = [0, 0, 255]
                    imgChanged[int(xp) + 1, int(yp) - 1] = [0, 0, 255]
                    imgChanged[int(xp) + 2, int(yp) - 2] = [0, 0, 255]
                    imgChanged[int(xp) - 1, int(yp) + 1] = [0, 0, 255]
                    imgChanged[int(xp) - 2, int(yp) + 2] = [0, 0, 255]
            counter += step
            self.var.set(counter)
            self.window.update_idletasks()
            cv2.imwrite("changed.png", imgChanged)
            newImg= cv2.imread("changed.png",cv2.IMREAD_COLOR)
            self.img = tk.PhotoImage(file="changed.png")
            self.label2.configure(image=self.img)
            self.label2.image = newImg
            print("loaded :",infile)

    def coordsToPixel(self, xCordToFind, yCordToFind):#  , x0_cord, y0_cord, x_res, y_res):
        x_res = (self.X1_CORD - self.X0_CORD) / self.RASTER_XSIZE
        y_res = (self.Y1_CORD - self.Y0_CORD) / self.RASTER_YSIZE

        """Returns global coordinates to pixel center using base-0 raster index"""
        Xpixel = int((xCordToFind - self.X0_CORD) / x_res)
        Yline = int((yCordToFind - self.Y0_CORD) / y_res)

        return (Yline, Xpixel)


mw = MainWindow()
mw.mainWindow()

