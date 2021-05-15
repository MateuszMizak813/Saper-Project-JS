import tkinter as tk


class SaperGame:
    def __init__(self):
        pass

    def start_game(self):
        root = self.prepare_minefield()
        root.mainloop()

    def get_size_and_mines(self):
        """
        Metoda get_size_and_mines tworzy okno do wpisania wymiaru planszy oraz ilości min.
        po wpisaniu ich przez
        """

        get_data = tk.Tk()
        get_data.geometry("400x200")
        get_data.wm_title("Saper")
        get_data.grid_columnconfigure(0, weight=1)
        get_data.grid_columnconfigure(5, weight=1)
        get_data.grid_rowconfigure(0, weight=1)
        get_data.grid_rowconfigure(3, weight=1)
        get_data.grid_rowconfigure(5, weight=1)

        l1 = tk.Label(get_data, text="Podaj wymiar planszy:", font=("Calibri", 18))
        l1.grid(row=1, column=2, columnspan=3)

        get_x1 = MyEntry(get_data, width=20)
        get_x1.grid(row=2, column=2, padx=20, pady=10)
        get_x1.bind("<Return>", submit_data)

        l2 = tk.Label(get_data, text="x")
        l2.grid(row=2, column=3)

        get_x2 = MyEntry(get_data, width=20)
        get_x2.grid(row=2, column=4, padx=20, pady=10)
        get_x2.bind("<Return>", submit_data)

        l3 = tk.Label(get_data, text="Ilość min:", font=("Calibri", 18))
        l3.grid(row=4, column=2, columnspan=2)

        get_x3 = MyEntry(get_data, width=20)
        get_x3.grid(row=4, column=4, padx=20, pady=10)
        get_x3.bind("<Return>", submit_data)

        get_data.eval('tk::PlaceWindow . center')

        get_data.mainloop()

    def prepare_minefield(self):
        root = tk.Tk()
        root.wm_title("Saper")
        for i in range(15):
            for j in range(15):
                button = MyButton(i, j, root, padx=20, pady=15, relief="raised", borderwidth=3, state="disabled")
        root.eval('tk::PlaceWindow . center')
        return root


class MyButton(tk.Button):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=x, column=y)
        self.bind("<Button-1>", left_click)
        self.bind("<Button-2>", right_click)
        self.bind("<Button-3>", right_click)


class MyEntry(tk.Entry):
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data


def left_click(event):
    tmp_button = event.widget
    tmp_button['relief'] = 'sunken'
    tmp_button['state'] = 'disabled'
    tmp_button.unbind("<Button-1>")
    tmp_button.unbind("<Button-2>")
    tmp_button.unbind("<Button-3>")
    tmp_button["bg"] = "#cccccc"


def right_click(event):
    event.widget.configure(bg="red")


def submit_data(event):
    tmp_entry = event.widget
    x = tmp_entry.get()
    tmp_entry['state'] = 'disable'
    tmp_entry['bg'] = "#cccccc"
    print(x)
