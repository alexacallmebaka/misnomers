"""
Quick preface: I have never done anything with ML. I have never even played with numpy. I really wanted to try something though.
A lot of my model training code is a modified version of the code from this article (https://towardsdatascience.com/generating-pok%C3%A9mon-names-using-rnns-f41003143333)
which really walked me through the sort of thing I was doing. Please go easy on me.
"""

import tensorflow as tf
import numpy as np

#Dataset containing thousands of human names.
#I opted to not use this dataset for training as it includes a bunch of uncommon names, and we wanted the model to learn from relativly common names.
#We use this to validate the model didn't produce a name that already exists, as it is a bit overfit.
from names_dataset import NameDataset

#Here is a class built around a previously trained model.
class Model:

    def __init__(self,model):
        
        #Load in our previous model.
        self.model=tf.keras.models.load_model(model)
        
        #The next part sets up some important variables which allow our model to build a name. I don't quite understand what is going on here, I just know I need it for other things.
        self.char_indices = dict( (chr(i+96), i) for i in range(1,27))
        self.char_indices[' '] = 0
        self.char_indices['.'] = 27

        self.indices_char = dict( (i, chr(i+96)) for i in range(1,27))
        self.indices_char[0] = ' '
        self.indices_char[27] = '.'

        self.max_char = 10

        self.char_dim = len(self.char_indices)

        #Initialize the names database for validating we don't produce a name that already exists.
        self.names_dataset = NameDataset()

    #From what I understand, the model is basically predicting what characters it thinks will go where based on what it has learned.
    def make_name(self):
        name = []
        x = np.zeros((1, self.max_char, self.char_dim))
        end = False
        i = 0
        
        while end==False:
            probs = list(self.model.predict(x)[0,i])
            probs = probs / np.sum(probs)
            index = np.random.choice(range(self.char_dim), p=probs)
            if i == self.max_char-2:
                character = '.'
                end = True
            else:
                character = self.indices_char[index]
            name.append(character)
            x[0, i+1, index] = 1
            i += 1
            #If we get a period, that marks the end of the name.
            if character == '.':
                end = True
        
        #Join together all of the predicted characters into a complete name, as well as some formatting.
        name = ''.join(name).strip(". ").capitalize()

        return name
    
    #This function is used to get a name. It basically makes a name and then runs some quality checks before presenting it.
    def get_name(self):

        good = False

        name = self.make_name()

        while good == False: 

            #We wnat to make sure the name is of reasonable length, as well as not a name that already exists.
            if len(name) < 3 or self.names_dataset.search_first_name(name):

                #If that name doesn;t pass, make a new one.
                name = self.make_name()
            
            else:
                
                #If it passes the test, we are good to go!
                good = True
        
        return name

#Generate 50 names if running standalone.
if __name__ == "__main__":
    model=Model("namegen-300.hdf5")

    for x in range(50):
        print(model.get_name())
        x+=1

################
#Ending Remarks#
################

# As stated previously, this has sort of been a baptism by fire for me when it comes to machine learning. However it has really encouraged me to learn more
# about the field as a whole. Next year, I hope to be able to produce something amazing after reasearching ML more!