word1 = str("frick")

print(word1[4]+word1[3]+word1[2]+word1[1]+word1[0])

word2 = str("frick")

if word2[0] != "a" or "e" or "i" or "o" or "u":
	print(word2[1]+word2[2]+word2[3]+word2[4]+ "-"+word2[0]+"ay")

word3 = str("frick")

vcounter = 0;

vowels = [
	(["i"])
]

for (vowel) in vowels:
	if word3[0] == vowel:
		vcounter += 1
	if word3[1] == vowel:
		vcounter += 1
	if word3[2] == vowel:
		vcounter += 1
	if word3[3] == vowel:
		vcounter += 1
	if word3[4] == vowel:
		vcounter += 1
print(vcounter)
