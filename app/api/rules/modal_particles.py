import regex as re

MODAL_PARTICLES_LIST = (
    'что за',
    'только',
    'лишь',
    'почти',
    'все\-таки',
    'всё\-таки',
    'даже',
    'же',
    'ведь',
    'точно',
    'отнюдь не',
    'ну и',
    'еще бы',
    'ещё бы',
    'ишь как',
    'ишь какой',
    'а что',
    'неужели',
    'разве',
    'да и',
    'хотя бы',
    'как раз',
    'именно',
    'ровно',
    'вот и',
    'вон и',
    'вот',
    'вон',
    'неужели',
    'вряд ли',
    'едва',
    'едва ли',
    'навряд ли',
    'авось',
    'то\-то',
    'просто',
    'прямо',
    'точно',
    'ровно',
    'подлинно',
    'в точности',
    'исключительно',
)

MODAL_PARTICLES_REGEX = re.compile(f'(^|[\\s,:\-—«»"\'])({"|".join(MODAL_PARTICLES_LIST)})($|[\\s,.:\-—«»"\'])', flags=re.IGNORECASE)
