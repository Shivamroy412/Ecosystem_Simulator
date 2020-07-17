import config


# Stats
def print_stats():
    for rabbit in config.rabbit_list:
        print(rabbit.id, rabbit.age, rabbit.steps,
              rabbit.gender, rabbit.reason_of_death)
