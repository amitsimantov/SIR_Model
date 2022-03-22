import tkinter
import matplotlib.pyplot as plt
from tkinter import *
import math
import numpy as np
import pymsgbox

DAY = 1
WEEK = 7
MONTH = 30


class State:
    def __init__(self, s, i, r):
        self.n = s + i + r
        self.s = s
        self.i = i
        self.r = r

    def __repr__(self):
        return f"S={self.s}, I={self.i}, R={self.r}\nTotal Population={self.n}"


class System:
    def __init__(self, init, tr, rr):
        self.initial_state = init
        self.transmission_rate = tr
        self.recovery_rate = rr

    @property
    def reproductive_rate(self):
        return self.initial_state.s * float(self.transmission_rate / self.recovery_rate)

    @property
    def herd_immunity_threshold(self):
        return 1 - float(1 / self.reproductive_rate)

    def update(self, state):
        s = state.s
        i = state.i
        r = state.r
        infected = float(self.transmission_rate * s * i)
        recovered = float(self.recovery_rate * i)
        s -= infected
        i += infected - recovered
        r += recovered
        return State(s=s, i=i, r=r)

    def is_valid_number(self, x):
        if math.isnan(x) or math.isinf(x):
            return False
        return True

    def is_valid_state(self, state):
        SIR = {0: "S", 1: "I", 2: "R"}
        val_list = [state.s, state.i, state.r]
        for k in range(len(val_list)):
            if math.isnan(val_list[k]) or math.isinf(val_list[k]) or val_list[k] < 0:
                print(f"Got {val_list[k]} for {SIR[k]} value")
                return False
        return True

    def run_simulation(self, t_end):
        states = {}
        state = self.initial_state
        for t in range(t_end):
            if self.is_valid_state(state):
                states[t] = state
                state = self.update(state)
            else:
                print(f"State for time: {t} is not valid!")
                break
        return states


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


def show_results():
    S = float(Entry.get(s))
    I = float(Entry.get(i))
    R = float(Entry.get(r))
    T = int(Entry.get(t))
    TR = eval(Entry.get(transmission_rate))
    RR = eval(Entry.get(recovery_rate))
    Name = str(Entry.get(n1))

    init = State(s=S, i=I, r=R)
    sys = System(init=init,
                 tr=TR,
                 rr=RR)

    states = sys.run_simulation(t_end=T)
    S_values = [states[i].s for i in range(0, len(states))]
    I_values = [states[j].i for j in range(0, len(states))]
    R_values = [states[k].r for k in range(0, len(states))]
    T_values = [l for l in range(len(states))]
    hit_diffs = np.abs([((1 - S_values[j] / init.n) - sys.herd_immunity_threshold) for j in range(len(S_values))])

    if display_hit.get() == 1:
        pymsgbox._alertTkinter(f'Final Values:\n\n'
                               f'S: {int(S_values[-1])}\n'
                               f'I:   {int(I_values[-1])}\n'
                               f'R: {int(R_values[-1])}\n\n'
                               f'Reproductive Rate: {sys.reproductive_rate}\n\n'
                               f'Max Number of Infected: {int(max(I_values))}   |   Day: {T_values[np.argmax(I_values)]}\n'
                               f'Percentage of total population: {round(max(I_values) / init.n, 2) * 100}%\n\n'
                               f'Total Number of Recovered: {int(R_values[-1])}\n'
                               f'Percentage of total population: {round((R_values[-1]) / init.n, 2) * 100}%\n\n'
                               f'HIT: {sys.herd_immunity_threshold * 100}%   |   Day: {np.argmin(hit_diffs)}   |   S: {S_values[np.argmin(hit_diffs)]}',
                               'Results')
    else:
        pymsgbox._alertTkinter(f'Final Values:\n\n'
                               f'S: {int(S_values[-1])}\n'
                               f'I:   {int(I_values[-1])}\n'
                               f'R: {int(R_values[-1])}\n\n'
                               f'Reproductive Rate: {sys.reproductive_rate}\n\n'
                               f'Max Number of Infected: {int(max(I_values))}   |   Day: {T_values[np.argmax(I_values)]}\n'
                               f'Percentage of total population: {round(max(I_values) / init.n, 2) * 100}%\n\n'
                               f'Total Number of Recovered: {int(R_values[-1])}\n'
                               f'Percentage of total population: {round((R_values[-1]) / init.n, 2) * 100}%\n',
                               'Results')


