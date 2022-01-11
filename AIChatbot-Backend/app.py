from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
from tensorflow.python.keras.models import load_model
import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.util import ngrams
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import wordnet
import re
import os

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)  # to start
# Session(app)
app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'  #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'
db = SQLAlchemy(app)
# app.config['SECRET_KEY'] = '3r3243f3fffdda'
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# redis = redis.from_url(redis_url)
# app.config['SESSION_REDIS'] = redis

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')

intents = json.loads(open('intent_latest.json').read())
res = pickle.load(open('res.pkl', 'rb'))
tag = pickle.load(open('tag.pkl', 'rb'))
tag_new = pickle.load(open('tag_new.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
detected_tags = []
symptoms_list = []
detected_rules = []

symptoms = [
    'Itching',  # 1
    'Skin rash',  # 2
    'Dischromic patches',  # 3
    'continuous sneezing',  # 4
    'shivering',  # 5
    'chills',  # 6
    'stomach pain',  # 7
    'acidity',  # 8
    'ulcer on tongue',  # 9
    'vomiting',  # 10
    'yellowish skin',  # 11
    'nausea',  # 12
    'indigestion',  # 13
    'patches throat',  # 14
    'high fever',  # 15
    'extra marital contacts',  # 16
    'fatigue',  # 17
    'weight loss',  # 18
    'restlessness',  # 19
    'dehydration',  # 20
    'diarrhoea',  # 21
    'cough',  # 22
    'breathlessness',  # 23
    'headache',  # 24
    'chest pain',  # 25
    'dizziness',  # 26
    'back pain',  # 27
    'neck pain',  # 28
    'lethargy',  # 29
    'sweating',  # 30
    'cramps',  # 31
    'bruising',  # 32
    'obesity',  # 33
    'anxiety',  # 34
    'joint pain',  # 35
    'knee pain',  # 36
    'hip joint pain',  # 37
    'swelling joints',  # 38
    'stiff neck',  # 39
    'loss of appetite',  # 40
    'movement stiffness',  # 41
    'painful walking',  # 42
    'blackhead',  # 43
    'scurring',  # 44
    'blister',  # 45
    'yellow crust zone',  # 46
    'muscle pain',  # 47
    'abdominal pain',  # 48
    'yellowing of eyes',  # 49
    'burning micturition',  # 50
    'spotting urination',  # 51
    'internal itching',  # 52
    'irregular sugar level',  # 53
    'excessive hunger',  # 54
    'polyuria',  # 55
    'increase appetite',  # 56
    'loss balance',  # 57
    'lack concentration',  # 58
    'Muscle weakness'  # 59
]

rules = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '9', '10', '22', '25'],
    ['1', '10', '11', '12', '40', '48', '49'],
    ['1', '2', '7', '50', '51'],
    ['10', '13', '40', '48', '52'],
    ['14', '15', '16'],
    ['18', '19', '29', '53', '33', '54', '55', '56'],
    ['10', '20', '21'],
    ['24', '26', '57', '58'],
    ['27', '28', '26', '57'],
    ['2', '6', '35', '10', '17', '12', '24', '27', '40'],
    ['23', '30', '25'],
    ['35', '28', '36', '37', '42'],
    ['59', '38', '39', '41', '42'],
    ['2', '43', '44'],
    ['2', '15', '45', '46'],
    ['6', '10', '15', '24', '30', '12', '47'],
    ['8', '13', '24', '54'],
    ['17', '31', '32', '33'],
    ['10', '17', '34', '30', '24']
]

diseases = [
    'Fungal infection',
    'Allergy',
    'GERD',
    'Chronic cholestasis',
    'Drug reaction',
    'Peptic ulcer disease',
    'AIDS',
    'Diabetes',
    'Gastroenteritis',
    'Hypertension',
    'Cervical spondylosis',
    'Dengue',
    'heart attack',
    'Osteoarthristis',
    'Arthristis',
    'Acne',
    'Impetigo',
    'Malaria',
    'Migraine',
    'Varicose veins',
    'Hypoglycemia'
]

symptoms = [" ".join(x.lower().split()) for x in symptoms]
diseases = [" ".join(x.lower().split()) for x in diseases]


def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'

    def replace(old_word):
        if wordnet.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word

    correct_tokens = [replace(word) for word in tokens]
    return correct_tokens


