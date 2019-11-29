# -*- coding: utf-8 -*-
"""MultiPlayer-Doom.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OUfcId6uCIBPTb0yRH_HbODNiRxZhprn

#Setup
"""

# !pip install --upgrade torch

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# # Install deps from
# # https://github.com/mwydmuch/ViZDoom/blob/master/doc/Building.md#-linux
#
# apt-get update
# apt-get install build-essential zlib1g-dev libsdl2-dev libjpeg-dev \
# nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev \
# libopenal-dev timidity libwildmidi-dev unzip
# apt-get install libboost-all-dev
# apt-get install liblua5.1-dev
# pip install vizdoom

"""## Change cfg

### cig.cfg
"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile /usr/local/lib/python3.6/dist-packages/vizdoom/scenarios/cig.cfg
# # Lines starting with # are treated as comments (or with whitespaces+#).
# # It doesn't matter if you use capital letters or not.
# # It doesn't matter if you use underscore or camel notation for keys, e.g. episode_timeout is the same as episodeTimeout.
#
# doom_scenario_path = deathmatch_shotgun.wad
#
# #12 minutes
# episode_timeout = 25200
#
# # Rendering options
# screen_resolution = RES_640X480
# screen_format = CRCGCB
# render_hud = true
# render_crosshair = true
# render_weapon = true
# render_decals = false
# render_particles = false
#
# window_visible = true
#
# # Available buttons
# available_buttons =
# 	{
# 		ATTACK
# 		USE
#
# 		TURN_LEFT
# 		TURN_RIGHT
# 		MOVE_RIGHT
# 		MOVE_LEFT
# 		MOVE_FORWARD
# 		MOVE_BACKWARD
#
# 		TURN_LEFT_RIGHT_DELTA
# 		LOOK_UP_DOWN_DELTA
# 	}
#
# mode = ASYNC_PLAYER

"""### bots.cfg"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile /usr/local/lib/python3.6/dist-packages/vizdoom/bots.cfg
# {
#     name        Rambo
#     aiming      67
#     perfection  50
#     reaction    70
#     isp         50
#     color       "40 cf 00"
#     skin        base
#     //weaponpref    012385678
# }
#
# {
#     name        McClane
#     aiming      34
#     perfection  75
#     reaction    15
#     isp         90
#     color       "b0 b0 b0"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        MacGyver
#     aiming      80
#     perfection  67
#     reaction    72
#     isp         87
#     color       "50 50 60"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Plissken
#     aiming      15
#     perfection  50
#     reaction    50
#     isp         50
#     color       "8f 00 00"
#     skin        base
#     //weaponpref    082345678
# }
#
# {
#     name        Machete
#     aiming      50
#     perfection  13
#     reaction    20
#     isp         100
#     color       "ff ff ff"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Anderson
#     aiming      45
#     perfection  30
#     reaction    70
#     isp         60
#     color       "ff af 3f"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Leone
#     aiming      56
#     perfection  34
#     reaction    78
#     isp         50
#     color       "bf 00 00"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Predator
#     aiming      25
#     perfection  55
#     reaction    32
#     isp         70
#     color       "00 00 ff"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Ripley
#     aiming      61
#     perfection  50
#     reaction    23
#     isp         32
#     color        "00 00 7f"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        T800
#     aiming      90
#     perfection  85
#     reaction    10
#     isp         30
#     color       "ff ff 00"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Dredd
#     aiming      12
#     perfection  35
#     reaction    56
#     isp         37
#     color       "40 cf 00"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Conan
#     aiming      10
#     perfection  35
#     reaction    10
#     isp         100
#     color       "b0 b0 b0"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Bond
#     aiming      67
#     perfection  15
#     reaction    76
#     isp         37
#     color       "50 50 60"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Jones
#     aiming      52
#     perfection  35
#     reaction    50
#     isp         37
#     color       "8f 00 00"
#     skin        base
#     //weaponpref    012345678
# }
#
# {
#     name        Blazkowicz
#     aiming      80
#     perfection  80
#     reaction    80
#     isp         100
#     color       "00 00 00"
#     skin        base
#     //weaponpref    012345678
# }

