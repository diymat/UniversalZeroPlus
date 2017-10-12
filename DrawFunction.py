import tkinter as tk
import sys
import string
import math

class DrawFunction:

    colours = [ 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta' ]

    def __init__(self, tk, canvas, xmargin = 80, ymargin = 80):
    
        self.tk = tk
        self.canvas = canvas
        self.xsize = canvas.winfo_width() - 2
        self.ysize = canvas.winfo_height() - 2
        self.dxsize = 0
        self.dysize = 0
        self.xmargin = xmargin
        self.ymargin = ymargin
        self.lastdraw = None
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.xstart = 0
        self.ystart = 0
        self.yend = 0
        self.xend = 0
        self.first = True

    def GC(self, x, y):
        return (x + self.xstart, self.ystart + self.dysize - y)

    def GCX(self, x):
        return x + self.xstart

    def GCY(self, y):
        return self.ystart + self.dysize - y

    def GetRanges(self, data):

        if len(data[0]) < 2:
            return
        self.minX = data[0][0][0]
        self.maxX = data[0][0][0]
        self.minY = data[0][0][1]
        self.maxY = data[0][0][1]

        for dataset in data:
            for point in dataset:
                if self.minX > point[0]:
                    self.minX = point[0]
                if self.maxX < point[0]:
                    self.maxX = point[0]
                if self.minY > point[1]:
                    self.minY = point[1]
                if self.maxY < point[1]:
                    self.maxY = point[1]

    def Unit(self, value):
        if abs(value) < 1e-6:
            return "{0:2.2f} n".format(value * 1e9)
        if abs(value) < 1e-3:
            return "{0:2.2f} u".format(value * 1e6)
        if abs(value) < 1:
            return "{0:2.2f} m".format(value * 1e3)
        return "{0:2.2f}".format(value)

    def DrawGrid(self, data, xgrid = 5, ygrid = 5, debug = 0):
        if not self.first:
            return
        self.first = False
        if debug > 0:
            print(self.xmargin - 1, self.ymargin - 1, self.xsize - 2 * self.xmargin + 1, self.ysize - 2 * self.ymargin + 1, self.xsize, self.ysize)
        rect = self.canvas.create_rectangle(self.xmargin - 1, self.ymargin - 1, self.xsize - self.xmargin, self.ysize - self.ymargin)
        self.dxsize = xsize = self.xsize - 2 * self.xmargin
        self.dysize = ysize = self.ysize - 2 * self.ymargin
        xstep = xsize / xgrid
        ystep = ysize / ygrid
        self.xstart = self.xmargin
        self.ystart = self.ymargin
        self.GetRanges(data)
        for y in range(0, ygrid + 1):
            #text = "{0:2.2f}V".format(self.minY + y *(self.maxY - self.minY) / ygrid)
            text = self.Unit(self.minY + y *(self.maxY - self.minY) / ygrid) + "V"
            if y > 0 and y < ygrid:
                self.canvas.create_line(self.GC(0, y * ystep),self.GC(xsize, y * ystep), dash=(3,2,1,2), fill = 'gray') 
                self.canvas.create_text(self.xmargin - 5, self.GCY(y * ystep), text = text, anchor = tk.E)
            if y == 0:
                self.canvas.create_text(self.xmargin - 5, self.GCY(y * ystep), text = text, anchor = tk.SE)
            if y == ygrid:
                self.canvas.create_text(self.xmargin - 5, self.GCY(y * ystep), text = text, anchor = tk.NE)
        for x in range(0, xgrid + 1):
            text = self.Unit(self.minX + x *(self.maxX - self.minX) / xgrid) + "s"
            if x > 0 and x < xgrid:
                self.canvas.create_line(self.GC(x * xstep, 0),self.GC(x * xstep, ysize), dash=(3,2,1,2), fill = 'gray') 
                self.canvas.create_text(self.GCX(x * xstep), self.dysize + self.ymargin + 6 , text = text, anchor = tk.N)
            if x == 0:
                self.canvas.create_text(self.GCX(x * xstep), self.dysize + self.ymargin + 6 , text = text, anchor = tk.NW)
            if x == xgrid:
                self.canvas.create_text(self.GCX(x * xstep), self.dysize + self.ymargin + 6 , text = text, anchor = tk.NE)
        self.canvas.create_text(self.xsize / 2, self.ymargin / 2 , text = "UNIVERSAL ZERO PLUS RPi HAT DEMO\nhttps://www.diymat.co.uk", anchor = tk.CENTER, fill = 'red', font = ("TkDefaultFont", 15,'bold'), justify = tk.CENTER)

    def DrawFunctions(self, data):
        self.canvas.delete("func")
        ccolour = 0
        if len(data) < 1:
            return
        for function in data:
            dataset = []
            length = len(function)
            xstep = self.dxsize / (length - 1)
            ystep = self.dysize / (length - 1) 
            dy = self.dysize / (self.maxY - self.minY)
            for x in range(0, length):
                dataset.append([self.GCX(x * xstep), self.GCY((function[x][1] - self.minY) * dy)])
            self.canvas.create_line(dataset, fill = self.colours[ccolour], width = 4, tag = "func")
            ccolour += 1
            if(ccolour == len(self.colours)):
                ccolour = 0

    def Convert(self, data, frequency, port):
        func = []
        i = 0
        for sample in data[port][1]:
            func.append([i/(len(data[port][1]) * frequency), sample])
            i += 1
        return func


