import tkinter as tk
from tkinter import ttk

from ergast_api import Ergast
import argparse

largeFont = ('Verdana', 12)
mediumFont = ('Helvetica', 10)
smallFont = ('Helvetica', 8)

parser = argparse.ArgumentParser()
parser.add_argument('--season', type=str, default='current',
                    help='F1 season data you want to see. 1950-2019')
args = parser.parse_args()

if args.season == 'current':
    pass
else:
    try:
        int(args.season)
    except ValueError:
        print('Season must be between 1950 and 2019 or current')
        quit()

ergast = Ergast(args.season)
  
class ErgastApiClient(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, 'F1 Data')
        
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        showmenu = tk.Menu(menubar, tearoff=0)
        showmenu.add_command(label='Start page',
                             command=lambda: self.show_frame(StartPage))
        showmenu.add_command(label='Driver standings',
                             command=lambda: self.show_frame(DriverStandings))
        showmenu.add_command(label='Constructor standings',
                             command=lambda: self.show_frame(ConstructorStandings))
        showmenu.add_command(label='Show {} season races'.format(ergast.season),
                             command=lambda: self.show_frame(CurrentSeason))
        menubar.add_cascade(label='Show', menu=showmenu)

        tk.Tk.config(self, menu=menubar)



        self.frames = {}

        for F in (StartPage, CurrentSeason, DriverStandings,
                  ConstructorStandings):
            
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = ttk.Label(self,text='Welcome to use Ergast API Client',
                          font=largeFont)
        label.pack()
        label = ttk.Label(self,
                          text='You are looking {} season data'.format(ergast.season),
                          font=largeFont)
        label.pack(pady=50)

        driverStanding_button = ttk.Button(self, text='Driver Standings',
                                           style='my.TButton',
                                          command= lambda: controller.show_frame(DriverStandings))
        driverStanding_button.pack(side='left', padx=50)
        currentSeason_button = ttk.Button(self, text='Current Season',
                                           style='my.TButton',
                                          command= lambda: controller.show_frame(CurrentSeason))
        currentSeason_button.pack(side='right', padx=50)
        constructorStanding_button = ttk.Button(self, text='Constructor Standings',
                                           style='my.TButton',
                                          command= lambda: controller.show_frame(ConstructorStandings))
        constructorStanding_button.pack( padx=50)


class CurrentSeason(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self)
        frame = tk.Frame(canvas)

        scrollbar = tk.Scrollbar(self,orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side = 'right', fill='y')

        raceName_label = tk.Label(frame, text='Race Name', font=largeFont)
        raceName_label.grid(row=0,column=0, padx=200)

        time_label = tk.Label(frame, text='Time', font=largeFont)
        time_label.grid(row=0,column=1)

        allRaces, total_races = ergast.allRaces()


        for race in range(int(total_races)):
            label = tk.Label(frame,text=allRaces[race][0], font=largeFont)
            label.grid(row=race+1,column=0)
            label = tk.Label(frame,text=allRaces[race][1], font=largeFont)
            label.grid(row=race+1,column=1)
            
        def scrollfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),
                             width=800,height=650)
     
        frame.pack()
        canvas.pack()
        canvas.create_window((0,0), window=frame, anchor='n')
        frame.bind("<Configure>",scrollfunction)

class DriverStandings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        driverStandings, total_drivers = ergast.driverStandings()

        canvas = tk.Canvas(self)
        frame = tk.Frame(canvas)
        
        scrollbar = tk.Scrollbar(self,orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side = 'right', fill='y')

        label1 = ttk.Label(frame, text='Driver Standings', font=largeFont)
        label1.grid(row=0, column=2, pady=10)

        label2 = ttk.Label(frame, text='Season:', font=largeFont)
        label2.grid(row=1, column=0, pady=10)

        label3 = ttk.Label(frame, text=ergast.season, font=largeFont)
        label3.grid(row=1, column=1, pady=10)
        
        position_label = ttk.Label(frame, text='Position', font=largeFont)
        position_label.grid(column=0,row=2, padx = 20, pady=10)

        driver_label = ttk.Label(frame, text='Driver', font=largeFont)
        driver_label.grid(column=1,row=2, padx = 40, pady=10)

        constructor_label = ttk.Label(frame, text='Constructor', font=largeFont)
        constructor_label.grid(column=2,row=2, padx = 40, pady=10)

        points_label = ttk.Label(frame, text='Points', font=largeFont)
        points_label.grid(column=3,row=2, padx = 20, pady=10)

        wins_label = ttk.Label(frame, text='Wins', font=largeFont)
        wins_label.grid(column=4,row=2, padx = 20, pady=10)

        for driver in range(total_drivers):
            for i in range(5):
                label = ttk.Label(frame, text=str(driverStandings[driver][i]),
                                  font=largeFont)
                label.grid(row=driver+3, column=i)

        def scrollfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),
                             width=800,height=650)
##            canvas.bind("<1>",lambda event: canvas.focus_set())
##            canvas.bind("<Up>",lambda event: canvas.yview_scroll(-1, "units"))
##            canvas.bind("<Down>",lambda event: canvas.yview_scroll( 1, "units"))
     
        frame.pack()
        canvas.pack()
        canvas.create_window((0,0), window=frame, anchor='n')
        frame.bind("<Configure>",scrollfunction)


class ConstructorStandings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self)
        frame = tk.Frame(canvas)

        scrollbar = tk.Scrollbar(self,orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side = 'right', fill='y')

        label1 = ttk.Label(frame, text='Constructor Standings', font=largeFont)
        label1.grid(row=0, column=2, pady=10)

        label2 = ttk.Label(frame, text='Season:', font=largeFont)
        label2.grid(row=1, column=0, pady=20)

        label3 = ttk.Label(frame, text=ergast.season, font=largeFont)
        label3.grid(row=1, column=1, pady=20)
        
        position_label = ttk.Label(frame, text='Position', font=largeFont)
        position_label.grid(column=0,row=2, padx = 20, pady=10)

        driver_label = ttk.Label(frame, text='Constructor', font=largeFont)
        driver_label.grid(column=1,row=2, padx = 40, pady=10)


        points_label = ttk.Label(frame, text='Points', font=largeFont)
        points_label.grid(column=2,row=2, padx = 40, pady=10)

        wins_label = ttk.Label(frame, text='Wins', font=largeFont)
        wins_label.grid(column=3,row=2, padx = 20, pady=10)

        constructorStandings, total_constructors = ergast.constructorStandings()


        for constructor in range(int(total_constructors)):
            for i in range(4):
                label = ttk.Label(frame, text=str(constructorStandings[constructor][i]),
                                  font=largeFont)
                label.grid(row=constructor+3, column=i, pady=5)
            
        def scrollfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),
                             width=800,height=650)
     
        frame.pack()
        canvas.pack()
        canvas.create_window((0,0), window=frame, anchor='n')
        frame.bind("<Configure>",scrollfunction)
        

app = ErgastApiClient()
app.geometry('800x650')
s = ttk.Style()
s.configure('my.TButton', font=('Verdana', 12))
app.mainloop()