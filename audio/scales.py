tones = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
#         0            .        .        .       .            ..
gamma = dict()
#gamma[name] = [... frets/semitones ...]
gamma['major'] = [2,2,1,2,2,2,1]
gamma['minor'] = [2,1,2,2,1,2,2]
gamma['south'] = [1,3,1,2,1,2,2]

chord = dict()
chord['major'] = [4,3]
chord['minor'] = [3,4]
chord['quint'] = [5,7]

#note fret tone  name
#A    0    1       unison 1
#A#   1    1.5  Sm second 2
#B    2    2    Lg second 2
#C    3    2.5  Sm tercia 3
#C#   4    3    Lg tercia 3
#D    5    3.5     quarta 4
#D#   6    4       3 tone ?
#E    7    4.5     quinta 5
#F    8    5    Sm secsta 6
#F#   9    5.5  Lg secsta 6
#G    10   6    Sm sept   7
#G#   11   6.5  Lg sept   7
#A    12   7       octave 8

def scale(base, ptr):
     #search tone
     t = 0
     for i in range(len(tones)):
             if tones[i]==base:
                     t = i
                     break
     #make result
     out = []
     out.append(tones[t])
     for k in ptr:
             t += k
             if t >= 12:
                     t-=12
             out.append(tones[t])
     return out