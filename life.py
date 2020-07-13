import game
import kinetics
import random
import config
import organisms


def live(population_list, gestation_period,food_list,creature_class):
    for creature in population_list:
        if creature.isAlive:
            kinetics.move_creature(creature)

            # Step counter
            creature.steps += 1

            # Age counter
            creature.age += 1

            # Hunger Counter
            creature.hunger += 1
            if creature.hunger >= 100:
                creature.isAlive = False
                creature.reason_of_death = "Hunger"

            # Rabbit eats only when hungry
            if creature.hunger > 50:
                eaten_grass = game.isCollided(creature, food_list)
                if eaten_grass:
                    eaten_grass.isAlive = False
                    creature.hunger = 0

            # Reproduction
            if creature.gender == 'M' and creature.isAdult:
                mother = game.isCollided(creature, list(filter(lambda female: (
                        (female.gender == 'F' and not female.isPregnant) and
                        creature.isAdult), population_list)))
                if mother:
                    mother.isPregnant = True
                    print("Rabbit got pregnant")

            if creature.isPregnant:
                creature.gestation_days += 1

            if creature.isPregnant and creature.gestation_days == (gestation_period/2):
                litter_size = random.randint(5 ,10)
                birth(creature_class ,litter_size ,population_list )

            if creature.gestation_days == gestation_period:
                creature.isPregnant = False
                creature.gestation_days = 0

            if creature.age > config.rabbit_childhood:
                creature.isAdult = True


            #Death
            if creature.age == creature.life_span:
                creature.isAlive = False
                creature.reason_of_death = "Age"


#Creature Birth
def birth(creature_class , creature_quantity, creature_population: list):
    present_population = len(creature_population)
    print("birth", present_population)
    for i in range(present_population, present_population + creature_quantity):
        creature = creature_class()
        gender = 'M' if random.randint(1, 9) % 3 == 0 else 'F'
        # Purposely slightly biased towards generating more females
        creature.id = i
        creature.pos_X = random.randint(30, config.screen_width - 30)
        creature.pos_Y = random.randint(30, config.screen_height - 30)
        if creature_class != organisms.Grass:
            creature.gender = gender
            creature.life_span = random.randint(450,500)
        creature_population.append(creature)