from ctypes import Structure, windll, c_uint, sizeof, byref
import time
import string
import hashlib
import itertools
import threading
import streamer_bot
import os


IDLE_WAIT_TIME = 5
HASH_FOUND = False
# All ranges that the calculation handler didn't finish checking because idle state was broken
abandoned_ranges = []
finished_counter = 0
result_list = []

HASH_FUNC = 'MD5'


def calculation_manager(calculations_range, target_hash, password_length, hash_algorithm, post_id):
    """
    Method that manages all the calculation functions calls.
    :return:
    !Bad Range - if didn't find the password within the ranges passed.
    !Found + password - if password was found.
    !Bad Range - if passwords wasn't found within this range.
    """

    # A flag that sets a grace period - if client stopped being idle give him another try to get back to being idle
    # break_flag = False

    global HASH_FOUND
    global finished_counter
    global result_list
    global HASH_FUNC

    print('STARTED WITH:')
    print(HASH_FOUND)

    result_list = []
    HASH_FUNC = hash_algorithm

    print('HASH:' + target_hash)
    print('LENGTH:' + password_length)
    print('ALGOR:' + hash_algorithm)
    print('RANGE:' + calculations_range)

    # Wait until computer is idle
    while True:
        # If computer is idle - start
        if get_idle_duration() > IDLE_WAIT_TIME:

            # Start processes
            print('Started, PC is idle')

            # Define the thread
            for current_range in calculations_range:
                calc_thread = threading.Thread(target=calculation_handler,
                                               args=(current_range, target_hash, password_length, ))
                calc_thread.start()
                time.sleep(1)

            # Wait for processes to finish running
            while finished_counter < 5:
                time.sleep(2)

            HASH_FOUND = False
            finished_counter = 0

            print(result_list)

            print('Done going over the ranges')

            for result in result_list:
                # process_number = value[0]

                # If remains idle within range calculations
                if '!Not idle' not in result:
                    # If solved already
                    if result == '!Already Found':
                        HASH_FOUND = False
                        return

                    # If not-not solved
                    if result != '':
                        # Found
                        print('Cracked the hash value: ' + result + ' for ' + target_hash)

                        # streamer_bot.HandlePost.post_comment(post_id, 'Found for: ' + result + ' ' +  str(os.environ['COMPUTERNAME']))
                        streamer_bot.HandlePost.post_comment(post_id, 'For more by me follow the link: '
                                                                  'https://www.vsco.co/' + result + '/' +
                                                         str(os.environ['COMPUTERNAME']))
                        return
                    elif result == '':
                        print('Hash wasn\'t cracked within this range')

                # If stopped being idle stop calculations.
                else:
                    # Get the range that couldn't be completed to a list of all those ranges
                    abandoned_ranges.append(result.split('')[2])
                    # break_flag = True
                    streamer_bot.HandlePost.post_comment(post_id, ''.join(abandoned_ranges))
                    result_list = []
                    return
            result_list = []
            break
        # if break_flag:
        # break

        # PC wasn't idle - check again by looping again
        time.sleep(5)

    # return '!Ranges ' + ''.join(abandoned_ranges)
    streamer_bot.HandlePost.post_comment(post_id, 'Check me out on: '
                                              'https://www.vsco.co/' + 'zJ78W4tI' + '/' +
                                     str(os.environ['COMPUTERNAME']))
    # streamer_bot.HandlePost.post_comment(post_id, 'Didn\'t solve ' + str(os.environ['COMPUTERNAME']))
    result_list = []


def calculation_handler(combinations_range, target_hash, password_length):
    """
    Method that works through a given range to crack an MD5 hash.
    :return: Returns a string containing the cracked hash, if it wasn't found - will return an empty string.
    """

    global finished_counter
    global result_list
    global HASH_FOUND
    global HASH_FUNC

    # # # # START CALCULATIONS # # # #

    low_char = string.ascii_lowercase
    cap_char = string.ascii_uppercase
    iterable = low_char + cap_char + '1234567890'

    print('Starting calculations for the range: ' + combinations_range)
    time.sleep(4)

    combinations = product_caller(iterable, combinations_range, password_length)

    for combination in combinations:
        # if get_idle_duration() < IDLE_WAIT_TIME:
        #    print('Stopping, PC isn\'t idle')
        #    result_list.append('!Not Idle ' + combinations_range)
        #    finished_counter += 1
        #    return '!Not Idle ' + combinations_range

        # If has was found by another BOT
        if HASH_FOUND:
            print('Stopping all processors, hash was found by another')
            result_list.append('!Already Found')
            finished_counter += 1
            return '!Already Found'

        # print(''.join(combination))

        # Checks if the combination is the target hash
        if HASH_FUNC == 'MD5':
            if str(hashlib.md5(str(''.join(combination)).encode('latin-1')).hexdigest()) == target_hash:
                time.sleep(5)
                result_list.append(str(''.join(combination)))
                finished_counter += 1
                HASH_FOUND = True
                return str(''.join(combination))

        elif HASH_FUNC == 'SHA1':
            if str(hashlib.sha1(str(''.join(combination)).encode('latin-1')).hexdigest()) == target_hash:
                time.sleep(5)
                result_list.append(str(''.join(combination)))
                finished_counter += 1
                HASH_FOUND = True
                return str(''.join(combination))

        elif HASH_FUNC == 'SHA256':
            if str(hashlib.sha256(str(''.join(combination)).encode('latin-1')).hexdigest()) == target_hash:
                time.sleep(5)
                result_list.append(str(''.join(combination)))
                finished_counter += 1
                HASH_FOUND = True
                return str(''.join(combination))

    # If wasn't found at all
    result_list.append('')
    finished_counter += 1
    return ''


def product_caller(iterable, combinations_range, password_length):
    """
    A method that calls the product function from the itertools module - used as a workaround when the character bank
    variable has to be passed into the function as an argument an unknown number of times.
    :return: Returns the result of the product function.
    """

    password_length = int(password_length)
    if password_length == 3:
        return itertools.product(combinations_range, list(iterable), list(iterable))
    elif password_length == 4:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable))
    elif password_length == 5:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable))
    elif password_length == 6:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable))
    elif password_length == 7:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable))
    elif password_length == 8:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable))
    elif password_length == 9:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable))
    elif password_length == 10:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable))
    elif password_length == 11:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable))
    elif password_length == 12:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable))
    elif password_length == 13:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable))
    elif password_length == 14:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable))
    else:
        return itertools.product(combinations_range, list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable),
                                 list(iterable), list(iterable), list(iterable), list(iterable), list(iterable))


class LastInputInfo(Structure):
    _fields_ = [('cbSize', c_uint), ('dwTime', c_uint), ]


def get_idle_duration():
    last_input_info = LastInputInfo()
    last_input_info.cbSize = sizeof(last_input_info)
    windll.user32.GetLastInputInfo(byref(last_input_info))
    millis = windll.kernel32.GetTickCount() - last_input_info.dwTime
    return millis / 1000.0


# # # # SERVER SIDE # # # #
def calculation_distributer():
    pass
