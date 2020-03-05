import logging
import os
import re
import subprocess
from spacy.matcher import PhraseMatcher
import pandas
import yaml


CONFS = None

def load_confs(confs_path='config.yaml'):
    # TODO Docstring
    global CONFS

    if CONFS is None:
        try:
            CONFS = yaml.load(open(confs_path),Loader=yaml.FullLoader)
        except IOError:
            confs_template_path = confs_path + '.template'
            logging.warn(
                'Confs path: {} does not exist. Attempting to load confs template, '
                'from path: {}'.format(confs_path, confs_template_path))
            CONFS = yaml.load(open(confs_template_path))
    return CONFS

def get_conf(conf_name):
    return load_confs()[conf_name]

def term_count(string_to_search, term, nlp):
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
        matcher = PhraseMatcher(nlp.vocab)
        pattern_list = [term]
        pattern = [nlp(term) for term in pattern_list]
        matcher.add(term,None,*pattern)
        found_matches = matcher(nlp(string_to_search.lower()))
        return len(found_matches)
        # regular_expression = re.compile(term, re.IGNORECASE)
        # result = re.findall(regular_expression, string_to_search)
        # return len(result)
    except Exception:
        logging.error('Error occurred during regex search')
        return 0

# def term_match(string_to_search, term):
#     """
#     A utility function which return the first match to the `regex_pattern` in the `string_to_search`
#     :param string_to_search: A string which may or may not contain the term.
#     :type string_to_search: str
#     :param term: The term to search for the number of occurrences for
#     :type term: str
#     :return: The first match of the `regex_pattern` in the `string_to_search`
#     :rtype: str
#     """
#     try:
#         # if(term!=r"^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$"):
#         regular_expression = re.compile(term, re.IGNORECASE)
#         print(regular_expression)
#         result = re.findall(regular_expression, string_to_search)
#         if len(result) > 0:
#             return result[0]
#         else:
#             return None
#     except Exception:
#         logging.error('Error occurred during regex search')
#         return None


def regex_match(string_to_search, term):
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
        result = re.findall(regular_expression, string_to_search)
        if len(result) > 0:
            return result[0]
        else:
            return None
    except Exception:
        logging.error('Error occurred during regex search')
        return None