def clean_up_sentence(sentence):
    stopWords = set(stopwords.words('english'))
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = remove_repeated_characters(sentence_words)
    sentence_words = [word for word in sentence_words if word.isalnum()]
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    filtered_words = []
    [filtered_words.append(i) for i in sentence_words if not i in stopWords]

    bw = ngrams(filtered_words, 2)
    result = map(lambda x: ' '.join(x), list(bw))

    filtered_words.extend(list(result))
    print(filtered_words)
    return filtered_words


def bow(sentence, model):
    sentence_words = clean_up_sentence(sentence)
    if not sentence_words:
        bags = []
        return bags
    else:
        sentence_words = list(map(lambda el: [el], sentence_words))
        vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
        data_x = pd.DataFrame(res)
        my_series = data_x.squeeze()
        vectorizer.fit(my_series)
        bags = []
        for sentence in sentence_words:
            bag = vectorizer.transform(sentence).toarray()
            bags.append(bag)
        bags = np.vstack(bags)
    return bags


def predict_class(sentence, model):
    bags = bow(sentence, model)
    if (len(bags) == 0):
        return 0
    results = []
    for bag in bags:
        predict_result = model.predict(np.array([bag]))[0]
        ERROR_THRESHOLD = 0.25
        PROBABILITY_THRESHOLD = 0.80
        result = [[i, r] for i, r in enumerate(predict_result) if r > ERROR_THRESHOLD]
        result.sort(key=lambda x: x[1], reverse=True)  # sort into descending order
        results.append(result)

    # print("Results: ", results)
    return_list = []
    for result in results:
        for i in result:
            if (i[1] > PROBABILITY_THRESHOLD):
                return_list.append({'intent': classes[i[0]], 'probability': str(i[1])})
    return return_list  # return tuple of intent and probability


def getPrediction(ints):
    # ints = [i for n,i in enumerate(ints) if i not in ints[n+1:]]
    data_intents = {}
    for intent in ints:
        tag = intent['intent'].lower()
        if (tag != ''):
            detected_tags.append(tag)  # which tag in the dataset(can be redundant)
            if any(tag in symptom for symptom in symptoms):
                if (tag not in symptoms_list):
                    symptoms_list.append(tag)  # symptoms(not redundant)
                    detected_rules.append(symptoms.index(tag) + 1)  # symtomp in which rule number

            detected_diseases = []
            for detected_rule in detected_rules:
                for rule in rules:
                    if str(detected_rule) in rule:
                        detected_diseases.append(
                            diseases[rules.index(rule)])  # the rule(each symptom) corresponding to which disease
                        temp = list(set(detected_diseases))  # the disease
            if 'temp' in locals():
                detected_disease_probabilities = []
                for index, disease in enumerate(temp, start=1):
                    disease_index = diseases.index(disease)
                    rules_list = rules[disease_index]
                    total_rules = len(rules_list)
                    matched_rules = 0
                    for rule in rules_list:
                        for detected_rule in detected_rules:
                            if str(detected_rule) == rule:
                                matched_rules += 1
                    rule_probability = matched_rules / total_rules
                    detected_disease_probabilities.append(
                        {'disease': disease, 'probability': rule_probability, 'index': diseases.index(disease)})
                detected_disease_probabilities = sorted(detected_disease_probabilities, key=lambda x: x['probability'],
                                                        reverse=True)  # descending order

        data_intents['detected_tags'] = detected_tags
        data_intents['symptoms_list'] = symptoms_list
        data_intents['detected_rules'] = detected_rules
        data_intents['detected_diseases'] = detected_diseases

    if 'detected_disease_probabilities' in locals():
        data_intents['temp'] = temp
        data_intents['detected_disease_probabilities'] = detected_disease_probabilities
        # print("Diseases: ", temp)
        # print("Probabilities: ", detected_disease_probabilities)

    return data_intents


