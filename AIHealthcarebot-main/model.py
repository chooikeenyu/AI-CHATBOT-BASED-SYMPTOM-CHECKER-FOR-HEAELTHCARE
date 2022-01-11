import random
from keras.optimizers import gradient_descent_v2
from keras.optimizers import adam_v2
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
import numpy as np
import pickle
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
lemmatizer = WordNetLemmatizer()
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
# from keras import callbacks
#
# earlystopping = callbacks.EarlyStopping(monitor ="accuracy",
#                                         mode ="max", patience = 300,
#                                         restore_best_weights = True)
classes = []
documents = []

ignore_words = [',', '|']

combined_intents = open('intent_latest.json').read()

intents = json.loads(combined_intents)

stopWords = set(stopwords.words('english'))

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern) #tokenize each word
        w = [word for word in w if word.isalnum()] #check if character is alphanumeric(a-z,0-9)
        w = [lemmatizer.lemmatize(word.lower()) for word in w if word not in ignore_words] #lemmatize each word

        filtered_words = [i for i in w if not i in stopWords] #filter the word that are stop words

        w = filtered_words

        documents.append((w, intent['tag']))#add each wtoken and the tag

    if intent['tag'] not in classes:
        classes.append(intent['tag'])


classes = sorted(list(set(classes))) #sort classes

pickle.dump(classes, open('classes.pkl', 'wb'))

vectorizer = TfidfVectorizer(ngram_range=(1, 3),stop_words='english')

new_bag = [] #[['Hi'],['Hello'],['What'],['Good','day','Good day']]
for doc in documents:
    pattern_words = doc[0]                  #each pattern
    new_bag.append(pattern_words)           #trianing data
res = []   #['Hi,'Hello','What','GooddayGood day']
res = [' '.join(ele) for ele in new_bag] # change list of list into list of string


new_tag = [] #create tag
for i in documents:
    tag = i[1]
    new_tag.append(tag)


pickle.dump(new_tag,open('tag.pkl','wb'))
pickle.dump(res, open('res.pkl', 'wb'))

tfidf_vectors = vectorizer.fit_transform(res).toarray()     #tfidf (array)
train_x = tfidf_vectors.tolist() #change array to list of list

bag_y = [] # create series of tag
for doc in documents:
    pattern_words = doc[1]
    bag_y.append(pattern_words)
trainy_1 = []
trainy_1 = [''.join(ele) for ele in bag_y]
df_y = pd.DataFrame(trainy_1)
my_series = df_y.squeeze()

pickle.dump(my_series, open('tag_new.pkl', 'wb'))

le = LabelEncoder()
training_data_tags_le = pd.DataFrame({"tags": le.fit_transform(my_series)})
training_data_tags_dummy_encoded = pd.get_dummies(training_data_tags_le["tags"]).to_numpy()


#(trainX, testX, trainY, testY) = train_test_split(np.array(train_x), training_data_tags_dummy_encoded,test_size=0.4, random_state=42)


model = Sequential() #to create models layer by layers
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu')) #first layer 128 neurons, input_shape not neurons, is like a tensor
# (multi-dimensional array)
model.add(Dropout(0.3)) #dropout - randomly selected neurons are ignored during training
model.add(Dense(64,activation='relu')) # second layer 64 neurons
model.add(Dropout(0.3))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(training_data_tags_dummy_encoded[0]), activation='softmax')) #output layer stochastic gradient descent with nestrov accelerated gradient
sgd = gradient_descent_v2.SGD(learning_rate=0.02, decay=1e-6, momentum=0.9, nesterov=True)
adam = adam_v2.Adam(learning_rate=0.0003)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy']) # accuracy performance, Gradient Descent,
history = model.fit(np.array(train_x), training_data_tags_dummy_encoded , epochs=400, batch_size=8, verbose=1)

#model.fit(trainX,trainY, epochs=300, batch_size=8, verbose=1,validation_data=(testX,testY))
# predictions = model.predict(testX,batch_size=8)
# print(classification_report(testY.argmax(axis=1),predictions.argmax(axis=1)))
# y_pred=np.argmax(model.predict(testX), axis=1)
# y_test=np.argmax(testY, axis=1)
# cm = confusion_matrix(y_test, y_pred)


model.save("chatbot_model.h5",model)

print("model created")
