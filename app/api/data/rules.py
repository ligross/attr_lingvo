import re

UNIFORM_ROWS = (
    r'(NOUN,\s*NOUN,\s*NOUN)',
    r'(ADJF,\s*ADJF,\s*ADJF)',
    r'(ADJS,\s*ADJS,\s*ADJS)',
    r'(VERB,\s*VERB,\s*VERB)',
    r'(INFN,\s*INFN,\s*INFN)',
    r'((и|да и|ни|или|либо) NOUN,\s*(и|да и|ни|или|либо) NOUN,\s*(и|да и|ни|или|либо) NOUN)',
    r'(NOUN,\s*NOUN (да|и|либо|или|да и) NOUN)',
    r'(NOUN,\s*(да|и|да и|также|тоже|также и|либо|или) NOUN,\s*(да|и|да и|также|тоже|также и|либо|или) NOUN)',
    r'(NOUN,\s*(а|но) NOUN,\s*NOUN)',
    r'(NOUN,\s*NOUN,\s*(а|но) NOUN)',
    r'(NOUN и NOUN,\s*(а|но) NOUN)',
)

UNIFORM_ROWS_REGEX = re.compile('|'.join(UNIFORM_ROWS), flags=re.IGNORECASE)

COMPARATIVES_REGEX_POS = re.compile('(с целью|из расч(е|ё)та) INFN', flags=re.IGNORECASE)
COMPARATIVES_REGEX = re.compile('(кроме|помимо|включая|наряду с)|(как|будто)', flags=re.IGNORECASE)

SYNTAX_SPLICES_REGEX_POS = re.compile('(VERB (да и|да) VERB)', flags=re.IGNORECASE)
SYNTAX_SPLICES_REGEX = re.compile(r'(что было,\s*то было|что было,\s*то и есть|что было,\s*то есть|что есть,\s*то есть|что есть,\s*то и есть|что есть,\s*то и будет|что есть,\s*то будет)',
                                  flags=re.IGNORECASE)

COMPARATIVE_CLAUSES_REGEX = re.compile(r'((как|подобно тому как|ровно тому как) .+, .+)|(,\s*как .+)|((подобно тому|ровно тому,\s*как) .+)|((как будто|будто|словно|точно) .+, .+)|(.+, (как будто|будто|словно|точно) .+)', flags=re.IGNORECASE)
