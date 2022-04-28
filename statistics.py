from organisms import *

# Stats
def print_stats():
    Organism.save_fittest_creatures(Rabbit)
    for rabbit in Rabbit.rabbit_list:
        print(rabbit.id, rabbit.age, rabbit.steps,
              rabbit.gender, rabbit.reason_of_death, rabbit.father, rabbit.mother)
        print("___________________________")

    



