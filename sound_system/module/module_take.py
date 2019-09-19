import os
from pocketsphinx import LiveSpeech, get_model_path

from .import module_speak

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
            start_sentence = "May I help you ?"
            print("\n---------------------------------\n", start_sentence, "\n---------------------------------\n")
            module_speak.speak(start_sentence)
            # Noise list
            noise_words = read_noise_word(take_gram_path)
            # Setup live_speech
            setup_live_speech(False, take_dic_path, take_gram_path, 1e-10)

            print("\n[*] PLEASE SAY PLACE ...")
            for question1 in live_speech:
                # print(question)
                if str(question1) not in noise_words:
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now()) + ": " + str(question1) + "\n")
                    file.close()
                    place = str(question1).replace("take this bag to the ", "")
                    print("\n----------------------------\n", str(question1), "\n----------------------------\n")
                    print("\n-----------PLACE-----------\n", place,
                          "\n----------------------------\n")
                    counter += 1

                    sentence = "Is it " + str(place) + " ?"
                    print("\n---------------------------------\n",sentence,"\n---------------------------------\n")
                    pause()
                    module_speak.speak(sentence)

                    # Detect yes or no
                    setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
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
                                answer = "Sure, I will take the bag to the " + str(place) + "."
                                print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                                pause()
                                module_speak.speak(answer)
                                return str(place)

                            elif str(question2) == "no":

                                # Fail, oreder one more time
                                answer = "Sorry."
                                print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                                pause()
                                module_speak.speak(answer)
                                setup_live_speech(False, take_dic_path, take_gram_path, 1e-10)
                                break


                            elif str(question2) == "please say again":

                                pause()
                                print("\n---------------------------------\n",sentence,"\n---------------------------------\n")
                                module_speak.speak(sentence)

                                # Ask yes-no question to barman
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
                    print("\n[*] PLEASE SAY PLACE ...")
                    pass

        end_sentence = "I can't detect, so I will ask all places."
        print("\n---------------------------------\n", end_sentence, "\n---------------------------------\n")
        module_speak.speak(end_sentence)
        file = open(result_path, 'a')
        file.write(str(datetime.datetime.now()) + ": " + str(end_sentence) + "\n")
        file.close()

        i = 0
        places_list = read_place_word()
        while i < len(places_list):
            sentence = "Is it " + places_list[i] + " ?"
            print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
            pause()
            module_speak.speak(sentence)
            file = open(result_path, 'a')
            file.write(str(datetime.datetime.now()) + ": " + str(sentence) + "\n")
            file.close()

            # Detect yes or no
            setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
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
                        answer = "Sure, I will take the bag to the " + places_list[i] + "."
                        print("\n---------------------------------\n", answer, "\n---------------------------------\n")
                        pause()
                        module_speak.speak(answer)
                        return places_list[i]

                    elif str(question3) == "no":

                        # Fail, oreder one more time
                        answer = "Sorry, I will ask next place."
                        print("\n---------------------------------\n", answer, "\n---------------------------------\n")
                        pause()
                        module_speak.speak(answer)
                        setup_live_speech(False, take_dic_path, take_gram_path, 1e-10)
                        break


                    elif str(question3) == "please say again":

                        pause()
                        print("\n---------------------------------\n", sentence, "\n---------------------------------\n")
                        module_speak.speak(sentence)

                        # Ask yes-no question to barman
                        setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)

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
