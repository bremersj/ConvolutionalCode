# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 10:53:02 2020

@author: Steve Bremer
"""

from conv_enc import ConvolutionalCode as CC
import random

def add_noise(bitstream, noise_lvl):
    stream_len = len(bitstream)
    flip_index = random.sample(range(stream_len), noise_lvl)
    altered = bitstream[:]
    for index in flip_index:
        if altered[index] == '0':
            altered = altered[:index] + '1' + altered[index+1:]
        else:
            altered = altered[:index] + '0' + altered[index+1:]
    return altered   

def run_exmperiment(convo_code, iterations, code_len, noise_start, noise_stop):
    random.seed()
    print('Experiment code length: %d, iterations: %d' % (code_len, iterations))
    for noise_lvl in range(noise_start, noise_stop):
        err_count = 0
        for i in range(iterations):
            code = ''
            stream = [x%2 for x in random.sample(range(code_len+1), code_len)]
            code = code.join(map(str, stream))
            send = convo_code.encode(code)
            noisy = add_noise(send, noise_lvl)
            decoded = convo_code.decode(noisy)
            if decoded != code:
                err_count += 1
        print('% .2f%% errors at noise level %.2f%%' % (err_count/iterations*100, (noise_lvl/(code_len*convo_code.n))*100))
        
if __name__ == '__main__':
    cc = CC(['1001', '1010', '1100', '1011', '1101', '1110', '1111'])
    #cc = CC(['10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111'])
    #cc = CC(['11100101', '10011111'])
    #cc = CC(['1101110', '1010111', '1111001']) 
    run_exmperiment(cc, 500, 8, 1, 20)