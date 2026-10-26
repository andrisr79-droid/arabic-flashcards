"""Verbs deck data for v3: pronouns, patterns (Kanafani table), particles, and conjugation of regular verbs.
Forms are generated from root + pattern, then checked against Глаголы.pdf (كتب, درس).
Writes /home/claude/build/verbs.json"""
import json, re, sys

FATHA, KASRA, DAMMA, SUKUN, SHADDA = 'َ', 'ِ', 'ُ', 'ْ', 'ّ'
MARKS = FATHA + KASRA + DAMMA + SUKUN + SHADDA + 'ًٌٍ'

PERSONS = ['ana', 'anta', 'anti', 'antum', 'huwa', 'hiya', 'hum', 'nahnu']
PRONOUN = {  # arabic, latin, russian (Глаголы.pdf), ru label, en label
  'ana':   ('أَنَا',  'anā',   'Ана',   'я',     'I'),
  'anta':  ('أَنْتَ', 'anta',  'Анта',  'ты (м)', 'you (m.)'),
  'anti':  ('أَنْتِ', 'anti',  'Анти',  'ты (ж)', 'you (f.)'),
  'antum': ('أَنْتُمْ', 'antum', 'Антом', 'вы',    'you (pl.)'),
  'huwa':  ('هُوَ',   'huwa',  'Хуа',   'он',    'he'),
  'hiya':  ('هِيَ',   'hiya',  'Хия',   'она',   'she'),
  'hum':   ('هُمْ',   'hum',   'Хом',   'они',   'they'),
  'nahnu': ('نَحْنُ', 'naḥnu', 'Нахно', 'мы',    'we'),
}
TENSES = {'past': ('past', 'прошедшее'), 'pres': ('present', 'настоящее'), 'fut': ('future', 'будущее')}
MODES = {'pos': ('+', 'affirmative', 'утверждение'), 'neg': ('−', 'negative', 'отрицание'), 'q': ('?', 'question', 'вопрос')}

# ---- endings: (vowel on last root letter, suffix) ----
PAST = {'ana': (SUKUN, 'تُ'), 'anta': (SUKUN, 'تَ'), 'anti': (SUKUN, 'تِ'), 'antum': (SUKUN, 'تُمْ'),
        'huwa': (FATHA, ''), 'hiya': (FATHA, 'تْ'), 'hum': (DAMMA, 'وا'), 'nahnu': (SUKUN, 'نَا')}
PREFIX = {'ana': 'أَ', 'anta': 'تَ', 'anti': 'تَ', 'antum': 'تَ', 'huwa': 'يَ', 'hiya': 'تَ', 'hum': 'يَ', 'nahnu': 'نَ'}
INDIC = {'ana': (DAMMA, ''), 'anta': (DAMMA, ''), 'anti': (KASRA, 'ينَ'), 'antum': (DAMMA, 'ونَ'),
         'huwa': (DAMMA, ''), 'hiya': (DAMMA, ''), 'hum': (DAMMA, 'ونَ'), 'nahnu': (DAMMA, '')}
JUSS = {'ana': (SUKUN, ''), 'anta': (SUKUN, ''), 'anti': (KASRA, 'ي'), 'antum': (DAMMA, 'وا'),
        'huwa': (SUKUN, ''), 'hiya': (SUKUN, ''), 'hum': (DAMMA, 'وا'), 'nahnu': (SUKUN, '')}
SUBJ = {'ana': (FATHA, ''), 'anta': (FATHA, ''), 'anti': (KASRA, 'ي'), 'antum': (DAMMA, 'وا'),
        'huwa': (FATHA, ''), 'hiya': (FATHA, ''), 'hum': (DAMMA, 'وا'), 'nahnu': (FATHA, '')}
PARTICLE = {'lam': 'لَمْ', 'la': 'لَا', 'lan': 'لَنْ', 'hal': 'هَلْ', 'sa': 'سَ'}

