import random
import time
import post_constructor
import streamer
import utility
import ccp
import ccp_support

EXIT_COMMAND = False


def make_noise():
    print('Making noise')
    time.sleep(10)
    if not ccp.HANDLER_THREAD_RUNNING:
        ccp_support.update_feedback('Generating noise while idle')
        status, filename = post_constructor.get_post()
        result = utility.hide(filename, 'Noise')
        if result:
            streamer.HandlePost.post_tweet(filename, status)

    while True:
        print('Waiting')
        time.sleep(random.randint(1800, 3600))

        if not ccp.HANDLER_THREAD_RUNNING:
            status, filename = post_constructor.get_post()
            result = utility.hide(filename, 'Noise')
            if result:
                streamer.HandlePost.post_tweet(filename, status)


if __name__ == '__main__':
    print('Started noise maker')
    make_noise()