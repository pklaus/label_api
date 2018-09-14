"""
### Name Badge Plugin

Fonts distributed with this plugin:

* Roboto (License: Apache 2.0)
"""

import os
from PIL import Image, ImageDraw, ImageFont

# What's required from a plugin:
# BROTHER_QL_LABEL, ARGUMENTS, create_label()

BROTHER_QL_LABEL = "62"
#BROTHER_QL_LABEL = "38"

ARGUMENTS = {
  'first': {'help': 'First Name', 'type': str, 'default': 'Emmanuelle'},
  'last': {'help': 'Last Name', 'type': str, 'default': 'Baroness Willoughby de Eresby'},
  'company': {'help': 'Company Name', 'type': str, 'default': 'Coláiste na Tríonóide, Baile Átha Cliath'},
}

#FONT_REGULAR = "FreeSans.ttf"
#FONT_MEDIUM  = "FreeSansBold.ttf"
FONT_REGULAR = "Roboto-Regular.ttf"
FONT_MEDIUM  = "Roboto-Medium.ttf"

#LABEL_SIZE = (696, 756)
LABEL_SIZE = (756, 696)
#LABEL_SIZE = (413, 413)
FONT_SCALING = 4.2
#FONT_SCALING = 4.2*0.593

BROTHER_QL_CONVERT_KWARGS = {
  'rotate': '90',
}

def resource_path(rel_path):
    return os.path.join(os.path.dirname(__file__), rel_path)

def create_label(first="", last="", company=""):
    if not first: first = ARGUMENTS['first']['default']
    if not last: last = ARGUMENTS['last']['default']
    if not company: company = ARGUMENTS['company']['default']
    im = Image.new("L", LABEL_SIZE, 255)
    draw = ImageDraw.Draw(im)
    ## FIRST NAME
    #print("Placing first name")
    x_pos, y_pos = 0, 0
    font_path = resource_path(FONT_MEDIUM)
    ifs = int(35*FONT_SCALING) # initial font size
    font = fit_text(first, LABEL_SIZE[0], font_path, ifs)
    draw.text((x_pos, y_pos), first, font=font, fill=0)
    ## LAST NAME
    #print("Placing last name")
    y_pos += font.size * 1.3
    font_path = resource_path(FONT_REGULAR)
    ifs = int(20*FONT_SCALING) # initial font size
    font = fit_text(last, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(last, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)
    ## COMPANY NAME
    #print("Placing company name")
    y_pos = 450
    font_path = resource_path(FONT_MEDIUM)
    ifs = int(24*FONT_SCALING) # initial font size
    font = fit_text(company, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.2)
    for i, line in enumerate(break_text_whitespace(company, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)
    ## Done, returning the Image instance
    return im

def break_text_any(txt, font, max_width):
    """ 
    break text at any character
    https://stackoverflow.com/a/43828315/183995
    """

    # We share the subset to remember the last finest guess over 
    # the text breakpoint and make it faster
    subset = len(txt)
    letter_size = None

    text_size = len(txt)
    while text_size > 0:

        subsets_tried = []
        # Let's find the appropriate subset size
        while True:
            width, height = font.getsize(txt[:subset])
            letter_size = width / subset

            # min/max(..., subset +/- 1) are to avoid looping infinitely over a wrong value
            if width < max_width - letter_size and text_size >= subset: # Too short
                subset = max(int(max_width * subset / width), subset + 1)
            elif width > max_width: # Too large
                subset = min(int(max_width * subset / width), subset - 1)
            else: # Subset fits, we exit
                break

            if subset in subsets_tried:
                break
            else:
                subsets_tried.append(subset)

        yield txt[:subset]
        txt = txt[subset:]   
        text_size = len(txt)

def break_text_whitespace(txt, font, max_width):
    """
    break text at whitespace
    https://stackoverflow.com/a/43830313/183995
    """

    line = ""
    width_of_line = 0
    # break string into multi-lines that fit max_width
    for token in txt.split():
        token = token+' '
        token_width = font.getsize(token)[0]
        if width_of_line + token_width < max_width:
            line += token
            width_of_line += token_width
        else:
            yield line
            width_of_line = 0
            line = ""
            line += token
            width_of_line += token_width
    if line:
        yield line

def fit_text(txt, max_width, font_path, initial_font_size, max_lines=1, delta=-1, break_func=break_text_any):
    """
    Tries to fit the given text in the given
    max_width with the given max_lines.
    Adjusts the font size until it fits.
    Returns the font with the adjusted size.
    """
    font_size = initial_font_size
    font = ImageFont.truetype(font_path, font_size)
    while len(list(break_func(txt, font, max_width))) > max_lines:
        font_size += delta
        if font_size == 5: return font
        font = ImageFont.truetype(font_path, font_size)
    return font
