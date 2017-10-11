import collections

import config
import StateDate

states_list = []
len_max_list = 2
len_all_state = 1000
from_define_state = 70 #100フレーム後から判定を始める

counter = 0 #global left right

mode_list = ["no input", "words", "number", "others", "move", "delete", "read"]
command_list = ["normal", "smile", "surprised", "right", "left"]
add_modes_count = len(mode_list)
state_face = {
    "smile": False,
    "surprised": False,
    "normal": True,
}

st = StateDate.State()

def detect_face_state(predict):
    global counter
    if len(states_list) > len_all_state:
        #states_list.pop(0)
        #states_list.clear()
        del(states_list[0:from_define_state])
    states_list.append(predict)
    _sum = 0
    if len(states_list) == len_all_state:
        count_dict = collections.Counter(states_list[len(states_list) - from_define_state:len(states_list) - 1])
        #print(count_dict, states_list[len(states_list) - from_define_state:len(states_list) - 1])
        #define_count_dict = collections.Counter(states_list[-1:-from_define_state])
        command_num = count_dict.most_common(1)[0][0]
        command = command_list[command_num]
        '''
        連続でsmileやsurprisedが出る確率は低そう
        '''
        #
        pre_state_face = st.history_commands[len(st.history_commands) - 1]
        if command == "smile" or command == "surprised":
            if command == pre_state_face:
                command = "normal"
        #
        one_bool(command)
        #print(state_face, command)
        st.change_modes(state_face)
        st.change_mode_index_counter(command)

def one_bool(command):
    if command != "right" and command != "left":
        for sf in state_face:
            state_face[sf] = False
        if command in state_face.keys():
            state_face[command] = True
        #print(state_face)

my_round=lambda x:(x*2+1)//2
