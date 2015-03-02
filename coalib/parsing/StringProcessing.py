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


def split(pattern,
          string,
          max_split = 0,
          remove_empty_matches = False):

    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function ignores escape sequences.
    :param pattern:              A regex pattern that defines where to split.
    :param string:               The string to split by the defined pattern.
    :param max_split:            Defines the maximum number of splits. If 0 is
                                 provided, unlimited splits are made.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the resulting list.
    :raises ValueError:          Raised when a negative number is provided for
                                 max_split.
    :return:                     A list containing the split up strings.
    """

    # re.split() is not usable any more for this function. It has a bug when
    # using too much capturing groups "()". Using the same approach like
    # unescaped_split().
    match_strings = []
    matches = search_for(r"(.*?)(?:" + pattern + r")",
                         string,
                         max_split,
                         re.DOTALL)

    # Holds the end position of the last processed and matched string. Needed
    # since matches is a callable_iterator and is not subscriptable, means the
    # last element of the result is not accessible with [] on the fly.
    last_pos = 0
    # Process each returned MatchObject.
    for item in matches:
        if (not remove_empty_matches or len(item.group(1)) != 0):
            # Return the first matching group. The pattern from parameter can't
            # change the group order.
            match_strings.append(item.group(1))

        # Update the end position.
        last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if (not remove_empty_matches or len(string[last_pos : ]) != 0):
        match_strings.append(string[last_pos : ])

    return match_strings

