def highlight_match(sentence, matches, from_group=0):
    highlighted_sentence = ''
    current_pos = 0
    for match in sorted(matches, key=lambda x: x.start(from_group) if from_group else x.start()):
        match_start = match.start(from_group) if from_group else match.start()
        match_end = match.end(from_group) if from_group else match.end()
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
