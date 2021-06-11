L = '''
001001
101001
111001
011001
010001
110001
100001
000001
010101
000101
101111
111111
011111
010111
110111
100111
000111
001011
011011
010011
000011
001010
011010
010010
000010
001110
101110
111110
011110
010110
110110
100110
001100
011100
001000
101000
111000
011000
010000
110000
100000
000000
'''
 
a = []
for line in L.splitlines():
	if line:
		a.append(line)
a = sorted(a)
 
for i in range(64):
	f = False
	for line in a:
		if int(line, 2) == i:
			f = True
	if f:
		print(1, end='')
	else:
		print(0, end='')
 
print()
print()
 
 
for x in a:
	print(x[0:3]+'.'+x[3:6], int(x, 2))
print()
 
 
# def c(a):
# 	m=0
# 	for i in a:
# 		if i == '1':
# 			m+=1
# 	return m
 
# for i in range(7):
# 	print(f'------------------{i}------------------')
# 	for x in a:
# 		if c(x) == i:
# 			print(x[0:3]+'.'+x[3:6], f'  M{int(x, 2)}')