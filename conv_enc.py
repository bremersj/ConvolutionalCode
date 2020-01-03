# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:33:43 2019

@author: Steve Bremer
"""

STATE = 0
HISTORY = 1
SCORE = 2

class ConvolutionalCode():
    def __init__(self, gen_poly):
        if len(gen_poly) > 0:
            poly_len = len(gen_poly[0])
        else:
            # Raise an error?
            poly_len = 0
        for poly in gen_poly:
            if poly_len != len(poly):
                # Raise an error; generator polys not of same length
                return
        self.n = len(gen_poly)
        self.constraint = poly_len - 1
        self.state = '0'*self.constraint
        self.generators = gen_poly
        
    def poly_mult(self, a, b):
        if len(a) != len(b):
            #raise an error
            return
        result = 0
        for i, bit in enumerate(a):
            bit = int(bit)*int(b[i])
            result = (result + bit)%2
        return str(result)
    
    def shift_state(self, bit):
        self.state = bit + self.state[:-1]
            
    def encode(self, bitstream):
        self.state = '0'*self.constraint #reset init state
        output = ''
        for bit in bitstream:
            stream = bit + self.state
            for generator in self.generators:
                output += (self.poly_mult(stream, generator))
            self.shift_state(bit)
        return output
    
    def encode_from_state(self, state, bit):
        stream = bit + state
        output = ''
        for generator in self.generators:
            output += (self.poly_mult(stream, generator))
        return output
    
    def decode(self, bitstream):
        rate = self.n     
        prev_state = []
        score = []
        # states (state, history, score)
        states =[('0'*self.constraint,'',0)]
        
        for i in range(0, len(bitstream), rate):
            rx_symbol = bitstream[i:i+rate]
            next_step = []
            for prev_state in states:
                # next bit 0
                next_state = '0' + prev_state[STATE][:-1]
                symbol = self.encode_from_state(prev_state[STATE], '0')
                history = prev_state[HISTORY] + '0'
                score = prev_state[SCORE] + self.__hamming_dist__(symbol, rx_symbol)
                next_step.append((next_state, history, score))
    
                # next bit 1
                next_state = '1' + prev_state[STATE][:-1]
                symbol = self.encode_from_state(prev_state[STATE], '1')
                history = prev_state[HISTORY] + '1'
                score = prev_state[SCORE] + self.__hamming_dist__(symbol, rx_symbol)
                next_step.append((next_state, history, score))
                
            states = next_step[:]
            
            # Prune the trellis; remove worst score path for each state
            states = self.__prune_trellis__(states)
    
        # Find the best scoring path
        score = states[0][SCORE]
        best = states[0][HISTORY]
        for item in states:
            if item[SCORE] < score:
                score = item[SCORE]
                best = item[HISTORY]

        return best

    def __prune_trellis__(self, trellis):
        # trellis -> (state, history, score)
        new_trellis = []
        considered_states = []
        for i, item in enumerate(trellis):
            compared = 0
            if item[STATE] not in considered_states:
                considered_states.append(item[STATE])
            else:
                continue
            for j in range(i+1, len(trellis)):
                comp_item = trellis[j]
                if item[STATE] == comp_item[STATE]:
                    compared = 1
                    if item[SCORE] < comp_item[SCORE]:
                        new_trellis.append(item)
                    # we don't consider case where the two paths are equal
                    # currently choose the latter path
                    else:
                        new_trellis.append(comp_item)
            if compared == 0:
                new_trellis.append(item)
            
        return(new_trellis)
        
    def __hamming_dist__(self, a, b):
        count = 0
        for i, bita in enumerate(a):
            if bita != b[i]:
                count += 1
        return count