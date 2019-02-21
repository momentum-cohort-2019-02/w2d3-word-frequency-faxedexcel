import string # this statement is needed in order to use the 'string.method's below such as 'string.ascii_letters', 'string.digits', & 'string.whitespace' https://docs.python.org/3.7/library/string.html

# exclude the words below from being counted
STOP_WORDS = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'were',
    'will', 'with'
]

def normalize_text(text):
    """ Given a text, lowercases it, removes all punctuation, and replaces all whitespace with normal spaces. Multiple whitespace will be compressed into a single space. """
    text = text.casefold()
        # '<sample_string>.casefold()' method lowercases the string but is more aggressive b/c it is intended to remove all case distinctions in a string: https://docs.python.org/3.7/library/stdtypes.html?highlight=casefold#str.casefold

    text = text.replace("--", " ")
        # '<sample_string>.replace(old, new, count)' method replaces all occurences of '--' with 'blank space', so words don't get combined
        # https://docs.python.org/3.7/library/stdtypes.html?highlight=replace#str.replace

    valid_chars = string.ascii_letters + string.digits + string.whitespace + "-"
        # assigns the string: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789' + ' \t\n\r\x0b\x0c' to the variable 'valid_chars'
        # ' \t\n\r\x0b\x0c' --> blank space, tab, newline, carriage return, line tabulation, form feed
        # 'import string' statement is required above in order for this to work
        # added hypen '-' so hyphenated words will count as a word

    # remove all punctuation
    new_text = ""
    for char in text:
        if char in valid_chars:
            new_text += char
    text = new_text
    text = text.replace("\n", " ") # replaces all occurences of 'newline' with 'blank space'
        
    return text


def print_word_freq(filename):
    """ Read in `file` and print out the frequency of words in that file. """
    # 'pass' statement is a null operation, useful in places where your code will eventually go, but has not been written yet https://docs.python.org/3.7/reference/simple_stmts.html#the-pass-statement
 
    # read in the text
    with open(filename) as file:
        # 'with' statement is used to wrap the execution of a block with methods defined by a context manager https://docs.python.org/3.7/reference/compound_stmts.html#the-with-statement
        # a 'context manager' is an object that defines the runtime context to be established when executing a 'with' statement. the 'context manager' handles the entry into, and the exit from, the desired runtime context for the execution of the block of code https://docs.python.org/3.7/reference/datamodel.html#context-managers
        # 'context manager types' https://docs.python.org/3.7/library/stdtypes.html#typecontextmanager
        # 'open(file, mode='r', bufferring=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)' function opens 'file' named 'filename' https://docs.python.org/3.7/library/functions.html#open
        # simpler explanation: https://www.pythonforbeginners.com/files/with-statement-in-python
        text = file.read()
    
    # create list of valid words in 'text' to count
    text = normalize_text(text)
    words = []
    for word in text.split(" "):
        # '<sample_string>.split(sep=None, maxsplit=-1)' method will split 'text' using blank spaces as the delimiter and returns a list of words
        if word != '' and word not in STOP_WORDS:
            words.append(word)

    # sort 'words' list alphanumerically
    words = sorted(words, key=str.lower) 
    
    # create dictionary with 'unique words' as keys and 'word count' as values
    word_count = {} # declare an empty dictionary called 'word_count'
    for word in words:
        if word in word_count:
            # if 'word' key is already in the 'word_count' dictionary, then add 1 to the value of the 'word' key
            word_count[word] = word_count[word] + 1
        else:
            # if 'word' key is not in the 'word_count' dictionary, then declare the key and set the value to 1 and add it to the 'word-count' dictionary
            word_count[word] = 1

    # sorts 'word_count' dictionary
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        # 'sorted()' function returns a list of tuples
        # ***** NEED TO UNDERSTAND THE SYNTAX OF THIS *****

    # determine the length of the longest word to adjust spacing of the report
    max_word_length = len(sorted_word_count[0][0])
    i = 0
    while i < len(sorted_word_count):
        if len(sorted_word_count[i][0]) > max_word_length:
            max_word_length = len(sorted_word_count[i][0])
        i += 1

    # iterate through 'sorted_word_count' list to print desired report
    i = 0
    while i < len(sorted_word_count):
        print(f"{sorted_word_count[i][0].rjust(max_word_length, ' ')} | {str(sorted_word_count[i][1]).ljust(2, ' ')} {'*' * sorted_word_count[i][1]}")
            # 'sorted_word_count[i][0]' accesses the 1st item of the tuple within the 'i'th list item and thus returns the word
            # 'sorted_word_count[i][1]' accesses the 2nd item of the tuple within the 'i'th list item and thus returns the word count
            # '.rjust(20, ' ')' method creates a string with 'max_word_length' spaces, right-aligns the string object and fills in the rest of the space with blank spaces
            # '.ljust(2, ' ')' method creates a string with 2 spaces, left-aligns the string object and fills in the rest of the space with blank spaces...here the 'str()' function had to be used to convert integer to string in order for the method to work
            # '*' * sorted_word_count[i][1] --> repeats the string '*' sorted_word_count[i][1] times
        i += 1

