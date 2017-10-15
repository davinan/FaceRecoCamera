import speech_recognition as sr
import threading
import os
import timeout_decorator



class voice2text:
    def __init__(self):
        self.mic_name = "HDA Intel PCH: ALC892 Analog (hw:1,0)"
        #Sample rate is how often values are recorded
        self.sample_rate = 48000
        #Chunk is like a buffer. It stores 2048 samples (bytes of data)
        #here. 
        #it is advisable to use powers of 2 such as 1024 or 2048
        self.chunk_size = 2048
        #Initialize the recognizer
        self.r = sr.Recognizer()
        
        #generate a list of all audio cards/microphones
        mic_list = sr.Microphone.list_microphone_names()
        print(mic_list)
        #the following loop aims to set the device ID of the mic that
        #we specifically want to use to avoid ambiguity.
        for i, microphone_name in enumerate(mic_list):
            if microphone_name == self.mic_name:
                self.device_id = i

    @timeout_decorator.timeout(10)
    def v2t(self):
        with sr.Microphone(device_index = self.device_id, sample_rate = self.sample_rate, 
                        chunk_size = self.chunk_size) as source:
            #wait for a second to let the recognizer adjust the 
            #energy threshold based on the surrounding noise level
            # self.r.adjust_for_ambient_noise(source)
            # print "Say Something"
            #listens for the user's input
            audio = self.r.listen(source)
                
            try:
                text = self.r.recognize_google(audio)

                print "you said: " + text
                return text
            
            #error occurs when google could not understand what was saidword2t
            
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return "X"
            
            except sr.RequestError as e:
                print("Could not request results from Google peech Recognition service")
                return "X"

if __name__ == "__main__":
    # t = voice2text()
    # x = threading.Thread(target=t.v2t)
    # x.start()
    t = voice2text()
    large = t.v2t()
    print(large)

