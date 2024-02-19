def get_frequency(text):
  frequency = {}
  text = "".join(text.split())
  for c in text:
    if c is not in frequency:
      frequency[c] = 1
    else:
      frequency[c] = frequency[c] + 1

  total = len(text)
  for c in frequency:
    r = frequency[c] / total
    frequency[c] = r

  return frequency

f = open("ciphertext.txt", "r")
ciphertext = f.read()
cipher_freq = get_frequency(ciphertext)
f.close()

f = open("words.txt", "r")
words = f.read()
words_freq = get_frequency(words)
f.close()

print("Words:")
print(words_freq)
print("Cipher:")
print(cipher_freq)
