import opencc

found_start = False
word_freqs = {}
for line in open('pinyin_simp.dict.yaml'):
  line = line.strip()
  if not found_start:
    if line == '...':
      found_start = True
    continue
  parts = line.split('\t')
  if len(parts) != 3:
    continue
  word, pinyin, weight = parts
  word_freqs[word] = weight

output_simp = open('../terra_pinyin_simp.dict.yaml', 'wt')
output_tradsimp = open('../terra_pinyin_tradsimp.dict.yaml', 'wt')
print('''---
name: terra_pinyin_simp
version: "2018.04.10"
sort: by_weight
use_preset_vocabulary: false
max_phrase_length: 7
min_phrase_weight: 100
...
''', file=output_simp)
print('''---
name: terra_pinyin_tradsimp
version: "2018.04.10"
sort: by_weight
use_preset_vocabulary: false
max_phrase_length: 7
min_phrase_weight: 100
...
''', file=output_tradsimp)
found_start = False
for line in open('terra_pinyin.dict.yaml'):
  line = line.strip()
  if not found_start:
    if line == '...':
      found_start = True
    continue
  parts = line.split('\t')
  word = parts[0]
  word_simp = opencc.convert(word, config='t2s.json')
  if word_simp in word_freqs:
    if len(parts) == 2:
      parts.append(word_freqs[word_simp])
    elif len(parts) == 3:
      parts[2] = word_freqs[word_simp]
  if word != word_simp:
    newparts = parts[:]
    newparts[0] = word_simp
    print('\t'.join(newparts), file=output_simp)
    print('\t'.join(newparts), file=output_tradsimp)
    print('\t'.join(parts), file=output_tradsimp)
  else:
    print('\t'.join(parts), file=output_simp)
    print('\t'.join(parts), file=output_tradsimp)
output_tradsimp.close()
output_simp.close()
