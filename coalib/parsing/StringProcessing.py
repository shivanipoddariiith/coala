import re


# Searches for a specific pattern. Is a generator function used by
# search_for() to create easily an iterator.
def __search_for_generator__(pattern, string, max_matches, flags):
    # Compile the regex expression to gain performance.
    compiled_pattern = re.compile(pattern, flags)
    # The in-string position that indicates the beginning of the regex
    # processing.
    pos = 0

    for x in range(0, max_matches):
        current_match = compiled_pattern.search(string, pos)

        if (current_match is None):
            # Break out, no more matches found.
            break
        else:
            # Else, append the found match to the match list.
            yield current_match
            # Update the in-string position.
            pos = current_match.end()


def search_for(pattern, string, max_matches = 0, flags = 0):

    """
    Searches for a given pattern in a string max_matches-times.
    :param pattern:     The pattern to search for. Providing regexes (and not
                        only fixed strings) is allowed.
    :param string:      The string to search in.
    :param max_matches: The maximum number of matches to perform.
    :param flags:       Additional flags to pass to the regex processor.
    :raises ValueError: Raised when a negative number is provided for
                        max_matches.
    :return:            A list of MatchGroup's containing information about
                        each match performed.
    """
    if (max_matches == 0):
        # Use plain re.finditer() to find all matches.
        return re.finditer(pattern, string, flags)
    elif (max_matches > 0):
        return __search_for_generator__(pattern, string, max_matches, flags)
    else:
        # Throw an exception.
        raise ValueError("Provided value for parameter 'max_matches' below "
                         "zero. Negative numbers are not allowed.")

