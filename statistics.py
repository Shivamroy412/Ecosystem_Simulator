import config



# Stats
def print_stats():
    for rabbit in config.rabbit_population:
        print(rabbit.id, rabbit.age, rabbit.steps,
              rabbit.gender)
