from nltk.parse.generate import generate
from nltk import CFG

import random

from sequence.sequencegrammar import grammar
from sequence.adjacency_pair.adjacency_pair import AdjacencyPair


class Sequence:
    def __init__(self, speakers, fabula_element):
        self.grammar = CFG.fromstring(grammar)
        self.speakers = speakers
        self.adjacency_pairs = []
        self.generate()

    def generate(self):
        generated = []
        for pair in generate(self.grammar, depth=5):
            generated.append(pair)
        adjpairs = random.choices(generated)[0]
        for pair in adjpairs:
            l = "".join(pair)
            adj_pair = AdjacencyPair(self.speakers, pair)
            self.adjacency_pairs.append(adj_pair)

    def print_sequence(self):
        print(self)

    def __str__(self):
        ret = ""
        for pair in self.adjacency_pairs:
            for pair_part in pair.inflected:
                line = f"{pair_part[0].name}: "
                for word in pair_part[1]:
                    line += pair_part[0].style.getStyledExpression(word) + " "
                line += "\n"
                ret += line
        return ret


def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