# ---- regular verbs (no weak letters, no doubled root) ----
# id, past stem, present stem, en (base, past, 3sg), ru (inf, past m/f/pl, present я/ты/вы/он/они/мы, future same order)
VERBS = [
  dict(id='katab', past='كَتَب', pres='كْتُب', en=('write', 'wrote', 'writes'), ru=('писать', ('писал', 'писала', 'писали'),
       ('пишу', 'пишешь', 'пишете', 'пишет', 'пишут', 'пишем'), ('буду писать', 'будешь писать', 'будете писать', 'будет писать', 'будут писать', 'будем писать'))),
  dict(id='daras', past='دَرَس', pres='دْرُس', en=('study', 'studied', 'studies'), ru=('учить', ('учил', 'учила', 'учили'),
       ('учу', 'учишь', 'учите', 'учит', 'учат', 'учим'), ('буду учить', 'будешь учить', 'будете учить', 'будет учить', 'будут учить', 'будем учить'))),
  dict(id='sharib', past='شَرِب', pres='شْرَب', en=('drink', 'drank', 'drinks'), ru=('пить', ('пил', 'пила', 'пили'),
       ('пью', 'пьёшь', 'пьёте', 'пьёт', 'пьют', 'пьём'), ('буду пить', 'будешь пить', 'будете пить', 'будет пить', 'будут пить', 'будем пить'))),
  dict(id='dhahab', past='ذَهَب', pres='ذْهَب', en=('go', 'went', 'goes'), ru=('идти', ('пошёл', 'пошла', 'пошли'),
       ('иду', 'идёшь', 'идёте', 'идёт', 'идут', 'идём'), ('пойду', 'пойдёшь', 'пойдёте', 'пойдёт', 'пойдут', 'пойдём'))),
  dict(id='takallam', past='تَكَلَّم', pres='تَكَلَّم', en=('speak', 'spoke', 'speaks'), ru=('говорить', ('говорил', 'говорила', 'говорили'),
       ('говорю', 'говоришь', 'говорите', 'говорит', 'говорят', 'говорим'), ('буду говорить', 'будешь говорить', 'будете говорить', 'будет говорить', 'будут говорить', 'будем говорить'))),
  dict(id='saal', past='سَأَل', pres='سْأَل', en=('ask', 'asked', 'asks'), ru=('спрашивать', ('спросил', 'спросила', 'спросили'),
       ('спрашиваю', 'спрашиваешь', 'спрашиваете', 'спрашивает', 'спрашивают', 'спрашиваем'), ('спрошу', 'спросишь', 'спросите', 'спросит', 'спросят', 'спросим'))),
]
VERBS += [
  dict(id='jalas', past='جَلَس', pres='جْلِس', en=('sit', 'sat', 'sits'), ru=('сидеть', ('сидел', 'сидела', 'сидели'),
       ('сижу', 'сидишь', 'сидите', 'сидит', 'сидят', 'сидим'), ('буду сидеть', 'будешь сидеть', 'будете сидеть', 'будет сидеть', 'будут сидеть', 'будем сидеть'))),
  dict(id='waqaf', past='وَقَف', pres='قِف', en=('stand', 'stood', 'stands'), ru=('стоять', ('стоял', 'стояла', 'стояли'),
       ('стою', 'стоишь', 'стоите', 'стоит', 'стоят', 'стоим'), ('буду стоять', 'будешь стоять', 'будете стоять', 'будет стоять', 'будут стоять', 'будем стоять'))),
  dict(id='akal', past='أَكَل', pres='أْكُل', en=('eat', 'ate', 'eats'), ru=('есть', ('ел', 'ела', 'ели'),
       ('ем', 'ешь', 'едите', 'ест', 'едят', 'едим'), ('буду есть', 'будешь есть', 'будете есть', 'будет есть', 'будут есть', 'будем есть'))),
  dict(id='nam', past='نَام', past_short='نِم', pres='نَام', pres_short='نَم', en=('sleep', 'slept', 'sleeps'), ru=('спать', ('спал', 'спала', 'спали'),
       ('сплю', 'спишь', 'спите', 'спит', 'спят', 'спим'), ('буду спать', 'будешь спать', 'будете спать', 'будет спать', 'будут спать', 'будем спать'))),
  dict(id='qal', past='قَال', past_short='قُل', pres='قُول', pres_short='قُل', en=('say', 'said', 'says'), ru=('сказать', ('сказал', 'сказала', 'сказали'),
       ('говорю', 'говоришь', 'говорите', 'говорит', 'говорят', 'говорим'), ('скажу', 'скажешь', 'скажете', 'скажет', 'скажут', 'скажем'))),
]
# Russian transcription from Глаголы 2.pdf (past and present tables, persons in the usual order).
# Obvious typos in the PDF corrected: akal nahnu "наколко"→"наколо", sharib huwa "шараба"→"шареба" (Arabic شَرِبَ),
# jalas anta/anti "тажлосо/тажлосин"→"тажлисо/тажлисин" (like the other present forms).
PDF2_RUS = {
  'nam':      ('немто немта немти немтом нама намат намо немна', 'анамо танамо танамин танамон янамо танамо янамон нанамо'),
  'akal':     ('акалто акалта акалти акалтом акала акалат акало акална', 'аколо таколо таколин таколон яаколо таколо яаколон наколо'),
  'sharib':   ('шаребто шаребта шаребти шаребтом шареба шаребат шаребо шаребна', 'ашрабо ташрабо ташрабин ташрабон яшрабо ташрабо яшрабон нашрабо'),
  'takallam': ('такаламто такаламта такаламти такаламтом такалама такаламат такаламо такаламна', 'атакаламо татакаламо татакаламин татакаламон ятакаламо татакаламо ятакаламон натакаламо'),
  'dhahab':   ('захабто захабта захабти захабтом захаба захабат захабо захабна', 'азхабо тазхабо тазхабин тазхабон язхабо тазхабо язхабон назхабо'),
  'waqaf':    ('уакафто уакафта уакафти уакафтом уакафа уакафат уакафо уакафна', 'акефо такефо такефин такефон якефо такефо якефон накефо'),
  'jalas':    ('жаласто жаласта жаласти жаластом жаласа жаласат жаласо жаласна', 'ажлисо тажлисо тажлисин тажлисон яжлисо тажлисо яжлисон нажлисо'),
  'qal':      ('коль-то коль-та коль-ти коль-том ка-ла каль-ат каль-о коль-на', 'ако-ло тако-ло тако-лин тако-лон яко-ло тако-ло яко-лон нако-ло'),
}
def _juss(x): return x[:-2] + 'и' if x.endswith('ин') else x[:-2] + 'о' if x.endswith('он') else x[:-1] if x.endswith('о') else x
def _subj(x): return x[:-2] + 'и' if x.endswith('ин') else x[:-2] + 'о' if x.endswith('он') else x[:-1] + 'а' if x.endswith('о') else x
def pdf2_verb_rus(vid, tense, mode, i):
    past, pres = (t.split() for t in PDF2_RUS[vid])
    if tense == 'past': return past[i] if mode != 'neg' else 'лам ' + _juss(pres[i])
    if tense == 'pres': return pres[i] if mode != 'neg' else 'ла ' + pres[i]
    return 'са-' + pres[i] if mode != 'neg' else 'лан ' + _subj(pres[i])

