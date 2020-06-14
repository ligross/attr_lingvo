import re

UNIFORM_ROWS = (
    'NOUN, NOUN, NOUN',
    'ADJF, ADJF, ADJF',
    'ADJS, ADJS, ADJS',
    'VERB, VERB, VERB',
    'INFN, INFN, INFN',
    '(и|да и|ни|или|либо) NOUN, (и|да и|ни|или|либо) NOUN, (и|да и|ни|или|либо) NOUN',
    'NOUN, NOUN (да|и|либо|или|да и) NOUN',
    'NOUN, (да|и|да и|также|тоже|также и|либо|или) NOUN, (да|и|да и|также|тоже|также и|либо|или) NOUN',
    'NOUN, (а|но) NOUN, NOUN',
    'NOUN, NOUN, (а|но) NOUN',
    'NOUN и NOUN, (а|но) NOUN',
)

COMPARATIVES_REGEX_POS = re.compile('(с целью|из расч(е|ё)та) INFN', flags=re.IGNORECASE)
COMPARATIVES_REGEX = re.compile('(кроме|помимо|включая|наряду с)|(как|будто)', flags=re.IGNORECASE)

SYNTAX_SPLICES_REGEX_POS = re.compile('(VERB (да и|да) VERB)', flags=re.IGNORECASE)
SYNTAX_SPLICES_REGEX = re.compile('(что было, то было|что было, то и есть|что было, то есть|что есть, то есть|что есть, то и есть|что есть, то и будет|что есть, то будет)',
                                  flags=re.IGNORECASE)

COMPARATIVE_CLAUSES_REGEX = re.compile('((как|подобно тому как|ровно тому как) .+, .+)|(, как .+)|((подобно тому|ровно тому, как) .+)|((как будто|будто|словно|точно) .+, .+)|(.+, (как будто|будто|словно|точно) .+)', flags=re.IGNORECASE)
