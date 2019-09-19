import os
from pocketsphinx import LiveSpeech, get_model_path

from .import module_speak

import datetime
from time import sleep

noise_words = []
file_path = os.path.abspath(__file__)

# pocketsphinx path
model_path = get_model_path()

# Define order path
yes_no_dic_path = file_path.replace(
    'module/module_make_map.py', 'dictionary/yes_no.dict')
yes_no_gram_path = file_path.replace(
    'module/module_make_map.py', 'dictionary/yes_no.gram')
map_dic_path = file_path.replace(
    'module/module_make_map.py', 'dictionary/map_test.dict')
map_gram_path = file_path.replace(
    'module/module_make_map.py', 'dictionary/map_test.gram')
# log file
result_path = file_path.replace(
    'module/module_make_map.py', 'log/map-{}.txt').format(str(datetime.datetime.now()))

# Manipulate robot arm
def make_map(do = None):

    ###############
    #
    # use this module to make map, tell this place and go them
    #
    # param >> go or None (or nothing)
    #
    # return >> place | to remember
    #                 | to go to
    #
    ###############

    global noise_words
    global live_speech

    if do == None:
        while True:
            sentence = "Where is here ?"
            print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
            module_speak.speak(sentence)
            file = open(result_path, 'a')
            file.write(str(datetime.datetime.now()) + ": " + sentence + "\n")
            file.close()

            setup_live_speech(False, map_dic_path, map_gram_path, 1e-10)
            sleep(1)
            for question1 in live_speech:
                print("\n[*] WHERE IS HERE ...")
                # print(question1)

                # Noise list
                noise_words = read_noise_word(map_gram_path)
                if str(question1) == "":
                    pass
                elif str(question1) not in noise_words and str(question1).split(" ")[0] == "Here":
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now()) + ": " + str(question1) + "\n")
                    file.close()
                    print("\n-----------your order-----------\n", str(question1), "\n---------------------------------\n")
                    place = str(question1).replace("Here is the ", "")
                    sentence = "Is here " + str(place) + " ?"
                    print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
                    pause()
                    module_speak.speak(sentence)

                    # Ask yes-no question
                    setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                    # Ask yes-no question
                    for question2 in live_speech:
                        print("\n[*] CONFIRMING ...")
                        # print(question2)

                        # Noise list
                        noise_words = read_noise_word(yes_no_gram_path)
                        if str(question2) not in noise_words:
                            file = open(result_path, 'a')
                            file.write(str(datetime.datetime.now()) + ": " + str(question2) + "\n")
                            file.close()

                            if str(question2) == "yes":

                                answer = "Sure, I understand here is " + place + "."
                                print("\n---------------------------------\n", answer,
                                      "\n---------------------------------\n")
                                print("\n------------place--------------\n", str(place),
                                      "\n---------------------------------\n")
                                pause()
                                module_speak.speak(answer)
                                return str(place)

                            elif str(question2) == "no":

                                # Fail, listen one more time
                                answer = "Sorry."
                                print("\n---------------------------------\n", answer,
                                      "\n---------------------------------\n")
                                pause()
                                module_speak.speak(answer)
                                setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                                break

                            elif str(question2) == "please say again":

                                pause()
                                print("\n---------------------------------\n", sentence,
                                      "\n---------------------------------\n")
                                module_speak.speak(sentence)

                                # Ask yes-no question
                                setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)

                        # noise
                        else:
                            print(".*._noise_.*.")
                            print("\n[*] CONFIRMING ...")
                            pass
                    break
                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] WHERE IS HERE ...")
                    pass

    elif do == "go":
        while True:
            sentence = "Where shall I go ?"
            print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
            module_speak.speak(sentence)
            file = open(result_path, 'a')
            file.write(str(datetime.datetime.now()) + ": " + sentence + "\n")
            file.close()

            setup_live_speech(False, map_dic_path, map_gram_path, 1e-10)
            sleep(1)
            for question1 in live_speech:
                print("\n[*] WHERE SHALL I GO ...")
                # print(question1)

                # Noise list
                noise_words = read_noise_word(map_gram_path)
                if str(question1) == "":
                    pass
                elif str(question1) not in noise_words and str(question1).split(" ")[0] == "Please":
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now()) + ": " + str(question1) + "\n")
                    file.close()
                    print("\n-----------your order-----------\n", str(question1),
                          "\n---------------------------------\n")
                    place = str(question1).replace("Please go to the ", "")
                    sentence = "Is is " + str(place) + " ?"
                    print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
                    pause()
                    module_speak.speak(sentence)

                    # Ask yes-no question
                    setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                    # Ask yes-no question
                    for question2 in live_speech:
                        print("\n[*] CONFIRMING ...")
                        # print(question2)

                        # Noise list
                        noise_words = read_noise_word(yes_no_gram_path)
                        if str(question2) not in noise_words:
                            file = open(result_path, 'a')
                            file.write(str(datetime.datetime.now()) + ": " + str(question2) + "\n")
                            file.close()

                            if str(question2) == "yes":

                                answer = "Sure, I will go to the " + place + "."
                                print("\n---------------------------------\n", answer,
                                      "\n---------------------------------\n")
                                print("\n------------place--------------\n", str(place),
                                      "\n---------------------------------\n")
                                pause()
                                module_speak.speak(answer)
                                return str(place)

                            elif str(question2) == "no":

                                # Fail, listen one more time
                                answer = "Sorry."
                                print("\n---------------------------------\n", answer,
                                      "\n---------------------------------\n")
                                pause()
                                module_speak.speak(answer)
                                setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                                break

                            elif str(question2) == "please say again":

                                pause()
                                print("\n---------------------------------\n", sentence,
                                      "\n---------------------------------\n")
                                module_speak.speak(sentence)

                                # Ask yes-no question
                                setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)

                        # noise
                        else:
                            print(".*._noise_.*.")
                            print("\n[*] CONFIRMING ...")
                            pass
                    break
                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] WHERE SHALL I GO ...")
                    pass

# Stop lecognition
def pause():

    ###############
    #
    # use this module to stop live speech
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(no_search=True)

# Make noise list
def read_noise_word(gram_path):

    ###############
    #
    # use this module to put noise to list
    #
    # param >> gram_path: grammer's path which you want to read noises
    #
    # return >> words: list in noises
    #
    ###############

    words = []
    with open(gram_path) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace(
                    " = ", "").replace("\n", "").replace(";", "")
            words = line.split(" | ")
    return words

# Setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):

    ###############
    #
    # use this module to set live espeech parameter
    #
    # param >> lm: False >> means useing own dict and gram
    # param >> dict_path: ~.dict file's path
    # param >> jsgf_path: ~.gram file's path
    # param >> kws_threshold: mean's confidence (1e-○)
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)

if __name__ == '__main__':
    make_map("go")
