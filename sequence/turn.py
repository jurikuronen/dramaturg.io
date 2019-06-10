from language.word_token import WordToken
from language.sentence import Sentence

import random

class Turn:
    def __init__(self, speaker, listeners, turn_type, project):
        self.speaker = speaker
        self.listeners = listeners
        self.turn_type = turn_type
        self.verb = project.verb
        self.subj = project.subj
        self.obj = project.obj
        self.obj_type = project.obj_type
        self.time = project.time
        self.word_tokens = {
            "ter": [WordToken("tpart")],
            "kys": [WordToken("ppron", "subj", self.subj), WordToken("verb", None, self.verb), WordToken("noun", None, self.obj)],
            "vas": [WordToken("vpart")],
            "ilm": [WordToken("ppron", "subj", self.subj), WordToken("verb", None, self.verb), WordToken("noun", None, self.obj)],
            "kui": [WordToken("kpart")]
        }
        self.inflected = self.inflect()

    def __str__(self):
        return f"{self.speaker.name}: {self.inflected}"

    def inflect(self):
        tokens = self.word_tokens[self.turn_type]
        ques = self.turn_type is "kys"
        if self.turn_type in ["ter", "vas", "kui"]:
            #todo: change to accept cases with more than one token
            return tokens[0].word
        sentence = Sentence(self.speaker, self.listeners, {"subj": tokens[0], "verb": tokens[1], "obj": tokens[2]}, ques, self.obj_type, self.time)
        return sentence.styled


def main():
    print("Generated turn")


if __name__ == "__main__":
    main()
