#
# definition of class SimpleFiniteAutomata
# for csc427 semester 232 (jan 2023-may 2023)
# last-update:
#      22 jan 2023 -bjr: created
#      23 jan -bjr: added assertion handling
#
# copyright (c) 2020-2023 burton rosenberg All rights reserved.
#


class SimpleFiniteAutomata:
    
    def __init__(self,fa_description,verbose=False):
        self.fa = fa_description
        self.state = self.fa['start']
        self.verbose = verbose
        
    def one_step(self,symbol):
        assert symbol in self.fa['alphabet'] , f"Symbol |{symbol}| not in the alphabet."
        assert (self.state,symbol) in self.fa['transitions'] , f"Transition |{(self.state,symbol)}| undefined."
        return self.fa['transitions'][(self.state,symbol)]
        
    def compute(self,string):
        self.state = self.fa['start']
        if self.verbose:
            print(f'\ninput: |{string}|')
        for symbol in string:
            s = self.one_step(symbol)
            if self.verbose:
                print(f'({self.state},{symbol}) -> {s}')
            self.state = s
        if self.verbose:
            s = ('reject','accept')[self.state in self.fa['accept']]
            print(s)
        return self.state in self.fa['accept']

    
#end class SimpleFiniteAutomata


def simple_fa_test(fa_name,fa_desc,test_vect,verbose=False):
    fa = SimpleFiniteAutomata(fa_desc,verbose)
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
