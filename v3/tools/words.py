"""Special words (question words with an example, prepositions with 8 personal forms) and nouns — from Глаголы 2.pdf.
Russian transcription as in the PDF where it gives one; Latin with full endings; 'say' = text sent to the voices.
Writes /home/claude/build/words.json"""
import json

PERSONS = ['ana', 'anta', 'anti', 'antum', 'huwa', 'hiya', 'hum', 'nahnu']

def Q(id, ar, lat, rus, ru, en, ex_pre, ex_w, ex_post, ex_lat, ex_rus, ex_ru, ex_en, say=None, ex_say=None):
    return dict(id=id, ar=ar, lat=lat, rus=rus, ru=ru, en=en, say=say or ar,
                ex=dict(pre=ex_pre, w=ex_w, post=ex_post, lat=ex_lat, rus=ex_rus, ru=ex_ru, en=ex_en,
                        say=ex_say or (ex_pre + ex_w + ex_post).replace('؟', '')))

QUESTIONS = [
  Q('what', 'مَاذَا / مَا', 'mādhā / mā', 'ма-за / ма', 'что?', 'what?', '', 'مَاذَا', ' تَكْتُبُ؟',
    'mādhā taktubu?', 'ма-за тактобо?', 'Что ты пишешь?', 'What are you writing?', say='مَاذَا، مَا'),
  Q('who', 'مَنْ', 'man', 'мань', 'кто?', 'who?', '', 'مَنْ', ' أَنْتَ؟',
    'man anta?', 'мань анта?', 'Кто ты?', 'Who are you?'),
  Q('when', 'مَتَى', 'matā', 'ма-та', 'когда?', 'when?', '', 'مَتَى', ' طَائِرَتُكَ؟',
    'matā ṭāʾiratuka?', 'ма-та таиратока?', 'Когда твой самолёт?', 'When is your plane?'),
  Q('where', 'أَيْنَ', 'ayna', 'айна', 'где?', 'where?', '', 'أَيْنَ', ' مَكْتَبُهُ؟',
    'ayna maktabuhu?', 'айна мактабохо?', 'Где его офис?', 'Where is his office?'),
  Q('whereto', 'إِلَى أَيْنَ', 'ilā ayna', 'ила айна', 'куда?', 'where to?', '', 'إِلَى أَيْنَ', ' سَتَذْهَبُ؟',
    'ilā ayna sa-tadhhabu?', 'ила айна са-тазхабо?', 'Куда ты пойдёшь?', 'Where will you go?',
    ex_say='إِلَى أَيْنَ سَتَذْهَبُ'),
  Q('wherefrom', 'مِنْ أَيْنَ', 'min ayna', 'мен айна', 'откуда?', 'where from?', '', 'مِنْ أَيْنَ', ' أَنْتَ؟',
    'min ayna anta?', 'мен айна анта?', 'Откуда ты?', 'Where are you from?'),
  Q('how', 'كَيْفَ', 'kayfa', 'кайфа', 'как?', 'how?', '', 'كَيْفَ', ' سَتَذْهَبُ إِلَى مَنْزِلِكَ؟',
    'kayfa sa-tadhhabu ilā manzilika?', 'кайфа са-тазхабо ила манзелика?', 'Как ты доберёшься домой?', 'How will you get home?'),
  Q('why', 'لِمَاذَا', 'limādhā', 'лимаза', 'почему?', 'why?', '', 'لِمَاذَا', ' لَمْ تَذْهَبْ؟',
    'limādhā lam tadhhab?', 'лимаза лам тазхаб?', 'Почему ты не пошёл?', "Why didn't you go?"),
  Q('howmany', 'كَمْ', 'kam', 'камь', 'сколько?', 'how many? how much?', '', 'كَمْ', ' عُمْرُكَ؟',
    'kam ʿumruka?', 'камь омрока?', 'Сколько тебе лет?', 'How old are you?'),
]

def P(id, ar, lat, rus, ru, en, forms):
    return dict(id=id, ar=ar, lat=lat, rus=rus, ru=ru, en=en, say={'بِدُون': 'بِدُونْ'}.get(ar, ar),
                forms=[dict(p=p, ar=f[0], lat=f[1], rus=f[2], ru=f[3], en=f[4], say=f[0]) for p, f in zip(PERSONS, forms)])

