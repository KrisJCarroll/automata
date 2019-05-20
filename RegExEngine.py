#####################################################################################################
# Name: Kristopher Carroll
# CSCE A351
# Assignment 1
#####################################################################################################



#########################################################################
#                         **** RESOURCE DUMP ***
#------------------------------------------------------------------------
# General Procedure:
#   https://www.geeksforgeeks.org/theory-of-computation-conversion-from-nfa-to-dfa/
#   https://math.stackexchange.com/questions/1478718/union-of-two-non-deterministic-finite-automata
#   https://www.tutorialspoint.com/automata_theory/ndfa_to_dfa_conversion.htm
#   http://condor.depaul.edu/glancast/444class/docs/nfa2dfa.html
#
# Implementation Examples:
#   https://github.com/caleb531/automata/blob/master/automata/fa
#   http://www.nightmare.com/rushing/python/nfa.py
#   https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code
#   http://www-bcf.usc.edu/~breichar/teaching/2011cs360/NFAtoDFA.py
#   https://github.com/handylim/E-NFA-to-DFA-Converter
#
# Regular Expression Procedure:
#   https://swtch.com/~rsc/regexp/regexp1.html
#
# Testing:
#   https://cyberzhg.github.io/toolbox/nfa2dfa (regex to NFA generator)
#
#########################################################################


######################################
# A model of a DFA:
#   DFA = (Q, sigma, delta, q0, F)
#       Q = set of all states in DFA
#       sigma = alphabet recognized by DFA
#       delta = transition dictionary to process state transitions
#       q0 = starting state
#       F = accepted state(s)
#   This DFA accepts words with any number of zeroes or 0 or more '0'
#   followed by '10' followed by 0 or more '1', followed by '01', followed by 0
#   or more '0'
#   Ex: "00000000000" or "000101111111101" or "100100000000"
#       but not "11111" or "0101010101"
#   https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code
#######################################
Q = {'0', '1', '2'}
sigma = {'0', '1'}
delta = {'0':{
            '0':{'0'}, '1':{'1'}},
         '1':{
             '0':{'2'}, '1':{'0'}},
         '2':{
             '0':{'1'}, '1':{'2'}}
        }
q0 = {'0'}
F = {'0'}

dfa = (Q, sigma, delta, q0, F)

######################################
# A model of an NFA:
#   NFA = (Q, sigma, delta, q0, F)
#       Q = set of all states in the NFA
#       sigma = alphabet recognized by DFA
#       delta = transition dictionary to process tate transitions
#       q0 = starting state
#       F = accepted state(s)
# Modeled from example NFA found in online textbook (Maheshwari & Smid) p. 45
#######################################
Q = {'1', '2', '3'}
sigma = {'a', 'b'}
delta = {'1':{
            'a':{'3'}, 'b':{}, None: {'2'}},
         '2':{
            'a':{'1'}, 'b':{}, None: {}},
         '3':{
             'a':{'2'}, 'b':{'2','3'}, None: {}}
         }
q0 = {'1'}
F = {'2'}
nfa = (Q, sigma, delta, q0, F)

#######################################
# Another NFA modeled from https://www.geeksforgeeks.org/theory-of-computation-conversion-from-nfa-to-dfa/
# Accepts any string that ends in 'ab'
#######################################
Q = {'0', '1', '2'}
sigma = {'a', 'b'}
delta = {'0':{
            'a':{'0', '1'},'b':{'0'}, None: {}},
         '1':{
            'a':{}, 'b':{'2'}, None: {}},
         '2':{
             'a':{}, 'b':{}, None: {}}
        }
q0 = {'0'}
F = {'2'}
nfa2 = (Q, sigma, delta, q0, F)

#######################################
# Same NFA as above but changed Q to be 'a', 'b' and 'c' states for union and concat testing
# Accepts strings ending in 'ab'
#######################################
Q = {'a', 'b', 'c'}
sigma = {'a', 'b'}
delta = {'a':{
            'a':{'a', 'b'},'b':{'a'}, None: {}},
         'b':{
            'a':{}, 'b':{'c'}, None: {}},
         'c':{
             'a':{}, 'b':{}, None: {}}
        }
q0 = {'a'}
F = {'c'}
nfa2b = (Q, sigma, delta, q0, F)

######################################
# A third NFA modeled from http://condor.depaul.edu/glancast/444class/docs/nfa2dfa.html
# Accepts strings 'a', 'aa', 'aba' and 'abb' only
######################################
Q = {'1', '2', '3', '4', '5'}
sigma = {'a', 'b'}
delta = {'1':{
            'a':{'3'}, 'b':{}, None:{'2'}},
         '2':{
             'a':{'4', '5'}, 'b':{}, None:{}},
         '3':{
             'a':{}, 'b':{'4'}, None: {}},
         '4':{
             'a':{'5'}, 'b':{'5'}, None:{}},
         '5':{
             'a':{}, 'b':{}, None:{}}
         }
