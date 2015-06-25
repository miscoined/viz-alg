from config import DEFAULT_SOURCE, AVAILABLE_ALGS


def parse_source(source):
    """Return source as a list of integers, using default if necessary."""
    try:
        if source.strip() == "":
            return DEFAULT_SOURCE
        else:
            # convert to a list of integers
            return list(map(int, source.strip().split()))
    except AttributeError:
        return DEFAULT_SOURCE


def remap(l, min_val=0, max_val=200):
    """Return a list with values mapped to a specified range."""
    old_min = min(l)
    for i in l:
        try:
            i = ((i - old_min) * (max_val - min_val) / (max(l) - old_min)
                 + min_val)
        except ZeroDivisionError:
            # for case where list contains all of one value
            # i.e. max(l) == min(l). In this case,
            # map to half of total range.
            i = (min_val + max_val) / 2
    return l


class SortAlg:
    def __init__(self, alg, source=DEFAULT_SOURCE):
        """
        Setup sorting algorithm object with specified alg and source. Alg must
        be a string containing the name of a sort function (e.g.
        "sort_selection"). Source can be ommitted, in which case a default
        source from config is used, a list of integers, or a
        whitespace-separated string of integers.
        """
        self.alg = getattr(self, alg)
        # props for displaying in page
        self.props = {
            "name": {i[0]: i[1] for i in AVAILABLE_ALGS}[alg],
            "source": parse_source(source)
        }
        self.props["steps"] = [self.props["source"]]
        self.alg(self.props["steps"])

    def selection_step(self, l, i):
        """Return list after one step of selection sort."""
        l = list(l)
        cur_min = min(enumerate(l[i:]), key=lambda p: p[1])[0]
        if l[i] != l[cur_min + i]:
            l[i], l[cur_min + i] = l[cur_min + i], l[i]
        return l

    def selection(self, steps):
        """Build list with state of list after each stage of sort."""
        for i in range(len(steps[-1])):
            step = self.selection_step(steps[-1], i)
            if step != steps[-1]:
                steps.append(step)

    def bogo_step(self, l):
        """Return list after one step of bogosort."""
        from random import shuffle
        l = list(l)
        shuffle(l)
        return l

    def bogo(self, steps):
        """ Build list containing state of list after each stage of sort. """
        while sorted(steps[-1]) != steps[-1]:
            steps.append(self.bogo_step(steps[-1]))