RU_IDX = {'ana': 0, 'anta': 1, 'anti': 1, 'antum': 2, 'huwa': 3, 'hiya': 3, 'hum': 4, 'nahnu': 5}
PAST_G = {'ana': 'mf', 'anta': 'm', 'anti': 'f', 'antum': 'pl', 'huwa': 'm', 'hiya': 'f', 'hum': 'pl', 'nahnu': 'pl'}

# ---- transliteration (vowelled Arabic -> Latin / Russian, in the style of Глаголы.pdf) ----
LAT = {'ب':'b','ت':'t','ث':'th','ج':'j','ح':'ḥ','خ':'kh','د':'d','ذ':'dh','ر':'r','ز':'z','س':'s','ش':'sh','ص':'ṣ','ض':'ḍ','ط':'ṭ','ظ':'ẓ',
       'ع':'ʿ','غ':'gh','ف':'f','ق':'q','ك':'k','ل':'l','م':'m','ن':'n','ه':'h','و':'w','ي':'y','ء':'ʾ','أ':'ʾ','إ':'ʾ','ؤ':'ʾ','ئ':'ʾ'}
RUS = {'ب':'б','ت':'т','ث':'с','ج':'ж','ح':'х','خ':'х','د':'д','ذ':'з','ر':'р','ز':'з','س':'с','ش':'ш','ص':'с','ض':'д','ط':'т','ظ':'з',
       'ع':'’','غ':'г','ف':'ф','ق':'к','ك':'к','ل':'л','м':'м','م':'м','ن':'н','ه':'х','و':'у','ي':'й','ء':'’','أ':'’','إ':'’','ؤ':'’','ئ':'’'}
