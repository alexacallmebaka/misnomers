"""
Quick preface: I have never done anything with ML. I have never even played with numpy. I really wanted to try something though.
A lot of my model training code is a modified version of the code from this article (https://towardsdatascience.com/generating-pok%C3%A9mon-names-using-rnns-f41003143333)
which really walked me through the sort of thing I was doing. Please go easy on me.
"""

from tensorflow.keras.callbacks import LambdaCallback
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import numpy as np

#Alternative functiom to get the names function from the web as opposed to a local file.
"""
def get_names():
    import requests

    data = requests.get("https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes")
    names = str(data.content).split("\\n")

    for name in names:
        name = name + "."
    
    return names
"""
#Open the dataset of names we will learn from.
raw_names=open("names.txt","r").readlines()

#Instatiate the array which will store our finished names.
names = []

#Cleaning up our raw data by making the name all lowercase, stripping newlines, and adding a period after each name to indicate it is finished. We need to use this as
#the names vary in length.
for i in range(len(raw_names)):
    name = raw_names[i].lower().replace("\n",".")
    names.append(name)

#Here we "one-hot" encode all the ascii characters, plus a space and a period.
#I still don't 100% understand what's going on here, so see the aforemntioned article.
#There is probably a better way than using a space as char 0, but it's a hackathon and time is of the essence,
#so, I will just clean that up later because I don't fully understand this "vectoriztion" proccess.
char_indices = dict( (chr(i+96), i) for i in range(1,27))
char_indices[' '] = 0
char_indices['.'] = 27

indices_char = dict( (i, chr(i+96)) for i in range(1,27))
indices_char[0] = ' '
indices_char[27] = '.'

max_char = len(max(names, key=len))

m = len(names)

char_dim = len(char_indices)


x = np.zeros((m, max_char, char_dim))
y = np.zeros((m, max_char, char_dim))

for i in range(m):
    name = list(names[i])
    for j in range(len(name)):
        x[i, j, char_indices[name[j]]] = 1
        if j < len(name)-1:
            y[i, j, char_indices[name[j+1]]] = 1

#Time to build the model!!!!
model = Sequential()
model.add(LSTM(128, input_shape=(max_char, char_dim), return_sequences=True))
model.add(Dense(char_dim, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

#This function uses the model to create a name!
def make_name(model):
    name = []
    x = np.zeros((1, max_char, char_dim))
    end = False
    i = 0
    
    #From what I understand, the model is basically predicting what characters it thinks will go where based on what it has learned.
    while end==False:
        probs = list(model.predict(x)[0,i])
        probs = probs / np.sum(probs)
        index = np.random.choice(range(char_dim), p=probs)
        if i == max_char-2:
            character = '.'
            end = True
        else:
            character = indices_char[index]
        name.append(character)
        x[0, i+1, index] = 1
        i += 1
        #If we get a period, that marks the end of the name.
        if character == '.':
            end = True

    #Join together all of the predicted characters into a complete name. 
    return ''.join(name)

#This is a quick function that just outputs three names each epoch when training so I can watch the progession to see how many epochs produce a model with the best fit.
def generate_name_loop(epoch, _):
    print('Names generated after epoch {}:'.format(epoch))

    for i in range(3):
        make_name(model)
              
name_generator = LambdaCallback(on_epoch_end = generate_name_loop)

#A couple different model training functions.

#model.fit(x, y, batch_size=128, epochs=250, verbose=0)
#model.fit(x, y, batch_size=64, epochs=10, verbose=0)
model.fit(x, y, batch_size=64, epochs=300, callbacks=[name_generator], verbose=0)

#Here we save the trained model to a file for later use.
model.save('namegen-300.hdf5')

################
#Ending Remarks#
################

# As stated previously, this has sort of been a baptism by fire for me when it comes to machine learning. However it has really encouraged me to learn more
# about the field as a whole. Next year, I hope to be able to produce something amazing after reasearching ML more!