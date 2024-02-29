cipher_file = "ciphertext-o2.txt"
words_file = "words.txt"

#Method to obtain single-letter frequency
def get_frequency(text):

  #clean text to be lowercase, remove whitespace
  frequency = {}
  text = "".join(text.split())
  text = text.lower()

  #store character frequencies
  for c in text:
    if c not in frequency:
      frequency[c] = 1
    else:
      frequency[c] = frequency[c] + 1

  #store character frequencies as a percentage of total
  total = len(text)
  for c in frequency:
    r = frequency[c] / total
    frequency[c] = f"{r:.5f}"

  return frequency

#Method to obtain bigram frequency
def get_bigram_frequency(text):

  #clean string
  frequency = {}
  text = "".join(text.split())
  text = text.lower()

  #check every instance of a bigram and store it
  total = 0
  for i in range(len(text)-2):
    bi = text[i] + text[i+1]
    total += 1
    if bi not in frequency:
      frequency[bi] = 1
    else:
      frequency[bi] = frequency[bi] + 1

  #check whether a bigram occures enough to be significant
  significant_frequencies = {}
  for bi in frequency:
    r = frequency[bi] / total
    if r > 0.01:
      significant_frequencies[bi] = f"{r:.5f}"

  return significant_frequencies

#Method to obtain trigram frequency
def get_trigram_frequency(text):

  #clean string
  frequency = {}
  text = "".join(text.split())
  text = text.lower()

  #check every instance of a trigram and store it
  total = 0
  for i in range(len(text)-3):
    tri = text[i] + text[i+1] + text[i+2]
    total += 1
    if tri not in frequency:
      frequency[tri] = 1
    else:
      frequency[tri] = frequency[tri] + 1

  #check whether a trigram occures enough to be significant
  significant_frequencies = {}
  for tri in frequency:
    r = frequency[tri] / total
    if r > 0.01:
      significant_frequencies[tri] = f"{r:.5f}"

  return significant_frequencies

f = open(cipher_file, "r")
ciphertext = f.read()
cipher_freq = get_frequency(ciphertext)
cipher_bigram_freq = get_bigram_frequency(ciphertext)
cipher_trigram_freq = get_trigram_frequency(ciphertext)
f.close()

f = open(words_file, "r")
words = f.read()
words_freq = get_frequency(words)
words_bigram_freq = get_bigram_frequency(words)
words_trigram_freq = get_trigram_frequency(words)
f.close()

print("Words:")
for key, value in words_freq.items():
  print(key.ljust(5), str(value).rjust(3))
  
print("Cipher:")
for key, value in cipher_freq.items():
  print(key.ljust(5), str(value).rjust(3))

print("Significant Bigrams (>0.01):")
print("Words:")
for key, value in words_bigram_freq.items():
  print(key.ljust(5), str(value).rjust(3))
print("Cipher:")
for key, value in cipher_bigram_freq.items():
  print(key.ljust(5), str(value).rjust(3))

print("Significant Trigrams (>0.01):")
print("Words:")
for key, value in words_trigram_freq.items():
  print(key.ljust(5), str(value).rjust(3))
print("Cipher:")
for key, value in cipher_trigram_freq.items():
  print(key.ljust(5), str(value).rjust(3))