q0 = {'1'}
F = {'5'}

nfa3 = (Q, sigma, delta, q0, F)
####################################################
# Function: dfa_accept
# Inputs: 5-tuple (Q, sigma, delta, q0, F) representing a DFA matching the structure seen in the example DFA above
#         String of the word to be tested for the DFA
# Outputs: Boolean value representing if the DFA accepts the word
# Purpose: Test DFAs with words for accept or reject
####################################################
# Modeled on dfa_accept() provided by Dr. Lauter for assignment
def dfa_accept(dfa, word):
    (Q, sigma, delta, q0, F) = dfa
    q = next(iter(q0))

    if q not in Q: # if start state not in Q, reject
        return False
    # Process transitions
    for input in word:
        if input not in sigma: # if input isn't in alphabet, reject
            return False
        try:
            q = next(iter(delta[q][input]))
            if q not in Q: # if state returned not in Q, reject
                return False
        except:
            return False

    if q in F:
        return True
    return False
####################################################
# Function: set_to_string
# Inputs: A set
# Outputs: String representation of the elements in the set, separated by ', '
# Purpose: Convert set elements to strings to be used for dictionary keys for delta transitions
####################################################
def set_to_string(set):
    set_string = ""
    set_list = list(set)
    set_list.sort()
    if len(set_list) > 1:
        for i in range(len(set_list)):
            set_string = set_string + str(set_list[i])
            if i < len(set_list) - 1:
                set_string = set_string + ", "
        return set_string
    elif len(set_list) == 1:
        return next(iter(set))

# http://www.nightmare.com/rushing/python/nfa.py
####################################################
# Function: epsilon_closure
# Inputs: Dictionary representing the delta function of an NFA
#         A set containing an element representing a state in the NFA
# Outputs: The set containing all elements in the epsilon-closure of the input set
# Purpose: Find the epsilon-closures of states for use in conversion from an NFA to a DFA
####################################################
def epsilon_closure(delta, state):
    # Get the states that can be epsilon transitioned to
    e_moves = delta[set_to_string(state)][None]

    # No epsilon transitions, return the set containing only the state
    if len(e_moves) == 0:
        return set(state)
    # Epsilon transitions possible
    else:
        r = set() # empty set that will hold all states in the closure
        r = r.union(state) # add the input state to closure
        # for every state that can be epsilon-transitioned to, get their epsilon closures to add to the overall closure
        for s in e_moves:
            r = r.union(epsilon_closure(delta, set(s)))
        return r
####################################################
# Function: convert_nfa_to_dfa
# Inputs: 5-tuple (Q, sigma, delta, q0, F) representing an NFA matching the structure seen in examples above
# Outputs: 5-tuple (Q, sigma, delta, q0, F) representing the DFA that accepts the same language as the input NFA
# Purpose: Convert an NFA into the corresponding DFA that accepts the same language, with minimization
####################################################
def convert_nfa_to_dfa(nfa):
    (nfa_Q, nfa_sigma, nfa_delta, nfa_q0, nfa_F) = nfa


    q0 = {set_to_string(epsilon_closure(nfa_delta, nfa_q0))} # q0 of DFA should be the epsilon closure of the NFA's q0
    Q = set()
    Q = Q.union(q0) # Add q0 to Q
    delta = {}
    F = set()
    sigma = nfa_sigma

    # Establish a stack to process states that are possible to be transitioned to, starting with q0
    stack = []
    stack.append(set_to_string(epsilon_closure(nfa_delta, nfa_q0)))
    # Continue while there are more states to be checked
    while len(stack) > 0:
        r = set([x.strip() for x in stack.pop().split(',')]) # get composite state as new possible state for DFA
        r_string = set_to_string(r) # get string representation of states
        delta[r_string] = {} # establish transition dictionary for associated state
        # check transitions for every letter in sigma to define delta transitions
        for input in sigma:
            transfer_states = set() # establish empty set for adding all transitions possible
            # for every individual state in composite state
            for split_state in r:
                r_epsilon = epsilon_closure(nfa_delta, {split_state}) # get epsilon closure of individual state
                # add states possible to be transitioned to for every state in epsilon closure
                for state in r_epsilon:
                    transfer_states = transfer_states.union(nfa_delta[set_to_string({state})][input])
            states_string = set_to_string(transfer_states) # convert transition states into string representing a composite state possible for DFA
            if states_string is None: # No states can be transitioned to
                delta[r_string][input] = {} # define no transitions
            else:
                delta[r_string][input] = {states_string} # add composite state as transition to r with input letter checked
            if states_string in Q or len(transfer_states) == 0: # If new state found already in Q or no state found, continue
                continue
            # else, add the newly found state to DFA's Q and the stack to be checked
            Q.add(states_string)
            stack.append(states_string)
    # Check all composite states found to see if they contain a state found in the input NFA's F
    for r in Q:
        r_set = set([x.strip() for x in r.split(',')])
        try: # simple handling for composite states vs. single states
            for state in r_set:
                if state in nfa_F:
                    F.add(r)
                    break
        except: # composite state contains only a single state, check it
            if r in nfa_F:
                F.add(r)

    dfa = (Q, sigma, delta, q0, F)
    return dfa

