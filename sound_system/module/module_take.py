import os
from pocketsphinx import LiveSpeech, get_model_path

from . import module_pico
from . import module_beep

import datetime

noise_words = []
places_list = []
file_path = os.path.abspath(__file__)
model_path = get_model_path()

# Define path
take_dic_path = file_path.replace(
    'module/module_take.py', 'dictionary/take_bag.dict')
take_gram_path = file_path.replace(
    'module/module_take.py', 'dictionary/take_bag.gram')
result_path = file_path.replace(
    'module/module_take.py', 'log/carry-{}.txt').format(str(datetime.datetime.now()))

yes_no_dic_path = file_path.replace(
    'module/module_take.py', 'dictionary/yes_no.dict')
yes_no_gram_path = file_path.replace(
    'module/module_take.py', 'dictionary/yes_no.gram')

# Listen place
def take():
    ###############
    #
    # use this module at help my carry section
    #
    # param >> None
    #
    # return >> place
    #
    ###############

    counter = 0
    global noise_words
    global places_list
    global live_speech

    # Where to take the bag
    while True:
        # If I can't get place, count 1
        while counter < 3:
            print("- " + str(counter + 1) + " cycle -")
            start_sentence = "May I help you ?"
            print("\n---------------------------------\n", start_sentence, "\n---------------------------------\n")
            module_pico.speak(start_sentence)
            # Noise list
            noise_words = read_noise_word(take_gram_path)
            # Setup live_speech
            setup_live_speech(False, take_dic_path, take_gram_path, 1e-10)

            print("\n[*] TAKE THIS BAG TO THE ...")
            module_beep.beep("start")
            for question1 in live_speech:
                # print(question)
                if str(question1) not in noise_words and str(question1).split(" ")[0] == "take":
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now()) + ": " + str(question1) + "\n")
                    file.close()
                    pause()
                    module_beep.beep("stop")
                    place = str(question1).replace("take this bag to the ", "").replace("take this bag to thing ", "")
                    print("\n----------------------------\n", str(question1), "\n----------------------------\n")
                    print("\n-----------PLACE-----------\n", place,
                          "\n----------------------------\n")
                    counter += 1

                    sentence = "Is it " + str(place) + " ?"
                    print("\n---------------------------------\n",sentence,"\n---------------------------------\n")
                    module_pico.speak(sentence.replace("_", " "))

                    # Detect yes or no
                    setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                    module_beep.beep("start")
                    for question2 in live_speech:
                        print("\n[*] CONFIRMING ...")
                        #print(question2)

                        # Noise list
                        noise_words = read_noise_word(yes_no_gram_path)

                        if str(question2) not in noise_words:
                            file = open(result_path, 'a')
                            file.write(str(datetime.datetime.now())+": "+str(question2)+"\n")
                            file.close()

                            if str(question2) == "yes":

                                # Deside order
                                pause()
                                module_beep.beep("stop")
                                answer = "Sure, I will take the bag to the " + str(place) + "."
                                print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                                module_pico.speak(answer.replace("_", " "))
                                return str(place)

                            elif str(question2) == "no":

                                # Fail, oreder one more time
                                pause()
                                module_beep.beep("stop")
                                answer = "Sorry."
                                print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                                module_pico.speak(answer)
                                setup_live_speech(False, take_dic_path, take_gram_path, 1e-10)
                                noise_words = read_noise_word(yes_no_gram_path)
                                break


                            elif str(question2) == "please say again":

                                pause()
                                module_beep.beep("stop")
                                print("\n---------------------------------\n",sentence,"\n---------------------------------\n")
                                module_pico.speak(sentence.replace("_", " "))
                                module_beep.beep("start")
                                # Ask yes-no question to barman
                                setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                                noise_words = read_noise_word(yes_no_gram_path)

                        # noise
                        else:
                            print(".*._noise_.*.")
                            print("\n[*] CONFIRMING ...")
                            pass
                    break


                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] TAKE THIS BAG TO THE ...")
                    pass

        end_sentence = "I can't detect, so I will ask all places."
        print("\n---------------------------------\n", end_sentence, "\n---------------------------------\n")
        module_pico.speak(end_sentence)
        file = open(result_path, 'a')
        file.write(str(datetime.datetime.now()) + ": " + str(end_sentence) + "\n")
        file.close()

        i = 0
        places_list = read_place_word()
        while i < len(places_list):
            sentence = "Is it " + places_list[i] + " ?"
            print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
            pause()
            module_pico.speak(sentence.replace("_", " "))
            file = open(result_path, 'a')
            file.write(str(datetime.datetime.now()) + ": " + str(sentence) + "\n")
            file.close()

            # Detect yes or no
            setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
            module_beep.beep("start")
            for question3 in live_speech:
                print("\n[*] CONFIRMING ...")
                # print(question2)

                # Noise list
                noise_words = read_noise_word(yes_no_gram_path)

                if str(question3) not in noise_words:
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now()) + ": " + str(question3) + "\n")
                    file.close()

                    if str(question3) == "yes":

                        # Deside order
                        pause()
                        module_beep.beep("stop")
                        answer = "Sure, I will take the bag to the " + places_list[i] + "."
                        print("\n---------------------------------\n", answer, "\n---------------------------------\n")
                        module_pico.speak(answer.replace("_", " "))
                        return places_list[i]

                    elif str(question3) == "no":

                        # Fail, oreder one more time
                        pause()
                        module_beep.beep("stop")
                        answer = "Sorry, I will ask next place."
                        print("\n---------------------------------\n", answer, "\n---------------------------------\n")
                        module_pico.speak(answer)
                        setup_live_speech(False, take_dic_path, take_gram_path, 1e-10)
                        noise_words = read_noise_word(yes_no_gram_path)
                        break


                    elif str(question3) == "please say again":

                        pause()
                        module_beep.beep("stop")
                        print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
                        module_pico.speak(sentence.replace("_", " "))
                        module_beep.beep("start")
                        # Ask yes-no question to barman
                        setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                        noise_words = read_noise_word(yes_no_gram_path)

                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] CONFIRMING ...")
                    pass

            i += 1
            if i == len(places_list):
                i = 0


def pause():
    ###############
    #
    # use this module to stop lecognition
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

# Make noise list
def read_place_word():

    ###############
    #
    # use this module to put place to list
    #
    # param >> gram_path: grammer's path which you want to read places
    #
    # return >> places: list in places
    #
    ###############

    places = []
    with open(take_gram_path) as f:
        for line in f.readlines():
            if "<place>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<place>", "").replace(
                    " = ", "").replace("\n", "").replace(";", "")
            places = line.split(" | ")
    return places

def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):

    ###############
    #
    # use this module to set live speech parameter
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
    take()
