"""
Read in a note for CHRIS and make a word doc.

Stephen Pollard

2020-08-10

"""


import sys
# ~ import oyaml as yaml
import ruamel.yaml
import re

# Installed
# ~ from docx import Document
# ~ from docx.enum.text import WD_BREAK

from Ptsurvey import Survey
from Writeptnote import Ptnote


def main():
    big() # works mostly at least


# Does not produce correct results, so far as I can tell
def big():
    print("Testing survey and ptnote on samples/Sample BigCHRIS input")
    bodytext = read_survey_bodytext("samples/Sample BigCHRIS input")
    survey = Survey(bodytext)
    # ~ print_survey_data(survey.data)
    note = Ptnote(survey)
    note.export_to_docx("bigchris_output.docx")
    # ~ print(note.whole_note)

def print_survey_data(survey_data):
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.dump(survey_data, sys.stdout)

# Do whatever I have to do to pass the data in this file into survey()
def read_survey_bodytext(filename):
    bodytext = []
    with open(filename) as f:
        for i in f.readlines():
            if "\xa0" in i:
                i = i.replace("\xa0", " ")
            bodytext.append(i.strip())
    # Find the start of the survey
    startIndex = 0 # necessary this time
    for i in bodytext:
        if i == "A survey has been completed.":
            startIndex = bodytext.index(i)
    bodytext = bodytext[startIndex:]
    for x in bodytext:
        if x == '':
            bodytext.pop(bodytext.index(x))

    return bodytext


if __name__ == "__main__":
    main()
