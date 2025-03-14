from tkinter import Tk, Frame, Label, Button, Toplevel, IntVar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from backend import SmartPlug, SmartTV, SmartWashingMachine, SmartHome
from frontend import SmartHomeApp

class SmartHomesApp:

    def __init__(self):
        self.win = Tk()
        self.win.title("Smart Home Manager")

        self.window_width = 680
        self.window_height = 280

        x_position, y_position = SmartHomeApp.calc_centre_of_screen(self)

        self.win.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")

        self.main_frame = Frame(self.win)
        self.main_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        for i in range(4):
            self.main_frame.columnconfigure(i, weight=1)
            self.main_frame.rowconfigure(i, weight=1)
        self.win.grid_columnconfigure(0, weight=1)
        
        self.next_smart_home_id = 1
        self.smart_homes_dict = {}
        self.widgets_list = []

    def run(self):
        self.create_widgets()
        self.win.mainloop()

    def create_widgets(self):
        self.delete_all_smart_home_widgets()

        title_label = Label(
            self.main_frame,
            text="Smart Home Manager",
            font=("Arial")
        )
        title_label.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="ew"
        )

        load_save_button = Button(
            self.main_frame,
            text="Load Save",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=self.load_save
        )
        load_save_button.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5,
        )
        
        save_state_button = Button(
            self.main_frame,
            text="Save State",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=self.save_state
        )
        save_state_button.grid(
            row=1,
            column=2,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5
        )

        add_button = Button(
            self.main_frame,
            text="Add",
            font=("Arial", 11),
            bg="white",
            bd=1,
            command=self.add_smart_home
        )
        add_button.grid(
            row=2,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=5,
            pady=5
        )
        
        count_smart_homes = len(self.smart_homes_dict)
        smart_home_names = list(self.smart_homes_dict.keys())

        for i in range(count_smart_homes):
            smart_home_name = smart_home_names[i]
            
            smart_home_app_object = self.smart_homes_dict[smart_home_name][0]
            devices = smart_home_app_object.smart_home.devices
            number_of_devices = len(smart_home_app_object.smart_home.devices)
            
            number_of_devices_currently_on = 0
            for device in devices:
                if device.switched_on:
                    number_of_devices_currently_on += 1
            
            smart_home_label = Label(
                self.main_frame,
                text=f"{smart_home_name}: {number_of_devices} devices, {number_of_devices_currently_on} switched on",
                font=("Arial", 11),
            )
            smart_home_label.grid(
                row=i+3,
                column=0,
                columnspan=2,
                pady=5,
            )
            self.widgets_list.append(smart_home_label)

            modify_smart_home_button = Button(
                self.main_frame,
                text="Modify",
                font=("Arial", 11),
                bg="white",
                bd=1,
                command=lambda index=smart_home_name :self.modify_smart_home(index)
            )
            modify_smart_home_button.grid(
                row=i+3,
                column=2,
                sticky="ew",
                padx=5,
                pady=5,
            )
            self.widgets_list.append(modify_smart_home_button)

            delete_smart_home_button = Button(
                self.main_frame,
                text="Delete",
                font=("Arial", 11),
                bg="white",
                bd=1,
                command=lambda index=smart_home_name :self.remove_smart_home(index)
            )
            delete_smart_home_button.grid(
                row=i+3,
                column=3,
                sticky="ew",
                padx=5,
                pady=5,
            )
            self.widgets_list.append(delete_smart_home_button)

        self.win.geometry(f"{self.window_width}x{(self.window_height // 2) + (count_smart_homes * 38)}")

    def add_smart_home(self):
        add_win = Toplevel(self.win)
        smart_home_app_object = SmartHomeApp(add_win)
        
        smart_home_app_object.update_parent_win = self.create_widgets
        smart_home_app_object.create_widgets()
        
        smart_home_name = f"Smart Home {self.next_smart_home_id}"
        self.next_smart_home_id += 1
        
        # create new dictionary entry
        self.smart_homes_dict[smart_home_name] = [smart_home_app_object, []]
        self.create_widgets()

    def remove_smart_home(self, smart_home_name):
        del self.smart_homes_dict[smart_home_name]
        self.create_widgets()

    def modify_smart_home(self, smart_home_name):
        modify_win = Toplevel(self.win)
        x_position, y_position = SmartHomeApp.calc_centre_of_screen(self)
        modify_win.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")

        # temporarily store the SmartHome from the current SmartHomeApp
        smart_home_app_object = self.smart_homes_dict[smart_home_name][0]
        temp_smart_home = smart_home_app_object.smart_home
        
        # create a new SmartHomeApp with the same smart home data
        new_app = SmartHomeApp(modify_win)
        new_app.smart_home = temp_smart_home 
        
        # update the parent window
        new_app.update_parent_win = self.create_widgets
        new_app.create_widgets()
        
        # update the dictionary so it points to the new SmartHomeApp object
        self.smart_homes_dict[smart_home_name][0] = new_app
    
    def delete_all_smart_home_widgets(self):
        for widget in self.widgets_list:
            widget.destroy()
        self.widgets_list = []

    def load_save(self):
        file_name = askopenfilename(filetypes=[("CSV files only", "*.csv")])
        if not file_name:
            return
        
        self.smart_homes_dict = {}

        file = open(file_name, "r")
        max_id_seen = 0
        new_win = Toplevel()
        new_win.withdraw()

        for line in file:
            smart_home_data = line.strip().split(",")
            smart_home_name = smart_home_data[0]
            max_items = int(smart_home_data[1])
            
            smart_home = SmartHome(max_items)
            smart_home_app_object = SmartHomeApp(new_win)
            smart_home_app_object.smart_home = smart_home
            
            smart_home_id = int(smart_home_name.split()[-1])
            if smart_home_id > max_id_seen:
                max_id_seen = smart_home_id
            
            i = 2
            while i + 2 < len(smart_home_data):
                device_type = smart_home_data[i]
                if smart_home_data[i+1] == "True":
                    device_state = True
                elif smart_home_data[i+1] == "False":
                    device_state = False
                
                device_value = smart_home_data[i+2]
                if device_type == "SmartPlug":
                    device = SmartPlug(int(device_value))
                elif device_type == "SmartTV":
                    device = SmartTV()
                    device.channel = int(device_value)
                elif device_type == "SmartWashingMachine":
                    device = SmartWashingMachine()
                    device.wash_mode = device_value
                
                device.switched_on = device_state
                smart_home.add_device(device)
                i += 3
            
            self.smart_homes_dict[smart_home_name] = [smart_home_app_object,[]]
            
        smart_home_app_object.update_parent_win = self.create_widgets
        self.next_smart_home_id = max_id_seen + 1
        self.create_widgets()
        file.close()

    def save_state(self):
        file_name = asksaveasfilename(defaultextension=".csv")
        if not file_name:
            return
        file = open(file_name, "w")
        
        for smart_home_name in self.smart_homes_dict:
            smart_home = self.smart_homes_dict[smart_home_name][0].smart_home
            values = [smart_home_name, str(smart_home.max_items)]

            for device in smart_home.devices:
                device_type = type(device).__name__
                device_state = device.switched_on

                if device_type == "SmartPlug":
                    device_value = str(device.consumption_rate)
                elif device_type == "SmartTV":
                    device_value = str(device.channel)
                elif device_type == "SmartWashingMachine":
                    device_value = device.wash_mode
                
                values.append(device_type)
                values.append(str(device_state))
                values.append(str(device_value))

            line = ",".join(values)
            file.write(line + "\n")
        
        file.close()


def main():
    app = SmartHomesApp()
    app.run()

main()