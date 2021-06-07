"""
Plik zawierający główną klasę gry, jest ona głównie odpowiedzialna za interfejs graficzny
oraz funkcjonalność tego interfejsu
"""

import tkinter as tk
import tkinter.messagebox
import functionality


class SaperGame:
    def __init__(self):
        self.mines = 0
        self.mine_field = []
        self.event_list = []
        self.flagged_fields = 0
        self.flagged_mines = 0

    def start_game(self):
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

        # Przycisk zapisania danych
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

        # Sprawdzanie wprowadzonych danych, w wypadku sukcesu przejście do głównego
        try:
            functionality.check_settings(h, w, m)
        except functionality.WrongTypeOfArguments as wtoa:
            error_text = "Podana " + wtoa.argument_name + " (" + wtoa.content + ") musi być liczbą całkowitą"
            tkinter.messagebox.showerror(title="Error", message=error_text)
        except functionality.ArgumentNotInRange as anir:
            if anir.argument_name == "ilość min":
                error_text = "Podana " + anir.argument_name + " (" + anir.value + ") musi być z przedziału od 0 do " + str(int(h)*int(w))
            else:
                error_text = "Podana " + anir.argument_name + " (" + anir.value + ") musi być z przedziału od 2 do 15"
            tkinter.messagebox.showerror(title="Error", message=error_text)
        else:
            window.destroy()
            self.mines = int(m)
            self.prepare_minefield(int(h), int(w), int(m))

    def prepare_minefield(self, height, width, mines):
        """ Funkcja tworząca plansze i rozpoczęcie właściwej części gry """
        root = tk.Tk()
        root.wm_title("Saper")

        # Przypisanie funkcji umożliwiającej podświetlenie min
        root.bind("<Key>", self.highlight_mines)

        # Funkcja losująca miejsca z minami
        mine_field_list = functionality.get_minefield(height, width, mines)

        # Zapełnianie planszy obiektami klasy 'Fields' i 'FieldWithMine'
        self.mine_field = [[self.get_button_with_mine(root, j, i) if mine_field_list[j][i]
                            else self.get_button_without_mine(root, j, i) for i in range(width)] for j in range(height)]

        self.label_mines = tk.Label(root, text="Pozostało min: "+str(self.mines - self.flagged_fields), font=("Calibri", 18))
        self.label_mines.grid(row=height+1, column=0, columnspan=int(width), pady=5)

        reset_button = tk.Button(root, text="Reset", command=lambda: self.reset_game(root), width=20)
        reset_button.grid(row=height+2, column=0, columnspan=int(width), pady=5)

        root.eval('tk::PlaceWindow . center')

        # Główna pętla gry
        root.mainloop()

    def get_button_without_mine(self, root, row, column):
        """ Funkcja zwracająca pojedynczy obiekt klasy 'Fields' z odpowiednimi ustawieniami"""
        return self.Fields(lambda event: self.left_click(event), lambda event: self.right_click(event), row, column,
                           root, relief="raised", borderwidth=3,  width=4, height=2, font=13)

    def get_button_with_mine(self, root, row, column, ):
        """ Funkcja zwracająca pojedynczy obiekt klasy 'FieldWithMines' z odpowiednimi ustawieniami"""
        return self.FieldWithMine(lambda event: self.game_over(event), lambda event: self.right_click(event), row, column, root, relief="raised",
                                  borderwidth=3, width=4, height=2, font=13)

    class Fields(tk.Button):
        """ Podstawowa klasa pola planszy"""
        def __init__(self, fun, fun2, x, y, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.row = x
            self.column = y
            self.grid(row=x, column=y)
            self.state = 0
            self.bind("<Button-3>", fun2)
            self.bind("<Button-1>", fun)

    class FieldWithMine(Fields):
        """ Klasa pola na którym znajduje się mina"""
        def __init__(self, fun, fun2, x, y, *args, **kwargs):
            super().__init__(None, fun2, x, y, *args, **kwargs)
            self.bind("<Button-1>", fun)
            self.window = args[0]

    def left_click(self, event):
        """ Funkcja Lewego przycisku myszy na polach bez min"""
        if isinstance(event, tk.Event):
            tmp_button = event.widget
        else:
            tmp_button = event

        # Wyłączenie funkcji przycisku i zmiana graficzna
        tmp_button['relief'] = 'sunken'
        tmp_button['state'] = 'disabled'
        tmp_button.unbind("<Button-1>")
        tmp_button.unbind("<Button-3>")
        tmp_button["bg"] = "#cccccc"
        if tmp_button["text"] == "!":
            self.flagged_fields -= 1
            self.label_mines["text"] = "Pozostało min: " + str(self.mines - self.flagged_fields)

        tmp_button["text"] = " "

        # zliczanie min w okolicy
        amount, field_list = functionality.check_surroundings(tmp_button.row, tmp_button.column, self.mine_field)
        if amount > 0:
            tmp_button["text"] = amount
        else:
            for j, i in field_list:
                if self.mine_field[i][j]['state'] != 'disabled':
                    self.left_click(self.mine_field[i][j])

    def highlight_mines(self, event):
        """ Funkcja zaznaczająca gdzie znajdują się miny po wpisaniu x,y,z,z,y"""
        self.event_list.append(event.char)
        if len(self.event_list) > 5:
            self.event_list.pop(0)
        if self.event_list == ['x', 'y', 'z', 'z', 'y']:
            for buttons in self.mine_field:
                for button in buttons:
                    if isinstance(button, self.FieldWithMine):
                        button.configure(bg="#9A9A9A")

    def right_click(self, event):
        """ Funkcja prawego przycisku myszy, odpowiedzialna za oznaczanie pól 'tu jest bomba', 'tu może być bomba'"""
        tmp_button = event.widget
        if tmp_button.state == 0:
            # Sprawdzanie czy gracz nie zaznaczył więcej pól niż jest min
            if self.flagged_fields < self.mines:
                tmp_button.configure(text="!")
                tmp_button.state += 1
                self.flagged_fields += 1
                self.label_mines["text"] = "Pozostało min: "+str(self.mines - self.flagged_fields)
                if isinstance(tmp_button, SaperGame.FieldWithMine):
                    self.flagged_mines += 1
                    if self.flagged_mines == self.mines:
                        # Wygrana - wyłączenie planszy
                        tkinter.messagebox.showinfo(title="Saper", message="Gratulacje, wygrałeś! :D")
                        for row in self.mine_field:
                            for tmp_button in row:
                                tmp_button.unbind("<Button-1>")
                                tmp_button.unbind("<Button-3>")
                                tmp_button['state'] = 'disabled'
            else:
                tmp_button.configure(text="?")
                tmp_button.state += 2
        elif tmp_button.state == 1:
            self.flagged_fields -= 1
            self.label_mines["text"] = "Pozostało min: " + str(self.mines - self.flagged_fields)
            if isinstance(tmp_button, SaperGame.FieldWithMine):
                self.flagged_mines -= 1
            tmp_button.configure(text="?")
            tmp_button.state += 1
        elif tmp_button.state == 2:
            tmp_button.configure(text=" ")
            tmp_button.state = 0

    def game_over(self, event):
        """ Funkcja kończąca grę w momencie kliknięcia na bombe """
        tmp_button = event.widget
        tmp_button["bg"] = "red"
        for row in self.mine_field:
            for button in row:
                if isinstance(button, SaperGame.FieldWithMine):
                    button["bg"] = "red"
                button.unbind("<Button-1>")
                button.unbind("<Button-3>")
                button['state'] = 'disabled'
        tkinter.messagebox.showerror(title="Saper", message="Trafiłeś na mine! :(")

    def reset_game(self, window):
        window.destroy()
        self.start_game()
