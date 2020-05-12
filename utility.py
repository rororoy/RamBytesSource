# Functions to handel image steganography - last significant hex value.

from PIL import Image


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex_to_rgb(hex_value):
    """
    Method to convert the hex value of the color to a tuple of rgb.
    :param hex_value: The hex value to convert.
    :return: A tuple representing the rgb values - (r, g, b).
    """
    return tuple(int(hex_value[1:][i:i+2], 16) for i in (0, 2, 4))


def string_to_binary(data):
    """
    Method to convert each character of the string to a byte.
    :param data: The string containing bits.
    :return: The message in the form of bytes.
    """
    # Data to byte tuple
    data = (format(ord(i), 'b') for i in data)
    binary = ''
    # Fixing bytes by adding 0/00 to the end
    for i in data:
        if len(i) == 6:
            binary += '00' + i
        elif len(i) == 7:
            binary += '0' + i
        elif len(i) == 5:
            binary += '000' + i

    return str(binary)


def binary_to_string(binary):
    """
    Method to convert bytes representing ASCII characters to a string.
    :param binary: The string of the bits.
    :return: The message in a form of the string.
    """
    n = int('0b' + binary, 2)
    print(n)
    data = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return data


def encode(hex_value, digit):
    """
    Method to put the next bit of the message in binary into the hex
    value of the rgb values.
    :param hex_value: The hex value representing the rgb color.
    :param digit: The next bit of the binary message to encode.
    :return: The updated hex value, None if hex value wasn't right.
    """
    # If the blue channel value's digit has a low enough value (between 0
    # and 5) so that it won't be noticeable, replace with digit.
    if 0 <= int(hex_value[-1], 16) <= 5:
        hex_value = hex_value[:-1] + digit
        return hex_value
    return None


def decode(hex_value):
    """
    Method to extract the last digit of the blue channel if 1 or 0.
    :param hex_value: The hex value representing the rgb value to inspect.
    :return: The last digit of the blue channel, None if it's not 0 or 1.
    """
    # If last digit of the blue channel is 0 or 1 that means it's part
    # of the message.
    if hex_value[-1] in ('0', '1'):
        return hex_value[-1]
    return None


def hide(filename, message):
    """
    Method to hide the message inside the picture.
    :param filename: The name of the picture file to hide the message in.
    :param message: The message to hide inside the picture.
    :return: True if it worked, False if it didn't (Bad image mode).
    """
    img = Image.open(filename)
    # The #FFFE at the end indicates the end of the message,
    # comes after the last character of the message.
    binary = string_to_binary(message) + '1111111111111110'

    print(filename)

    img = img.convert('RGB')

    if img.mode == 'RGB':
        # Each element in data list is in rgb form.
        data = img.getdata()

        new_data = []
        bin_len_count = 0

        for i in data:
            if bin_len_count < len(binary):
                # Craft the new pixel with the next binary digit
                new_pixel = encode(rgb_to_hex(i[0], i[1], i[2]), binary[bin_len_count])
                if new_pixel is None:
                    new_data.append(i)
                else:
                    r, g, b = hex_to_rgb(new_pixel)
                    new_data.append((r, g, b))
                    bin_len_count += 1
            else:
                # If we've reached the end of the message we want to hide
                # put the rest of the pixels to the new img.
                new_data.append(i)
        img.putdata(new_data)
        img.save(filename, "PNG")
        # print('Done')
        return 'Done'
    # print('Bad image mode')
    return 'Bad image mode'


def retrieve(filename):
    """
    Method to extract the hidden message from the picture.
    :param filename: The name of the picture file to extract the hidden message from.
    :return: The message or an error message.
    """
    img = Image.open(filename)
    binary = ''

    if img.mode == 'RGB':
        img = img.convert('RGB')
        data = img.getdata()

        for i in data:
            # Extract the last digit of the pixel color hex value color.
            digit = decode(rgb_to_hex(i[0], i[1], i[2]))
            if digit is not None:
                binary += digit
                if binary[-16:] == '1111111111111110':
                    print('Found')
                    return binary_to_string(binary[:-16])
        return binary_to_string(binary)
    return 'Bad image mode'


if __name__ == '__main__':
    # text = input('M> ')
    # file_name = input('F> ')
    # print(hide(file_name, text))
    print(retrieve('testImg.png'))
