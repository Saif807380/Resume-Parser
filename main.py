import inspect
import logging
import os
import sys
import pandas as pd
import spacy
import yaml
import re
from pathlib import Path
import csv
from lib import *
from ResumeParser.field_extraction import *
from ResumeParser.generate_top_skills import *

EMAIL_REGEX = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
PHONE_REGEX = r"\+?\d[\d -]{8,12}\d"
#\(?(\d{3})?\)?[\s\.-]{0,2}?(\d{3})[\s\.-]{0,2}(\d{4})


def transform(observations, nlp,resume_string):
    logging.info('Begin transform')
    observations['candidate_name'] = candidate_name_extractor(resume_string, nlp)
    observations['email'] = regex_match(resume_string, EMAIL_REGEX)
    observations['phone'] = regex_match(resume_string, PHONE_REGEX)
    observations = extract_fields(observations,resume_string,nlp)
    return observations, nlp

def main():
    resume_string = '''
    Add the string here
'''
    logging.getLogger().setLevel(logging.INFO)
    nlp = spacy.load('en')
    observations = dict()
    observations, nlp = transform(observations, nlp,resume_string)
    for k,v in observations.items():
        print(f'{k:{30}} - {str(v):>{50}}')
    big_dict,top_skills,top_titles = extract_top_skills(observations)
    print(big_dict)
    print(top_skills)
    print(top_titles)
    pass

main()