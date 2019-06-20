from concepts.affect.emotion import Emotion

emotions = Emotion.load_emotions()


class FabulaElement:
    def __init__(self, elem, subj, goal):
        self.elem = elem
        self.subj = subj
        self.goal = goal
        self.obj = self.get_object()
        self.transition = self.get_transition()

    def __str(self):
        return self.elem

    def get_object(self):
        """
        Todo: replace hard-coding with actual functionality
        is this used anywhere?
        """
        if self.elem is "G":
            return self.subj
        if self.elem is "A":
            return self.subj
        if self.elem is "P":
            return None
        if self.elem is "IE":
            return self.subj
        if self.elem is "E":
            return None

    def get_transition(self):
        if self.elem is "IE":
            emotion = "happy_for" if self.goal else "disappointment"
            return ("affect", emotions[emotion])
        return (self.goal.attribute_name, self.goal.get_object())