VLAT = {FATHA: 'a', KASRA: 'i', DAMMA: 'u'}
VRUS = {FATHA: 'а', KASRA: 'и', DAMMA: 'о'}

def word_units(w):
    """split a vowelled word into [letter, marks] units"""
    units = []
    for ch in w:
        if ch in MARKS and units: units[-1][1] += ch
        else: units.append([ch, ''])
    return units

def translit_word(w, rus):
    u = word_units(w); out = []  # list of [consonant, vowel]
    LONG_L = {'a': 'ā', 'u': 'ū', 'i': 'ī'}
    for i, (ch, mk) in enumerate(u):
        vowel = next((m for m in mk if m in VLAT), None); first = (i == 0)
        prev_v = out[-1][1] if out else ''
        # long vowels: fatha+ا, damma+و, kasra+ي — the long letter lengthens the previous vowel
        if ch == 'ا' and not first and not vowel:
            if out and not rus: out[-1][1] = LONG_L.get(prev_v, prev_v)
            continue
        if ch == 'و' and out and prev_v in ('u', 'о') and not vowel:
            if not rus: out[-1][1] = 'ū'
            continue
        if ch == 'ي' and out and prev_v in ('i', 'и') and not vowel:
            if not rus: out[-1][1] = 'ī'
            continue
        if ch == 'آ':
            out.append(['' if (first or rus) else 'ʾ', 'а' if rus else 'ā']); continue
        cons = '' if (first and ch in 'أإ') else (RUS if rus else LAT)[ch]
        if SHADDA in mk: cons = cons * 2
        v = (VRUS if rus else VLAT).get(vowel, '') if vowel else ''
        if rus:
            if cons == 'й' and v == 'а': cons, v = '', 'я'
            elif cons == 'й' and v == 'о': cons, v = '', 'ю'
            nxt = u[i+1][0] if i + 1 < len(u) else None
            if cons == 'л' and not v and nxt != 'ل': cons = 'ль'
        out.append([cons, v])
    return ''.join(c + v for c, v in out)

def translit(phrase, rus):
    return ' '.join(translit_word(w, rus) for w in phrase.split())

def pausal(phrase):
    """the text as it is said (Глаголы.pdf style): -ūna/-īna lose the final a; silent alif of -ū drops"""
    words = []
    for w in phrase.split():
        w = re.sub('ونَ$', 'ون' + SUKUN, w); w = re.sub('ينَ$', 'ين' + SUKUN, w); w = re.sub('وا$', 'و', w)
        words.append(w)
    return ' '.join(words)

def tts_text(phrase):
    """text for the voices: pausal + geminates spelled out (the phonemizer drops a vowel after shadda+vowel)"""
    t = pausal(phrase)
    t = re.sub('(.)' + '([' + FATHA + KASRA + DAMMA + '])' + SHADDA, lambda m: m.group(1) + SUKUN + m.group(1) + m.group(2), t)
    t = re.sub('(.)' + SHADDA + '([' + FATHA + KASRA + DAMMA + '])', lambda m: m.group(1) + SUKUN + m.group(1) + m.group(2), t)
    t = t.replace('سَيَ', 'سَـيَ')   # future ya-: otherwise read as sa-i-a
    return t

# ---- building forms as coloured segments: pt = particle, af = affix, rt = root ----
CONS_SUFFIX = {'ana', 'anta', 'anti', 'antum', 'nahnu'}   # past suffixes starting with a consonant (-tu, -ta, -ti, -tum, -nā)
def _hamza_merge(segs):
    out = [list(x) for x in segs]
    for i in range(len(out) - 1):
        if out[i][1].endswith('أَ') and out[i+1][1].startswith('أْ'):
            out[i][1] = out[i][1][:-2] + 'آ'; out[i+1][1] = out[i+1][1][2:]
    return [tuple(x) for x in out]
def verb_segments(v, tense, mode, p):
    return _hamza_merge(_verb_segments(v, tense, mode, p))
