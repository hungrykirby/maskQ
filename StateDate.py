import string

dict_number_0_rl = {
    "right":"plus",
    "left":"???"
}

dict_number_is_surprised = {
    "0":"plus",
    "1":"minus"
}

list_normal_smile_1 = {
    "words":{
        #dict_words
    }
} #smile == true 各機能の詳細へと移行する

list_normal_smile_0 = [
    "number", "words", "move", "delete", "read"
] #smile == false modeを変更する

list_symbols = [" ", "\n",'"', "(", ")", "'", "_"]
list_symbols_calc = ["+", "-", "*", "/", "%"]

def add_loop_max(_input, _max):
    if _input < _max - 1:
        return _input + 1
    else:
        return 0

def substract_loop_min(_input, _max):
    if _input > 0:
        return _input - 1
    else:
        return _max - 1

class State():
    counter = 0
    mode = 0 #現在のモードの添え字
    frames_define_mode = 3
    list_counters = [0 for n in range(frames_define_mode)]
    list_modes = [0 for n in range(frames_define_mode)]
    list_commands = ["normal" for n in range(frames_define_mode)] #normalが連続で来たら補正しない
    modes = {
        "change":True,
        "addition":False #普通の入力ではなく、特別な入力
    }
    all_data = ""

    def __init__(self):
        print("initialized")

    def change_modes(self, state):
        is_smile = state["smile"]
        is_surprised = state["surprised"]
        is_normal = state["normal"]
        if is_smile:
            if self.modes["change"] == True:
                self.counter = 0
            else:
                #all_data = str(self.counter)
                self.counter = 0
            self.modes["change"] = not self.modes["change"]
            #self.counter = 0
            #self.all_data = self.all_data + all_data
            #self.list_normals.append(False)
        if is_surprised:
            self.modes["addition"] = not self.modes["addition"]
            #self.list_normals.append(False)
            #self.counter = 0
        if is_normal:
            output_num = self.counter

    def change_mode_index_counter(self, command):
        is_change = self.modes["change"]
        is_addition = self.modes["addition"]
        m = self.mode
        result = None
        print("counter", self.counter, "mode", list_normal_smile_0[m])
        print("Change Mode", is_change, "Additional Mode", is_addition)
        print("all result:", self.all_data)
        self.list_commands.append(command)
        if len(self.list_commands) > self.frames_define_mode:
            self.list_commands.pop(0)
            self.list_modes.pop(0)
            self.list_counters.pop(0)
        self.list_modes.append(m)
        self.list_counters.append(self.counter)

        #決定するところ
        pre_command = self.list_commands[len(self.list_commands) - 2]
        if not pre_command == "normal" and self.list_commands[len(self.list_commands) - 1] == "normal":
            self.counter = self.list_counters[0]
            m = self.list_modes[0]
            if not is_change:
                if m == 0:
                    result = self.counter
                elif m == 1:
                    if not is_addition:
                        if pre_command == "right":
                            str_lu = string.ascii_lowercase
                            result = str_lu[abs(self.counter)]
                        elif pre_command == "left":
                            str_lu = string.ascii_uppercase
                            result = str_lu[abs(self.counter)]
                    else:
                        #symbols = None
                        if pre_command == "right":
                            symbols = list_symbols[self.counter]
                            result = str(symbols)
                        elif pre_command == "left":
                            symbols = list_symbols_calc[self.counter]
                            result = str(symbols)
                else:
                    pass

                self.counter = 0
                pre_face = self.list_commands[len(self.list_commands) - 2]
                if not result == None and not (pre_face == "smile" or pre_face == "surprised"):
                    self.all_data = self.all_data + str(result)
        #決定するところ

        #いろいろ
        if is_change == True:
            if command == "right":
                m = add_loop_max(m, len(list_normal_smile_0))
            elif command == "left":
                m = substract_loop_min(m, len(list_normal_smile_0))
            self.mode = m
        elif is_change == False:
            if is_addition == False:
                if command == "right":
                    if m == 0: #number
                        self.counter = self.counter + 1
                    elif m == 1:
                        s = string.ascii_lowercase
                        self.counter = add_loop_max(self.counter, len(s))
                    else:
                        pass
                elif command == "left":
                    if m == 0:
                        self.counter = self.counter - 1
                    elif m == 1:
                        s = string.ascii_uppercase
                        self.counter = add_loop_max(self.counter, len(s))
                    elif m == 2:
                        pass
                    elif m == 3:
                        if len(all_data) > 0:
                            self.all_data = self.all_data[0:len(self.all_data) - 1]
                    else:
                        pass
            elif is_addition == True:
                if command == "right":
                    if m == 0:
                        self.counter = self.counter + 10
                    elif m == 1:
                        self.counter = add_loop_max(self.counter, len(list_symbols))
                    else:
                        pass
                elif command == "left":
                    if m == 0:
                        self.counter = self.counter - 10
                    elif m == 1:
                        self.counter = add_loop_max(self.counter, len(list_symbols_calc))
                    else:
                        pass
