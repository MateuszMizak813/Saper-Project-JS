import tkinter as tk
import tkinter.messagebox
import temporary_name


class SaperGame:
    def __init__(self):
        self.mines = 0
        self.mine_field = []

    def start_game(self):
        pass

    def get_size_and_mines(self):
        """
        Metoda get_size_and_mines tworzy okno odpowiedzialne za sczytanie wielkości
        planszy oraz ilości min wprowadzonych przez użytkownika
        """

        # Ustawienia okna ustawień planszy:
        get_data = tk.Tk()
        get_data.iconphoto(True, tk.PhotoImage(file='./graphics/saper_window_icon.png'))
        get_data.geometry("400x300")
        get_data.wm_title("Saper")
        get_data.grid_columnconfigure(0, weight=1)
        get_data.grid_columnconfigure(5, weight=1)
        get_data.grid_rowconfigure(0, weight=1)
        get_data.grid_rowconfigure(3, weight=1)
        get_data.grid_rowconfigure(5, weight=1)

        l1 = tk.Label(get_data, text="Ustawienia planszy:", font=("Calibri", 18))
        l1.grid(row=0, column=2, columnspan=3)

        # Wejście (Wysokość planszy)
        l2 = tk.Label(get_data, text="Wysokość :", font=("Calibri", 18))
        l2.grid(row=2, column=2)
        get_x1 = tk.Entry(get_data, width=20)
        get_x1.grid(row=2, column=4, padx=20, pady=10)

        # Wejście (Szerokość planszy)
        l2 = tk.Label(get_data, text="Szerokość :", font=("Calibri", 18))
        l2.grid(row=3, column=2)
        get_x2 = tk.Entry(get_data, width=20)
        get_x2.grid(row=3, column=4, padx=20, pady=10)

        # Wejście (Ilość Min)
        l3 = tk.Label(get_data, text="Ilość min:", font=("Calibri", 18))
        l3.grid(row=4, column=2)
        get_x3 = tk.Entry(get_data, width=20)
        get_x3.grid(row=4, column=4, padx=20, pady=10)

        button = tk.Button(get_data, text="Submit", font=("Calibri", 18), width=15, borderwidth=3,
                           command=lambda: self.submit_data(get_x1, get_x2, get_x3, get_data))
        button.grid(row=5, column=2, columnspan=3)

        # Główna pętla
        get_data.eval('tk::PlaceWindow . center')
        get_data.mainloop()

    def submit_data(self, height, width, mines, window):
        """ Funkcja przycisku zatwierdzającego ustawienia gry """
        h = height.get()
        w = width.get()
        m = mines.get()
        try:
            temporary_name.check_settings(h, w, m)
        except temporary_name.WrongTypeOfArguments as wtoa:
            error_text = "Podana " + wtoa.argument_name + " (" + wtoa.content + ") musi być liczbą całkowitą"
            tkinter.messagebox.showerror(title="Error", message=error_text)
        except temporary_name.ArgumentNotInRange as anir:
            if anir.argument_name == "ilość min":
                error_text = "Podana " + anir.argument_name + " (" + anir.value + ") musi być z przedziału od 0 do " + str(int(h)*int(w))
            else:
                error_text = "Podana " + anir.argument_name + " (" + anir.value + ") musi być z przedziału od 2 do 15"
            tkinter.messagebox.showerror(title="Error", message=error_text)
        else:
            print("Ustawienia poprawne")  # Chwilowe
            window.destroy()
            self.mines = int(m)
            self.prepare_minefield(int(h), int(w), int(m))

    def prepare_minefield(self, height, width, mines):  # Funkcja do zmiany
        root = tk.Tk()
        root.wm_title("Saper")
        mine_field_list = temporary_name.get_minefield(height, width, mines)
        # Do zmiany
        get_button_with_mine = lambda row, column: FieldWithMine(row, column, root, relief="raised", borderwidth=3,
                                                                 state="disabled", width=4, height=2, font=13)
        # Do zmiany
        get_button_without_mine = lambda row, column: Fields(row, column, root, relief="raised", borderwidth=3,
                                                             state="disabled", width=4, height=2, font=13)
        self.mine_field = [[get_button_with_mine(j, i) if mine_field_list[j][i] else get_button_without_mine(j, i)
                            for i in range(width)] for j in range(height)]
        print(self.mine_field)
        root.eval('tk::PlaceWindow . center')
        root.mainloop()


class Fields(tk.Button):
    """ Podstawowa klasa pola planszy"""
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=x, column=y)
        self.state = 0
        self.bind("<Button-3>", right_click)
        self.bind("<Button-1>", left_click)


class FieldWithMine(Fields):
    """ Klasa pola na którym znajduje się mina"""
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(x, y, *args, **kwargs)
        self.bind("<Button-1>", game_over)
        self.window = args[0]


# Do zmiany - funkcja chwilowa
def left_click(event):
    tmp_button = event.widget
    tmp_button['relief'] = 'sunken'
    tmp_button['state'] = 'disabled'

    tmp_button.unbind("<Button-1>")
    tmp_button.unbind("<Button-2>")
    tmp_button.unbind("<Button-3>")
    tmp_button["bg"] = "#cccccc"


# Wersja bazowa - Wymagane poprawki wizualne i blokada liczby oznaczeń wykrzyknikiem
def right_click(event):
    """ Funkcja prawego przycisku myszy, odpowiedzialna za oznaczanie pól 'tu jest bomba', 'tu może być bomba'"""
    tmp_button = event.widget
    if tmp_button.state == 0:
        tmp_button.configure(text="!")
        tmp_button.state += 1
    elif tmp_button.state == 1:
        tmp_button.configure(text="?")
        tmp_button.state += 1
    elif tmp_button.state == 2:
        tmp_button.configure(text=" ")
        tmp_button.state = 0


# Nie dokończone - brak możliwości restartu gry oraz brak komunikatu
def game_over(event):
    """ Funkcja kończąca grę w momencie kliknięcia na bombe """
    tmp_button = event.widget
    print("Game Over")
    tmp_button.window.destroy()
