import tkinter as tk
from tkinter import DISABLED, NORMAL

LARGE_FONT_STYLE = ("Arial", 35, "bold")
MEDIUM_FONT_STYLE = ("Arial", 15, "bold")
DIGITS_FONT_STYLE = ("Arial", 12, "bold")
DEFAULT_FONT_STYLE = ("Arial", 10)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#ebf0f7"
DARK_GRAY = "#878480"
LABEL_COLOR = "#25265E"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("440x513")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.letters_list = []
        self.digits_list = []
        self.current_base = 0
        self.display_frame = self.create_display_frame()

        self.total_label, \
        self.hex_base_label, \
        self.dec_base_label, \
        self.oct_base_label, \
        self.bin_base_label, \
        self.label = self.create_display_labels()

        self.digits = {
            7: (3, 1), 8: (3, 2), 9: (3, 3),
            4: (4, 1), 5: (4, 2), 6: (4, 3),
            2: (5, 2), 3: (5, 3), 1: (5, 1),
            0: (6, 2)
        }
        self.operations = {"+": "+", "-": "-"}
        self.hex_letters = {"A": "10", "B": "11", "C": "12", "D": "13", "E": "14", "F": "15"}
        self.numeric_bases = {"HEX": "1", "DEC": "2", "OCT": "3", "BIN": "4"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=10)
        self.buttons_frame.columnconfigure(0, weight=0)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_hex_letters()
        self.create_numeric_bases_buttons()
        self.call_numeric_bases(self)
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()

    def create_display_labels(self):
        # label superior
        total_label = tk.Label(self.display_frame,
                               text=self.total_expression,
                               anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR,
                               padx=24,
                               pady=10,
                               font=MEDIUM_FONT_STYLE)

        total_label.pack(expand=True, fill='both')

        # label principal
        label = tk.Label(self.display_frame,
                         text=f"{self.current_expression}",
                         anchor=tk.E,
                         bg=LIGHT_GRAY,
                         height=3,
                         fg=LABEL_COLOR,
                         padx=24,
                         font=LARGE_FONT_STYLE)

        label.pack(expand=True, fill='both')

        # labels bases
        # HEXADECIMAL LABEL

        text_hex_value = tk.StringVar()
        text_hex_value.set("HEX:")
        hex_base_label = tk.Label(self.display_frame,
                                  textvariable=text_hex_value,
                                  anchor=tk.W, bg=LIGHT_GRAY,
                                  height=1, fg=LABEL_COLOR,
                                  padx=4,
                                  font=DEFAULT_FONT_STYLE)

        hex_base_label.pack(expand=True, fill=tk.X)

        # DECIMAL LABEL

        text_dec_value = tk.StringVar()
        text_dec_value.set("DEC:")
        dec_base_label = tk.Label(self.display_frame,
                                  textvariable=text_dec_value,
                                  anchor=tk.W, bg=LIGHT_GRAY,
                                  height=1,
                                  fg=LABEL_COLOR,
                                  padx=4,
                                  font=DEFAULT_FONT_STYLE)

        dec_base_label.pack(expand=True, fill=tk.X)

        # OCTA LABEL

        text_oct_value = tk.StringVar()
        text_oct_value.set("OCT:")
        oct_base_label = tk.Label(self.display_frame,
                                  textvariable=text_oct_value,
                                  anchor=tk.W,
                                  bg=LIGHT_GRAY,
                                  height=1,
                                  fg=LABEL_COLOR,
                                  padx=4,
                                  font=DEFAULT_FONT_STYLE)

        oct_base_label.pack(expand=True, fill=tk.X)

        # BINARY LABEL

        text_bin_value = tk.StringVar()
        text_bin_value.set("BIN:")
        bin_base_label = tk.Label(self.display_frame,
                                  textvariable=text_bin_value,
                                  anchor=tk.W,
                                  bg=LIGHT_GRAY,
                                  height=1,
                                  fg=LABEL_COLOR,
                                  padx=4,
                                  font=DEFAULT_FONT_STYLE)

        bin_base_label.pack(expand=True, fill=tk.X)

        # fim labels bases

        return total_label,    hex_base_label, dec_base_label, \
               oct_base_label, bin_base_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=100, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
        self.numeric_bases_display()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame,
                               text=str(digit),
                               bg=WHITE,
                               fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE,
                               borderwidth=0,
                               bd=0.5,
                               command=lambda x=digit: self.add_to_expression(x))

            self.digits_list.append(button)
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.numeric_bases_display()
        self.update_label()

    def create_operator_buttons(self):
        i = 3
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame,
                               text=symbol,
                               bg=OFF_WHITE,
                               fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE,
                               bd=0.5,
                               command=lambda x=operator: self.append_operator(x))

            button.grid(row=i, column=4, rowspan=2, sticky=tk.NSEW)
            i += 2

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.numeric_bases_display()
        self.update_total_label()
        self.update_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame,
                           text="CE",
                           bg=DARK_GRAY,
                           fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           bd=0.5,
                           command=self.clear)

        button.grid(row=6, column=1, sticky=tk.NSEW)

    def create_hex_letters(self):

        i = 1
        for symbol, value in self.hex_letters.items():
            letters_button = tk.Button(self.buttons_frame,
                                       state=DISABLED,
                                       text=symbol,
                                       bg=OFF_WHITE,
                                       fg=LABEL_COLOR,
                                       font=DIGITS_FONT_STYLE,
                                       borderwidth=0,
                                       padx=24,
                                       bd=0.5,
                                       command=lambda x=symbol: self.append_operator(x))

            self.letters_list.append(letters_button)
            letters_button.grid(row=i, column=0, sticky=tk.NSEW)
            i += 1

    def create_numeric_bases_buttons(self):
        i = 0
        for base, operation in self.numeric_bases.items():
            button = tk.Button(self.buttons_frame,
                               state=NORMAL,
                               text=base,
                               bg=LIGHT_BLUE,
                               fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE,
                               bd=0.5,
                               padx=24,
                               command=lambda x=operation: self.call_numeric_bases(x))

            print(operation, i)
            button.grid(row=1, rowspan=2, column=i + 1, sticky=tk.NSEW)
            i += 1

    def evaluate(self):
        self.total_expression += self.current_expression
        try:
            # aqui eu devo fazer as benditas manipulacoes
            if self.current_base == 0 or self.current_base == 2:
                self.update_total_label()
                self.current_expression = str(eval(self.total_expression))
                self.total_expression = ""
            elif self.current_base == 1:
                print("Modo hexadecimal")
            elif self.current_base == 3:
                print("Modo Octa")
            elif self.current_base == 4:
                print("Modo binario")


        except Exception as e:
            self.current_expression = "Error"

        finally:
            self.numeric_bases_display()
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame,
                           text="=",
                           bg=LIGHT_BLUE,
                           fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           bd=0.5,
                           command=self.evaluate)

        button.grid(row=6, column=3, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    # label superior
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    # label principal
    def update_label(self):
        self.label.config(text=self.current_expression[:20])

    # label bases
    def numeric_bases_display(self):

        if self.current_expression != "":
            hex_display = str(hex(int(self.current_expression)))
            dec_display = str(int(self.current_expression))
            oct_display = str(oct(int(self.current_expression)))
            binary_display = str(bin(int(self.current_expression)))
        else:
            hex_display = ""
            dec_display = ""
            oct_display = ""
            binary_display = ""

        text_hex_value = tk.StringVar()
        text_hex_value.set(f"HEX: {hex_display}")
        self.hex_base_label.config(textvariable=f"{text_hex_value}")

        text_dec_value = tk.StringVar()
        text_dec_value.set(f"DEC: {dec_display}")
        self.dec_base_label.config(textvariable=f"{text_dec_value}")

        text_oct_value = tk.StringVar()
        text_oct_value.set(f"OCT: {oct_display}")
        self.oct_base_label.config(textvariable=f"{text_oct_value}")

        text_bin_value = tk.StringVar()
        text_bin_value.set(f"BIN: {binary_display}")
        self.bin_base_label.config(textvariable=f"{text_bin_value}")

    def call_numeric_bases(self, x):

        # HEXA
        if x == "1":
            self.current_base = 0
            self.current_base = 1
            def hex_base():
                self.clear()
                for i in self.letters_list:
                    i['state'] = NORMAL
                for j in self.digits_list[0:9]:
                    j['state'] = NORMAL
            hex_base()

        # DECIMAL
        elif x == "2":
            self.current_base = 0
            self.current_base = 2
            def dec_base():
                self.clear()
                for i in self.letters_list:
                    i['state'] = DISABLED
                for j in self.digits_list[0:9]:
                    j['state'] = NORMAL
            dec_base()

        # OCTA
        elif x == "3":
            self.current_base = 0
            self.current_base = 3
            def oct_base():
                self.clear()
                for i in self.letters_list:
                    i['state'] = DISABLED
                for j in self.digits_list:
                    j['state'] = NORMAL
                for k in self.digits_list[1:3]:
                    k['state'] = DISABLED
            oct_base()

        # BINARIO
        elif x == "4":
            self.current_base = 0
            self.current_base = 4
            def bin_base():
                self.clear()
                for i in self.letters_list:
                    i['state'] = DISABLED
                for j in self.digits_list[0:8]:
                    j['state'] = DISABLED
            bin_base()

    def convert(self):
        return print(self.current_expression)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
