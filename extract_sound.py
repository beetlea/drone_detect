import subprocess
import os
import random
from pydub import AudioSegment

name = "./no_process/audio4.wav"
begin = str(549)
end = str(55)
name_out = name[:-4] + begin + end + name[-5:]

path = "./no_detect_copter/wav_file/"
path_out = "./no_detect_copter/audio_mono_level/"
#subprocess.call(command, shell=True)

#command = "ffmpeg -i C:/test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"

def convert_mp3_to_wav(name1, path):
    command = "ffmpeg -i {0} {1}".format(path+name1,   name1[:-5] + ".wav")
    subprocess.call(command, shell=True)

def cut_file(name1, begin, length, name_out):
    command = "ffmpeg -ss {0} -i {1} -t {2} -c copy {3}".format(str(begin), name1, str(length), name_out)
    subprocess.call(command, shell=True)

def gen_one_channel(name1, path):
    cmd = "ffmpeg -y -i {0} -ac 1 {1}".format(path + name1, path + name1)
    subprocess.call(cmd, shell=True)

def set_volume_level(name1, level_volume, path_in, path_out, name_out):
    command = "ffmpeg -y -i {0} -filter:a \"volume={1}\" {2}".format( path_in + name1, str(level_volume), path_out + name1[:-5] + str(level_volume) + ".wav")
    subprocess.call(command, shell=True)

def mix_two_file(name1, name2, name_out):
    command = "ffmpeg -i {0} -i {1} -filter_complex amix=inputs=2:duration=longest {2}".format( name1, name2, name1[:3] +name2[:3], name_out)
    print(command)
    subprocess.call(command, shell=True)


def change_bitrate(name1, bitrate, path, path_out):
    #command = "ffmpeg -y -i {0} -ab {1} {2}".format( path + name1, str(bitrate), path_out + name1)
    #command = "ffmpeg -i {0} -ab {1} {2}".format( path + name1, str(bitrate), path_out + name1)
    command = "ffmpeg -i {0} -ar {1} {2}".format( path + name1, str(bitrate), path_out + name1)
    subprocess.call(command, shell=True)

change_bitrate("drone.wav", 16000, "./",  "./drone_detect_audio/") 

'''
for root, dirs, files in os.walk(path):  
    for name_file in files:
        convert_mp3_to_wav(name_file, path)
'''
'''
for root, dirs, files in os.walk(path):  
    for name_file in files:
        if name_file[-1:] == "v":
            change_bitrate(name_file, 16000, path,  path_out) 
            gen_one_channel(name_file, path_out) 
            for z in range(1, 10, 1): 
                set_volume_level(name_file, str(z%10), path_out, path_out, name_file[:-5] + str(z) + name_file[-5:]) 

'''
'''

def mix_path_file(path1):
    list_ = []
    list_ = os.listdir(path1)

    return list_

path1 = "./detect_copter/audio_mono_level/"
path2 = "./no_detect_copter/audio/"
path_save = "./dataset/drone/"

files1_copter = mix_path_file(path1)
files2_no_copter = mix_path_file(path2)

length_cop = len(files1_copter)
length_no_cop = len(files2_no_copter)
num_no_cop = 0
num2 = 0
lat_num = []
for i in range(3000):
    while True:
        num_no_cop = random.randint(0, length_no_cop - 1)
        try:
            lat_num.index(num_no_cop)
        except:
            break 

    num2 = random.randint(0, length_cop - 1)

    sound1 = AudioSegment.from_file(path1 + files1_copter[num2])
    sound2 = AudioSegment.from_file(path2 + files2_no_copter[num_no_cop])

    combined = sound1.overlay(sound2)

    combined.export(path_save + str(i) + ".wav", format='wav', bitrate=256)
    gen_one_channel(str(i) + ".wav",  path_save) 
    #change_bitrate( str(i) + ".wav", str(i) + ".wav" + ".wav", path_save, path_save)

'''