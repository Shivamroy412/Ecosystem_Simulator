from organisms import *

# Statistics
def print_stats():
    for rabbit in Rabbit.rabbit_list:
        print(rabbit.id, rabbit.age, rabbit.steps,
              rabbit.gender, rabbit.reason_of_death, rabbit.father, rabbit.mother)
        print("___________________________")

    



