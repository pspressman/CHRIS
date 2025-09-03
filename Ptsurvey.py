#survey class that contains mappings of survey questions, question types, and possible responses, as well as functions that scrape
#these responses from a completed survey, assign these responses to variables, and serve this data to a physician note-writing program.

#Gordon Matthewson, Fall 2019
#Adapted from code written by Dr. Peter Pressman, 2015.

#Please see the Readme.md document for usage and tips.
#STP: Where is Readme.md?

import yaml
import sys
import traceback

from debugging import format_stacktrace

# Class names are usually capitalized
class Survey:

    #STP: Unused?
    # ~ responsetypes = {"freetext" : 1, "forced" : 2, "ymn" : 3, "multiple" : 4, "survey" : 5}
    ynmappings = {"No" : 0, "Maybe" : 0.5, "Yes" : 1, "I'm not sure" : "I'm not sure", "I don't know" : "I don't know"}

    #the dictionary below, "sections", contains the hard question/response mappings, and is organized as follows:
    #   each section of the survey (i.e. 'intro', 'demographics', etc.) is organized as a dictionary, in the following key, value structure:
    #       'string containing variable name' : (question text, question type, possible responses)

    #Note that both the question text and the possible responses need to be IDENTICAL in this script to how they appear in your survey.
    #i.e. "Im not sure" != "I'm not sure", "Not sure" != "not sure" etc...

    # Read the dictionary from survey.yaml
    with open('survey.yaml') as f:
        sections = yaml.safe_load(f)

    def __init__(self, body):

        #sets the instance's "body" variable to the input variable "body"
        self.body = body

        # Make the sections for our data to go into
        self.data = {section: {} for section in self.sections.keys()}

        #uses to the self.fill function (see below) to set each variable in the survey type to its respective survey response
        [self.fill(section, key) for section in self.sections for key in self.sections[section]]


    #this function takes a section (i.e. 'intro' or 'language') and a key (i.e. 'behStart') as input, creates a new attribute named after the key (i.e. self.behStart),
    #and fills this attribute with data corresponding to the response in the body of the survey that was fed into this class as data.
    #it does this in several ways, depending on the type of question.
    def fill(self, section, key):

        question = self.sections[section][key]

        #sets the temporary variable "questiontext" to the text of the survey question being processed, for readability
        questiontext = question[0]

        #sets the temporary variable "questiontype" to the type of survey question being processed (i.e. will be 1 for free text, 2 for forced choice, etc.)
        questiontype = question[1]

        # STP: These hard coded numbers would be better as real descriptive strings
        # or possibly constants with all caps variable names
        #free text, forced response, and yes/maybe/no
        # ~ if questiontype == 1 or questiontype == 2 or questiontype == 3:
        if questiontype in [1, 2, 3]:
            if questiontext in self.body:
                #sets the temporary variable "questionindex", to the index number in self.body of where the question is.
                questionindex = self.body.index(questiontext)
                #assigns a variable named after the key to the data in the index immediately proceeding the question
                setattr(self, key, self.body[questionindex + 1])
                self.data[section][key] = self.body[questionindex + 1]
            else:
                setattr(self, key, "#" + key + "#")
                self.data[section][key] = "#" + key + "#"

        #multiple response (i.e. more than one answer possible)
        elif questiontype == 4:
            if questiontext in self.body:
                #sets the temporary variable "questionindex", to the index number in self.body of where the question is.
                questionindex = self.body.index(questiontext)
                #creates an empty list to store responses.
                setattr(self, key, [])
                self.data[section][key] = []
                #if the question has data about responses (i.e. if it's not a free text question), sets the temporary variable questionresponses to the question's possible
                #responses, for readability

                #loops through question responses, and quieries whether they are in the body of the text, starting at the index immediately proceeding the question,
                #and ending at the next index where anything other than a response is present (this uses the stepper function, defined below).  Adds each response to the list.

                questionresponses = self.possibleresponses(section, key)
                for x in questionresponses:
                    if x in self.body[questionindex+1:questionindex + 1 + self.stepper(self.body[questionindex+1:questionindex+len(questionresponses)], questionresponses)]:
                        self.__getattribute__(key).append(x)
                        self.data[section][key].append(x)
            else:
                setattr(self, key, "#" + key + "#")
                self.data[section][key] = ["#" + key + "#"]

        #embedded surveys (i.e. eCOG, zarit)
        elif questiontype == 5:
            #identical to the free text/forced response/ymn algorithm, but does it iteratively for question in the embedded survey
            #a little tricky, because sometimes questions can be repeated, but with different response choices (i.e. npiq, npiqCaregiver)
            for i in question[0]:
                questiontext = question[0][i]
                if questiontext in self.body:
                    if self.body.count(questiontext) > 1:
                        self.data[i] = []
                        for ii,line in enumerate(self.body):
                            #print(self.body[ii])
                            questionresponses = self.possibleresponses(section, key)
                            if line == questiontext and self.body[ii+1] in questionresponses:
                                #print(self.body[questionindex+1])
                                setattr(self, str(i), self.body[ii+1])
                                self.data[i].append(self.body[ii+1])
                    else:
                        questionindex = self.body.index(questiontext)
                        setattr(self, str(i), self.body[questionindex+1])
                        self.data[i] = self.body[questionindex+1]
                else:
                    setattr(self, str(i), "#" + str(i) + "#")
                    self.data[i] = ["#" + i + "#"]
        else:
            print(f"ERROR: Unknown question type {questiontype}")

    # this function takes two lists of items as input, and returns the index of
    # the first list in which ANY element of the second list is NOT present in.
    #Used in the "fill" function for gathering responses to a question in which more than one response is possible.
    def stepper(self, itemlist, conditionlist):
        x = enumerate(itemlist)
        for i,j in x:
            try:
                if str(j) in conditionlist:
                    indexlist = next(x)
                    continue
                else:
                    return i
            except Exception as e:
                print(f"Stepper failed: {e}")
                #5 is an arbitrary number here.
                #STP: What is 5? Why?
                return 5

    #returns the section that a variable is in (i.e. intro, demographics, etc.).  Handy for accessing question information.
    #Note that if the variable is a part of a survey (i.e. 'npiq') this won't work.
    #STP: Used only in Writeptnote.py
    #STP: I don't think this should exist. If you're accessing the data, you already
    # should know what section you are in.
    def section(self, variable):
        return ''.join([x for x in self.sections if variable in self.sections[x]])

    #returns a number associated with a survey response.  Note that for scoring, it is assumed the least severe responses start at 0 and increase numerically, but this is not always the case,
    #so you need to check how the responses are recorded in the above response section.  If the response is a part of a survey, you need to also include the name of the survey.
    # STP: Used only in Writeptnote.py
    def responsenumber(self, variable, survey=None):
        if survey:
            try:
                num =  [value[1] for key, value in self.sections[self.section(survey)][survey][2].items() if value[0] == self.__getattribute__(str(variable))]
                if num != []:
                    return int(num[0])
                else:
                    print("Can't find the number for survey response " + variable + "!!", file=sys.stderr)
                    # ~ print(format_stacktrace())
                    return 0
            except KeyError:
                print("responsenumber can't find key " + str(variable) + "!", file=sys.stderr)
                # ~ print(format_stacktrace())
                return 0
            except AttributeError:
                print("responsenumber can't find key " + str(variable) + "!" + " AttributeError", file=sys.stderr)
                # ~ print(format_stacktrace())
                return 0
        try:
            if self.sections[self.section(variable)][variable][1] == 3:
                return self.ynmappings[self.__getattribute__(str(variable))]
            else:
                return self.sections[self.section(variable)][variable][2][str(self.__getattribute__(variable))]
        except KeyError:
            print("responsenumber can't find key " + str(variable) + "!", file=sys.stderr)
            # ~ print(format_stacktrace())
            return 0
        except AttributeError:
            print("responsenumber can't find key " + str(variable) + "!" + " AttributeError", file=sys.stderr)
            # ~ print(format_stacktrace())
            return 0

    #returns the highest numerical value associated with possible responses in a survey (i.e. for "ecogMem", this would return a 3)
    #STP: Used only in Writeptnote.py
    def highestresponse(self, survey):
        keylist = []
        try:
            for key in self.sections[self.section(survey)][survey][2].items():
                keylist.append(key[1][1])
            return max(keylist)
        except KeyError:
            print("highestresponse can't find survey " + str(survey) + "!")

    #returns a dictionary or list of all of the possible responses, attached to their numbers.  Input needs to be either a variable or the name of a survey,
    #but can't be variables within a survey)
    def possibleresponses(self, section, key):

        questiontype = self.sections[section][key][1]
        if questiontype != 5:
            try:
                return self.sections[section][key][2]
            except KeyError:
                print("possibleresponses can't find key!")
                return 0
        else:
            try:
                responselist = []
                for x in self.sections[section][key][2].values():
                    responselist.append(x[0])
                return responselist
            except KeyError:
                print("possibleresponses can't find key!")
                return 0


    #TESTING AND Q/A FUNCTIONS


    #this function will print out each variable that was assigned from the text in an easy to read format.
    #STP: Perhaps we could just use YAML here?
    def printallvariables(self):
        for x in self.sections:
            try:
                print('\n\n\n\n\n', x + ' section:')
                for y in self.sections[x]:
                    print()
                    # STP: What do 1 and 5 here mean?
                    if self.sections[x][y][1] == 5:
                        print(y + ":")
                        for i in self.sections[x][y][0]:
                            print(i + ":", self.__getattribute__(str(i)))
                    else:
                        print(y + ":", self.__getattribute__(str(y)))
            except AttributeError:
                print("Printallvariables can't find variable " + y)

    #if elements of the text are niether a question in your survey class or a response, it prints these elements.  Useful for catching any variables in your survey that you forgot to code in this class.
    #STP: Unused
    def notassignedtext(self):
        pass



class Survey99483(Survey):

    #TO-DO: remove spaces at the end of many questions in qualtrics.

    # These are unnecessary because they are inherited from survey above
    # ~ responsetypes = {"freetext" : 1, "forced" : 2, "ymn" : 3, "multiple" : 4, "survey" : 5}
    # ~ ynmappings = {"No" : 0, "Maybe" : 0.5, "Yes" : 1, "I'm not sure" : "I'm not sure", "I don't know" : "I don't know"}

    # It would probably be good to only change the bits of the sections that
    # are different from the above survey. There are a few fixes above that
    # did not get propagated here.
    with open('survey99483.yaml') as f:
        sections = yaml.safe_load(f)




if __name__ == "__main__":
    # STP: I used these lines to make the survey.yaml files
    import yaml
    # ~ print(yaml.dump(survey.sections))
    # ~ print(yaml.dump(survey99483.sections))


    bodytext =[]
    with open("samples/Sample BigCHRIS input") as f:
        bodytext = [i.replace("\xa0", " ").strip() for i in f.readlines()]

    bodytext = list(filter(None, bodytext))
    survey_item = Survey(bodytext)
    yaml.dump(survey_item.data,sys.stdout)