# need block of code below to be able to run 'python3 word_frequency.py seneca_falls.txt' in command line
# ***** NEED TO UNDERSTAND THE SYNTAX OF THIS *****
if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Get the word frequency in a text file.')
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        print_word_freq(file)
    else:
        print(f"{file} does not exist!")
        exit(1)

# questions:
# how does this statement: 'sorted(word_count.items(), key=lambda x: x[1], reverse=True)' work?

# output: 
#              her | 33 *********************************
#              all | 12 ************
#            which | 12 ************
#              she | 7  *******
#            their | 7  *******
#             they | 7  *******
#            right | 6  ******
#           rights | 6  ******
#             such | 6  ******
#             them | 6  ******
#             this | 6  ******
#            women | 6  ******
#              but | 5  *****
#       government | 5  *****
#              man | 5  *****
#          history | 4  ****
#              law | 4  ****
#             laws | 4  ****
#          mankind | 4  ****
#             most | 4  ****
#            these | 4  ****
#             when | 4  ****
#         absolute | 3  ***
#           causes | 3  ***
#           giving | 3  ***
#        happiness | 3  ***
#           having | 3  ***
#             made | 3  ***
#              men | 3  ***
#              not | 3  ***
#           object | 3  ***
#           powers | 3  ***
#         property | 3  ***
#            shall | 3  ***
#      usurpations | 3  ***
#            woman | 3  ***
#            world | 3  ***
#          against | 2  **
#            among | 2  **
#              any | 2  **
#          becomes | 2  **
#            being | 2  **
#              can | 2  **
#           candid | 2  **
#           church | 2  **
#         claiming | 2  **
#        compelled | 2  **
#           course | 2  **
#          created | 2  **
#         deprived | 2  **
#        different | 2  **
#           direct | 2  **
#         elective | 2  **
#            equal | 2  **
#    establishment | 2  **
#            facts | 2  **
#            false | 2  **
#             form | 2  **
#        franchise | 2  **
#            given | 2  **
#              god | 2  **
#      governments | 2  **
#             have | 2  **
#          himself | 2  **
#              his | 2  **
#          husband | 2  **
#               if | 2  **
#      inalienable | 2  **
#         injuries | 2  **
#           insist | 2  **
#              let | 2  **
#          liberty | 2  **
#             life | 2  **
#             long | 2  **
#          married | 2  **
#              new | 2  **
#              now | 2  **
#              one | 2  **
#             only | 2  **
#        oppressed | 2  **
#             over | 2  **
#             part | 2  **
#           people | 2  **
#        permitted | 2  **
#         position | 2  **
#            power | 2  **
#       profitable | 2  **
#            prove | 2  **
#           public | 2  **
#         repeated | 2  **
#           should | 2  **
#        submitted | 2  **
#           suffer | 2  **
#       themselves | 2  **
#            those | 2  **
#           toward | 2  **
#          tyranny | 2  **
#            under | 2  **
#             upon | 2  **
#             view | 2  **
#               we | 2  **
#           abject | 1  *
#       abolishing | 1  *
#            above | 1  *
#           abuses | 1  *
#      accordingly | 1  *
#          account | 1  *
#       accustomed | 1  *
#           action | 1  *
#       administer | 1  *
#        admission | 1  *
#          affairs | 1  *
#            after | 1  *
#        aggrieved | 1  *
#       allegiance | 1  *
#           allows | 1  *
#        apostolic | 1  *
#           assign | 1  *
#           assume | 1  *
#        authority | 1  *
#          avenues | 1  *
#          because | 1  *
#         becoming | 1  *
#             been | 1  *
#           belong | 1  *
#          belongs | 1  *
#             both | 1  *
#             case | 1  *
#            cases | 1  *
#          certain | 1  *
#          changed | 1  *
#     chastisement | 1  *
#         children | 1  *
#          citizen | 1  *
#         citizens | 1  *
#          civilly | 1  *
#           closed | 1  *
#           closes | 1  *
#             code | 1  *
#         colleges | 1  *
#           commit | 1  *
#       confidence | 1  *
#       conscience | 1  *
#          consent | 1  *
#        considers | 1  *
#       constrains | 1  *
#            could | 1  *
#          country | 1  *
#         covenant | 1  *
#          creator | 1  *
#           crimes | 1  *
#             dead | 1  *
#           decent | 1  *
#          declare | 1  *
#           deemed | 1  *
#      degradation | 1  *
#         degraded | 1  *
#    delinquencies | 1  *
#           demand | 1  *
#           denied | 1  *
#        dependent | 1  *
#          deprive | 1  *
#        depriving | 1  *
#         deriving | 1  *
#           design | 1  *
#        despotism | 1  *
#          destroy | 1  *
#      destructive | 1  *
#          dictate | 1  *
# disfranchisement | 1  *
#         disposed | 1  *
#      distinction | 1  *
#          divorce | 1  *
#               do | 1  *
#             done | 1  *
#             duty | 1  *
#            earns | 1  *
#            earth | 1  *
#        education | 1  *
#           effect | 1  *
#      employments | 1  *
#       endeavored | 1  *
#          endowed | 1  *
#             ends | 1  *
#           entire | 1  *
#          entitle | 1  *
#         entitled | 1  *
#      established | 1  *
#             even | 1  *
#           events | 1  *
#            every | 1  *
#            evils | 1  *
#          evinces | 1  *
#       exceptions | 1  *
#          exclude | 1  *
#        exclusion | 1  *
#         exercise | 1  *
#       experience | 1  *
#              eye | 1  *
#       facilities | 1  *
#           family | 1  *
#             feel | 1  *
#            first | 1  *
#           follow | 1  *
#       foreigners | 1  *
#        formation | 1  *
#            forms | 1  *
#       foundation | 1  *
#           framed | 1  *
#     fraudulently | 1  *
#           future | 1  *
#            going | 1  *
#         governed | 1  *
#     guardianship | 1  *
#           guards | 1  *
#              had | 1  *
#            halls | 1  *
#            hands | 1  *
#             hath | 1  *
#              him | 1  *
#         hitherto | 1  *
#             hold | 1  *
#        honorable | 1  *
#            human | 1  *
#         ignorant | 1  *
#        immediate | 1  *
#            impel | 1  *
#         impunity | 1  *
#           indeed | 1  *
#       instituted | 1  *
#      institution | 1  *
#          intents | 1  *
#             into | 1  *
#       invariably | 1  *
#    irresponsible | 1  *
#          jehovah | 1  *
#             just | 1  *
#            known | 1  *
#           laying | 1  *
#             lead | 1  *
#          leaving | 1  *
#      legislation | 1  *
#           lessen | 1  *
#            light | 1  *
#           likely | 1  *
#           little | 1  *
#             make | 1  *
#             many | 1  *
#         marriage | 1  *
#           master | 1  *
#         medicine | 1  *
#        mentioned | 1  *
#         ministry | 1  *
#      monopolized | 1  *
#            moral | 1  *
#          morally | 1  *
#           morals | 1  *
#             more | 1  *
#          natives | 1  *
#           nature | 1  *
#          natures | 1  *
#           nearly | 1  *
#        necessary | 1  *
#        necessity | 1  *
#            never | 1  *
#               no | 1  *
#        obedience | 1  *
#        obtaining | 1  *
#         occupied | 1  *
#              off | 1  *
#         one-half | 1  *
#         opinions | 1  *
#               or | 1  *
#       organizing | 1  *
#              own | 1  *
#            owner | 1  *
#    participation | 1  *
#          patient | 1  *
#          portion | 1  *
#      prerogative | 1  *
#         presence | 1  *
#       principles | 1  *
#       privileges | 1  *
#          promise | 1  *
#           proper | 1  *
#          provide | 1  *
#         provided | 1  *
#         prudence | 1  *
#         purposes | 1  *
#         pursuing | 1  *
#          pursuit | 1  *
#         receives | 1  *
#       recognizes | 1  *
#           reduce | 1  *
#           refuse | 1  *
#       regardless | 1  *
#        religious | 1  *
#     remuneration | 1  *
#   representation | 1  *
#         requires | 1  *
#          respect | 1  *
#           sacred | 1  *
#           safety | 1  *
#             same | 1  *
#           scanty | 1  *
#           secure | 1  *
#         security | 1  *
#             seem | 1  *
#     self-evident | 1  *
#     self-respect | 1  *
#        sentiment | 1  *
#       separation | 1  *
#            shown | 1  *
#            sides | 1  *
#           single | 1  *
#               so | 1  *
#           social | 1  *
#          society | 1  *
#             some | 1  *
#           sphere | 1  *
#            state | 1  *
#           states | 1  *
#          station | 1  *
#           submit | 1  *
#      subordinate | 1  *
#       sufferable | 1  *
#       sufferance | 1  *
#          support | 1  *
#      supposition | 1  *
#        supremacy | 1  *
#            taken | 1  *
#            taxed | 1  *
#          teacher | 1  *
#             than | 1  *
#         theology | 1  *
#          thereby | 1  *
#         thorough | 1  *
#            throw | 1  *
#        tolerated | 1  *
#            train | 1  *
#        transient | 1  *
#           truths | 1  *
#           united | 1  *
#           unjust | 1  *
#          usurped | 1  *
#            voice | 1  *
#            wages | 1  *
#              way | 1  *
#           wealth | 1  *
#             well | 1  *
#             what | 1  *
#         whenever | 1  *
#            while | 1  *
#              who | 1  *
#           wholly | 1  *
#             whom | 1  *
#          willing | 1  *
#         withheld | 1  *
#          without | 1  *