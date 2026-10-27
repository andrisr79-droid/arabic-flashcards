# usage: python3 genverbs.py <miro|dii> <male|female> [verb ids and/or 'words' (all) / 'words2' (time+adjectives) / 'family', comma-separated]
# generates v3/audio/<dir>/<male|female>/<file> for every verb phrase, pronoun and هل
import json, sys, os, subprocess, numpy as np, soundfile as sf, sherpa_onnx
d=json.load(open('/home/claude/build/verbs.json'))
only=sys.argv[3].split(',') if len(sys.argv)>3 else None   # e.g. nam,akal  or  words  or  nam,akal,words
jobs=[]
for v in d['verbs']:
  if only and v['id'] not in only: continue
  for t in ['past','pres','fut']:
    for m in ['pos','neg']:
      for p in d['persons']:
        f=v['forms'][t][m][p]; jobs.append((f['audio'][0], f['audio'][1], f['say']))
if not only:
  for pr in d['pronouns']: jobs.append((pr['audio'][0], pr['audio'][1], pr['say']))
  jobs.append((d['halAudio'][0], d['halAudio'][1], 'هَلْ'))
if not only or 'words' in only or 'words2' in only or 'family' in only:   # special words + nouns (words.json)
  w=json.load(open('/home/claude/build/words.json'))
  if only and 'words2' in only: w = {**w, 'questions': [], 'preps': [], 'nouns': [], 'family': []}   # only time + adjectives
  if only and 'family' in only and 'words' not in only: w = {**w, 'questions': [], 'preps': [], 'nouns': [], 'time': [], 'adjs': []}
  for q in w['questions']: jobs += [(*q['audio'], q['say']), (*q['ex']['audio'], q['ex']['say'])]
  for p in w['preps']: jobs += [(*p['audio'], p['say'])] + [(*f['audio'], f['say']) for f in p['forms']]
  for n in w['nouns'] + w['time'] + w.get('family', []): jobs.append((*n['audio'], n['say']))
  for a in w['adjs']: jobs += [(*a['audio'], a['say']), (*a['comp']['audio'], a['comp']['say']), (*a['sup']['audio'], a['sup']['say'])]
voice, gender = sys.argv[1], sys.argv[2]
dd=f'/home/claude/tts/vits-piper-ar_JO-SA_{voice}-high/'
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
  model=dd+f'ar_JO-SA_{voice}-high.onnx', tokens=dd+'tokens.txt', data_dir=dd+'espeak-ng-data'), num_threads=4)))
short=[]
for adir, afile, text in jobs:
  out=f'/home/claude/v3/audio/{adir}/{gender}'; os.makedirs(out, exist_ok=True)
  takes=[]
  for i in range(3):
    a=tts.generate(text+'.', sid=0, speed=0.85); s=np.array(a.samples,dtype='float32')
    act=np.where(np.abs(s)>0.05*np.abs(s).max())[0]; takes.append(((act[-1]-act[0])/a.sample_rate,s,a.sample_rate))
  takes.sort(key=lambda x:x[0]); vl,s,sr=takes[1]
  if vl < 0.25: short.append((adir,afile,round(vl,2)))
  pad=np.zeros(int(sr*0.1),dtype='float32'); sf.write(f'/tmp/v_{gender}.wav',np.concatenate([pad,s,pad]),sr)
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'/tmp/v_{gender}.wav','-ac','1','-ar','22050','-b:a','48k',f'{out}/{afile}'],check=True)
print(gender, len(jobs), 'clips; short:', short)
