
from itertools import chain
import numpy as np
import config


class Universe:

    def __init__(self, *all_creature_lists):

        self.universe_width = config.universe_width
        self.universe_height = config.universe_height   

        self.day = config.days 

        self.creature_mapping = {'Grass': 1, 'Rabbit': 2, 'Fox': 3}

        if len(all_creature_lists) != len(self.creature_mapping):
            raise Exception("The number of list of elements passed do not match the mapping.")

        self.all_elements = list(chain(*all_creature_lists))
        #Python logic for the above line of code:
        # all_creature_lists is a tuple of the lists passed as argument
        # The above tuple is unwrapped using * and passed to itertools.chain
        # On unwrapping all the lists are passed as arguments to chain seperately
        # chain(*all_creature_lists) returns a chain yield object which contains all
        # elements of the list and then list() function converts the object to a list

        
    @property
    def universe_matrix(self):

        _matrix = np.zeros((self.universe_width, self.universe_height), dtype = np.float32)      
            
        for element in self.all_elements:
             
             _matrix[int(element.pos_X), int(element.pos_Y)] =  self.creature_mapping[element.__class__.__name__] 

        return _matrix



                
    

        









