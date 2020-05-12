import random

IMAGE_DIR = 'img/'
# IMAGE_DIR = ''
STATUSES1 = ['The entire world\'s population could fit inside Los Angeles.',
            'There are more twins now than ever before.',
            'More people visit France than any other country.',
            'The world\'s quietest room is located at Microsoft\'s headquarters in Washington state.',
            'There are only three countries in the world that don\'t use the metric system.',
            'Four babies are born every second.',
            'Only two countries use purple in their national flags.',
            'South Sudan is the youngest country in the world.',
            'All giant pandas in zoos around the world are on loan from China.',
            'Canada has nine percent of the world\'s forests.',
            'Around one in every 200 men are direct descendants of Genghis Khan.',
            'All the ants on Earth weigh about as much as all the humans.',
            'Two people die each second.',
            'In Svalbard, a remote Norwegian island, it is illegal to die.',
            'Saint Lucia is the only country in the world named after a woman.',
            'Banging your head against a wall for one hour burns 150 calories.',
            'The oldest your mom joke was discovered on a 3,500 year old Babylonian tablet.',
            'Heart attacks are more likely to happen on a Monday.',
            'Sea otters hold hands when they sleep so they don’t drift away from each other.',
            'There is an official Wizard of New Zealand.'
            ]
IMGS1 = ['la.png', 'twins.png', 'france.png', 'mc.png', 'meter.png', 'baby.png', 'flag.png', 'southsudan.png',
        'panda.png', 'canada.png', 'khan.png', 'ants.png', 'graveyard.png', 'svalbard.png', 'stlucia.png', 'head.png',
        'yourmom.png', 'heart.png', 'otters.png', 'wizard.png']

STATUSES = ['The entire world\'s population could fit inside Los Angeles.']
IMGS = ['la.png']


def get_post():
    ran = random.randint(0, len(IMGS)-1)
    return STATUSES[ran], IMAGE_DIR + IMGS[ran]


if __name__ == '__main__':
    print(get_post())