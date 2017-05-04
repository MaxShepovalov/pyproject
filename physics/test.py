from vec4f import vec4f

k = vec4f()
m = vec4f(2)
i = ~k
p = vec4f()
p.x=2

#test
if k!=i:
	print 'i should be equal to k'
if k==m:
	print 'k and m should be different'
if k==0:
	print 'vector and number should be different'
if k=='haha':
	print 'vector and string should be different'
if p!=m:
	print 'normalized and non-normalized vectors should be equal'


if k-k != vec4f(0,0,0,0):
	print 'subtraction is wrong'
if -k != k*(-1):
	print 'multiplication -1 is wrong'
if k+k != k*2:
	print 'multiplication 2 or addition is wrong'
if k^k != 0:
	print 'angle is wrong'
