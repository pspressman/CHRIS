"""
Run the programs provided on all the sample data provided and see what happens.

Stephen Pollard

2020-08-05

"""


import sys
import yaml

# SoCRatesBuild.py can be run from the command line as is.


# CHRIS cannot because it reads from an email account. Therefore I can test
# what it does with the body of the email separately from the email gathering
# process.


from Ptsurvey import Survey, Survey99483
from Writeptnote import Ptnote, Ptnote99483


# survey() input has has 'strong urges' while survey99483() does not.
# survey99483 input is marked by 99483

def main():
    # ~ bigchris() # works mostly at least
    # ~ ftd() # many empty fields
    # ~ tbi() # Almost all blank fields
    # ~ self()  # Almost all blank fields
    # ~ sample_99bodytext() # Almost all blank fields
    sample_99_input() # Almost all blank fields

def print_survey_data(survey_data):
    import ruamel.yaml
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.dump(survey_data, sys.stdout)

def read_survey(filename, docx):
    bodytext =[]
    with open(filename) as f:
        for i in f.readlines():
            if "\xa0" in i:
                i = i.replace("\xa0", " ")
            bodytext.append(i.strip())

    for x in bodytext:
        if x == '':
            bodytext.pop(bodytext.index(x))
    survey = Survey(bodytext)
    # ~ print_survey_data(survey.data)
    note = Ptnote(survey)
    note.export_to_docx(docx)


# Does not produce correct results, so far as I can tell
def bigchris():
    print("Testing survey and ptnote on samples/Sample BigCHRIS input")
    # Do whatever I have to do to pass the data in this file into survey()
    sys.stdout = open('test_output_new/Sample BigCHRIS input.txt','w')
    sys.stderr = sys.stdout
    # Copied from CHRIS
    bodytext =[]

    with open("samples/Sample BigCHRIS input") as f:
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

    ptTest = Survey(bodytext)
    note = Ptnote(ptTest)
    note.export_to_text("test_output_new/Sample BigCHRIS input note.txt")
    note.export_to_docx("test_output_new/Sample BigCHRIS input.docx")

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# Does not produce correct results, so far as I can tell
def ftd():
    print("Testing survey and ptnote on samples/Sample FTD input")
    # Do whatever I have to do to pass the data in this file into survey()
    sys.stdout = open('test_output_new/Sample FTD input.txt','w')
    sys.stderr = sys.stdout
    # Copied from CHRIS
    bodytext =[]
    read_survey("samples/Sample FTD input", "test_output_new/Sample FTD input.docx")

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# Does not produce correct results, so far as I can tell
def tbi():
    print("Testing survey and ptnote on samples/Sample TBI input")
    # Do whatever I have to do to pass the data in this file into survey()
    sys.stdout = open('test_output_new/Sample TBI input.txt','w')
    sys.stderr = sys.stdout
    # Copied from CHRIS
    bodytext =[]
    read_survey("samples/Sample TBI input", "test_output_new/Sample TBI input.docx")

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# Does not produce correct results, so far as I can tell
def self():
    print("Testing survey and ptnote on samples/sample self input")
    # Do whatever I have to do to pass the data in this file into survey()
    sys.stdout = open('test_output_new/sample self input.txt','w')
    sys.stderr = sys.stdout
    # Copied from CHRIS
    bodytext =[]
    read_survey("samples/sample self input", "test_output_new/sample self input.docx")

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


# Does not produce correct results, so far as I can tell
def sample_99bodytext():
    print("Skipping samples/Sample99483BodyTExt because it is a note example and not input to CHRIS")
    return
    print("Testing survey99 and ptnote99 on samples/Sample99483BodyText")
    # Do whatever I have to do to pass the data in this file into survey()
    sys.stdout = open('test_output_new/Sample99483BodyText.txt','w')
    sys.stderr = sys.stdout
    # Copied from CHRIS
    # This file looks like json, but json doesn't read it... perhaps bc of the \"
    bodytext = yaml.safe_load("samples/Sample99483BodyText")

    # Find the start of the survey
    startIndex = 0 # necessary this time
    for i in bodytext:
        if i == "A survey has been completed.":
            startIndex = bodytext.index(i)
    bodytext = bodytext[startIndex:]
    for x in bodytext:
        if x == '':
            bodytext.pop(bodytext.index(x))
    # We know the survey type
    # ~ surveytype = "PtCareCombo"
    # ~ if surveytype == "PtCareCombo":
    ptTest = Survey99483(bodytext)
    note = Ptnote99483(ptTest)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


# Does not produce correct results, so far as I can tell
def sample_99_input():
    print("Testing survey99 and ptnote99 on samples/Sample 99483 input")
    # Do whatever I have to do to pass the data in this file into survey()
    sys.stdout = open('test_output_new/Sample 99483 input.txt','w')
    sys.stderr = sys.stdout
    # Copied from CHRIS
    bodytext =[]
    with open("samples/Sample 99483 input") as f:
        for i in f.readlines():
            i = i.replace("\xa0", " ")
            bodytext.append(i.strip())

    for x in bodytext:
        if x == '':
            bodytext.pop(bodytext.index(x))
    # We know the survey type
    # ~ surveytype = "PtCareCombo"
    # ~ if surveytype == "PtCareCombo":
    ptTest = Survey99483(bodytext)
    note = Ptnote99483(ptTest)

    note.export_to_text("test_output_new/Sample 99483 input note.txt")
    note.export_to_docx("test_output_new/Sample 99483 input.docx")

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


if __name__ == "__main__":
    main()
