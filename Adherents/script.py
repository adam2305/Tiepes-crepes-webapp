
with open('nom.txt','r') as f:
	lines = f.readlines()
	lines.pop(0)
	noms = []
	mails = []
	temp = []
	for line in lines:
		for word in line.split():
			temp.append(word.lower())
		mails.append(temp[-1]+"."+temp[0]+"@etu.emse.fr")
		temp.clear()
f.close()

with open('mails.txt','w+') as f:
	for k in mails:
		f.write(k+'\n')
f.close()