def _verb_segments(v, tense, mode, p):
    if tense == 'past' and mode in ('pos', 'q'):
        vw, suf = PAST[p]; stem = v.get('past_short') if (p in CONS_SUFFIX and v.get('past_short')) else v['past']
        return [('rt', stem + vw), ('af', suf)]
    if tense == 'past' and mode == 'neg':
        vw, suf = JUSS[p]; stem = v.get('pres_short') if (not suf and v.get('pres_short')) else v['pres']
        return [('pt', PARTICLE['lam'] + ' '), ('af', PREFIX[p]), ('rt', stem + vw), ('af', suf)]
    if tense == 'pres':
        vw, suf = INDIC[p]; segs = [('af', PREFIX[p]), ('rt', v['pres'] + vw), ('af', suf)]
        return ([('pt', PARTICLE['la'] + ' ')] if mode == 'neg' else []) + segs
    if tense == 'fut' and mode in ('pos', 'q'):
        vw, suf = INDIC[p]; return [('af', PARTICLE['sa'] + PREFIX[p]), ('rt', v['pres'] + vw), ('af', suf)]
    if tense == 'fut' and mode == 'neg':
        vw, suf = SUBJ[p]; return [('pt', PARTICLE['lan'] + ' '), ('af', PREFIX[p]), ('rt', v['pres'] + vw), ('af', suf)]

def segs_text(segs): return ''.join(t for _, t in segs)

def translations(v, tense, mode, p):
    ru_p, en_p = PRONOUN[p][3], PRONOUN[p][4]
    inf, past, pres, fut = v['ru']; base, ed, s3 = v['en']
    third = p in ('huwa', 'hiya')
    if tense == 'past':
        m, f, pl = past
        form = {'m': m, 'f': f, 'pl': pl, 'mf': (m + '(' + f[len(m):] + ')') if f.startswith(m) else m + ' / ' + f}[PAST_G[p]]
        ru = f"{ru_p} {'не ' if mode == 'neg' else ''}{form}"
        en = {'pos': f"{en_p} {ed}", 'neg': f"{en_p} didn't {base}", 'q': f"did {en_p} {base}"}[mode]
    elif tense == 'pres':
        form = pres[RU_IDX[p]]
        ru = f"{ru_p} {'не ' if mode == 'neg' else ''}{form}"
        en = {'pos': f"{en_p} {s3 if third else base}", 'neg': f"{en_p} {'doesn' if third else 'don'}'t {base}",
              'q': f"{'does' if third else 'do'} {en_p} {base}"}[mode]
    else:
        form = fut[RU_IDX[p]]
        ru = f"{ru_p} {'не ' if mode == 'neg' else ''}{form}"
        en = {'pos': f"{en_p} will {base}", 'neg': f"{en_p} won't {base}", 'q': f"will {en_p} {base}"}[mode]
    if mode == 'q': ru += '?'; en = en[0].upper() + en[1:] + '?'
    else: en = en[0].upper() + en[1:]
    return ru, en

def form_record(v, tense, mode, p):
    segs = verb_segments(v, tense, mode, p)
    if mode == 'q': segs = [('pt', PARTICLE['hal'] + ' ')] + segs
    verb_txt = segs_text(segs)
    phrase = PRONOUN[p][0] + ' ' + verb_txt
    if mode == 'q':  # هل comes first: هَلْ أَنْتَ كَتَبْتَ؟ is fine, but the PDF puts هل before the verb; keep pronoun after هل
        phrase = PARTICLE['hal'] + ' ' + PRONOUN[p][0] + ' ' + segs_text(segs[1:])
    said = pausal(phrase)
    pw = PRONOUN[p][0]
    def tl(rus):
        parts = []
        for w in said.split():
            parts.append((PRONOUN[p][2].lower() if rus else PRONOUN[p][1]) if w == pw else translit_word(w, rus))
        return ' '.join(parts)
    lat = tl(False); rus = tl(True)
    if v['id'] in PDF2_RUS:   # Russian exactly as in Глаголы 2.pdf (derived the same way for −, future and ?)
        vr = pdf2_verb_rus(v['id'], tense, mode, PERSONS.index(p))
        rus = ('халь ' if mode == 'q' else '') + PRONOUN[p][2].lower() + ' ' + vr
    lat = lat.replace(' sa', ' sa-', 1).replace('sa-ʾ', 'sa-') if (tense == 'fut' and mode != 'neg') else lat
    rus = rus.replace(' са’', ' са ', 1) if (tense == 'fut' and mode != 'neg' and v['id'] not in PDF2_RUS) else rus
    ru, en = translations(v, tense, mode, p)
    if mode == 'q': lat += '?'; rus += '?'
    # audio: questions = هل clip + the affirmative clip (same voice)
    audio = [f"verbs/{v['id']}", f"{tense}-{'pos' if mode == 'q' else mode}-{p}.mp3"]   # audio/<dir>/<voice>/<file>
    return {'segs': segs, 'phrase': phrase, 'lat': lat, 'rus': rus, 'ru': ru, 'en': en, 'audio': audio, 'hal': mode == 'q',
            'say': tts_text(PRONOUN[p][0] + ' ' + segs_text(verb_segments(v, tense, 'pos' if mode == 'q' else mode, p)))}