"""### deathmatch_shotgun.wad"""

# !cp /content/gdrive/My\ Drive/Doom/deathmatch_shotgun.wad /usr/local/lib/python3.6/dist-packages/vizdoom/scenarios/deathmatch_shotgun.wad

"""## Import"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import pandas as pd
import numpy as np
from vizdoom import *        # Doom Environment
import random
import time
from skimage import transform
from collections import deque
import matplotlib.pyplot as plt
import cv2
from collections import OrderedDict
import vizdoom as vzd
import pickle
from tqdm import tqdm

"""## Clone"""

# !git clone https://github.com/glample/Arnold.git
# !git clone https://github.com/mwydmuch/ViZDoom.git

# """## Mount Save Folder"""

# from google.colab import drive
# drive.mount('/content/gdrive')
save_folder = './host/'

"""# Action Mappings"""

mapping_action = [[False, False, False, False, False, False, True, True, False], [False, False, True, False, False, False, False, True, False], [False, False, True, False, False, False, True, True, False], [False, False, False, True, False, False, False, True, False], [False, False, False, True, False, False, True, True, False], [True, False, False, False, False, False, False, True, False], [True, False, False, False, False, False, True, True, False], [True, False, True, False, False, False, False, True, False], [True, False, True, False, False, False, True, True, False], [True, False, False, True, False, False, False, True, False], [True, False, False, True, False, False, True, True, False], [False, True, False, False, False, False, False, True, False], [False, True, False, False, False, False, True, True, False], [False, True, True, False, False, False, False, True, False], [False, True, True, False, False, False, True, True, False], [False, True, False, True, False, False, False, True, False], [False, True, False, True, False, False, True, True, False], [False, False, False, False, True, False, False, True, False], [False, False, False, False, True, False, True, True, False], [False, False, True, False, True, False, False, True, False], [False, False, True, False, True, False, True, True, False], [False, False, False, True, True, False, False, True, False], [False, False, False, True, True, False, True, True, False], [False, False, False, False, False, True, False, True, False], [False, False, False, False, False, True, True, True, False], [False, False, True, False, False, True, False, True, False], [False, False, True, False, False, True, True, True, False], [False, False, False, True, False, True, False, True, False], [False, False, False, True, False, True, True, True, False]]
iden = np.eye(9)
keys = {'MOVE_FORWARD':0, 'MOVE_BACKWARD':1, 'TURN_LEFT':2, 'TURN_RIGHT':3, 'MOVE_LEFT':4, 'MOVE_RIGHT':5, 'ATTACK':6, 'SPEED':7, 'CROUCH':8}
mapping = [['ATTACK'],
['TURN_LEFT'],
['TURN_LEFT', 'ATTACK'],
['TURN_RIGHT'],
['TURN_RIGHT', 'ATTACK'],
['MOVE_FORWARD'],
['MOVE_FORWARD', 'ATTACK'],
['MOVE_FORWARD', 'TURN_LEFT'],
['MOVE_FORWARD', 'TURN_LEFT', 'ATTACK'],
['MOVE_FORWARD', 'TURN_RIGHT'],
['MOVE_FORWARD', 'TURN_RIGHT', 'ATTACK'],
['MOVE_BACKWARD'],
['MOVE_BACKWARD', 'ATTACK'],
['MOVE_BACKWARD', 'TURN_LEFT'],
['MOVE_BACKWARD', 'TURN_LEFT', 'ATTACK'],
['MOVE_BACKWARD', 'TURN_RIGHT'],
['MOVE_BACKWARD', 'TURN_RIGHT', 'ATTACK'],
['MOVE_LEFT'],
['MOVE_LEFT', 'ATTACK'],
['MOVE_LEFT', 'TURN_LEFT'],
['MOVE_LEFT', 'TURN_LEFT', 'ATTACK'],
['MOVE_LEFT', 'TURN_RIGHT'],
['MOVE_LEFT', 'TURN_RIGHT', 'ATTACK'],
['MOVE_RIGHT'],
['MOVE_RIGHT', 'ATTACK'],
['MOVE_RIGHT', 'TURN_LEFT'],
['MOVE_RIGHT', 'TURN_LEFT', 'ATTACK'],
['MOVE_RIGHT', 'TURN_RIGHT'],
['MOVE_RIGHT', 'TURN_RIGHT', 'ATTACK']
]