# def getResposne(ints):
#     prediction = getPrediction(ints)
#     list_of_intents = intents['intents']
#     result = ints[-1]['intent']
#     if (result == 'no_other_symptoms'):
#         result = "Hi, sorry to say that I can't find related diseases in your case."
#         print(result)
#     else:
#         for i in list_of_intents:
#             if (i['tag'] == result):
#                 if (len(symptoms_list) == 0):
#                     result = random.choice(i['responses'])
#                     # print(result)
#                 elif (len(symptoms_list) < 2 and result != 'no_other_symptoms'):
#                     result = random.choice(i['responses'])
#                     print(result) #NEED
#                     inp_moresym = input().lower().strip()
#                     if 'no' in inp_moresym:
#                         result = "I have diagnosed your symptoms and I guess you are having "
#                         result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
#                     else:
#                         abc = predict_class(inp_moresym, model)
#                         #tmp = []
#                         for result in abc:
#                             ints.append(result)
#                         prediction = getPrediction(ints)
#                         result = "I have diagnosed your symptoms and I guess you are having "
#                         result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
#                 elif (len(symptoms_list) >= 2):
#                     index_highest_disease_probability = prediction['detected_disease_probabilities'][0]['index']
#                     for rule in rules[index_highest_disease_probability]:
#                         if (int(rule) not in detected_rules):
#                             result = "Hi, based on my dataset, people that have your symptoms are also have " + \
#                                      symptoms[int(rule) - 1] + " , do you also feel it? symtoms no: " + rule
#                             print(result) #NEED
#                             user_input = input().lower().strip()
#                             if 'yes' in user_input:
#                                 ints.append({'intent': symptoms[int(rule) - 1], 'probability': 1})
#                                 prediction = getPrediction(ints)
#                                 result = "I have diagnosed your symptoms and I guess you are having "
#                                 result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
#                             if 'no' in user_input:
#                                 result = "I have diagnosed your symptoms and I guess you are having "
#                                 result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
#     return result

# def symptoms_m2():
#     session["symptoms_list"] = symptoms_list
#     session["prediction_1"] = prediction['detected_disease_probabilities'][0]['disease']
#     session["ints"] = ints
#     session["symptoms"] = symptoms
#     session["detected_rules"] = detected_rules
#     for rule in checkrules:
#         if (rule not in detected_rules):
#             result = "Hi, based on my dataset, people that have your symptoms are also have " + \
#                      symptoms[rule - 1] + " , do you also feel it? symtoms no: " + str(rule)
#         session["rule"] = rule
#         user_input = input().lower().strip()#need
#         if 'yes' in user_input:
#             ints.append({'intent': symptoms[int(rule) - 1], 'probability': 1})
#             prediction = getPrediction(ints)
#             result = "I have diagnosed your symptoms and I guess you are having "
#             result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
#         if 'no' in user_input:
#             result = "I have diagnosed your symptoms and I guess you are having "
#             result += prediction['detected_disease_probabilities'][0]['disease'] + " . "