# ---- patterns (Kanafani table) ----
LAT_PAT = {'past': {'ana': '… + tu', 'anta': '… + ta', 'anti': '… + ti', 'antum': '… + tum', 'huwa': '… + a', 'hiya': '… + at', 'hum': '… + ū', 'nahnu': '… + nā'},
           'pres': {'ana': 'a + … + u', 'anta': 'ta + … + u', 'anti': 'ta + … + īn', 'antum': 'ta + … + ūn', 'huwa': 'ya + … + u', 'hiya': 'ta + … + u', 'hum': 'ya + … + ūn', 'nahnu': 'na + … + u'}}
RUS_PAT = {'past': {'ana': '… + то', 'anta': '… + та', 'anti': '… + ти', 'antum': '… + том', 'huwa': '… + а', 'hiya': '… + ат', 'hum': '… + о', 'nahnu': '… + на'},
           'pres': {'ana': 'а + … + о', 'anta': 'та + … + о', 'anti': 'та + … + ин', 'antum': 'та + … + он', 'huwa': 'я + … + о', 'hiya': 'та + … + о', 'hum': 'я + … + он', 'nahnu': 'на + … + о'}}
def pattern(tense, p):
    if tense == 'past':
        vw, suf = PAST[p]; pre, end = '', {'huwa': 'ـَ', 'hum': 'ـُوا'}.get(p, 'ـ' + suf)
        lat, rus = LAT_PAT['past'][p], RUS_PAT['past'][p]
    else:
        vw, suf = INDIC[p]
        pre = (PARTICLE['sa'] if tense == 'fut' else '') + PREFIX[p] + ('ـ' if PREFIX[p] != 'أَ' else '')
        end = 'ـ' + {'': 'ُ'}.get(suf, ('ِ' if p == 'anti' else 'ُ') + suf)
        lat, rus = LAT_PAT['pres'][p], RUS_PAT['pres'][p]
        if tense == 'fut': lat, rus = 'sa + ' + lat, 'са + ' + rus
    return {'pre': pre, 'end': end, 'lat': lat, 'rus': rus}

PARTICLES = [
  dict(id='sa', ar='سَـ / سَوْفَ', lat='sa / sawfa', rus='са / сауфа', en='will (future)', ru='буду (будущее время)',
       rule_en='sa- is written joined to the present-tense verb; sawfa is a separate word before it. The verb itself does not change.',
       rule_ru='са пишется слитно с глаголом настоящего времени, сауфа — отдельно перед ним. Сам глагол не меняется.',
       ex=('katab', 'fut', 'pos', 'ana')),
  dict(id='la', ar='لَا', lat='lā', rus='ла', en='not (present)', ru='не (настоящее время)',
       rule_en='lā + the present-tense verb, unchanged.', rule_ru='ла + глагол настоящего времени без изменений.',
       ex=('daras', 'pres', 'neg', 'huwa')),
  dict(id='lam', ar='لَمْ', lat='lam', rus='лам', en='did not (past)', ru='не (прошедшее время)',
       rule_en='lam + the present-tense form with no final vowel (-u drops; -īna → -ī, -ūna → -ū).',
       rule_ru='лам + форма настоящего времени без конечного гласного (-о пропадает; -ин → -и, -он → -о).',
       ex=('daras', 'past', 'neg', 'nahnu')),
  dict(id='lan', ar='لَنْ', lat='lan', rus='лан', en='will not (future)', ru='не буду (будущее время)',
       rule_en='lan + the present-tense form ending in -a (-īna → -ī, -ūna → -ū). No sa-/sawfa.',
       rule_ru='лан + форма настоящего времени с окончанием -а (-ин → -и, -он → -о). Без са/сауфа.',
       ex=('katab', 'fut', 'neg', 'ana')),
  dict(id='hal', ar='هَلْ', lat='hal', rus='халь', en='question word (any tense)', ru='вопрос (все времена)',
       rule_en='hal at the start turns a statement into a yes/no question.', rule_ru='халь в начале превращает утверждение в вопрос.',
       ex=('daras', 'pres', 'q', 'anta')),
]

