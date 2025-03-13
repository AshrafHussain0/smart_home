class SmartDevice:
    
    def __init__(self):
        self._switched_on = False
    
    @property
    def switched_on(self):
        return self._switched_on
    
    @switched_on.setter
    def switched_on(self, value: bool):
        self._switched_on = value
    
    def toggle_switch(self):
        self.switched_on = not self.switched_on
    
    def __str__(self):
        state = "on" if self._switched_on else "off"
        return state


class SmartPlug(SmartDevice):
    
    def __init__(self, consumption_rate=0):
        super().__init__()
        if 0 <= consumption_rate <= 150:
            self._consumption_rate = consumption_rate
        else:
            raise ValueError("Consumption rate must be between 0 and 150")
    
    @property
    def consumption_rate(self):
        return self._consumption_rate
    
    @consumption_rate.setter
    def consumption_rate(self, value):
        if 0 <= value <= 150:
            self._consumption_rate = value
        else:
            raise ValueError("Consumption rate must be between 0 and 150")
            
    def __str__(self):
        state = super().__str__()
        return f"SmartPlug is {state} with a consumption rate of {self.consumption_rate}"


class SmartTV(SmartDevice):
    
    def __init__(self):
        super().__init__()
        self._channel = 1

    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self, value):
        if 1 <= value <= 734:
            self._channel = value
        else:
            raise ValueError("Channel number must be between 1 and 734")
            
    def __str__(self):
        state = super().__str__()
        return f"SmartTV is {state}, channel number {self._channel}"


class SmartWashingMachine(SmartDevice):
    
    valid_wash_modes = {
        "Daily wash",
        "Quick wash",
        "Eco",
    }

    def __init__(self):
        super().__init__()
        self._wash_mode = "Daily wash"

    @property
    def wash_mode(self):
        return self._wash_mode
    
    @wash_mode.setter
    def wash_mode(self, value):
        if value.capitalize() in self.valid_wash_modes:
            self._wash_mode = value.capitalize()
        else:
            output = ""
            for mode in self.valid_wash_modes:
                output += f"'{mode}', "
            raise ValueError(f"Wash mode must be one of: {output}")

    def __str__(self):
        state = super().__str__()
        return f"SmartWashingMachine is {state} with wash mode: {self.wash_mode}"


class SmartHome:
    
    def __init__(self, max_items=5):
        self._devices = []
        self._max_items = max_items
    
    @property
    def devices(self):
        return self._devices
    
    @property
    def max_items(self):
        return self._max_items
    
    @max_items.setter
    def max_items(self, value: int):
        self._max_items = value

    def add_device(self, device):
        if len(self.devices) >= self.max_items:
            raise ValueError(f"Maximum number of devices reached for this SmartHome: {self.max_items}")
        if isinstance(device, SmartDevice):
            self.devices.append(device)
        else:
            raise ValueError("Must be an object that inherits SmartDevice")
    
    def remove_device(self, index):
        if 0 <= index < len(self.devices):
            del self.devices[index]
        else:
            raise IndexError("Invalid index! Out of range")

    def get_device(self, index):
        if 0 <= index < len(self.devices):
            return self.devices[index]
        else:
            raise IndexError("Invalid index! Out of range")
        
    def toggle_device(self, index):
        device = self.get_device(index)
        device.toggle_switch()
        
    def switch_all_on(self):
        for device in self.devices:
            device.switched_on = True
    
    def switch_all_off(self):
        for device in self.devices:
            device.switched_on = False

    def update_option(self, index, value):
        if index < 0 or index >= len(self.devices):
            raise IndexError("Invalid index! Out of range")
        
        device = self.get_device(index)
        
        if isinstance(device, SmartPlug):
            if type(value) != int:
                raise TypeError("Consumption rate must be an integer")
            device.consumption_rate = value
        
        elif isinstance(device, SmartTV):
            if type(value) != int:
                raise TypeError("Channel number must be an integer")
            device.channel = value

        elif isinstance(device, SmartWashingMachine):
            if type(value) != str:
                raise TypeError("Wash mode must be a string")
            device.wash_mode = value
        else:
            raise ValueError("Wrong device type or update option")

    def attempt_conversion_to_int(self, value):
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            return e
    
    def input_validation(self, device_type, value):
        device = None
        int_value = self.attempt_conversion_to_int(value)
        
        if device_type == "SmartWashingMachine":
            device = SmartWashingMachine()
            device.wash_mode = value.lower()
            return device

        elif device_type == "SmartTV":
            if not isinstance(int_value, int):
                raise TypeError("Channel number must be a valid integer")
            try:
                device = SmartTV()
                device.channel = int_value
            except ValueError as e:
                raise e
            return device

        elif device_type == "SmartPlug":
            if not isinstance(int_value, int):
                raise TypeError("Consumption rate must be an integer")
            try:
                device = SmartPlug()
                device.consumption_rate = int_value
            except ValueError as e:
                raise e
            return device
            


    def __str__(self):
        output = f"SmartHome with {len(self.devices)} device(s): \n"
        for i in range(len(self.devices)):
            output += f"{i+1}- {self.devices[i]} \n"
            i += 1
        return output


