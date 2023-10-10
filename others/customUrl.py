# If you prefer not to use `urllib.parse`, you can implement URL encoding and decoding manually using Python's built-in string manipulation methods. Here's how you can do it:

# **URL Encoding (Percent-Encoding) Without urllib.parse:**

def custom_url_encode(input_string):
    encoded_string = ""
    for char in input_string:
        if char.isalnum() or char in ['-', '_', '.', '~']:
            encoded_string += char
        else:
            encoded_string += f"%{ord(char):02X}"
    return encoded_string

original_string = "Hello, world! How are you?"
encoded_string = custom_url_encode(original_string)

print(f"Original string: {original_string}")
print(f"Encoded string: {encoded_string}")


# This `custom_url_encode` function manually replaces special characters in the input string with their percent-encoded versions. It checks if a character is alphanumeric or belongs to the set of safe characters ('-', '_', '.', '~'), and if not, it converts the character to its hexadecimal ASCII code.

# **URL Decoding Without urllib.parse:**

def custom_url_decode(encoded_string):
    decoded_string = ""
    i = 0
    while i < len(encoded_string):
        char = encoded_string[i]
        if char == '%' and i + 2 < len(encoded_string):
            hex_digits = encoded_string[i + 1:i + 3]
            try:
                decoded_char = chr(int(hex_digits, 16))
                decoded_string += decoded_char
                i += 3  # Skip the percent-encoded characters
            except ValueError:
                decoded_string += char  # Leave invalid percent-encoded sequences as-is
                i += 1
        else:
            decoded_string += char
            i += 1
    return decoded_string

encoded_string = "Hello%2C%20world%21%20How%20are%20you%3F"
decoded_string = custom_url_decode(encoded_string)

print(f"Encoded string: {encoded_string}")
print(f"Decoded string: {decoded_string}")

# The `custom_url_decode` function manually decodes a URL-encoded string by iterating through the string, identifying percent-encoded sequences, and converting them back to their original characters. Invalid percent-encoded sequences are left as-is.

# These custom methods provide an alternative to `urllib.parse` for URL encoding and decoding in Python. However, please note that using `urllib.parse` is generally recommended because it's a standard library and provides a more comprehensive solution for working with URLs and percent encoding.