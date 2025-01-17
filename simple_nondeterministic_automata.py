#
# definition of class SimpleNondeterministicAutomata
# for csc427 semester 232 (jan 2023-may 2023)
# last-update:
#      1 feb 2023 -bjr: created
#
# copyright (c) 2020-2023 burton rosenberg All rights reserved.
#


class SimpleNondeterministicAutomata:
   
    def __init__(self,fa_description,verbose=False):
        self.fa = fa_description
        # the : is reserved
        assert ':' not in self.fa['alphabet'] , f"Symbol |:| appears in {fa_description}."
        self.states = self.epsilon_close({self.fa['start']})
        self.verbose = verbose
    
    def epsilon_one_step(self,state_set):
        e = set()
        for state in state_set:
            t = (state,':')
            if t in self.fa['transitions']:
                e = e.union(self.fa['transitions'][t])
        return e.union(state_set)
    
    def epsilon_close(self,state_set):
        n = 0
        while len(state_set)>n:
            n = len(state_set)
            state_set = self.epsilon_one_step(state_set)
        return state_set

    def one_step(self,symbol):
        assert symbol in self.fa['alphabet'] , f"Symbol |{symbol}| not in the alphabet."
        new_states = set()
        for s in self.states:
            if (s,symbol) in self.fa['transitions']:
                new_states = new_states.union(self.fa['transitions'][(s,symbol)])
        return self.epsilon_close(new_states)
            
    def compute(self,string,verbose=False):
        self.states = self.epsilon_close({self.fa['start']})
        if self.verbose:
            print(f'\ninput: |{string}|')
        for symbol in string:
            s = self.one_step(symbol)
            if self.verbose:
                print(f'({self.states},{symbol}) -> {s}')
            self.states = s
        res = len(self.states.intersection(self.fa['accept'])) > 0
        if self.verbose:
            s = ('reject','accept')[res]
            print(s)
        return res

# end class SimpleNondeterministicAutomata


def simple_nfa_test(fa_name,fa_desc,test_vect,verbose=False):
    fa = SimpleNondeterministicAutomata(fa_desc,verbose)
    tv_true, tv_false = test_vect
    
    try:
        correct = 0
        print(f'*** testing {fa_name}')
        for string in tv_true:
            if fa.compute(string):
                print(f'OK: correctly accepts: |{string}| ')
                correct += 1
            else:
                print(f'ERR: should accept but does not: |{string}| ')
        print(f'*** {correct} correctly accepted out of {len(tv_true)} strings')
        passed = correct == len(tv_true)

        correct = 0 
        for string in tv_false:
            if not fa.compute(string):
                print(f'OK: correctly rejects: |{string}| ')
                correct += 1
            else:
                print(f'ERR: should reject but does not: |{string}| ')
        print(f'*** {correct} correctly rejected out of {len(tv_false)} strings')
        passed = passed and (correct == len(tv_false))
        
    except AssertionError as ae:
        print(f'\tFailed Assert: {ae}')
        passed = False
    
    if passed:
        print(f'\n*** PASSES\n')
    else:
        print(f'\n*** FAILS\n')
    return passed
