try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import ccp_support
import handler_gui
import handler
import threading
import help
import time
import noise_maker
from tkinter import messagebox

pass_to_calc = False
first_time = True
HANDLER_THREAD_RUNNING = False


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root

    # calc_thread = threading.Thread(target=noise_maker.make_noise, args=())
    # calc_thread.start()

    root = tk.Tk()
    top = Toplevel1 (root)
    ccp_support.init(root, top)
    root.mainloop()
    print('TESTTT')


def keep_alive():
    while True:
        update_root()


def update_root():
    global val, w, root
    root.update()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    ccp_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("465x363+472+181")
        top.minsize(120, 1)
        top.maxsize(1364, 749)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(borderwidth="4")
        top.configure(background="#f1e1d3")
        top.configure(highlightbackground="#D9AF8B")
        top.configure(highlightcolor="black")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.516, rely=0.358, height=34, width=127)
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#c8b5a6")
        self.Button1.configure(borderwidth="1")
        self.Button1.configure(disabledforeground="#F2BC79")
        self.Button1.configure(font="-family {Arial} -size 10 -weight bold")
        self.Button1.configure(foreground="#141f26")
        self.Button1.configure(highlightbackground="#F2BC79")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief="flat")
        self.Button1.configure(text='''Start Calculating''')
        self.Button1.configure(command=start_calculations)

        self.Listbox1 = tk.Listbox(top)
        self.Listbox1.place(relx=0.0, rely=0.0, relheight=0.997, relwidth=0.396)
        self.Listbox1.configure(activestyle="none")
        self.Listbox1.configure(background="#c8b5a6")
        self.Listbox1.configure(borderwidth="4")
        self.Listbox1.configure(disabledforeground="#cb7a97")
        self.Listbox1.configure(exportselection="0")
        self.Listbox1.configure(font="-family {Dubai} -size 13")
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(highlightbackground="#d9d9d9")
        self.Listbox1.configure(highlightcolor="black")
        self.Listbox1.configure(highlightthickness="0")
        self.Listbox1.configure(justify='center')
        self.Listbox1.configure(relief="ridge")
        self.Listbox1.configure(selectbackground="#c4c4c4")
        self.Listbox1.configure(selectforeground="#141F26")
        self.Listbox1.configure(selectmode='single')

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.452, rely=0.028, height=61, width=234)
        self.Label1.configure(activebackground="#141F26")
        self.Label1.configure(activeforeground="white")
        self.Label1.configure(activeforeground="#7c6249")
        self.Label1.configure(background="#f1e1d3")
        self.Label1.configure(disabledforeground="#ffffff")
        self.Label1.configure(font="-family {Times New Roman} -size 40")
        self.Label1.configure(foreground="#876a50")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Roy's CCP''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.516, rely=0.193, height=21, width=174)
        self.Label2.configure(activebackground="#141F26")
        self.Label2.configure(activeforeground="white")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#f1e1d3")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Times New Roman} -size 12")
        self.Label2.configure(foreground="#876a50")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''V 1.0   2020''')

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.409, rely=0.826, height=51, width=264)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="#7c6249")
        self.Label3.configure(background="#c8b5a6")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Arial} -size 11")
        self.Label3.configure(foreground="#141F26")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Making noise''')

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.516, rely=0.744, height=21, width=164)
        self.Label4.configure(activebackground="#D9CDBF")
        self.Label4.configure(activeforeground="#D9CDBF")
        self.Label4.configure(background="#f1e1d3")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font="-family {Arial} -size 13 -weight bold")
        self.Label4.configure(foreground="#856950")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Program feedback''')

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.796, rely=0.358, height=34, width=37)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#c8b5a6")
        self.Button2.configure(borderwidth="1")
        self.Button2.configure(cursor="fleur")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font="-family {Times New Roman} -size 13 -weight bold")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief="flat")
        self.Button2.configure(text='''?''')
        self.Button2.configure(command=start_help_gui)

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

    def update_output(self, output):
        self.Label3.configure(text=output)
        update_root()

    def insert_bots(self, bots):
        self.Listbox1.delete(0, 'end')
        for bot in bots:
            self.Listbox1.insert('end', bot)
        update_root()


def start_help_gui():
    help.vp_start_gui()


def start_calculations():
    global first_time
    global HANDLER_THREAD_RUNNING
    root.withdraw()
    hash_type, params = handler_gui.vp_start_gui(first_time)
    root.deiconify()

    if first_time:
        first_time = False

    if HANDLER_THREAD_RUNNING:
        ccp_support.update_feedback('Already running calculations please wait')
        return

    validity = check_validity(hash_type, params)
    if validity == "ERROR:BAD HASH":
        ccp_support.update_feedback('Program supports only MD5 and SHA256')
        return
    elif validity == 'ERROR: TOO LONG':
        ccp_support.update_feedback('Length can only be less than 17')
        return
    elif validity == 'ERROR: BAD LENGTH':
        ccp_support.update_feedback('The length field should be a number 1-16')
        return
    elif not validity:
        ccp_support.update_feedback('Bad hash input')
        return

    print('Starting handler')
    calc_thread = threading.Thread(target=handler.start_handler, args=(hash_type, params,))
    calc_thread.start()

    HANDLER_THREAD_RUNNING = True


def pass_second_calculate():
    return


def check_validity(hash_type, params):
    aveliable_hashes = ['MD5', 'SHA256']

    try:
        val = int(params.split('#')[1])
    except ValueError:
        return 'ERROR: BAD LENGTH'

    if val > 16:
        return 'ERROR: TOO LONG'

    if hash_type not in aveliable_hashes:
        return "ERROR:BAD HASH"

    if hash_type == 'SHA256' and len(params.split('#')[0]) == 64:
        return True
    elif hash_type == 'MD5' and len(params.split('#')[0]) == 32:
        return True
    else:
        return False


if __name__ == '__main__':
    vp_start_gui()





