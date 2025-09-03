"""
Read in a note for the 99483 survey and make a word doc.

So far as I can tell, this works perfectly. There are no complaints from
Survey99483 or from Ptnote99483.

Stephen Pollard

2020-08-14

"""


import sys
import oyaml as yaml
import ruamel.yaml
import re

# Installed
# ~ from docx import Document
# ~ from docx.enum.text import WD_BREAK

from Ptsurvey import Survey99483
from Writeptnote import Ptnote99483



def main():
    s99()


def s99():
    print("Testing survey and ptnote on samples/Sample 99483 input")
    bodytext = read_survey_99bodytext("samples/Sample 99483 input")
    survey = Survey99483(bodytext)
    # ~ print_survey_data(survey.data)
    note = Ptnote99483(survey)
    note.export_to_docx("99_output.docx")
    # ~ print(note.whole_note)

def print_survey_data(survey_data):
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.dump(survey_data, sys.stdout)

# Do whatever I have to do to pass the data in this file into survey()
def read_survey_99bodytext(filename):

    bodytext =[]
    with open(filename) as f:
        for i in f.readlines():
            i = i.replace("\xa0", " ")
            bodytext.append(i.strip())

    for x in bodytext:
        if x == '':
            bodytext.pop(bodytext.index(x))

    return bodytext


if __name__ == "__main__":
    main()