PREPS = [
  P('maa', 'مَعَ', 'maʿa', 'ма-а', 'с', 'with', [
    ('مَعِي', 'maʿī', 'ма-и', 'со мной', 'with me'), ('مَعَكَ', 'maʿaka', 'ма-ака', 'с тобой (м)', 'with you (m.)'),
    ('مَعَكِ', 'maʿaki', 'ма-аки', 'с тобой (ж)', 'with you (f.)'), ('مَعَكُمْ', 'maʿakum', 'ма-аком', 'с вами', 'with you (pl.)'),
    ('مَعَهُ', 'maʿahu', 'ма-ахо', 'с ним', 'with him'), ('مَعَهَا', 'maʿahā', 'ма-аха', 'с ней', 'with her'),
    ('مَعَهُمْ', 'maʿahum', 'ма-ахом', 'с ними', 'with them'), ('مَعَنَا', 'maʿanā', 'ма-ана', 'с нами', 'with us')]),
  P('bidun', 'بِدُون', 'bidūn', 'бидун', 'без', 'without', [
    ('بِدُونِي', 'bidūnī', 'бидуни', 'без меня', 'without me'), ('بِدُونِكَ', 'bidūnika', 'бидуника', 'без тебя (м)', 'without you (m.)'),
    ('بِدُونِكِ', 'bidūniki', 'бидуники', 'без тебя (ж)', 'without you (f.)'), ('بِدُونِكُمْ', 'bidūnikum', 'бидуником', 'без вас', 'without you (pl.)'),
    ('بِدُونِهِ', 'bidūnihi', 'бидунихи', 'без него', 'without him'), ('بِدُونِهَا', 'bidūnihā', 'бидуниха', 'без неё', 'without her'),
    ('بِدُونِهِمْ', 'bidūnihim', 'бидунихим', 'без них', 'without them'), ('بِدُونِنَا', 'bidūninā', 'бидунина', 'без нас', 'without us')]),
  P('an', 'عَنْ', 'ʿan', 'а-ан', 'о (об)', 'about', [
    ('عَنِّي', 'ʿannī', 'анни', 'обо мне', 'about me'), ('عَنْكَ', 'ʿanka', 'анка', 'о тебе (м)', 'about you (m.)'),
    ('عَنْكِ', 'ʿanki', 'анки', 'о тебе (ж)', 'about you (f.)'), ('عَنْكُمْ', 'ʿankum', 'анком', 'о вас', 'about you (pl.)'),
    ('عَنْهُ', 'ʿanhu', 'анхо', 'о нём', 'about him'), ('عَنْهَا', 'ʿanhā', 'анха', 'о ней', 'about her'),
    ('عَنْهُمْ', 'ʿanhum', 'анхом', 'о них', 'about them'), ('عَنَّا', 'ʿannā', 'анна', 'о нас', 'about us')]),
  P('lada', 'لَدَى', 'ladā', 'лада', 'у … есть', 'have (at)', [
    ('لَدَيَّ', 'ladayya', 'ладайя', 'у меня есть', 'I have'), ('لَدَيْكَ', 'ladayka', 'ладайка', 'у тебя (м) есть', 'you (m.) have'),
    ('لَدَيْكِ', 'ladayki', 'ладайки', 'у тебя (ж) есть', 'you (f.) have'), ('لَدَيْكُمْ', 'ladaykum', 'ладайком', 'у вас есть', 'you (pl.) have'),
    ('لَدَيْهِ', 'ladayhi', 'ладайхи', 'у него есть', 'he has'), ('لَدَيْهَا', 'ladayhā', 'ладайха', 'у неё есть', 'she has'),
    ('لَدَيْهِمْ', 'ladayhim', 'ладайхим', 'у них есть', 'they have'), ('لَدَيْنَا', 'ladaynā', 'ладайна', 'у нас есть', 'we have')]),
]

def N(id, ar, lat, rus, ru, en, say=None): return dict(id=id, ar=ar, lat=lat, rus=rus, ru=ru, en=en, say=say or ar)
NOUNS = [  # Russian transcription from page 9 of the PDF; voice follows it (-ат endings)
  N('maktab', 'مَكْتَب', 'maktab', 'мактаб', 'офис', 'office'),
  N('kitab', 'كِتَاب', 'kitāb', 'китаб', 'книга', 'book'),
  N('madrasa', 'مَدْرَسَة', 'madrasah', 'мадрасат', 'школа', 'school', say='مَدْرَسَتْ'),
  N('manzil', 'مَنْزِل', 'manzil', 'манзел', 'дом', 'house'),
  N('bayt', 'بَيْت', 'bayt', 'байт', 'квартира, дом', 'home, apartment'),
  N('madina', 'مَدِينَة', 'madīnah', 'мадинат', 'город', 'city', say='مَدِينَتْ'),
  N('matar', 'مَطَار', 'maṭār', 'мат-ар', 'аэропорт', 'airport'),
  N('taira', 'طَائِرَة', 'ṭāʾirah', 'тай-ра', 'самолёт', 'airplane', say='طَائِرَه'),
  N('sayyara', 'سَيَّارَة', 'sayyārah', 'сая-рат', 'машина', 'car', say='سَيْيَارَتْ'),
  N('matjar', 'مَتْجَر', 'matjar', 'матжар', 'магазин', 'shop'),
]

if __name__ == '__main__':
    for q in QUESTIONS:
        q['audio'] = ['special', f"q-{q['id']}.mp3"]; q['ex']['audio'] = ['special', f"q-{q['id']}-ex.mp3"]
    for p in PREPS:
        p['audio'] = ['special', f"prep-{p['id']}.mp3"]
        for f in p['forms']: f['audio'] = ['special', f"prep-{p['id']}-{f['p']}.mp3"]
    for n in NOUNS: n['audio'] = ['nouns', f"{n['id']}.mp3"]
    json.dump({'questions': QUESTIONS, 'preps': PREPS, 'nouns': NOUNS}, open('/home/claude/build/words.json', 'w'), ensure_ascii=False, indent=0)
    print(len(QUESTIONS), 'question words,', len(PREPS), 'prepositions ×', len(PERSONS), 'forms,', len(NOUNS), 'nouns')
