print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
from .. import config
print("The value of config.count is {0}".format(config.count))
