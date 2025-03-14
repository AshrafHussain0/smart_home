from tkinter import Tk, Frame, Label, Button, Toplevel, Entry, StringVar, OptionMenu
from backend import SmartPlug, SmartTV, SmartWashingMachine, SmartHome

class SmartHomeApp:

    def __init__(self, win):
        self.smart_home = SmartHome()
        self.smart_home.add_device(SmartTV())
        self.smart_home.add_device(SmartWashingMachine())
        self.smart_home.add_device(SmartPlug())
        
        self.update_parent_win = None

        self.win = win
        self.win.title("Smart Home App")
        
        self.window_width = 680
        self.window_height = 280

        x_position, y_position = self.calc_centre_of_screen()
        
        self.win.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")
        
        self.main_frame = Frame(self.win)
        self.main_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )
        
        for i in range(5):
            self.main_frame.columnconfigure(i, weight=1, minsize=100)
            self.main_frame.rowconfigure(i, weight=1)
        
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_rowconfigure(0, weight=1)

        self.device_widgets = []

    def calc_centre_of_screen(self):
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        x_position = (screen_width - self.window_width) // 2
        y_position = (screen_height - self.window_height) // 2
        
        return x_position, y_position

    def run(self):
        self.create_widgets()
        self.win.mainloop()
    
    def create_widgets(self):
        self.delete_all_device_widgets()

        title_label = Label(
            self.main_frame,
            text="Smart Home",
            font=("Arial"),
        )
        title_label.grid(
            row=0,
            column=0,
            columnspan=5,
            sticky="ew"
        )

        turn_on_all_button = Button(
            self.main_frame,
            text="Turn All On",
            font=("Arial", 11),
            width=40,
            bg="white",
            bd=1,
            command=self.turn_all_on
        )
        turn_on_all_button.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5,
        )

        turn_off_all_button = Button(
            self.main_frame,
            text="Turn All Off",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=self.turn_all_off
        )
        turn_off_all_button.grid(
            row=1,
            column=2,
            columnspan=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        count_devices = len(self.smart_home.devices)
        
        for i in range(count_devices):
            device = self.smart_home.devices[i]
            device_type = type(device).__name__
            device_state = "On" if device.switched_on else "Off"
            
            if device_type == "SmartTV":
                device_attribute = f"Channel: {device.channel}"
            elif device_type == "SmartWashingMachine":
                device_attribute = f"Wash Mode: {device.wash_mode}"
            elif device_type == "SmartPlug":
                device_attribute = f"Consumption: {device.consumption_rate}W"
            else:
                device_attribute = "Unknown Attribute"

            device_label = Label(
                self.main_frame,
                text=f"{device_type}: {device_state}, {device_attribute}",
                font=("Arial", 11),
            )
            device_label.grid(
                row=i+2,
                column=0,
                columnspan=2,
                pady=5,
            )
            self.device_widgets.append(device_label)


            toggle_device_button = Button(
                self.main_frame,
                text="Toggle",
                font=("Arial", 11),
                bg="white",
                bd=1,
                command=lambda index=i: self.toggle_device(index)
            )
            toggle_device_button.grid(
                row=i+2,
                column=2,
                sticky="ew",
                padx=5,
                pady=5,
            )
            self.device_widgets.append(toggle_device_button)


            edit_device_button = Button(
                self.main_frame,
                text="Edit",
                font=("Arial", 11),
                bg="white",
                bd=1,
                command=lambda index=i: self.edit_device(index)
            )
            edit_device_button.grid(
                row=i+2,
                column=3,
                sticky="ew",
                padx=5,
                pady=5,
            )
            self.device_widgets.append(edit_device_button)


            delete_device_button = Button(
                self.main_frame,
                text="Delete",
                font=("Arial", 11),
                bg="white",
                bd=1,
                command=lambda index=i: self.delete_device(index)
            )
            delete_device_button.grid(
                row=i+2,
                column=4,
                sticky="ew",
                padx=5,
                pady=5
            )
            self.device_widgets.append(delete_device_button)

        add_device_button = Button(
            self.main_frame,
            text="Add Device",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=self.add_device
        )
        add_device_button.grid(
            row=count_devices+2,
            column=0,
            columnspan=5,
            sticky="ew",
            padx=5,
            pady=5,
        )
        self.device_widgets.append(add_device_button)
        
        self.win.geometry(f"{self.window_width}x{(self.window_height // 2) + (count_devices * 40)}")

    def delete_all_device_widgets(self):
        for widget in self.device_widgets:
            widget.destroy()
        self.device_widgets = []

    def turn_all_on(self):
        self.smart_home.switch_all_on()
        self.create_widgets()

        if self.update_parent_win:
            self.update_parent_win()

    def turn_all_off(self):
        self.smart_home.switch_all_off()
        self.create_widgets()

        if self.update_parent_win:
            self.update_parent_win()

    def toggle_device(self, index):
        self.smart_home.toggle_device(index)
        self.create_widgets()

        if self.update_parent_win:
            self.update_parent_win()

    def edit_device(self, index):
        device = self.smart_home.get_device(index)
        device_type = type(device).__name__
        
        edit_win = Toplevel(self.win)
        edit_win.title(f"Edit {device_type}")

        x_position, y_position = self.calc_centre_of_screen()
        edit_win.geometry(f"330x200+{x_position + self.window_width // 3}+{y_position + self.window_height // 3}")

        device_type_to_instruction_dict = {
            "SmartPlug": "Enter Consumption Rate:",
            "SmartTV": "Enter Channel:",
            "SmartWashingMachine": "Enter Wash Mode:"
        }

        user_instruction_text = device_type_to_instruction_dict.get(device_type)
        user_instruction_label = Label(
            edit_win,
            text=user_instruction_text,
            font=("Arial", 11)
        )
        user_instruction_label.pack(padx=10, pady=10)

        option_entry_text_var = StringVar(edit_win)
        option_entry = Entry(
            edit_win,
            textvariable=option_entry_text_var
        )
        option_entry.pack(padx=10, pady=10)

        def save_value():
            value = option_entry_text_var.get().strip()
            
            if value.strip() == "":
                error_info_label.config(text="Value cannot be empty")
                return
            
            try:
                if device_type == "SmartWashingMachine":
                    self.smart_home.update_option(index, value)
                
                elif device_type == "SmartTV" or device_type == "SmartPlug":
                    int_value = self.smart_home.attempt_conversion_to_int(value)
                    self.smart_home.update_option(index, int_value)

                edit_win.destroy()
                self.create_widgets()

                if self.update_parent_win:
                    self.update_parent_win()

            except (ValueError, TypeError, IndexError) as e:
                error_info_label.config(text=e)
                edit_win.geometry(f"{len(str(e)) * 8}x200")

        save_button = Button(
            edit_win,
            text="Save",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=save_value
        )
        save_button.pack(padx=5, pady=5)

        error_info_label = Label(
            edit_win,
            fg="red",
            font=("Arial", 11)
        )
        error_info_label.pack(padx=10, pady=10)

        edit_win.mainloop()
    
    def delete_device(self, index):
        self.smart_home.remove_device(index)
        self.create_widgets()

        if self.update_parent_win:
                    self.update_parent_win()

    def add_device(self):
        add_win = Toplevel(self.win)
        add_win.title("Add Device")

        x_position, y_position = self.calc_centre_of_screen()
        add_win.geometry(f"330x200+{x_position + self.window_width // 3}+{y_position + self.window_height // 3}")

        dropdown_label = Label(
            add_win,
            text="Select Device Type:",
            font=("Arial", 11)
        )
        dropdown_label.pack(padx=5, pady=5)

        selected_option = StringVar(add_win)
        selected_option.set("SmartPlug")
        
        dropdown_menu = OptionMenu(
            add_win,
            selected_option,
            "SmartPlug",
            "SmartTV",
            "SmartWashingMachine"
        )
        dropdown_menu.pack()
        dropdown_menu.config(
            font=("Arial", 11),
            bg="white",
            bd=1
        )

        custom_value_label = Label(
            add_win,
            text="Enter custom value:",
            font=("Arial", 11),
        )
        custom_value_label.pack(padx=5, pady=5)
        
        custom_value_text_var = StringVar(add_win)
        custom_value_entry = Entry(
            add_win,
            textvariable=custom_value_text_var
        )
        custom_value_entry.pack(padx=5, pady=5)

        def generate_device_on_ui():
            value = custom_value_entry.get().strip()
            device_type = selected_option.get()
            
            if value.strip() == "":
                error_info_label.config(text="Value cannot be empty")
                return
            
            try:
                device = self.smart_home.input_validation(device_type, value)
                self.smart_home.add_device(device)
                
                add_win.destroy()
                self.create_widgets()

                if self.update_parent_win:
                    self.update_parent_win()

            except (ValueError, AttributeError, TypeError) as e:
                error_info_label.config(text=e)
                add_win.geometry(f"{len(str(e)) * 8}x200")

        save_button = Button(
            add_win,
            text="Save",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=generate_device_on_ui
        )
        save_button.pack(padx=5, pady=5)

        error_info_label = Label(
            add_win,
            fg="red",
            font=("Arial", 11)
        )
        error_info_label.pack(padx=5, pady=5)

        add_win.mainloop()


def test_smart_home_system(app):
    try:
        pass # app.smart_home.add_device(SmartPlug())
    except Exception as e:
        print(e)    


def main():
    app = SmartHomeApp(win=Tk())
    test_smart_home_system(app)
    app.run()

#main()