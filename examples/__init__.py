import abc


class Example(abc.ABC):
    def run(self):
        raise NotImplementedError
