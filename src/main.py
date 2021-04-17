from pylfsr import LFSR
from nistrng import *
import numpy


bits_1 = 5
bits_2 = 7
bits_3 = 8

lfsr_seed_1 = [1, 0, 0, 1, 0] # 10010
lfsr_seed_2 = [0, 0, 1, 0, 0, 0, 1] # 0010001
lfsr_seed_3 = [0, 0, 1, 0, 0, 1, 0, 1] # 00100101

lfsr_polynom_1 = [5, 4, 2, 1] # x^5 + x^4 + x^2 + x + 1
lfsr_polynom_2 = [7, 6, 4, 1] # x^7 + x^6 + x^4 + x + 1
lfsr_polynom_3 = [8, 5, 3, 1] # x^8 + x^5 + x^3 + x + 1


def lfsr(bits, seed, polynom): # add ind to parameters if you want to check sequence length
    while True:
        nxt = sum([seed[i - 1] for i in polynom]) % 2 # xor
        yield nxt
        seed = ([nxt] + seed)[:bits] # new seed
        
        '''
        ind += 1
        if seed == lfsr_seed_3:
            print(ind)
            break
        '''


def lfsr_lib(L: LFSR, bits, length):
    for i in range(length - 1):
        if i >= (bits - 1):
            yield L.next()
        else:
            L.next()


def lfsr_check(bits, seed, polynom, length):
    index = 0
    for x in lfsr(bits, seed, polynom):
        print(x)

        index += 1
        if index == length:
            break

    for x in lfsr_lib(LFSR(fpoly=polynom, initstate=seed, verbose=True), bits, length + bits):
        print(x)


def lfsr_geffe(bits, seed, polynom):
    while True:
        nxt = sum([seed[i - 1] for i in polynom]) % 2
        seed = ([nxt] + seed)[:bits]
        yield nxt, seed


def geffe():
    seed_1 = lfsr_seed_1
    seed_2 = lfsr_seed_2
    seed_3 = lfsr_seed_3
    while True:
        s1, seed_1 = next(lfsr_geffe(bits_1, seed_1, lfsr_polynom_1))
        s2, seed_2 = next(lfsr_geffe(bits_2, seed_2, lfsr_polynom_2))
        s3, seed_3 = next(lfsr_geffe(bits_3, seed_3, lfsr_polynom_3))
        yield (s1 * s2) ^ ((s1 ^ 1) * s3)


def count_ones(sequence):
    count = 0
    for x in sequence:
        if x == 1:
            count += 1
    
    return count


def theta(x):
    return pow(-1, x)


def count_rstat(sequence):
    rs = []
    for i in (1, 2, 3, 4, 5):
        tmp = 0
        for j in range(10000 - i):
            tmp += theta(sequence[j] ^ sequence[j + i])
        
        rs.append(tmp)

    return rs


if __name__ == '__main__':
    '''
    print('LFSR #1:')
    lfsr_check(bits_1, lfsr_seed_1, lfsr_polynom_1, 10)
    print('\nLFSR #2:')
    lfsr_check(bits_2, lfsr_seed_2, lfsr_polynom_2, 10)
    print('\nLFSR #3:')
    lfsr_check(bits_3, lfsr_seed_3, lfsr_polynom_3, 10)
    '''

    '''
    ind = 0
    for x in lfsr(bits_1, lfsr_seed_1, lfsr_polynom_1, ind):
        print(x)
    ind = 0
    for x in lfsr(bits_2, lfsr_seed_2, lfsr_polynom_2, ind):
        print(x)
    ind = 0
    for x in lfsr(bits_3, lfsr_seed_3, lfsr_polynom_3, ind):
        print(x)
    '''

    ind = 0
    sequence = []
    for x in geffe():
        sequence.append(x)
        ind += 1
        if ind == 10000:
            break
    
    ones = count_ones(sequence)
    print(ones)
    print(10000 - ones)
    print(count_rstat(sequence))
    print(sequence)

    for x in geffe():
        sequence.append(x)
        ind += 1
        if ind == 10000000:
            break
    
    binary_sequence = numpy.array(sequence)
    eligible_battery: dict = check_eligibility_all_battery(binary_sequence, SP800_22R1A_BATTERY)
    results = run_all_battery(binary_sequence, eligible_battery, False)
    print("Test results:")
    for result, elapsed_time in results:
        if result.passed:
            print("- PASSED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        else:
            print("- FAILED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
