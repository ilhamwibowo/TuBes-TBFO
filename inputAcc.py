import numpy as np
import os
from PIL import image

def do_something(x):
    ''' This is a sample multiline comment
    '''
    
    i = 4
    while (i < 5):
    # This is a comment
        if (i > 3):
            continue
        else: 
            break
    #asdasd ####
    if x == 0:
        return 0
    elif x + 4 == 1:
        if True:
            return 3
        else:
            return 2
    elif x == 3:
        return 4
    else:
        return 'Doodoo'
