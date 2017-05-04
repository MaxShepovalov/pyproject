class vec4f:
    # x,y,z,scale
    # support +,-,*,/ 
    def __init__(self, x=1., y=0., z=0., s=1.):
        if type(x)==type((1,2,3,4)):
            self.x = float(x(0))
            self.y = float(x(1))
            self.z = float(x(2))
            self.s = float(x(3))
        elif isinstance(x, vec4f):
            self.x = x.x
            self.y = x.y
            self.z = x.z
            self.s = x.s
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
            self.s = float(s)
        self.normalize()
    def __repr__(self):
        return repr(self.__str__())
    def __eq__(self, other):
        if type(self)==type(other):
            t2 = 0
            t1 = abs(self)==abs(other)
            if abs(self) != 0 and abs(other) != 0:
                t2 = self^other
            return t1&(t2==0)
        else:
            return False
    def __ne__(self, other):
        return not self==other
    def __add__(self, other):
        #print 'add ',self.__str__(),' and ',other.__str__()
        out = vec4f()
        out.x = self.s*self.x + other.s*other.x
        out.y = self.s*self.y + other.s*other.y
        out.z = self.s*self.z + other.s*other.z
        out.s = 1.
        out.normalize()
        return out
    def __mul__(self, other):
        #print 'mult ',self.__str__(),' and ',other.__str__()
        out = vec4f(self)
        if type(other)==type(out):
            out = self.s*other.s*(self.x*other.x+self.y*other.y+self.z*other.z)
        else:
            out.s = self.s*other
            out.normalize()
        return out
    def __sub__(self, other):
        #print 'substract ',other.__str__(),' from ',self.__str__()
        return self+other*(-1)
    def __div__(self, other):
        return self*(~other)
    def __abs__(self):
        return self.s*pow(self.x**2 + self.y**2 + self.z**2, 0.5)
    def __xor__(self, other):
        import math
        num = round(self*other, 6)
        den = round(abs(self)*abs(other), 6)
        #print 'XOR ',num,'/',den
        return math.acos(num/den)
    def __neg__(self):
        #print 'negative ',self.__str__()
        return self*(-1)
    def __str__(self):
        out = '('+str(self.x)+', '+str(self.y)+', '+str(self.z)+', '+str(self.s)+')'
        return out
    def __invert__(self):
        N = 0
        x = 0.
        s = 0.
        z = 0.
        y = 0.
        if self.s!=0:
            s = 1./self.s
        if self.x!=0:
            x = 1./self.x
            N+=1
        if self.y!=0:
            y = 1./self.y
            N+=1
        if self.z!=0:
            z = 1./self.z
            N+=1
        if N!=0:
            x/=N
            y/=N
            z/=N
        return vec4f(x,y,z,s)
    def normalize(self):
        #print 'norm ',self.__str__()
        LOW_PRECISION = 1e-7
        length = pow(self.x**2 + self.y**2 + self.z**2, 0.5)
        if length!=0:
            self.s *= length
            self.x /= length
            self.y /= length
            self.z /= length
            if self.x < LOW_PRECISION:
                #print 'low precision at x'
                self.x = 0
            if self.y < LOW_PRECISION:
                #print 'low precision at y'
                self.y = 0
            if self.z < LOW_PRECISION:
                #print 'low precision at z'
                self.z = 0
            if self.s < LOW_PRECISION:
                #print 'low precision at s'
                self.s = 0
    def polar(self):
        if abs(self)==0:
            return 0.,0.,0.
        xy_proj = vec4f(self)
        xy_proj.z = 0
        #horizontal, alpha
        alp = xy_proj^vec4f()
        if self.y < 0:
            alp *= -1
        #vertical, theta
        tet = xy_proj^self
        if self.z < 0:
            tet *= -1
        # return len, alph, theta
        return abs(self), alp, tet
    def polar_deg(self):
        import math
        L,A,T = self.polar()
        return L, 180*A/math.pi, 180*T/math.pi

if __name__=="__main__":
    #vectors
    k = vec4f(1,1,1,1)
    b = vec4f(2,2,2,2)
    
    #beams
    m = vec4f(1,1,1,0)
    k = vec4f(-1,-5,20,0)
    
    print 'k=',k,'b=',b
    print '|k|=',abs(k)
    print '|b|=',abs(b)
    print '+  =',k+b
    print '-  =',k-b
    print '*# =',k*4
    print '*v =',k*b
    print '/# =',k/3
    print '^  =',k^b
    print '!^ =',b^k    