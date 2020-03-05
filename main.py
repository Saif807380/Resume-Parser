import inspect
import logging
import os
import sys
import pandas as pd
import spacy
import yaml
import re
# print(os.getcwd())
# from bin import field_extraction
# from bin import lib

CONFS = None

def load_confs(confs_path='config.yaml'):
    # TODO Docstring
    global CONFS

    if CONFS is None:
        try:
            CONFS = yaml.load(open(confs_path))
        except IOError:
            confs_template_path = confs_path + '.template'
            logging.warn(
                'Confs path: {} does not exist. Attempting to load confs template, '
                'from path: {}'.format(confs_path, confs_template_path))
            CONFS = yaml.load(open(confs_template_path))
    return CONFS

def get_conf(conf_name):
    return load_confs()[conf_name]

def term_count(string_to_search, term):
    """
    A utility function which counts the number of times `term` occurs in `string_to_search`
    :param string_to_search: A string which may or may not contain the term.
    :type string_to_search: str
    :param term: The term to search for the number of occurrences for
    :type term: str
    :return: The number of times the `term` occurs in the `string_to_search`
    :rtype: int
    """
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return len(result)
    except Exception:
        logging.error('Error occurred during regex search')
        return 0

def term_match(string_to_search, term):
    """
    A utility function which return the first match to the `regex_pattern` in the `string_to_search`
    :param string_to_search: A string which may or may not contain the term.
    :type string_to_search: str
    :param term: The term to search for the number of occurrences for
    :type term: str
    :return: The first match of the `regex_pattern` in the `string_to_search`
    :rtype: str
    """
    try:
        # if(term!=r"^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$"):
        regular_expression = re.compile(term, re.IGNORECASE)
        print(regular_expression)
        result = re.findall(regular_expression, string_to_search)
        if len(result) > 0:
            return result[0]
        else:
            return None
    except Exception:
        logging.error('Error occurred during regex search')
        return None


EMAIL_REGEX = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
PHONE_REGEX = r"((\+*)((0[ -]+)*|(91 )*)(\d{12}+|\d{10}+))|\d{5}([- ]*)\d{6}"

#\(?(\d{3})?\)?[\s\.-]{0,2}?(\d{3})[\s\.-]{0,2}(\d{4})
def candidate_name_extractor(input_string, nlp):

    doc = nlp(input_string)

    # Extract entities
    doc_entities = doc.ents
    print(doc_entities)
    # Subset to person type entities
    doc_persons = filter(lambda x: x.label_ == 'PERSON', doc_entities)
    doc_persons = filter(lambda x: len(x.text.strip().split()) >= 2, doc_persons)
    doc_persons = map(lambda x: x.text.strip(), doc_persons)
    doc_persons = list(doc_persons)

    # Assuming that the first Person entity with more than two tokens is the candidate's name
    if len(doc_persons) > 0:
        return doc_persons[0]
    return "NOT FOUND"

def extract_fields(df,resume_string):
    for extractor, items_of_interest in get_conf('extractors').items():
        df[extractor] = extract_skills(resume_string, extractor, items_of_interest)
    return df

def extract_skills(resume_text, extractor, items_of_interest):
    potential_skills_dict = dict()
    matched_skills = set()

    # TODO This skill input formatting could happen once per run, instead of once per observation.
    for skill_input in items_of_interest:

        # Format list inputs
        if type(skill_input) is list and len(skill_input) >= 1:
            potential_skills_dict[skill_input[0]] = skill_input

        # Format string inputs
        elif type(skill_input) is str:
            potential_skills_dict[skill_input] = [skill_input]
        else:
            logging.warn('Unknown skill listing type: {}. Please format as either a single string or a list of strings'
                         ''.format(skill_input))

    for (skill_name, skill_alias_list) in potential_skills_dict.items():

        skill_matches = 0
        # Iterate through aliases
        for skill_alias in skill_alias_list:
            # Add the number of matches for each alias
            skill_matches += term_count(resume_text, skill_alias.lower())

        # If at least one alias is found, add skill name to set of skills
        if skill_matches > 0:
            matched_skills.add(skill_name)
    return matched_skills


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

main()