class Symptom1(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sym_list = db.Column(db.Integer)
    intent_n = db.Column(db.String(25))
    intent_p = db.Column(db.Float(25))
    pred_dis = db.Column(db.String(25))
    pred_pro = db.Column(db.Float(25))
    pred_list = db.Column(db.JSON,nullable=False)

    def __repr__(self):
        return f"Symptom1('{self.id}','{self.symptoms_list}','{self.intent_n}','{self.intent_p}','{self.pred_dis}','{self.pred_pro}','{self.pred_list}')"

class Symptom2(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pred_dis = db.Column(db.String(25))
    pred_pro = db.Column(db.Float(25))
    intent_list = db.Column(db.JSON,nullable=False)
    sym_list = db.Column(db.Integer)
    pred_list = db.Column(db.JSON,nullable=False)

    def __repr__(self):
        return f"Symptom2('{self.id}','{self.pred_dis}','{self.pred_pro}','{self.intent_list}','{self.sym_list}','{self.pred_list}')"

class Symptom3(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sym = db.Column(db.String(25))

    def __repr__(self):
        return f"Symptom3('{self.id}','{self.sym}')"

@app.route("/bot", methods=["POST"])
def response():
    global symptoms

    msg = dict(request.form)['query']
    # start = Initiate.query.first()
    item = Symptom1.query.filter_by(id=1).first()
    item1 = Symptom2.query.filter_by(id=1).first()

    if item or item1 != None:
        if item != None:
            if int(item.sym_list) == 1:
                if 'no' in msg:
                    # prediction = session["prediction_1"]
                    # result = "I have diagnosed your symptoms and I guess you are having " + item.pred_dis
                    # result += ", probability =  " + str(item.pred_pro * 100) + "% ."

                    result = "Thank you, after analysing the information you have given us." \
                             "\n You may have symptoms " + item.intent_n + " and may suffering from " + \
                             item.pred_list[0]['disease'] + " problem"
                    # result += prediction['detected_disease_probabilities'][0]['disease']
                    # result += ", probability =  " + str(
                    #     (prediction['detected_disease_probabilities'][0]['probability']) * 100) + "% ."
                    result += ", probability =  " + str(round(item.pred_list[0]['probability'] * 100, 2)) + "% .\n"
                    result += "Other disease problem you may have as listed below: \n"
                    len_disease = len(item.pred_list)
                    disease_list = [item.pred_list[x]['disease'] for x in
                                    range(1, len_disease)]
                    prob_list = [str(round(item.pred_list[x]['probability'] * 100, 2)) + "%" for x in
                                 range(1, len_disease)]
                    new_list = np.array(disease_list, dtype=object) + " " + np.array(prob_list, dtype=object)
                    new_list = new_list.tolist()
                    result += ("\n".join(new_list))

                    list_of_intents = intents['intents']

                    for i in list_of_intents:
                        if (i['tag'].lower() == item.pred_list[0]['disease']):
                            response = ''.join(i['responses'])
                            result += "\nDefinition: \n" + response
                    # for key in list(session.keys()):
                    #     session.pop(key)
                    # db.drop_all()
                    db.session.query(Symptom1).delete()
                    db.session.commit
                    symptoms_list.clear()
                    detected_rules.clear()
                    detected_tags.clear()

                else:
                    abc = predict_class(msg, model)
                    # ints = session["ints"]
                    # ints = []
                    item = Symptom1.query.filter_by(id=1).first()
                    int_name = item.intent_n
                    int_prob = item.intent_p
                    dic0 = {}
                    dic1 = {}
                    dic0["intent"] = int_name
                    dic1['probability'] = str(int_prob)
                    dic0.update(dic1)
                    ints = []
                    ints.append(dic0)

                    # tmp = []
                    for result in abc:
                        ints.append(result)
                    prediction = getPrediction(ints)
                    # result = "I have diagnosed your symptoms and I guess you are having "
                    # result += prediction['detected_disease_probabilities'][0]['disease']
                    # result += ", probability =  " + str(
                    #     (prediction['detected_disease_probabilities'][0]['probability']) * 100) + "% ."
                    len_disease = len(prediction['detected_disease_probabilities'])
                    result = "Thank you, after analysing the information you have given us." \
                             "\n You may have symptoms " + ', '.join(
                        prediction['symptoms_list']) + " and may suffering from " + item.pred_dis + " problem"
                    result += ", probability =  " + str(round
                                                        (prediction['detected_disease_probabilities'][0][
                                                             'probability'] * 100, 2)) + "% .\n"
                    result += "Other disease problem you may have as listed below: \n"
                    disease_list = [prediction['detected_disease_probabilities'][x]['disease'] for x in
                                    range(1, len_disease)]
                    prob_list = [
                        str(round(prediction['detected_disease_probabilities'][x]['probability'] * 100, 2)) + "%" for x
                        in range(1, len_disease)]
                    new_list = np.array(disease_list, dtype=object) + " " + np.array(prob_list, dtype=object)
                    new_list = new_list.tolist()
                    result += ("\n".join(new_list))

                    list_of_intents = intents['intents']

                    for i in list_of_intents:
                        if (i['tag'].lower() == item.pred_list[0]['disease']):
                            response = ''.join(i['responses'])
                            result += "\nDefinition: \n" + response

                    db.session.query(Symptom1).delete()
                    db.session.commit
                    symptoms_list.clear()
                    detected_rules.clear()
                    detected_tags.clear()

        else:
            if (int(item1.sym_list) >= 2):
                # prediction = session["prediction_1"]
                # ints = session["ints"]
                # symptoms = session["symptoms"]
                # rule = session["rule"]
                if 'yes' in msg:
                    item = Symptom2.query.filter_by(id=1).first()
                    item1 = Symptom3.query.order_by(Symptom3.id.desc()).first()
                    ints = item.intent_list
                    symptom = item1.sym
                    ints.append({'intent': symptom, 'probability': 1})
                    # ints.append({'intent': symptoms[rule - 1], 'probability': 1})
                    prediction = getPrediction(ints)
                    len_disease = len(prediction['detected_disease_probabilities'])
                    # result = "I have diagnosed your symptoms and I guess you are having "
                    # result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
                    # result += ", probability =  " + str(
                    #     (prediction['detected_disease_probabilities'][0]['probability']) * 100) + "% ."
                    result = "Thank you, after analysing the information you have given us." \
                             "\n You may have symptoms " + ', '.join(
                        prediction['symptoms_list']) + " and may suffering from " + item.pred_dis + " problem"
                    result += ", probability =  " + str(round
                                                        (prediction['detected_disease_probabilities'][0][
                                                             'probability'] * 100, 2)) + "% .\n"
                    result += "Other disease problem you may have as listed below: \n"
                    disease_list = [prediction['detected_disease_probabilities'][x]['disease'] for x in
                                    range(1, len_disease)]
                    prob_list = [
                        str(round(prediction['detected_disease_probabilities'][x]['probability'] * 100, 2)) + "%" for x
                        in range(1, len_disease)]
                    new_list = np.array(disease_list, dtype=object) + " " + np.array(prob_list, dtype=object)
                    new_list = new_list.tolist()
                    result += ("\n".join(new_list))

                    list_of_intents = intents['intents']

                    for i in list_of_intents:
                        if (i['tag'].lower() == item.pred_list[0]['disease']):
                            response = ''.join(i['responses'])
                            result += "\nDefinition: \n" + response

                    # for key in list(session.keys()):
                    #     session.pop(key)
                    db.session.query(Symptom2).delete()
                    db.session.query(Symptom3).delete()
                    db.session.commit
                    symptoms_list.clear()
                    detected_rules.clear()
                    detected_tags.clear()

                else:
                    item = Symptom2.query.filter_by(id=1).first()
                    ints = item.intent_list
                    result = [d['intent'] for d in ints]
                    sym_list = []
                    [sym_list.append(x) for x in result if x not in sym_list]
                    # result = "I have diagnosed your symptoms and I guess you are having " + item.pred_dis
                    # result += ", probability =  " + str(item.pred_pro * 100) + "% ."
                    result = "Thank you, after analysing the information you have given us." \
                             "\n You may have symptoms " + ', '.join(
                        sym_list) + " and may suffering from " + item.pred_dis + " problem"
                    result += ", probability =  " + str(round(item.pred_pro * 100, 2)) + "% .\n"
                    result += "Other disease problem you may have as listed below: \n"
                    len_disease = len(item.pred_list)
                    disease_list = [item.pred_list[x]['disease'] for x in
                                    range(1, len_disease)]
                    prob_list = [str(round(item.pred_list[x]['probability'] * 100, 2)) + "%" for x in
                                 range(1, len_disease)]
                    new_list = np.array(disease_list, dtype=object) + " " + np.array(prob_list, dtype=object)
                    new_list = new_list.tolist()
                    result += ("\n".join(new_list))

                    list_of_intents = intents['intents']

                    for i in list_of_intents:
                        if (i['tag'].lower() == item.pred_list[0]['disease']):
                            response = ''.join(i['responses'])
                            result += "\nDefinition: \n" + response

                    db.session.query(Symptom2).delete()
                    db.session.commit
                    symptoms_list.clear()
                    detected_rules.clear()
                    detected_tags.clear()
    else:
        # session.clear()
        ints = predict_class(msg, model)
        if ints == int(0):
            ints = str(ints)
            ints = list(map(int, ints))
            ints.clear()

        if (len(ints) == 0):
            ints = [{"intent": "no_other_symptoms", "probability": "1.0"}]

        prediction = getPrediction(ints)
        list_of_intents = intents['intents']
        result = ints[-1]['intent']
        if (result == 'no_other_symptoms'):
            result = "Hi, sorry to say that I can't find related diseases in your case."
        else:
            for i in list_of_intents:
                if (i['tag'] == result):
                    if (len(symptoms_list) == 0):
                        result = random.choice(i['responses'])
                    elif (len(symptoms_list) == 1):
                        result = random.choice(i['responses'])
                        # session["symptoms_list"] = symptoms_list
                        # session["prediction_1"] = prediction
                        # session["ints"] = ints
                        ints_n = ints[0]['intent']
                        ints_p = ints[0]['probability']
                        # session["prediction_1"] = {key:prediction[key] for key in['detected_disease_probabilities']}
                        store_disease = {key: prediction[key] for key in ['detected_disease_probabilities']}
                        pred_disease = store_disease['detected_disease_probabilities'][0]['disease']
                        pred_proba = store_disease['detected_disease_probabilities'][0]['probability']
                        me = Symptom1(sym_list=len(symptoms_list), intent_n=ints_n, intent_p=ints_p,
                                      pred_dis=pred_disease, pred_pro=pred_proba,
                                      pred_list=prediction['detected_disease_probabilities'])
                        db.session.add(me)
                        db.session.commit()

                    elif (len(symptoms_list) >= 2):
                        index_highest_disease_probability = prediction['detected_disease_probabilities'][0]['index']
                        rule_chk = rules[index_highest_disease_probability]
                        integer_map = map(int, rule_chk)
                        rule_chk = list(integer_map)
                        check_rules = all(item in detected_rules for item in rule_chk)

                        if check_rules is True:
                            # result = "I have diagnosed your symptoms and I guess you are having "
                            # result += prediction['detected_disease_probabilities'][0]['disease']
                            # result += ", probability =  " + str(
                            #     (prediction['detected_disease_probabilities'][0]['probability']) * 100) + "% ."

                            len_disease = len(prediction['detected_disease_probabilities'])
                            result = "Thank you, after analysing the information you have given us." \
                                     "\n You may have symptoms " + ', '.join(
                                prediction['symptoms_list']) + " and may suffering from " + \
                                     prediction['detected_disease_probabilities'][0]['disease'] + " problem"
                            result += ", probability =  " + str(round(prediction['detected_disease_probabilities'][0][
                                                                          'probability'], 2) * 100) + "% .\n"
                            result += "Other disease problem you may have as listed below: \n"
                            disease_list = [prediction['detected_disease_probabilities'][x]['disease'] for x in
                                            range(1, len_disease)]
                            prob_list = [str(round(prediction['detected_disease_probabilities'][x]['probability'] * 100,
                                                   2)) + "%" for x in range(1, len_disease)]
                            new_list = np.array(disease_list, dtype=object) + " " + np.array(prob_list, dtype=object)
                            new_list = new_list.tolist()
                            result += ("\n".join(new_list))

                            list_of_intents = intents['intents']

                            for i in list_of_intents:
                                if (i['tag'].lower() == prediction['detected_disease_probabilities'][0]['disease']):
                                    response = ''.join(i['responses'])
                                    result += "\nDefinition: \n" + response

                            symptoms_list.clear()
                            detected_rules.clear()
                            detected_tags.clear()
                            # session.clear()
                        else:
                            # session["symptoms_list"] = symptoms_list
                            # session["prediction_1"] = prediction
                            # session["ints"] = ints
                            # session["symptoms"] = symptoms

                            store_disease = {key: prediction[key] for key in ['detected_disease_probabilities']}
                            pred_disease = store_disease['detected_disease_probabilities'][0]['disease']
                            pred_proba = store_disease['detected_disease_probabilities'][0]['probability']
                            me = Symptom2(pred_dis=pred_disease, pred_pro=pred_proba, intent_list=ints,
                                          sym_list=len(symptoms_list),
                                          pred_list=prediction['detected_disease_probabilities'])
                            db.session.add(me)
                            db.session.commit()

                            for rule in rule_chk:
                                if (rule not in detected_rules):
                                    result = "Hi, based on my dataset, people that have your symptoms are also have " + \
                                             symptoms[rule - 1] + " , do you also feel it? "
                                    # symptoms no: " + str(rule)
                                    me1 = Symptom3(sym=symptoms[rule - 1])
                                    db.session.add(me1)
                                    db.session.commit()

                                # print(result)#need
                                # user_input = input().lower().strip()#need
                                # if 'yes' in user_input:
                                #     ints.append({'intent': symptoms[int(rule) - 1], 'probability': 1})
                                #     prediction = getPrediction(ints)
                                #     result = "I have diagnosed your symptoms and I guess you are having "
                                #     result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
                                # if 'no' in user_input:
                                #     result = "I have diagnosed your symptoms and I guess you are having "
                                #     result += prediction['detected_disease_probabilities'][0]['disease'] + " . "
    db.session.commit()
    return jsonify({"response": result})


# @app.route('/processor', methods=["GET", "POST"])
# def chatbotResponse():
#
#     if request.method == 'POST':
#         the_question = request.form['question']
#
#         response = chatbot_response(the_question)
#
#     return jsonify({"response": response })


#
# print("You can start interact with the chatbot now.")
# while True:
#     user_input = input("What is your question?").lower().strip()
#     # user_input = "i have bad breathe, fever, cannot sleep, headache"
#     if (user_input != ""):
#         print("You: =====>>>", user_input)
#         print("Bot: =====>>>", chatbot_response(user_input))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

