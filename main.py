import os

import twint
from PIL import Image, ImageDraw


def download_tweets(handle):
    """
    Downloads the last 1000 tweets from 'handle' to 'handle'.tweets
    Returns the filename
    """

    filename = handle + ".tweets"

    # Checks if we already downloaded the tweets from this handle
    if not os.path.isfile(filename):
        c = twint.Config()

        c.Username = handle
        c.Output = filename
        c.Count = 1000

        twint.run.Profile(c)

    return filename


def process_tweets(filename):
    """
    Opens 'filename', assuming the file with this filename is the output of twint
    Removes unnecessary info from the string
    Returns the string list
    """

    with open(filename) as f:
        lines = f.readlines()
    
    # Remove some info at the beginning with slices
    # Limits all tweets to 300 chars
    return [line[61:361] for line in lines]


def tweet_list_to_numbers(tweet_list):
    """
    Merges 'tweet_list' into a list of numbers using character codes
    Then, limits the numbers to 255 using modolo
    """

    # Initialize array
    # Since we limited the tweets to 300 chars earlier, we only need to initialize 300 items
    number_list = [0 for i in range(300)]

    # Merging
    for tweet in tweet_list:
        for i, char in enumerate(tweet):
            # We initialized the array earlier for this
            number_list[i] += ord(char)

    # Limiting and returning
    return [n % 255 if n > 255 else n for n in number_list]


def numbers_to_rgb_list(number_list):
    """
    Groups the numbers in number_list by 3
    so they can be used as RGB colors
    """

    rgb_list = []

    # The number_list's size is always going to be 300,
    # So we can just group by 3 without worrying about rests
    while number_list:
        rgb_color = []
        while len(rgb_color) < 3:
            rgb_color.append(number_list.pop(0))
        rgb_list.append(tuple(rgb_color))

    return rgb_list


def create_image(rgb_list):
    """
    Returns a PIL image created from the colors in rgb_list
    Assumes rgb_list has 100 items
    """

    im = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(im)

    for i, color in enumerate(rgb_list):
        draw.point((i%10, i//10), color)

    return im


handle = input("Tweet handle:\n")
colors = numbers_to_rgb_list(tweet_list_to_numbers(process_tweets(download_tweets(handle))))
create_image(colors).resize((1000, 1000), Image.NEAREST).save(handle + ".png")