"""# Nets

## Conv
"""

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv0 = torch.nn.Conv2d(in_channels = 4, out_channels = 32, kernel_size = (8, 8), stride = (4,4))
        self.conv2 = torch.nn.Conv2d(in_channels = 32, out_channels = 64, kernel_size = (4, 4), stride = (2,2))

    def forward(self, x):

        x1 = F.relu(self.conv0(x))
        x2 = F.relu(self.conv2(x1))
        return x2.view(x2.shape[0], -1)

"""## Recurrent"""

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, out_features):
        super(RNN, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.out_features = out_features

        self.rnn = nn.LSTM(input_size = input_size, hidden_size = hidden_size, num_layers = num_layers, batch_first = True)
        self.proj_action_scores = nn.Linear(in_features = hidden_size, out_features = out_features, bias = True)

    def init_hidden(self, batch_size):
        return torch.zeros(1, batch_size , self.hidden_size)

    def forward(self, X, prev_state, back=False):

        ret = None

        out, next_state = self.rnn(X, prev_state)

        out2 = self.proj_action_scores(out[:, -1])

        if not back:
            ret = (out, next_state, out2)

        if back:
            out2_back = self.proj_action_scores(out[:, -2])
            ret = (out2_back, out2)

        return ret

"""# Game"""

def create_game():
    game = DoomGame()
    game.load_config("C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\vizdoom\\scenarios/cig.cfg")
    game.load_config("C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\vizdoom/bots.cfg")
    game.set_doom_map("map01")
    game.set_screen_format(vzd.ScreenFormat.CRCGCB)
    game.set_window_visible(False)

    # Sets resolution for all buffers.
    game.set_screen_resolution(vzd.ScreenResolution.RES_400X225)

    # Enables depth buffer.
    game.set_depth_buffer_enabled(True)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(True)

    # Enables buffer with top down map of he current episode/level .
    game.set_automap_buffer_enabled(True)
    game.set_automap_mode(vzd.AutomapMode.OBJECTS)
    game.set_automap_rotate(False)
    game.set_automap_render_textures(False)

    game.set_render_hud(True)
    game.set_render_minimal_hud(False)

    game.set_mode(vzd.Mode.SPECTATOR)

    game.add_available_game_variable(GameVariable.AMMO3)
    game.add_available_game_variable(GameVariable.HEALTH)

    game.add_game_args("-host 2 "
                    # This machine will function as a host for a multiplayer game with this many players (including this machine).
                    # It will wait for other machines to connect using the -join parameter and then start the game when everyone is connected.
                    "-deathmatch "           # Deathmatch rules are used for the game.
                    "+timelimit 0.5 "       # The game (episode) will end after this many minutes have elapsed.
                    "+sv_forcerespawn 1 "    # Players will respawn automatically after they die.
                    "+sv_noautoaim 1 "       # Autoaim is disabled for all players.
                    "+sv_respawnprotect 1 "  # Players will be invulnerable for two second after spawning.
                    "+sv_spawnfarthest 1 "   # Players will be spawned as far as possible from any other players.
                    "+sv_nocrouch 1 "        # Disables crouching.
                    "+viz_respawn_delay 1 " # Sets delay between respanws (in seconds).
                    "+viz_nocheat 0")        # Disables depth and labels buffer and the ability to use commands that could interfere with multiplayer game.

    game.set_mode(Mode.ASYNC_PLAYER)

    game.clear_available_buttons()

    game.add_available_button(MOVE_FORWARD)
    game.add_available_button(MOVE_BACKWARD)
    game.add_available_button(TURN_LEFT)
    game.add_available_button(TURN_RIGHT)
    game.add_available_button(MOVE_LEFT)
    game.add_available_button(MOVE_RIGHT)
    game.add_available_button(ATTACK)
    game.add_available_button(SPEED)
    game.add_available_button(CROUCH)

    return game

"""# Reward Shaping"""

def reward_shaping(game, param):

    reward_values = {
    'BASE_REWARD': 0.,
    'DISTANCE': 0.,
    'KILL': 5.,
    'DEATH': -5.,
    'SUICIDE': -5.,
    'MEDIKIT': 1.,
    'HIT': 2,
    'ARMOR': 1.,
    'INJURED': -1.,
    'WEAPON': 1.,
    'AMMO': 1.,
    'USE_AMMO': -0.2}


    tot_reward=0

    hit = game.get_game_variable(GameVariable.HITCOUNT)
    kill = game.get_game_variable(GameVariable.KILLCOUNT)
    death = game.get_game_variable(GameVariable.DEATHCOUNT)
    x = game.get_game_variable(GameVariable.POSITION_X)
    y = game.get_game_variable(GameVariable.POSITION_Y)
    ammo = game.get_game_variable(GameVariable.AMMO3)
    health = game.get_game_variable(GameVariable.HEALTH)
    frag = game.get_game_variable(GameVariable.FRAGCOUNT)
    armor= game.get_game_variable(GameVariable.ARMOR)

    distance = (param['x']-x)**2 + (param['y']-y)**2
    kill_diff = kill - param['kill']
    death_diff = death - param['death']
    frag_diff = frag - param['frag']
    health_diff = health - param['health']
    ammo_diff = ammo - param['ammo']
    armor_diff = armor - param['armor']
    hit_diff = hit - param['hit']

    tot_reward+=reward_values['DISTANCE']*distance

    if ammo_diff>0:
#         print('++++++++++++++2 reward')
        # print("Ammo found")
        tot_reward+=reward_values['AMMO']
    elif ammo_diff<0:
        # print("Ammo used")
        tot_reward+=reward_values['USE_AMMO']

    if health_diff>0:
        # print('+++++++++=== medkit')
        # print("health found")
        tot_reward+=reward_values['MEDIKIT']
    elif health_diff<0:
        # print("health used")
        tot_reward+=reward_values['INJURED']

    if armor_diff>0:
        tot_reward+=reward_values['ARMOR']
    elif armor_diff<0:
        tot_reward+=reward_values['INJURED']

    # if kill_diff>0:
    #     # print("killed")
    #     tot_reward+=reward_values['KILL']

    if death_diff>0:
        # print("death")
        tot_reward+=reward_values['DEATH']

        if frag_diff<0:
            frag_diff = 0

    if frag_diff<0:
        # print('suicide')
        tot_reward+=reward_values['SUICIDE']

    if frag_diff > 0:
        tot_reward+=reward_values['KILL']

    if hit_diff>0:
        # print("hit count")
        tot_reward+=reward_values['HIT']

    # if tot_reward != 0:
    #     print('old')
    #     print(param)

    param['x'], param['y'] = x, y
    param['ammo'] = ammo
    param['health'] = health
    param['frag'] = frag
    param['armor'] = armor
    param['kill'] = kill
    param['death'] = death
    param['hit'] = hit

    # if tot_reward != 0:
    #     print('new')
    #     print(param)
    #     print('-------------------------------------------------------------------------------------------------------------')
    #     print()

    return tot_reward, param

"""# Misc

## Label ID
"""

def get_label_type_id(label):
    """
    Map an object name to a feature map.
    0 = enemy
    1 = health item
    2 = weapon
    3 = ammo
    None = anything else
    """
    ENEMY_NAME_SET = set([
    'MarineBFG', 'MarineBerserk', 'MarineChaingun', 'MarineChainsaw',
    'MarineFist', 'MarinePistol', 'MarinePlasma', 'MarineRailgun',
    'MarineRocket', 'MarineSSG', 'MarineShotgun',
    'Demon'
    ])
    HEALTH_ITEM_NAME_SET = set([
        'ArmorBonus', 'BlueArmor', 'GreenArmor', 'HealthBonus',
        'Medikit', 'Stimpack'
    ])
    WEAPON_NAME_SET = set([
        'Pistol', 'Chaingun', 'RocketLauncher', 'Shotgun', 'SuperShotgun',
        'PlasmaRifle', 'BFG9000', 'Chainsaw'
    ])
    AMMO_NAME_SET = set([
        'Cell', 'CellPack', 'Clip', 'ClipBox', 'RocketAmmo', 'RocketBox',
        'Shell', 'ShellBox'
    ])

    name = label.object_name
    value = label.value
    if value != 255 and name == 'DoomPlayer' or name in ENEMY_NAME_SET:
        return 0
    elif name in HEALTH_ITEM_NAME_SET:
        return 1
    elif name in WEAPON_NAME_SET:
        return 2
    elif name in AMMO_NAME_SET:
        return 3

"""## Label Buffer"""

def return_u(s):
    mapping_u = np.zeros((256,), dtype=np.uint8)
    labels_buffer = s.labels_buffer
    for label in s.labels:
        type_id = get_label_type_id(label)
        if type_id is not None:
            mapping_u[label.value] = type_id + 1
    # -x is faster than x * 255 and is equivalent for uint8
    uu_labels_buffer = -(mapping_u[labels_buffer] ==
                        np.arange(1, 5)[:, None, None]).astype(np.uint8)

    # print(uu_labels_buffer.shape)
    game_labels_mapping = [0, None, None, None]


    n_feature_maps = max(x for x in game_labels_mapping
                         if x is not None) + 1

    u_labels_buffer = np.zeros((1,) + (225, 400),
                                          dtype=np.uint8)

    for i in range(4):
        j = game_labels_mapping[i]

        if j is not None:
            u_labels_buffer[j] += uu_labels_buffer[i]
    u_labels_buffer = np.concatenate([
        cv2.resize(
            u_labels_buffer[i],
            (108, 60),
            interpolation=cv2.INTER_AREA
        ).reshape(1, 60, 108)
        for i in range(u_labels_buffer.shape[0])
    ], axis=0)

    return u_labels_buffer

"""## Embeds"""

t = torch.ones(320)
a  = [ 0.9046,  0.2134, -0.4263,  0.6935, -0.1992, -0.7638, -0.7087,
         -0.7069, -0.5152,  0.9864,  0.3943,  1.0061, -0.2596,  0.2902,
          0.7169,  0.2853, -0.0477, -0.2059,  0.5542, -0.3423, -0.0104,
          0.2984, -0.6767, -0.0438, -0.4817,  0.1470, -0.4538,  0.6242,
         -0.1060, -0.8813, -0.0825,  0.6817, 0.3851, -0.8109, -0.0730,  0.5059,  0.3322, -1.0178, -0.2348,
         -0.6786,  1.0048, -0.8780,  0.5038, -0.5334, -0.3227, -0.8099,
          0.1141, -0.9171, -0.7294,  1.5010, -0.8287,  1.2967, -0.4908,
          1.0239,  0.8320,  0.8535, -0.3320, -0.4335,  0.9687, -0.6026,
          0.2370, -0.3944, -0.8017, -0.2437]
fixed_vec = t.new_tensor(a)

"""#  Experience Replay"""

def save_replay(cnn, rnn, episodes, frame_skip, bots):

    game = create_game()

    game.init()

    r_list = []

    f = open(save_folder + 'replay/list_file_name.txt', 'w+')
    f.close()


    for ep in tqdm(range(episodes), desc="Replay"):
        batch = torch.FloatTensor()

        game.send_game_command("removebots")
        for j in range(bots):
            game.send_game_command("addbot")
        game.new_episode()
        game.advance_action(3)
        prev_state = (torch.zeros(1, 1 , 512), torch.zeros(1, 1 , 512))
        total_reward = 0

        param = {}
        param['hit'] = game.get_game_variable(GameVariable.HITCOUNT)
        param['kill'] = game.get_game_variable(GameVariable.KILLCOUNT)
        param['death'] = game.get_game_variable(GameVariable.DEATHCOUNT)
        param['x'] = game.get_game_variable(GameVariable.POSITION_X)
        param['y'] = game.get_game_variable(GameVariable.POSITION_Y)
        param['ammo'] = game.get_game_variable(GameVariable.AMMO3)
        param['health'] = game.get_game_variable(GameVariable.HEALTH)
        param['frag'] = game.get_game_variable(GameVariable.FRAGCOUNT)
        param['armor'] = game.get_game_variable(GameVariable.ARMOR)

        step = 0

        while not game.is_episode_finished():

            sar = []

            all_buffers = []
            s = game.get_state()
            state_vars = s.game_variables
            s_image = s.screen_buffer
            s_image = cv2.resize(s_image.transpose(1, 2, 0),(108, 60),interpolation=cv2.INTER_AREA).transpose(2, 0, 1)
            all_buffers.append(s_image)
            u_labels_buffer = return_u(s)
            all_buffers.append(u_labels_buffer)
            final_s = np.concatenate(all_buffers, 0)
            final_s = final_s/255
            final_s = torch.from_numpy(final_s)
            final_s = torch.unsqueeze(final_s, dim = 0)
            final_s = final_s.type(torch.FloatTensor)

            #add s
            sar.append(final_s.detach().cpu().numpy())

            #get action
            encode = cnn(final_s)
            embeddings = fixed_vec.reshape(1, 1, 64)*0.01
            encode = encode.reshape(1, 1, 4608)
            finalize = torch.cat((encode,embeddings),2)
            rnn_out, next_state, out = rnn(finalize, prev_state)
            prev_state = next_state
            action_id = torch.argmax(out)

            #add a
            sar.append(action_id.detach().cpu().numpy())

            action = np.zeros(9)
            for m in mapping[action_id]:
                # print(m, end = " , ")
                action += iden[keys[m]]

            for fs in range(frame_skip):
                game.make_action(mapping_action[action_id])
                time.sleep(0.01)

                if game.is_player_dead():
                    # print("Player died.")
                    # Use this to respawn immediately after death, new state will be available.
                    game.respawn_player()
                    # game.advance_action(3)

            reward, param = reward_shaping(game, param)

            #add R
            sar.append(reward)

            #save sar
            torch.save(sar, save_folder + 'replay/sar_'+str(ep)+'_'+str(step)+'.pt')

            f = open(save_folder + 'replay/list_file_name.txt', 'a+')
            f.write('sar_'+str(ep)+'_'+str(step)+'.pt')
            f.write('\n')
            f.close()

            total_reward += reward

            step += 1

        r_list.append(total_reward)

    game.close()

    return r_list

"""# Data Loader"""

class Load_Data(torch.utils.data.Dataset):
    def __init__(self, save_folder, seq_len):
        self.save_folder = save_folder + 'replay/'
        self.seq_len = seq_len

        with open(self.save_folder + 'list_file_name.txt') as f:
            lines = f.readlines()

        self.n_data_points = len(lines) - 1

    def __len__(self):
        return self.n_data_points - (seq_len + 1)

    def __getitem__(self, index):

        index = index + seq_len

        with open(self.save_folder + 'list_file_name.txt') as f:
            lines = f.readlines()

        name_list = lines[index-self.seq_len + 1 : index+2]

        s, _, _ = torch.load(self.save_folder + name_list[0][:-1])
        s = torch.Tensor(s)
        for i in range(1, len(name_list)-2):
            s1, _, _ = torch.load(self.save_folder + name_list[i][:-1])
            s1 = torch.Tensor(s1)
            s = torch.cat((s, s1), dim=0)
        s1, a, r = torch.load(self.save_folder + name_list[-2][:-1])
        s_, _, _ = torch.load(self.save_folder + name_list[-1][:-1])
        s1 = torch.Tensor(s1)
        s_ = torch.Tensor(s_)
        s = torch.cat((s, s1, s_), dim=0)

        a = torch.tensor(a)
        r = torch.tensor([r])

        return s, a, r

"""# Initialize

## Params
"""

frame_skip = 4
replay_episodes = 10
bots = 8
total_epochs = 100
batch_size = 2
seq_len = 4
input_size = 4672
hidden_size = 512
num_layers = 1
out_features = 29
gamma = 0.9

"""## Nets"""

pretrained = torch.load(save_folder + 'renamed.pth')

cnn = CNN()
rnn = RNN(input_size, hidden_size, num_layers, out_features)
cnn.load_state_dict(pretrained, strict = False)
rnn.load_state_dict(pretrained, strict = False)
cnn = cnn.train()
rnn = rnn.train()

"""## Criterions"""

mse = nn.MSELoss(reduction='mean')
optimizer = torch.optim.Adam(list(cnn.parameters()) + list(rnn.parameters()))

"""## Data Loader"""

def prepare_data(save_folder, seq_len, batch_size):
    train_dataset = Load_Data(save_folder=save_folder, seq_len=seq_len)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    return train_loader

"""# Train"""

import time
import copy

epoch_avg_loss = [0]*total_epochs
epoch_avg_reward = [0]*total_epochs

#To time the code
# t = time.time()

for epoch in range(total_epochs):

    print('epoch', epoch)

    avg_loss = 0

    avg_reward = save_replay(cnn, rnn, replay_episodes-4, frame_skip, bots)
    avg_reward = np.array(avg_reward)/replay_episodes

    train_loader = prepare_data(save_folder, seq_len, batch_size)

    for batch_idx, (S, A, R) in tqdm(enumerate(train_loader), total=len(train_loader), desc='epoch '+str(epoch)):

        S, A, R = S.view(-1, S.shape[2], S.shape[3], S.shape[4]), A, R

        c = cnn(S)

        e = torch.cat([fixed_vec.view(1,-1)*0.01]*c.shape[0], dim=0)

        z = torch.cat((c, e), dim=1).view(c.shape[0]//(seq_len+1), seq_len+1, -1)

        prev_state = (rnn.init_hidden(c.shape[0]//(seq_len + 1)), rnn.init_hidden(c.shape[0]//(seq_len+1)))

        q, q_ = rnn(z, prev_state, True)

        y = torch.zeros(q.shape[0])
        for i in range(q.shape[0]):
            y[i] = q[i, A[i]]

        y_pred = R + gamma * torch.max(q_, 1)[0]

        loss = mse(y, y_pred)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        avg_loss += loss.cpu().detach().numpy()


        # if batch_idx % 100 == 0:
        #     print('epoch', epoch, 'batch', batch_idx, 'train batch loss', train_loss.cpu().detach().numpy(), 'train batch acc', train_acc.cpu().detach().numpy())
        #     print('saving...')
        #     torch.save(model.state_dict(), sfolder + sname + '.pt')
        #     print()
        #     print('time taken in min:', (time.time() - t)/60)
        #     t = time.time()
        # total_batches += 1

    epoch_avg_loss[epoch] = avg_loss/batch_idx
    epoch_avg_reward[epoch] = avg_reward

    loss_file = open(save_folder + 'loss_list.pkl', 'wb+')
    pickle.dump([epoch_avg_loss, epoch_avg_reward], loss_file)
    loss_file.close()

    save_dict = {
        'cnn':cnn.state_dict(),
        'rnn':rnn.state_dict(),
        'optimizer':optimizer.state_dict()
    }
    torch.save(save_dict, save_folder+'model'+str(epoch)+'.pt')

    print()
    print('epoch', epoch, 'epoch avg loss', epoch_avg_loss[epoch])
    print('epoch', epoch, 'epoch avg reward', epoch_avg_reward[epoch])
    print()

