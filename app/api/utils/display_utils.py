def highlight_match(sentence, matches):
    highlighted_sentence = ''
    current_pos = 0
    for match in sorted(matches, key=lambda x: x.start()):
        if not current_pos:
            highlighted_sentence += sentence[0:match.start()] + \
                                    '<span style="background-color:yellow">' + \
                                    sentence[match.start():match.end()] + \
                                    '</span>'
            current_pos = match.end()
        else:
            highlighted_sentence += sentence[current_pos:match.start()] + \
                                    '<span style="background-color:yellow">' + \
                                    sentence[match.start():match.end()] + \
                                    '</span>'
            current_pos = match.end()
    if current_pos < len(sentence):
        highlighted_sentence += sentence[current_pos:len(sentence)]
    return highlighted_sentence
