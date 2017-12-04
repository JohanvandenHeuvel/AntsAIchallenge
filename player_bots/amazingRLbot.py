#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class amzingRLbot:
    def __init__(self):
        # define class level variables, will be remembered between turns

        botFile = open('amazingRLbotWeights.txt', 'r+')
        self.weights = [x.strip() for x in botFile]

        # RL parameters
        self.epsilon = 0.3  # (exploration prob)
        self.alpha = 0.5    # (learning rate)
        self.discount = 0.9 # (discount rate)

        # write weights to file to save between iterations?
        # find out way to run a lot of iterations fast
        # find good features

        pass

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):


        self.hills = []

        # initialize data structures after learning the game settings
        self.unseen = []
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row,col))

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants): # track all moves, prevent collisions
        # print(self.weights)
        orders = {}
        def do_move_direction(loc, direction):
            # the destination method will wrap around the map properly
            # and give us a new (row, col) tuple
            new_loc = ants.destination(loc, direction)
            # unoccpied avoids food and others ant, in contrast to passable which
            # just checks for land
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                # an order is the location of a current ant and a direction
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False

        # food targets declaration
        targets = {}
        def do_move_location(loc, dest):
            directions = ants.direction(loc, dest)
            for direction in directions:
                if do_move_direction(loc, direction):
                    targets[dest] = loc
                    return True
            return False

        # prevent stepping on own hill
        for hill_loc in ants.my_hills():
            orders[hill_loc] = None

        # gather food
        ant_dist = []
        for food_loc in ants.food():
            for ant_loc in ants.my_ants():
                dist = ants.distance(ant_loc, food_loc)
                ant_dist.append((dist, ant_loc, food_loc))
        ant_dist.sort()
        for dist, ant_loc, food_loc in ant_dist:
            if food_loc not in targets and ant_loc not in targets.values():
                do_move_location(ant_loc, food_loc)

        # attack hills
        for hill_loc, hill_owner in ants.enemy_hills():
            if hill_loc not in self.hills:
                self.hills.append(hill_loc)
        ant_dist = []
        for hill_loc in self.hills:
            for ant_loc in ants.my_ants():
                if ant_loc not in orders.values():
                    dist = ants.distance(ant_loc, hill_loc)
                    ant_dist.append((dist, ant_loc, hill_loc))
        ant_dist.sort()
        for dist, ant_loc, hill_loc in ant_dist:
            do_move_location(ant_loc, hill_loc)

        # explore unseen areas
        for loc in self.unseen[:]:
            if ants.visible(loc):
                self.unseen.remove(loc)
        for ant_loc in ants.my_ants():
            if ant_loc not in orders.values():
                unseen_dist = []
                for unseen_loc in self.unseen:
                    dist = ants.distance(ant_loc, unseen_loc)
                    unseen_dist.append((dist, unseen_loc))
                unseen_dist.sort()
                for dist, unseen_loc in unseen_dist:
                    if do_move_location(ant_loc, unseen_loc):
                        break

        # unlock own hill
        for hill_loc in ants.my_hills():
            if hill_loc in ants.my_ants() and hill_loc not in orders.values():
                for direction in ('s', 'e', 'w', 'n'):
                    if do_move_direction(hill_loc, direction):
                        break


    """Reinforcement Learning Helper Functions"""
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.
        """

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.
        """

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability epsilon, we should take a random action and
          take the best policy action otherwise.
        """

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """

    def updateFile(self):
        """
           Update the weights file with most recent update
        """



if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(amzingRLbot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
