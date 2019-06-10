from concepts.worldstate import WorldState
from concepts.topic import Topic
from sequence.sequence import Sequence
from story.plot import PlotGraph
from story.transition import Transition

import random
import copy

class Story:
    def __init__(self):
        self.world_state = WorldState()
        self.possible_transitions = self.init_possible_transitions()
        for char in self.world_state.characters:
            char.set_perception(WorldState(self.world_state))
            char.set_goal(self.create_goal(char))
        self.graph = self.create_plot_points()
        self.topics = self.create_topics()
        self.sequences = self.create_sequences()

    def __str__(self):
        transitions = "\n".join(map(lambda x: f'{x.start_value} -> {x.end_value}', self.possible_transitions))
        return f"{self.world_state}\nPossible transitions:\n{transitions}"

    def init_possible_transitions(self):
        """
        Creates a list of tuples representing all possible transitions, keeping each transition at random
        """
        transition_space = []
        for loc in self.world_state.locations:
            for loc2 in self.world_state.locations:
                if loc != loc2:
                    if random.random() > 0.5:
                        for char in self.world_state.characters:
                            transition_space.append(Transition(char, "location", loc, loc2))
        for obj in self.world_state.objects:
            for char in self.world_state.characters:
                for char2 in self.world_state.characters:
                    if char != char2:
                        transition_space.append(Transition(obj, "owner", char, char2))
        if len(transition_space) is 0:
            return self.init_possible_transitions()
        return transition_space

    def print_possible_transitions(self):
        print("Possible transitions:")
        for transition in self.possible_transitions:
            print(str(transition.start_value), "->", str(transition.end_value))

    def create_goal(self, character):
        """
        Find a transition object whose end state represents the change the character wants to see in the world state
        """
        pool = list(filter(lambda x: x.get_person() is character, self.possible_transitions))
        goal = random.choices(pool)[0]

        return goal

    def create_plot_points(self):
        """
        Create a graph of fabula elements
        Todo: Before executing each story point, ensure we can make
        a chain that doesn't go back and forth between the same states?
        Ie. this genotype can be evaluated before moving on
        """
        plot = PlotGraph(self.world_state, self.possible_transitions)
        plot.print_plot()
        return plot.graph

    def create_topics(self):
        """
        A list of things that have to be handled within the story. World state (including characters) must be introduced,
        and plot must be furthered
        Todo: not all introductions must be done before any plot points are handled
        """
        topics = []
        added = []
        main_char = self.world_state.characters[0]
        #add topics that introduce the starting state of the story
        for attribute in main_char.attributes.items():
            topics.append(Topic(main_char, attribute, "statement", "present"))
        #add actual plot topics
        for plotpoint in self.graph.nodes:
            predecessors = list(self.graph.predecessors(plotpoint))
            if plotpoint.elem is "G":
                topics.append(Topic(plotpoint.subj, plotpoint.transition, "action", "future"))
                added.append(plotpoint)
            if plotpoint.elem is "A":
                topics.append(Topic(plotpoint.subj, plotpoint.transition, "action", "present"))
                added.append(plotpoint)
            if plotpoint.elem is "P":
                topics.append(Topic(plotpoint.subj, plotpoint.transition, "statement", "present"))
                added.append(plotpoint)
            if plotpoint.elem is "IE":
                topics.append(Topic(plotpoint.subj, plotpoint.transition, "statement", "present"))
                added.append(plotpoint)
            if len(predecessors) > 1:
                for predecessor in predecessors:
                    if predecessor not in added:
                        if predecessor.elem is "A":
                            topics.append(Topic(predecessor.subj, predecessor.transition, "statement", "present"))
                            topics.append(Topic(predecessor.subj, predecessor.transition, "action", "past"))
                            added.append(plotpoint)
                        if predecessor.elem is "P":
                            #relative clauses? "minä näin että..."
                            topics.append(Topic(predecessor.subj, predecessor.transition, "statement", "past"))
                            added.append(plotpoint)
            if len(list(self.graph.successors(plotpoint))) is 0:
                break

        return topics

    def create_sequences(self):
        """
        Generates sequences for each topic
        """
        init_sequences = []
        for topic in self.topics:
            init_sequences.append(Sequence(self.world_state.characters, topic))
        return init_sequences

    def get_sequences(self):
        return self.sequences


def main():
    s = Story()
    print(s)


if __name__ == "__main__":
    main()