def graph():
    S = float(Entry.get(s))
    I = float(Entry.get(i))
    R = float(Entry.get(r))
    T = int(Entry.get(t))
    TR = eval(Entry.get(transmission_rate))
    RR = eval(Entry.get(recovery_rate))
    Name = str(Entry.get(n1))

    init = State(s=S, i=I, r=R)
    sys = System(init=init,
                 tr=TR,
                 rr=RR)

    states = sys.run_simulation(t_end=T)
    S_values = [states[i].s for i in range(0, len(states))]
    I_values = [states[j].i for j in range(0, len(states))]
    R_values = [states[k].r for k in range(0, len(states))]
    T_values = [l for l in range(len(states))]
    hit_diffs = np.abs([((1 - S_values[j] / init.n) - sys.herd_immunity_threshold) for j in range(len(S_values))])

    plt.figure()
    # Discrete plot
    # plt.plot(T_values, S_values, 'o', color='gold', label='Susceptible')
    # plt.plot(T_values, I_values, 'o', color='indianred', label='Infected')
    # plt.plot(T_values, R_values, 'o', color='turquoise', label='Recovered')

    # Continuous plot
    plt.plot(T_values, S_values, '--', label='Susceptible')
    plt.plot(T_values, I_values, '-', label='Infected')
    plt.plot(T_values, R_values, '--', label='Recovered')

    if display_hit.get() == 1:
        plt.annotate('HIT',
                xy=(np.argmin(hit_diffs), I_values[np.argmin(hit_diffs)]), xycoords='data',
                xytext=(0.6, 0.8), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top', fontsize=14, fontweight='bold')

    plt.xlabel('Time (days)')
    plt.ylabel('SIR Populations')
    plt.title(Name, fontweight='bold')
    plt.legend()
    plt.show()

def fill_def():
    s.insert(0, '20000')
    i.insert(0, '1')
    t.insert(0, '150')
    transmission_rate.insert(0, '0.00005')
    recovery_rate.insert(0, '0.1')


def clear():
    s.delete(0, tkinter.END)
    i.delete(0, tkinter.END)
    t.delete(0, tkinter.END)
    transmission_rate.delete(0, tkinter.END)
    recovery_rate.delete(0, tkinter.END)


if __name__ == '__main__':
    root = Tk()
    root.option_add('*font', 'Gisha -15 bold')
    display_hit = tkinter.IntVar()

    X1Lab = Label(root, text="S(0)")
    X2Lab = Label(root, text="I(0)")
    X3Lab = Label(root, text="R(0)")
    X4Lab = Label(root, text="T")
    X5Lab = Label(root, text="a")
    X6Lab = Label(root, text="r")
    NameLab = Label(root, text="Graph Name")
    root.option_clear()

    root.option_add('*font', 'Gisha -15')

    # getting input from user:
    s = Entry(root)
    i = Entry(root)
    r = Entry(root)
    t = Entry(root)
    transmission_rate = Entry(root)
    recovery_rate = Entry(root)
    n1 = Entry(root)
    n1.insert(0, 'SIR Model')
    r.insert(0, '0')

    # Buttons and checkbox
    root.option_add('*font', 'Gisha -15 bold')
    graph_it = Button(root, text="Graph it!", fg='blue', command=graph)
    show_res = Button(root, text="Show me the results!", fg='green', command=show_results)

    root.option_add('*font', 'Gisha -15')
    fill_default = Button(root, text="Fill Default Values", fg='black', command=fill_def)
    clear_val = Button(root, text="Clear", fg='black', command=clear)
    show_hit = Checkbutton(root, text='Display HIT', variable=display_hit, onvalue=1, offvalue=0)
    # fill_default_val = Checkbutton(root, text='Fill Default Values', variable=y, onvalue=1, offvalue=0)

    # Label:
    X1Lab.grid(row=1, column=0)
    X2Lab.grid(row=2, column=0)
    X3Lab.grid(row=3, column=0)
    X4Lab.grid(row=4, column=0)
    X5Lab.grid(row=5, column=0)
    X6Lab.grid(row=6, column=0)
    NameLab.grid(row=15, column=0)
    s.grid(row=1, column=2)
    i.grid(row=2, column=2)
    r.grid(row=3, column=2)
    t.grid(row=4, column=2)
    transmission_rate.grid(row=5, column=2)
    recovery_rate.grid(row=6, column=2)
    n1.grid(row=15, column=2)

    graph_it.grid(row=16, column=0)
    show_res.grid(row=16, column=2)
    show_hit.grid(row=17, column=0)
    fill_default.grid(row=17, column=2)
    clear_val.grid(row=17, column=3)

    # App name:
    root.wm_title("SIR Model")

    root.mainloop()