# TODO: Finish logic to ensure all states in Q2 are converted to unique state names not found in Q1
def unique_states(nfa1, nfa2):
    (Q1, sigma1, delta1, q01, F1) = nfa1
    (Q2, sigma2, delta2, q02, F2) = nfa1

    intersection = Q1.intersection(Q2)
    if len(intersection) > 0:
        return

####################################################
# Function: nfa_union
# Inputs: Two 5-tuples (Q, sigma, delta, q0, F) representing NFAs matching structure in examples above
# Outputs: 5-tuple (Q, sigma, delta, q0, F) representing the NFA that accepts the union of the language of the input NFAs
# Purpose: Produce an NFA that accepts the union of the languages of two input NFAs
####################################################
def nfa_union(nfa1, nfa2):
    (Q1, sigma1, delta1, q01, F1) = nfa1
    (Q2, sigma2, delta2, q02, F2) = nfa2
    unique_states(nfa1, nfa2) # check to see if nfa1 and nfa2 have unique state names, convert one of them if they don't
    q0 = {'-1'} # create new starting state
    Q = q0.union(Q1).union(Q2) # new Q should be the union of Q1 and Q2 with our new start state
    sigma = sigma1.union(sigma2) # new sigma should be the union of sigma1 and sigma2
    delta = {} # establish empty delta for defining programmatically
    F = F1.union(F2) # new F should be the union of F1 and F2

    # Check every state in new Q
    for state in Q:
        delta[state] = {} # establish transition dictionary for state
        if state == '-1': # new start state, create epsilon transitions
            delta[state][None] = q01.union(q02)
        # define transitions for every letter in new sigma
        for input in sigma:
            if state in Q1: # we're in a state from nfa1, define transition with delta1 for input and epsilon
                delta[state][input] = delta1[state][input]
                delta[state][None] = delta1[state][None]
            elif state in Q2: # we're in a state from nfa2, define transition with delta2 for input and epsilon
                delta[state][input] = delta2[state][input]
                delta[state][None] = delta2[state][None]
            else: # add transition definitions for new start state
                delta[state][input] = {}

    nfa = (Q, sigma, delta, q0, F)
    return nfa
####################################################
# Function: nfa_concat
# Inputs: Two 5-tuples (Q, sigma, delta, q0, F) representing NFAs matching structure in examples above
# Outputs: 5-tuple (Q, sigma, delta, q0, F) representing the NFA that accepts the concatenation of the language of the input NFAs
# Purpose: Produce an NFA that accepts the concatenation of the languages of two input NFAs
####################################################
def nfa_concat(nfa1, nfa2):
    (Q1, sigma1, delta1, q01, F1) = nfa1
    (Q2, sigma2, delta2, q02, F2) = nfa2
    Q = Q1.union(Q2) # new Q should be the union of Q1 and Q2
    sigma = sigma1.union(sigma2) # new sigma should be the union of sigma1 and sigma2
    delta = {} # create blank transition dictionary
    q0 = q01 # start state is nfa1's start state
    F = F2 # new F should be the states in F2

    # Check every state in new Q for transitions
    for state in Q:
        delta[state] = {}
        # define transitions for every letter in sigma
        for input in sigma:
            if state in Q1: # we're in a state from Q1, define transitions using delta1 for input and epsilon
                delta[state][input] = delta1[state][input]
                delta[state][None] = delta1[state][None]
            elif state in Q2: # we're in a state from Q1, define transitions using delta2 for input and epsilon
                delta[state][input] = delta2[state][input]
                delta[state][None] = delta2[state][None]
            else: # error state, shouldn't be reachable but define empty transition anyway
                delta[state][input] = {}
        # if the state was in F1, define an epsilon transition to q02 but keep other epsilon transitions defined
        if state in F1:
            delta[state][None] = q02.union(delta[state][None])
    nfa = (Q, sigma, delta, q0, F)
    return nfa
