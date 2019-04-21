# -*- coding: utf-8 -*-
import json, requests, random, re ,psycopg2
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
import nltk
from nltk.corpus import wordnet as wn
from langdetect import detect
from mtranslate import translate
import goslate
import difflib
from difflib import SequenceMatcher
nltk.data.path.append('nltk_data')
# Create your views here.
PAGE_ACCESS_TOKEN = "EAAHEVy9y29gBAJWYSHQm8aQZCG5GrMwW0r4AmtDrhZCCJdCLZCZA0VO6ShNIR4jLsmyHENlV4JesqowWcJEVrgWIAMnnCOHyN9iHetFZCLSAv73eC6WTr677ZBG4ZC8Y1Y4Ip5f7H31JHfmkiM3SP2WwGKZAu6iuHOZCCJolACIVq5wZDZD"
VERIFY_TOKEN = "206296415366301"
conn = psycopg2.connect(database="d5tl5514j1t7c1", user="bbtegilfuzvzdl", password="43b1343c217ccbb232c85c68ce4280e61031025f0972fa04b754c40a4a5813c1", host="ec2-23-21-216-174.compute-1.amazonaws.com", port="5432")                    
# Helper function
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
   
    reply =  nlp(recevied_message)
    
    post_message_url = 'https://graph.facebook.com/v2.12/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":reply}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg) 
    
       


def penn_to_wn(tag):
    if tag.startswith('N'):
        return 'n'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('J'):
        return 'a'
    if tag.startswith('R'):
        return 'r'
    return None

 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    # if detect(sentence1) is not "en":


    # Tokenize and tag
    sentence1 = nltk.pos_tag(nltk.tokenize.word_tokenize(sentence1))
    sentence2 = nltk.pos_tag(nltk.tokenize.word_tokenize(sentence2))
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
    score, count = 0.0, 0
    # For each word in the first sentence
    for syn1 in synsets1:
        arr_simi_score = []
        for syn2 in synsets2:

            simi_score = syn1.path_similarity(syn2)
            if simi_score is not None:
                arr_simi_score.append(simi_score)
            if (len(arr_simi_score) > 0):
                best = max(arr_simi_score)
                score += best
            count += 1
    # Average the values

    if count !=0:
        score /= count
    return score
def nlp(receve):
    
    cur = conn.cursor()
    cur.execute("SELECT * from faq")
    sentences = cur.fetchall()
    
    loc = detect(receve)
    cur = conn.cursor()
    cur.execute("SELECT * from faq")
    sentences = cur.fetchall()
    Max=-1
    i=0
    id=0
    ar=2
    similarity_diff = -1
    sim_diff = []
    simo = []
    curr_question = []
    focus_sentence=receve
    if detect(receve) is not 'en':
        ar=1
        focus_sentence = translate(focus_sentence,"en","auto")
    for sentence in sentences:
        sentence1=sentence
        S = sentence_similarity(focus_sentence, sentence1[0])
        if S > Max:
            Max = S
            curr_question = sentence1
            id = i
        elif S == Max or S - Max <=0.1:
            sim_diff.append([curr_question[0], curr_question[ar]])
            sim_diff.append([sentence1[0], sentence1[ar]])

        i += 1
    if Max <= 0.2:
        replay = "please make sure your question is not out of my scope."
    else:
        #replay = sentences[id][ar]
        if detect(receve) is not 'en':
            replay = sentences[id][1]
        else:
            replay = sentences[id][2]
    for elem in sim_diff:
        sim = difflib.SequenceMatcher(None, elem[0], focus_sentence)
        sim = sim.ratio()
        simo.append(sim)
        if sim > similarity_diff:
            similarity_diff = sim
            replay = elem[1]
    
    return replay

        



class FCIView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')
        except KeyError:
            html="<html><body>hello</body></html"
            return render(request ,'index.html')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

                         

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    print(message)
                    global focus_message
                    focus_message = message
                    post_facebook_message(message['sender']['id'], message['message']['text'])
                    


        return HttpResponse()

