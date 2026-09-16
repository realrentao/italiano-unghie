# -*- coding: utf-8 -*-
"""Rigenera i file audio (edge-tts, voce it-IT-DiegoNeural) per questo sito.
Legge ./data.json e crea audio/audio_NNNN.mp3 per ogni voce in italiano.
Uso:  python generate_audio.py
"""
import os, json, asyncio, sys
import edge_tts

VOICE = "it-IT-DiegoNeural"
RATE = "-8%"

def has_chinese(t):
    return any('\u4e00' <= c <= '\u9fff' for c in t)

def has_audio(ita):
    s = ita.strip()
    return len(s) > 1 and not has_chinese(s)

def clean(t):
    return t.replace('\u201c', '"').replace('\u201d', '"').replace('\u2019', "'").strip()

async def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, 'data.json'), encoding='utf-8'))
    aud = os.path.join(here, 'audio')
    os.makedirs(aud, exist_ok=True)
    sem = asyncio.Semaphore(8)
    done = 0
    async def w(ita, path):
        nonlocal done
        async with sem:
            try:
                await edge_tts.Communicate(clean(ita), VOICE, rate=RATE).save(path)
                done += 1
            except Exception as e:
                print('FAIL', ita, e)
    jobs = [(e['ita'], os.path.join(aud, e['id'] + '.mp3')) for e in data['all_entries'] if has_audio(e['ita'])]
    await asyncio.gather(*[w(t, p) for t, p in jobs])
    print('generati', done, 'file audio')

if __name__ == '__main__':
    asyncio.run(main())
