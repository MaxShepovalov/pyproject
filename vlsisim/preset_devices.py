logic = dict()
active = dict()

#3:2 adder
logic['3:2+'] = dict()
logic['3:2+']['000']='00'
logic['3:2+']['001']='01'
logic['3:2+']['010']='01'
logic['3:2+']['011']='10'
logic['3:2+']['100']='01'
logic['3:2+']['101']='10'
logic['3:2+']['110']='10'
logic['3:2+']['111']='11'
logic['3:2+']['help'] = '3 inputs: A,B,Ci\n 2 outputs: Co, R\n perform A+B+Ci = R,Co'
logic['3:2+']['data'] = (3,2)

#and
logic['and'] = dict()
logic['and']['00'] = '0'
logic['and']['01'] = '0'
logic['and']['10'] = '0'
logic['and']['11'] = '1'
logic['and']['help'] = '2 inputs: A,B\n 1 output: R\n perform A&B=R'
logic['and']['data'] = (2,1)

#or
logic['or'] = dict()
logic['or']['00'] = '0'
logic['or']['01'] = '1'
logic['or']['10'] = '1'
logic['or']['11'] = '1'
logic['or']['help'] = '2 inputs: A,B\n 1 output: R\n perform A|B=R'
logic['or']['data'] = (2,1)

#not
logic['not'] = dict()
logic['not']['0'] = '1'
logic['not']['1'] = '0'
logic['not']['help'] = '1 input: A\n 1 output: R\n perform ~A=R'
logic['not']['data'] = (1,1)

#nand
logic['nand'] = dict()
logic['nand']['00'] = '1'
logic['nand']['01'] = '1'
logic['nand']['10'] = '1'
logic['nand']['11'] = '0'
logic['nand']['help'] = '2 inputs: A,B\n 1 output: R\n perform ~(A&B)=R'
logic['nand']['data'] = (2,1)

#nor
logic['nor'] = dict()
logic['nor']['00'] = '1'
logic['nor']['01'] = '0'
logic['nor']['10'] = '0'
logic['nor']['11'] = '0'
logic['nor']['help'] = '2 inputs: A,B\n 1 output: R\n perform ~(A|B)=R'
logic['nor']['data'] = (2,1)

#xor
logic['xor'] = dict()
logic['xor']['00'] = '0'
logic['xor']['01'] = '1'
logic['xor']['10'] = '1'
logic['xor']['11'] = '0'
logic['xor']['help'] = '2 inputs: A,B\n 1 output: R\n perform A!=B=R'
logic['xor']['data'] = (2,1)

#nxor
logic['nxor'] = dict()
logic['nxor']['00'] = '1'
logic['nxor']['01'] = '0'
logic['nxor']['10'] = '0'
logic['nxor']['11'] = '1'
logic['nxor']['help'] = '2 inputs: A,B\n 1 output: R\n perform A==B=R'
logic['nxor']['data'] = (2,1)

#delay
logic['delay'] = dict()
logic['delay']['0'] = '0'
logic['delay']['1'] = '1'
logic['delay']['help'] = '1 input: A\n 1 output: R\n perform delay for 1 task'
logic['delay']['data'] = (1,1)

#mux
logic['mux4'] = dict()
logic['mux4']['000'] = '0000'
logic['mux4']['100'] = '1000'
logic['mux4']['010'] = '0000'
logic['mux4']['110'] = '0100'
logic['mux4']['001'] = '0000'
logic['mux4']['101'] = '0010'
logic['mux4']['011'] = '0000'
logic['mux4']['111'] = '0001'
logic['mux4']['help'] = '3 input: A, addr_MSB, addr_LSB\n4 output: out0, out1, out2, out3\n Routes A to given output by address'
logic['mux4']['data'] = (3,4)

#demux
logic['demux'] = dict()
logic['demux']['000000'] = '0'
logic['demux']['000010'] = '0'
logic['demux']['000001'] = '0'
logic['demux']['000011'] = '0'
logic['demux']['100000'] = '1'
logic['demux']['100010'] = '0'
logic['demux']['100001'] = '0'
logic['demux']['100011'] = '0'
logic['demux']['010000'] = '0'
logic['demux']['010010'] = '1'
logic['demux']['010001'] = '0'
logic['demux']['010011'] = '0'
logic['demux']['110000'] = '1'
logic['demux']['110010'] = '1'
logic['demux']['110001'] = '0'
logic['demux']['110011'] = '0'
logic['demux']['001000'] = '0'
logic['demux']['001010'] = '0'
logic['demux']['001001'] = '1'
logic['demux']['001011'] = '0'
logic['demux']['101000'] = '1'
logic['demux']['101010'] = '0'
logic['demux']['101001'] = '1'
logic['demux']['101011'] = '0'
logic['demux']['011000'] = '0'
logic['demux']['011010'] = '1'
logic['demux']['011001'] = '1'
logic['demux']['011011'] = '0'
logic['demux']['111000'] = '1'
logic['demux']['111010'] = '1'
logic['demux']['111001'] = '1'
logic['demux']['111011'] = '0'
logic['demux']['000100'] = '0'
logic['demux']['000110'] = '0'
logic['demux']['000101'] = '0'
logic['demux']['000111'] = '1'
logic['demux']['100100'] = '1'
logic['demux']['100110'] = '0'
logic['demux']['100101'] = '0'
logic['demux']['100111'] = '1'
logic['demux']['010100'] = '0'
logic['demux']['010110'] = '1'
logic['demux']['010101'] = '0'
logic['demux']['010111'] = '1'
logic['demux']['110100'] = '1'
logic['demux']['110110'] = '1'
logic['demux']['110101'] = '0'
logic['demux']['110111'] = '1'
logic['demux']['001100'] = '0'
logic['demux']['001110'] = '0'
logic['demux']['001101'] = '1'
logic['demux']['001111'] = '1'
logic['demux']['101100'] = '1'
logic['demux']['101110'] = '0'
logic['demux']['101101'] = '1'
logic['demux']['101111'] = '1'
logic['demux']['011100'] = '0'
logic['demux']['011110'] = '1'
logic['demux']['011101'] = '1'
logic['demux']['011111'] = '1'
logic['demux']['111100'] = '1'
logic['demux']['111110'] = '1'
logic['demux']['111101'] = '1'
logic['demux']['111111'] = '1'
logic['demux']['help'] = '6 inputs: inp0, inp1, inp2, inp3, adr_LSB, adr_MSB\n1 output R\n Routes selected input to output using address'
logic['demux']['data'] = (6,1)