def test_smart_plug():
    print("Creating SmartPlug with consumption rate 45:")
    plug = SmartPlug(45)
    print(plug), print()
    
    print("Toggling the SmartPlug:")
    plug.toggle_switch()
    print(plug), print()
    
    print("Changing consumption rate to 75:")
    plug.consumption_rate = 75
    print(plug), print()
    
    print("Toggling the SmartPlug:")
    plug.toggle_switch()
    print(plug), print()
    
    print("Testing setting consumption rate to -10:")
    try:
        plug.consumption_rate = -10 # Invalid
    except ValueError as e:
        print(f"Error: {e}"), print()

    print("Testing setting consumption rate to 200:")
    try:
        plug.consumption_rate = 200 # Invalid
    except ValueError as e:
        print(f"Error: {e}"), print()
    
    print("Testing creation of SmartPlug with consumption rate -5:")
    try:
        plug_1 = SmartPlug(-5) # Invalid
    except ValueError as e:
        print(f"Error: {e}"), print()
    
    print("Testing creation of SmartPlug with consumption rate 160:")
    try:
        plug_2 = SmartPlug(160) # Invalid
    except ValueError as e:
        print(f"Error: {e}"), print()


def test_custom_device():
    print("Creating a SmartTV:")
    tv = SmartTV()
    print(tv), print()
    
    print("Toggling the SmartTV:")
    tv.toggle_switch()
    print(tv), print()

    print("Testing setting channel to 5:")
    try:
        tv.channel = 5 # Valid
        print(tv)
    except ValueError as e:
        print(f"Error: {e}")
    print()

    print("Testing setting channel to 800:")
    try:
        tv.channel = 800 # Invalid
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    print("Creating a SmartWashingMachine:")
    washing_machine = SmartWashingMachine()
    print(washing_machine), print()
    
    print("Toggling the SmartWashingMachine:")
    washing_machine.toggle_switch()
    print(washing_machine), print()

    print("Testing setting wash mode to 'Eco':")
    try:
        washing_machine.wash_mode = "Eco" # Valid
        print(washing_machine)
    except ValueError as e:
        print(f"Error: {e}")
    print()

    print("Testing setting wash mode to 'Wash and Dry':")
    try:
        washing_machine.wash_mode = "Wash and Dry" # Invalid
    except ValueError as e:
        print(f"Error: {e}")
    print()


def test_smart_home():

    plug = SmartPlug(120)
    tv = SmartTV()
    washing_machine = SmartWashingMachine()

    home = SmartHome(max_items=3)

    home.add_device(plug)
    home.add_device(tv)
    home.add_device(washing_machine)
    print(home)

    retrieved_plug = home.get_device(0)
    retrieved_tv = home.get_device(1)
    retrieved_washing_machine = home.get_device(2)
    print("Testing the get_device method:")
    print(f"Retrieved: {retrieved_plug}")
    print(f"Retrieved: {retrieved_tv}")
    print(f"Retrieved: {retrieved_washing_machine}")
    print()
    
    home.toggle_device(0)
    home.toggle_device(1)
    home.toggle_device(2)
    print("After toggling all devices individually:")
    print(home)
    
    try:
        home.toggle_device(-1)
    except (ValueError, TypeError, IndexError) as e:
        print("After trying to toggle the device in index -1:")
        print(f"Error: {e}"), print()
    print(home)

    home.switch_all_on()
    print("After switching all devices on:")
    print(home)
    
    home.switch_all_off()
    print("After switching all devices off:")
    print(home)
    
    home.update_option(0, 150)
    home.update_option(1, 734)
    home.update_option(2, "Eco")
    print("After updating options:")
    print(home)

    print("Checking if out-of-range values will raise exceptions:")
    try:
        home.update_option(0, 200) # Invalid value
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    
    try:
        home.update_option(1, 800) # Invalid value
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")

    try:
        home.update_option(2, "Wash and Dry") # Invalid value
    except (ValueError, TypeError) as e:
        print(f"Error: {e}"), print()
    print(home)
    
    home.remove_device(2)
    print("After removing SmartWashingMachine:")
    print(home)
    
    try:
        home.remove_device(-1) # Invalid index
    except (ValueError, TypeError, IndexError) as e:
        print("Successfully blocked -1 as index:")
        print(f"Error: {e}")
    print()
        
    print(f"Testing maximum devices ({home.max_items}) reached: ")
    try:
        home.add_device(washing_machine)
        home.add_device(washing_machine)
    except ValueError as e:
        print(f"Error: {e}")
    print()


#test_smart_plug()
#test_custom_device()
#test_smart_home()