####################################################
# Function: nfa_star
# Inputs: 5-tuple (Q, sigma, delta, q0, F) representing NFA matching structure in examples above
# Outputs: 5-tuple (Q, sigma, delta, q0, F) representing the NFA that accepts the star of the language of the input NFA
# Purpose: Produce an NFA that accepts the star of the language of input NFA
####################################################
def nfa_star(nfa1):
    (Q1, sigma1, delta1, q01, F1) = nfa1
    q0 = {'-1'}
    Q = q0.union(Q1)
    sigma = sigma1
    delta = {}
    F = F1.union(q0)

    for state in Q:
        delta[state] = {}
        for input in sigma:
            if state in Q1:
                delta[state][input] = delta1[state][input]
                delta[state][None] = delta1[state][None]
            else:
                delta[state][input] = {}
                delta[state][None] = {}
        if state == '-1' or state in F1:
            delta[state][None] = q01.union(delta[state][None])

    nfa = (Q, sigma, delta, q0, F)
    return nfa

# TODO: Finish this - currently incomplete and not used for testing.
def reg_ex_to_nfa(regex):
    Q = set()
    sigma = set()
    q0 = set()
    delta = {}
    F = set()

    operators = ['*', '|'] # TODO: add support for '(' and ')' parsing (stacks)
    for char in regex:
        if char not in operators:
            if char not in sigma:
                sigma.add(char)
####################################################
# Function: regex_accept
# Inputs: string representing the regular expression and a string representing the word to be checked from NFA representing regular expression
# Outputs: boolean representing whether the word is accepted by the NFA representing the regular expression
# Purpose: Check whether the NFA produced by the regular expression accepts the input word
####################################################
def regex_accept(regex, word):
    nfa = reg_ex_to_nfa(regex) # get NFA converted from regex
    dfa = convert_nfa_to_dfa(nfa) # get DFA converted from NFA
    return dfa_accept(dfa, word) # return whether the DFA accepts the word


# Testing DFA
print(dfa_accept(dfa, "00000000000"))
print(dfa_accept(dfa, "11111111111"))

# Outputting converted DFA from NFA
new_dfa = convert_nfa_to_dfa(nfa)
(newQ, newSigma, newDelta, newq0, newF) = new_dfa
print("Returned DFA is as follows:")
print("\tQ:", newQ)
print("\tSigma:", newSigma)
print("\tDelta:", newDelta)
print("\tq0:", newq0)
print("\tF:", newF)

# Testing NFA conversions
print("Testing nfa1 with accepted string:",dfa_accept(convert_nfa_to_dfa(nfa), "abbbbbbbbbbb"))
print("Testing nfa1 with rejected string:",dfa_accept(convert_nfa_to_dfa(nfa), "bbbbbbbbbbbb"))
print("Testing nfa2 with accepted string:",dfa_accept(convert_nfa_to_dfa(nfa2), "aaaaaaaaaaab"))
print("Testing nfa2 with rejected string:",dfa_accept(convert_nfa_to_dfa(nfa2), "aaaaaaaaaaaba"))
print("Testing nfa3 with accepted string:",dfa_accept(convert_nfa_to_dfa(nfa3), "abb"))
print("Testing nfa3 with rejected string:",dfa_accept(convert_nfa_to_dfa(nfa3), "abba"))

# Testing NFA union
print("Testing nfa1 union nfa2b with accepted string:", dfa_accept(convert_nfa_to_dfa(nfa_union(nfa, nfa2b)), "abbbbbbbbbbb"))
print("Testing nfa1 union nfa2b with second accepted string:", dfa_accept(convert_nfa_to_dfa(nfa_union(nfa, nfa2b)), "bbbbbbbbbbbab"))
print("Testing nfa1 union nfa2b with rejected string:", dfa_accept(convert_nfa_to_dfa(nfa_union(nfa, nfa2b)), "111111111"))

# Testing NFA concat
print("Testing nfa2 concat nfa2b with accepted string:", dfa_accept(convert_nfa_to_dfa(nfa_concat(nfa2, nfa2b)),"aaaaaaaaaaab" + "bbbbbbbbbbbab"))
print("Testing nfa2 concat nfa2b with rejected string:", dfa_accept(convert_nfa_to_dfa(nfa_concat(nfa2, nfa2b)),"aaaaaaaaaabb" + "bbbbbbbbbbbbb"))

# Testing NFA star
print("Testing nfa3 star with accepted string:", dfa_accept(convert_nfa_to_dfa(nfa_star(nfa3)), "abaaba"))
print("Testing nfa3 star with empty string:", dfa_accept(convert_nfa_to_dfa(nfa_star(nfa3)), ""))
print("Testing nfa3 star with rejected string:", dfa_accept(convert_nfa_to_dfa(nfa_star(nfa3)), "abbb"))
