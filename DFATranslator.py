#!/usr/bin/env python3
import re
import os
import sys

class DFA(object):
    def __init__(self, dfaSettings, sentences):
        self.dfaSettings = dfaSettings
        self.sentences = sentences
        self.initial = []
        self.final = []
        self.Machine = {}
        self.populateAll()

    def add_to_dict(self,rule):
        if rule[0] in self.Machine:
            self.Machine[rule[0]][rule[1]] = rule[2]
        else:
            self.Machine[rule[0]] = {rule[1] : rule[2]}

    def populateInitial(self,openFile):
        openFile.seek(0)
        self.initial = re.sub(pattern=r",",
                                repl=" ",
                                string=re.sub(pattern=r"\s*",
                                            repl="",
                                            string = openFile.readline())).split()
        #print(self.initial)

    def populateFinal(self, openFile):
        openFile.seek(0)
        openFile.readline()
        self.final = re.sub(pattern=r",",
                                repl=" ",
                                string=re.sub(pattern=r"\s*",
                                            repl="",
                                            string=openFile.readline())).split()
        #print(self.final)

    def populateMachine(self, openFile):
        openFile.seek(0)
        openFile.readline()
        openFile.readline()
        for line in openFile:
            rule = re.sub(pattern=r",",
                                  repl=" ",
                                  string=re.sub(pattern=r"\s*",
                                                repl="",
                                                string=line)).split()
            self.add_to_dict(rule)
        print(self.Machine)

    def populateAll(self):
        with open(file = self.dfaSettings) as dfa:
            self.populateInitial(dfa)
            self.populateFinal(dfa)
            self.populateMachine(dfa)

    def checkLambda(self):
        if (self.initial[0] in self.final):
            return True
        else:
            return False

    def Translate(self, sentence):
        """Check the sentence and return True if accepted, False otherwise"""
        current_pos = self.initial[0]

        if (sentence.lower() == "lambda"):
            return self.checkLambda()

        for letter in sentence:
            if current_pos in self.Machine:
                current_pos = self.Machine[current_pos][letter]
                #print(current_pos)

        if current_pos in self.final:
            return True
        else:
            return False

    def result(self):
        s = open(self.sentences)
        with open('Results.txt','w') as result:
            for line in s:
                if self.Translate(line.strip()):
                    print(line.strip() + ', Yes')
                    result.write(line.strip() + ', Yes\n')
                else:
                    print(line.strip() + ', No')
                    result.write(line.strip() + ', No\n')
        s.close()
        print('Results.txt Created and ovewritten.')



def main():
    x = DFA('dfa.txt','sentences.txt')
    x.result()


if __name__ == '__main__':
    main()