def build():
    verbs_out = []
    for v in VERBS:
        forms = {t: {m: {p: form_record(v, t, m, p) for p in PERSONS} for m in MODES} for t in TENSES}
        dict_form = v['past'] + FATHA + ' – ' + 'يَ' + v['pres'] + DAMMA
        verbs_out.append({'id': v['id'], 'dict': dict_form, 'dictLat': translit(v['past'] + FATHA, False) + ' – ' + translit('يَ' + v['pres'] + DAMMA, False),
                          'dictRus': translit(v['past'] + FATHA, True) + ' – ' + translit('يَ' + v['pres'] + DAMMA, True),
                          'en': 'to ' + v['en'][0], 'ru': v['ru'][0], 'forms': forms})
    pron = [{'id': p, 'ar': PRONOUN[p][0], 'lat': PRONOUN[p][1], 'rus': PRONOUN[p][2], 'ru': PRONOUN[p][3], 'en': PRONOUN[p][4],
             'audio': ['verbs/common', f'pron-{p}.mp3'], 'say': PRONOUN[p][0]} for p in PERSONS]
    pats = {t: {p: pattern(t, p) for p in PERSONS} for t in TENSES}
    return {'persons': PERSONS, 'tenses': {k: list(v) for k, v in TENSES.items()}, 'modes': {k: list(v) for k, v in MODES.items()},
            'pronouns': pron, 'patterns': pats, 'particles': PARTICLES, 'verbs': verbs_out,
            'halAudio': ['verbs/common', 'hal.mp3']}

# ---- check against Глаголы.pdf ----
PDF = {
  ('katab', 'past'): 'катабто катабта катабти катабтом катаба катабат катабо катабна',
  ('katab', 'pres'): 'актобо тактобо тактобин тактобон яктобо тактобо яктобон нактобо',
  ('daras', 'past'): 'дарасто дараста дарасти дарастом дараса дарасат дарасо дарасна',
  ('daras', 'pres'): 'адросо тадросо тадросин тадросон ядросо тадросо ядросон надросо',
}
PDF_PHRASES = [('katab', 'past', 'neg', 'nahnu', 'нахно лам нактоб'), ('katab', 'fut', 'neg', 'ana', 'ана лан актоба'),
               ('katab', 'fut', 'pos', 'ana', 'ана са актобо'), ('daras', 'fut', 'pos', 'ana', 'ана са адросо'),
               ('daras', 'pres', 'neg', 'huwa', 'хуа ла ядросо'), ('daras', 'past', 'neg', 'nahnu', 'нахно лам надрос'),
               ('daras', 'fut', 'neg', 'ana', 'ана лан адроса'), ('katab', 'past', 'q', 'huwa', 'халь хуа катаба?')]

if __name__ == '__main__':
    data = build(); errors = 0
    V = {v['id']: v for v in data['verbs']}
    for (vid, t), expected in PDF.items():
        got = [V[vid]['forms'][t]['pos'][p]['rus'].split(' ', 1)[1] for p in PERSONS]
        for p, g, e in zip(PERSONS, got, expected.split()):
            if g != e: print('MISMATCH', vid, t, p, g, '≠ PDF', e); errors += 1
    for vid, t, m, p, e in PDF_PHRASES:
        g = V[vid]['forms'][t][m][p]['rus'].lower()
        if g != e: print('PHRASE', vid, t, m, p, g, '≠ PDF', e); errors += 1
    json.dump(data, open('/home/claude/build/verbs.json', 'w'), ensure_ascii=False, indent=0)
    n = len(data['verbs']) * 3 * 3 * 8
    print(f"{len(data['verbs'])} verbs, {n} conjugation cards, {len(PERSONS)} pronouns, 24 patterns, {len(PARTICLES)} particles; PDF check errors: {errors}")
