import tkinter as tk
from tkinter import ttk

#------------------------------------------------------------------------------
class Menu(object):
#------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def __init__(self, title):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.ans = None
        self.title = title

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def run(self, a, func=str):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.root = tk.Tk()
        self.root.title(self.title)

        for i in a:
            if isinstance(i, tuple):
                ttk.Button(self.root, text=func(i[0]), command=self.callback(i[1])).pack()
            else:
                ttk.Button(self.root, text=func(i), command=self.callback(i)).pack()

        self.root.mainloop()
        return self.ans

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def callback(self, i):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        def cb():
            self.ans = i
            self.root.destroy()

        return cb	


#------------------------------------------------------------------------------
class BaseDialog(object):
#------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def __init__(self, title):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.root = tk.Tk()
        self.root.title(title)


#------------------------------------------------------------------------------
class Dialog(BaseDialog):
#------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def __init__(self, title):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        BaseDialog.__init__(self, title)
        self.ans = None

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def mkEntry(self, f, sv, row):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ttk.Label(self.root, text=f).grid(column=0, row=row, padx=4, pady=4)
        sv.set(self.dct[f])
        tk.Entry(self.root, textvariable=sv, relief=tk.SUNKEN, state='readonly').grid(column=1, row=row, padx=4, pady=4)
        self.l.append(self.callback(f, sv))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def run(self, dct):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.dct = dct
        self.l = []

        row = 0
        for f in dct:
            if isinstance(dct[f], bool):
                bv = tk.BooleanVar()
                bv.set(dct[f])
                ttk.Label(self.root, text=f).grid(column=0, row=row, padx=4, pady=4)
                ttk.Checkbutton(self.root, variable=bv).grid(column=1, row=row, padx=4, pady=4)
                self.l.append(self.callback(f, bv)) 

            elif isinstance(dct[f], int):
                self.mkEntry(f, tk.IntVar(), row)

            elif isinstance(dct[f], float):
                self.mkEntry(f, tk.DoubleVar(), row)

            else:
                self.mkEntry(f, tk.StringVar(), row)

            row += 1

        ttk.Button(self.root, text="Ok", command=self.finish).grid(column=0, row=row, sticky=tk.N+tk.S+tk.E+tk.W)
        ttk.Button(self.root, text="Cancel", command=self.root.destroy).grid(column=1, row=row, sticky=tk.N+tk.S+tk.E+tk.W)
                
        self.root.mainloop()
        return self.ans
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def finish(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        for i in self.l:
            i()
        self.ans = self.dct
        self.root.destroy()
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def callback(self, f, v):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        def cb():
            self.dct[f] = v.get()

        return cb
            

#------------------------------------------------------------------------------
class Dialog1(BaseDialog):
#------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def run(self, tp):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        row = 0

        for r in tp:
            col = 0
            for c in r:
                c.grid(column=col, row=row) 
                col += 1
            row += 1

        self.root.mainloop()


#------------------------------------------------------------------------------
class Dialog2(BaseDialog):
#------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def __init__(self, title):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        BaseDialog.__init__(self, title)
        self.row = 0
        self.col = 0
        self.maxc = 0
        self.dct = {}
        self.ans = None
        self.l = []

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def nextRow(self, c=1):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.row += c
        if self.col > self.maxc:
            self.maxc = self.col

        self.col = 0

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def nextCol(self, c=1):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.col += c
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def mkLabel(self, f):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ttk.Label(self.root, text=f).grid(column=self.col, row=self.row, padx=4, pady=4)
        self.col += 1

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def mkValue(self, name, default="", ro=False):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        sv = tk.StringVar()
        sv.set(str(default))
        if ro:
            tk.Entry(self.root, textvariable=sv, relief=tk.SUNKEN, state='readonly').grid(column=self.col, row=self.row, padx=4, pady=4)
        else:
            tk.Entry(self.root, textvariable=sv, relief=tk.SUNKEN).grid(column=self.col, row=self.row, padx=4, pady=4)
        self.l.append(self.callback(name, sv))
        self.col += 1

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def mkButton(self, f, cmd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ttk.Button(self.root, text=f, command=cmd).grid(column=self.col, row=self.row, padx=4, pady=4)
        self.col += 1

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def run(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.nextRow()

        print(self.maxc)
        if self.maxc % 2 == 0:
            ok = 0
            cancel = self.maxc - 1
        else:
            ok = 1
            cancel = self.maxc - 2

        ttk.Button(self.root, text="Ok", command=self.finish).grid(column=ok, row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)
        ttk.Button(self.root, text="Cancel", command=self.root.destroy).grid(column=cancel, row=self.row, sticky=tk.N+tk.S+tk.E+tk.W)
                
        self.root.mainloop()
        return self.ans
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def finish(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        for i in self.l:
            i()
        self.ans = self.dct
        self.root.destroy()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def callback(self, f, v):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        def cb():
            self.dct[f] = v.get()

        return cb
        


a = []
for i in range(7):
    a.append((i, i))


m = Menu("Select Int")
while 1:
    v = m.run(a)
    print("sel:", v)

    if v == 2:
        d = Menu("Select Letter")
        x = d.run("abcdef")
        print('x:', x)

    elif v == 1:
        d = Dialog("Boo")
        x = d.run({'s':'boo', 'b': True, 'c': 3.4})
        if x:
            print(x['s'], x['b'], x['c'])

    elif v == 3:

        d = Dialog1("cool")

        tp = [
            [tk.Button(d.root, text="press")],
            [tk.Entry(d.root, text=""), tk.Entry(d.root, text="cat")],
            [tk.Button(d.root, text="ok"), tk.Button(d.root, text="cancel")],
        ]

        d.run(tp)

        d = Dialog2("Test 2")

        def tp():
            print('here')

        d.mkButton('print', tp)
        d.nextRow()

        d.mkLabel("v1")
        d.mkValue("v1", "boo", ro=True)
        d.mkLabel("v2")
        d.mkValue("v2")

        d.nextRow()
        d.mkLabel("v3")
        d.mkValue("v3")
        d.mkLabel("v4")
        d.mkValue("v4")

        ans = d.run()

        if ans:
            print(ans['v1'])
            print(ans['v2'])
            print(ans['v3'])
            print(ans['v4'])

    elif v == 4:
        break
