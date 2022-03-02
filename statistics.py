from organisms import *
import config



# Stats
def print_stats():
    for rabbit in Rabbit.rabbit_list:
        print(rabbit.id, rabbit.age, rabbit.steps,
              rabbit.gender, rabbit.reason_of_death)
        print("___________________________")

    



