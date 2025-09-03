"""
Run the programs provided on all the sample data provided and see what happens.

Stephen Pollard

2020-08-05

"""


import sys
import yaml
import oyaml
import ruamel.yaml

ryaml = ruamel.yaml.YAML()
ryaml.indent(sequence=4, offset=2)

# ~ f = 'survey.yaml'
# ~ fo = 'survey2.yaml'
# ~ f = 'survey99483.yaml'
# ~ fo = 'survey99483_2.yaml'
f = 'ptnote.yaml'
fo = 'ptnote_2.yaml'

def main():
    fix_survey()

def fix_survey():
    with open(f) as fi:
        s = yaml.load(fi)
    with open(fo, 'w') as fou:
        ryaml.dump(s, fou)


if __name__ == "__main__":
    main()
