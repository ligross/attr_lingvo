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

SENTENCES_SPLIT_LIST = (
    r'([^,]\n+\s+\n+)',
    r'(\n+([А-Я]{1}))'
)

ADDITIONAL_ABBREVIATIONS = (
    'оф',
    'производствен',
    *set(map(str, range(0, 100))),
)

COLLATION_ROWS = (
    r'(если .+,\s*то .+$)',
    r'(между тем как .+,.+$)',
    r'(,\s*между тем как .+$)',
    r'(ровно как .+,.+$)',
    r'(,\s*ровно как .+$)',
    r'(так же как .+,.+$)',
    r'(,\s*так же как .+$)',
    r'(поскольку .+,\s*постольку .+$)',
    r'( постольку,\s*постольку .+$)',
)

COMPLEX_SYNTAX_ROWS = (
    r'(,\s*(и|а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и .+,\s*который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то, что|невзирая на то, что|правда,|так что|чем|нежели) \w+)',
    r'(,\s*(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя/хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели \w+,\s*(и|а|но|да)|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и) \w+)',
    r'(,\s*(и|а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и) .+:)',
    r'(:\s*\S+,\s*(а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и) \w+)',
    r'(,\s*(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели)\s*:\s*\w+)',
    r'(:\s*.+,\s*(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели)\s*\w+)',
    r'(,\s*(и|а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и .+,\s*который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели) .+:\s*\w+)',
    r'(,\s*(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели .+,\s*и|а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и)\s*:\s*\w+)',
    r'(:\s*.+,\s*.+,\s*(и|а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и .+,\s*который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели) \w+)',
    r'(:\s*.+,\s*(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели .+,\s*(и|а|но|да)|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и)\s*:\s*\w+)',
    r'(,\s*(и|а|но|да|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и .+:\s*.+,\s*(который|чей|что|какой|где|куда|откуда)|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели) \w*)',
    r'(,\s*(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|будто бы|как|словно|ли|кто|что|который|какой|чтобы|как будто|будто|словно|насколько|пока|пока не|как|как только|лишь только|едва только|стоило как|не прошло как|если|если бы|когда|кабы|как раз|скоро|ежели|если бы|когда бы|коли|коль|для того чтобы|с той целью чтобы|дабы|только бы|лишь бы|потому что|оттого что|благодаря тому что|так как|из-за того что|ибо|благодаря тому что|в виду того что|тем более что|хотя|хоть|пусть|пускай|даром что|несмотря на то,\s*что|невзирая на то,\s*что|правда,|так что|чем|нежели .+:\s*(и|а|но|да)|тоже|также|ни|зато|однако|то ли|или|только|не то|да и|но и) \w+)',
)

MODAL_POSTFIX_EXCLUSIONS = (
    'кто-то',
    'что-то',
    'какой-то',
    'чей-то',
    'сколько-то',
)

VERB_FORMS = ('VERB', 'INFN', 'PRTF', 'PRTS', 'GRND')

UNIFORM_ROWS_REGEX = re.compile('|'.join(UNIFORM_ROWS), flags=re.IGNORECASE)

COMPARATIVES_REGEX_POS = re.compile('(^|[\\s,:\-—«»"\'])(с целью|из расч(е|ё)та) INFN($|[\\s,.:\-—«»"\'])', flags=re.IGNORECASE)
COMPARATIVES_REGEX = re.compile('(^|[\\s,:\-—«»"\'])(кроме|помимо|включая|наряду с)|(как|будто)($|[\\s,.:\-—«»"\'])', flags=re.IGNORECASE)

SYNTAX_SPLICES_REGEX_POS = re.compile('(^|[\\s,:\-—«»"\'])(VERB (да и|да) VERB)($|[\\s,.:\-—«»"\'])', flags=re.IGNORECASE)
SYNTAX_SPLICES_REGEX = re.compile(r'(^|[\\s,:\-—«»"\'])(что было,\s*то было|что было,\s*то и есть|что было,\s*то есть|что есть,\s*то есть|что есть,\s*то и есть|что есть,\s*то и будет|что есть,\s*то будет)($|[\\s,.:\-—«»"\'])',
                                  flags=re.IGNORECASE)

COMPARATIVE_CLAUSES_REGEX = re.compile(r'((как|подобно тому как|ровно тому как) .+, .+)|(,\s*как .+)|((подобно тому|ровно тому,\s*как) .+)|((как будто|будто|словно|точно) .+, .+)|(.+, (как будто|будто|словно|точно) .+)', flags=re.IGNORECASE)

EPINTHETIC_CONSTRUCTIONS_REGEX = re.compile(r'(–.+–)|(\(.+\))|(-.+-)', flags=re.IGNORECASE)

COLLATION_CLAUSES_REGEX = re.compile('|'.join(COLLATION_ROWS), flags=re.IGNORECASE)

COMPLEX_SYNTAX_REGEX = re.compile('|'.join(COMPLEX_SYNTAX_ROWS), flags=re.IGNORECASE)

APPEAL_REGEX = re.compile('(?=(, (Name|Patr|Surn), )|(, Name (Patr|Surn), )|(, Name Patr Surn, ))', flags=re.IGNORECASE)

OURS_PRONOUNS, THEIRS_PRONOUNS = ('я', 'мы', 'ты'), ('он', 'она', 'они')

COMPLEX_WORDS_REGEX = re.compile(r'([a-я]+(-|—)[а-я]+)', flags=re.IGNORECASE)

MODAL_POSTFIX_REGEX = re.compile(r'[a-я]+(\-|\—)то(\s+|!|\?|.|$)', flags=re.IGNORECASE)

SENTENCES_SPLIT_REGEX = re.compile(r'\n+\s*\n+')
SENTENCES_SPLIT_ADD_REGEX = re.compile(r'(\n+)([А-Я]{1})([^А-Я]{1})')
