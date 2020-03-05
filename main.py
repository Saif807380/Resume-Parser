import inspect
import logging
import os
import sys
import pandas as pd
import spacy
import yaml
import re
from lib import *
from field_extraction import *

def transform(observations, nlp,resume_string):
    # TODO Docstring
    logging.info('Begin transform')
    # Extract candidate name
    observations['candidate_name'] = candidate_name_extractor(resume_string, nlp)
    # Extract contact fields
    observations['email'] = term_match(resume_string, EMAIL_REGEX)
    observations['phone'] = term_match(resume_string, PHONE_REGEX)
    # Extract skills
    observations = extract_fields(observations,resume_string)
    # Archive schema and return
    logging.info('End transform')
    return observations, nlp

def main():
    resume_string = '''SAIF KAZI
saif1204kazi@gmail.com
CE Undergrad, Graduating 2022
8104679894
Mumbai
Data Science enthusiast having keen interest
in designing complete solutions.
linkedin.com/in/saif-k-647640132 in
github.com/Saif807380 (>
EDUCATION
SKILLS
B.Tech in Computer Engineering
Veermata Jijabai Technological Institute
C
C+ +
Python
Dart
Flutter
(VJTI)
Machine Learning
Deep Learning
07/2018 -Present
CPI - 9.0
Neural Networks
JavaScript
HTML
CSS
HSC
Bootstrap
Java
Shri T.P. Bhatia College of Science
06/2016-04/2018
Marks - 94.92%
ACHIEVEMENTS
PROJECTS
Smart India Hackathon (SIH)
Qualified among the top 10 teams of VITI SIH internal hackathon
Voice Prescription (01/2020)
and will be representing VITI in the upcoming SIH 2020.
- A flutter app for digitisation of the process of creating
prescription for the patients by the doctor.
MHT-CET Cell
Developed as a part of VJTI's SIH internal hackathon.
Secured 58th rank in the state with aggregate score of 183/200.
Movie Recommender App (09/2019 - 12/2019)
Managing Workshops
Successfully conducted and managed C language and Web
A Flutter app that recommends movies based on the users
Development Workshop as a member of the Community of
selected genres and liked movies.
Coders, VITI
An Application of recommender system.
Healthify (10/2019)
ORGANIZATIONS
An app that helps identify diseases based on the symptoms,
ind out diseases that are widespread in any given area,
calculate BMI and dish out diet advice based on it.
Community of Coders, VJTI (06/2019 - Present)
Developed as a part of KJHACK 2019
Active Member
VJTI APP (05/2019 - 08/2019)
The VJTI-APP is an application designed for the purpose of
CERTIFICATIONS
easy notes sharing between the students and the teacher.
The application also features an events section and a map
Neural Networks and Deep Learning
section.
Developed under COC, VJTI's summer project internship
programme.
Improving Deep Neural Networks C
Structuring Machine Learning Projects C
Convolutional Neural Networks C
'''
    logging.getLogger().setLevel(logging.INFO)
    nlp = spacy.load('en')
    observations = dict()
    observations, nlp = transform(observations, nlp,resume_string)
    print(observations)
    pass

main()