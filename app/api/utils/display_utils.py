def highlight_match(sentence, raw_matches, from_group=0, start_shift=0, end_shift=0):
    highlighted_sentence = ''
    current_pos = 0

    matches = []
    for raw_match in raw_matches:
        overlapped = sum((1 for other_match in raw_matches
                          if raw_match.start() >= other_match.start() and raw_match.end() <= other_match.end()))
        if overlapped == 1:
            matches.append(raw_match)

    for match in sorted(matches, key=lambda x: x.start(from_group) if from_group else x.start()):
        match_start = match.start(from_group) + start_shift if from_group else match.start() + start_shift
        match_end = match.end(from_group) + end_shift if from_group else match.end() + end_shift
        if not current_pos:
            highlighted_sentence += sentence[0:match_start] + \
                                    '<span style="background-color:yellow">' + \
                                    sentence[match_start:match_end] + \
                                    '</span>'
            current_pos = match_end
        else:
            highlighted_sentence += sentence[current_pos:match_start] + \
                                    '<span style="background-color:yellow">' + \
                                    sentence[match_start:match_end] + \
                                    '</span>'
            current_pos = match_end
    if current_pos < len(sentence):
        highlighted_sentence += sentence[current_pos:len(sentence)]
    return highlighted_sentence
