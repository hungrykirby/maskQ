import string

import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

list_predict_words = ["print", "if", "for" ,"in", "range"]
list_modes = [
    "number", "words", "symbols", "move", "delete", "read"
] #smile == false modeを変更する

list_symbols = [" ", "\n",'"', "(", ")", "'", "_", ";", ":"]
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
    frames_history = 3
    history_outputs = ["" for n in range(frames_history)]
    history_counters = [0 for n in range(frames_history)]
    history_modes = [0 for n in range(frames_history)]
    history_commands = ["normal" for n in range(frames_history)] #normalが連続で来たら補正しない
    modes = {
        "change":True,
        "addition":False #普通の入力ではなく、特別な入力
    }
    all_data = ""
    single_word = ""
    #改行、タブ、空白、コンマで全文に組み込まれるやつ

    #one_word = ""
    predicted_word = ""

    list_detail_predict = []

    frame_fetch_history_counter = 1


    client = None

    def __init__(self):
        '''
        OSC
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1",
            help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=12345,
            help="The port the OSC server is listening on")
        args = parser.parse_args()

        self.client = udp_client.UDPClient(args.ip, args.port)

        parser1 = argparse.ArgumentParser()
        parser1.add_argument("--ip", default="127.0.0.1",
            help="The ip of the OSC server")
        parser1.add_argument("--port", type=int, default=12346,
            help="The port the OSC server is listening on")
        args1 = parser1.parse_args()

        self.client1 = udp_client.UDPClient(args1.ip, args1.port)

        print("initialized")

    def convert_not_null(self, _input):
        if _input is None or _input == "":
            return "No data here"
        return _input

    def define_read_part(self, command, m, result, ot, is_change, is_addition):
        #if command is None:
        #    return
        read_part = []
        if not self.history_commands[len(self.history_commands) - 1] == command:
            read_part = [command]
        if is_change:
            read_part.append(list_modes[m])
        else:
            if command == "surprised":
                if is_addition:
                    read_part.append("special")
                else:
                     read_part.append("normal")
            elif command == "right" or command == "left":
                if result is None or result == "" or result == None:
                    if not ot is None:
                        read_part.append(ot)
                else:
                    read_part.append(str(result))
        if read_part == []:
            read_part = [self.single_word]
            if read_part == []:
                read_part = [self.all_data]
                if read_part == []:
                    read_part = ["No read part"]

        print(read_part)
        return read_part


    def osc_send(self, command, m, result, ot, is_change, is_addition, read):
        msg = []

        msg.append(osc_message_builder.OscMessageBuilder(address = "/command"))
        msg[0].add_arg(self.convert_not_null(command))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/mode"))
        msg[1].add_arg(self.convert_not_null(m))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/result"))
        if result is None or result == "":
            msg[2].add_arg(self.convert_not_null(str(ot)))
        else:
            msg[2].add_arg(self.convert_not_null(result))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/word"))
        msg[3].add_arg(self.convert_not_null(self.single_word))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/all"))
        msg[4].add_arg(self.convert_not_null(self.all_data))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/change"))
        msg[5].add_arg(self.convert_not_null(is_change))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/addition"))
        msg[6].add_arg(self.convert_not_null(is_addition))

        msg.append(osc_message_builder.OscMessageBuilder(address = "/read"))
        msg[7].add_arg(self.convert_not_null(read))

        for m in msg:
            _m = m.build()
            if not self.client is None:
                self.client.send(_m)

        return True

    def osc_read(self, read):
        msg = osc_message_builder.OscMessageBuilder(address = "/read")
        for r in read:
            if not r == "":
                msg.add_arg(r)

        msg = msg.build()
        self.client1.send(msg)

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

    def symbol2display(self, symbol):
        '''
        記号による出力を行う
        return_strはotとして表示に用いられるもの
        '''
        return_str = ""
        if symbol == "\n":
            return_str = "Enter"
        elif symbol == " ":
            return_str = "Space"
        elif symbol == "\t":
            return_str == "Tab"
        else:
            return_str = symbol
        return return_str

    def define_word(self, symbol):
        '''
        記号によってはsingle_wordをall_dataに渡す
        '''
        result = None
        # TODO:もっときれいにできるよね
        if symbol in ["\n", ";", " ", "\t", "'", '"', "(", ")"]:
            self.all_data = self.all_data + self.single_word + symbol
            self.single_word = ""
        elif symbol in list_symbols_calc:
            self.all_data = self.all_data + symbol
            self.single_word = ""
        else:
            #self.single_word = self.single_word + symbol
            result = symbol
        return result


    def delete_last_word(self):
        ot = None
        if len(self.single_word) > 0:
            ot = self.single_word[-1] + " is deleted"
            self.single_word = self.single_word[0:len(self.single_word) - 1]
        elif len(self.all_data) > 0:
            ot = self.all_data[-1] + " is deleted"
            self.all_data = self.all_data[0:len(self.all_data) - 1]
        else:
            ot = "not enough length for delete"

        return ot

    def change_mode_index_counter(self, command):
        is_change = self.modes["change"]
        is_addition = self.modes["addition"]
        m = self.mode
        result = None
        ot = None
        osc_out = None
        c = 0

        h_c = self.history_commands[len(self.history_commands) - 1]
        is_same_now_past = command == h_c
        has_normal = (command == "normal" or h_c == "normal")
        is_right_left = command == "right" and h_c == "left"
        is_left_right = command == "left" and h_c == "right"
        if not has_normal and not is_same_now_past and not is_right_left and not is_left_right:
            print("normalをふくまない重複コマンドが実行されました")
            return

        #
        if command == "smile":
            self.modes["addition"] = False
        #笑顔の時は追加モードを解除する

        if is_change:
            self.counter = 0
            if command == "right":
                m = add_loop_max(m, len(list_modes))
            elif command == "left":
                m = substract_loop_min(m, len(list_modes))
            elif command == "normal":
                pre_command = self.history_commands[len(self.history_commands) - 1]
                if pre_command == "right" or pre_command == "left":
                    m = self.history_modes[1]
                #elif pre_command == "smile":
                #    self.all_data = self.all_data + self.single_word
                #    self.single_word = ""
        else: #変更モードではない
            #m = self.history_modes[len(self.history_modes) - 2]
            c = self.counter
            if m == 0:
                '''
                現在のモードが数字の時
                '''
                pre_command = self.history_commands[len(self.history_commands) - 1]
                if not is_addition: #not 追加モードの時
                    if command == "right":
                        c = c + 1
                        ot = str(c)
                    elif command == "left":
                        c = c - 1
                        ot = str(c)
                    elif command == "normal" and (pre_command == "right" or pre_command == "left"):
                        result = self.history_counters[self.frame_fetch_history_counter]
                        result = str(result)
                        ot = str(self.history_counters[self.frame_fetch_history_counter]) + " is setted"
                        c = 0
                else:
                    if command == "right":
                        c = c + 10
                        ot = str(c)
                    elif command == "left":
                        c = c - 10
                        ot = str(c)
                    elif command == "normal" and (pre_command == "right" or pre_command == "left"):
                        result = self.history_counters[self.frame_fetch_history_counter]
                        result = str(result)
                        ot = str(self.history_counters[self.frame_fetch_history_counter]) + " is setted"
                        c = 0

            elif m == 1:
                '''
                現在のモードが文字
                '''
                if not is_addition:
                    if command == "right":
                        #大文字入力
                        s = string.ascii_uppercase
                        c = add_loop_max(c, len(s))
                        ot = s[c]
                    elif command == "left":
                        #小文字力
                        s = string.ascii_lowercase
                        c = add_loop_max(c, len(s))
                        ot = s[c]
                    elif command == "normal":
                        #決定
                        pre_command = self.history_commands[len(self.history_commands) - 1]
                        c = self.history_counters[self.frame_fetch_history_counter]
                        if pre_command == "right":
                            #
                            #大文字決定
                            #
                            result = string.ascii_uppercase[c]
                            ot = string.ascii_uppercase[c] + " is setted"
                        elif pre_command == "left":
                            #
                            #小文字決定
                            #
                            result = string.ascii_lowercase[c]
                            ot = string.ascii_lowercase[c] + " is setted"
                        c = 0
                else:
                    if command == "right":
                        #予測変換
                        for l in list_predict_words:
                            if len(l) >= len(self.single_word): #ここをall_dataじゃなくす
                                if self.single_word == l[0:len(self.single_word)]:
                                    #print("predict", l)
                                    self.list_detail_predict.append(l)
                        if len(self.list_detail_predict) > 0:
                            c = add_loop_max(c, len(self.list_detail_predict))
                            ot = self.list_detail_predict[c]
                    elif command == "left":
                        #削除
                        ot = "Delete Mode"
                    elif command == "normal":
                        #決定
                        pre_command = self.history_commands[len(self.history_commands) - 1]
                        c = self.history_counters[self.frame_fetch_history_counter]
                        if pre_command == "right":
                            #
                            #予測変換
                            #
                            if len(self.list_detail_predict) > 0:
                                self.predicted_word = self.list_detail_predict[c]
                                ot = self.list_detail_predict[c] + " is setted"
                                self.single_word = ""
                            else:
                                ot = "no possible word"
                        elif pre_command == "left":
                            #
                            #文字削除
                            #
                            ot = self.delete_last_word()
                        c = 0
            elif m == 2:
                '''
                現在のモードが記号
                '''
                if not is_addition:
                    if command == "right":
                        #計算以外の記号
                        c = add_loop_max(c, len(list_symbols))
                        ot = self.symbol2display(list_symbols[c])
                    elif command == "left":
                        #計算記号
                        c = add_loop_max(c, len(list_symbols_calc))
                        ot = self.symbol2display(list_symbols_calc[c])
                    elif command == "normal":
                        #
                        #決定
                        #
                        pre_command = self.history_commands[len(self.history_commands) - 1]
                        c = self.history_counters[self.frame_fetch_history_counter]
                        if pre_command == "right":
                            #
                            #計算以外の記号の決定
                            #
                            #self.single_word = list_symbols[c]
                            result = self.define_word(list_symbols[c])
                            ot = self.symbol2display(list_symbols[c]) + " is setted"
                        elif pre_command == "left":
                            #
                            #計算記号の決定
                            #
                            result = self.define_word(list_symbols_calc[c])
                            ot = self.symbol2display(list_symbols_calc[c]) + " is setted"
                        c = 0
                else:
                    if command == "right":
                        pass
                    elif command == "left":
                        ot = "Delete Mode"
                    elif command == "normal":
                        pre_command = self.history_commands[len(self.history_commands) - 1]
                        c = self.history_counters[self.frame_fetch_history_counter]
                        if pre_command == "right":
                            pass
                        elif pre_command == "left": #文字削除
                            ot = self.delete_last_word()
                        c = 0
            elif m == 3:
                pass
            elif m == 4:
                pass

        if self.predicted_word == "":
            if not result is None and len(str(result)) > 0:
                self.single_word = self.single_word + str(result)
        else:
            self.all_data = self.all_data + self.predicted_word
            self.predicted_word = ""

        if is_change:
            print("現在のコマンド:", command, " Mode:", list_modes[m])
        else:
            print("入力される単語:", ot)
            print("現在入力中の単語:", self.single_word)
            if is_addition:
                print("追加モード")
            else:
                print("標準モード")
        print("記載された全コード", self.all_data)
        print("----------")

        read_contents = self.define_read_part(command, m, result, ot, is_change, is_addition)
        if read_contents is not None or not read_contents == []:
            self.osc_send(command, m, result, ot, is_change, is_addition, "".join(read_contents))
        self.osc_read(read_contents)

        self.history_commands.append(command)
        if len(self.history_commands) > self.frames_history:
            self.history_commands.pop(0)
            self.history_modes.pop(0)
            self.history_counters.pop(0)
        self.history_modes.append(m)
        self.history_counters.append(c)

        self.counter = c
        self.mode = m
