from tkinter import *

class RootWindow:
    root = None
    title = 'Simplex method resolver'
    geometry = '350x200'

    def __init__(self):
        root = Tk()
        root.title(self.title)
        root.geometry(self.geometry)
        # all widgets will be here
        
        # Execute Tkinter
        root.mainloop()


