# read & display BMS file
# Author: ProjectEli 2019

# function definitions
def GCD(a,b): # 최대공약수, 유클리드 호제법
    while(b!=0):
        residual = a%b
        a=b
        b=residual
    return abs(a)

def LCM(a,b): # 최소공배수
    gcd = GCD(a,b)
    return 0 if (gcd==0) else abs(int(a*b/gcd))

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

# initialize
import re
with open('Eli(obj_DEF).bms','r') as f:
    fileText = '\n'.join([x.strip() for x in f.readlines()]) #빈칸제거

    
# 유효한 라인만 뽑기 (1p 가정)
effectiveLines = sorted( re.findall(r'#\d\d\d1\d:.+',fileText) )

# 마디수 세기
N_node = int( effectiveLines[-1][1:4] ) # #ddd가 제일 큰 것. 정수 가정

# 공간 생성
objChannels = 8 # 키 갯수 (7키=8, 5키=6, 스크포함)
minBits = 8 # 기본 쪼개는 비트
noteChars = 2 # 노트를 표현하는 char 수
filler = ' '

messageSpace = [ [] for i in range(N_node) ] # 2D array, channel수 보존안됨
channelSpace = [ [] for i in range(N_node) ] # 채널이 전부 기록되진 않으므로 여기에 저장

bitSpace = []
fullSpace = []

# nodeNo로 라인 분리 (마디별)
for line in effectiveLines:
    nodeNo, objChannel, message = int(line[1:4]), int(line[5:6]), line[7:] # 끝점 미포함
    #print(nodeNo, objChannel, message)
    splitMessage = [message[k:k+noteChars] for k in range(0,len(message),noteChars)]
    messageSpace[nodeNo-1].append(splitMessage) # message 기억
    channelSpace[nodeNo-1].append(int(objChannel)) # channel 기억

# node 내 정제작업
for nodeIndex, channelList in enumerate(channelSpace):
    # 해당 node에서 가장 비트 많이쪼갠거 기준으로 정렬
    nodeMaxBit = minBits
    for channelIndex, channel in enumerate(channelList):
        nodeMaxBit = LCM(nodeMaxBit,len(messageSpace[nodeIndex][channelIndex]))
    bitSpace.append(nodeMaxBit) # 해당 node에서 bit 저장

    _nodeSpace_channel = []
    # 이제 max bit를 알기때문에 node내에서 matrix모양 만들 수 있다.
    for channel in range(1,objChannels+1): # robust하게 channel을 scan함
        if channel in channelList: # 해당 channel data가 존재하는지 확인.
            channelIndex = channelList.index(channel) #처음으로 나오는 index 찾아줌
            repeats = int( nodeMaxBit / len(messageSpace[nodeIndex][channelIndex]) ) # 해당 channel의 반복수
            tempList = []
            for note in messageSpace[nodeIndex][channelIndex]: # note를 sweep하면서 갯수늘림
                if not note == '00':
                    tempList = tempList + ['-'] + [filler]*(repeats-1) # 여기에서 note정보 소실됨
                else:
                    tempList = tempList +   [filler]*repeats
            _nodeSpace_channel.append(tempList)
        else: # 못찾으면 filler문자로 채움
            _nodeSpace_channel.append([filler]*nodeMaxBit)
    _nodeSpace_bit = transpose(_nodeSpace_channel) # bit에 관한 축이 되도록 바꿔줌

    # string으로 바꾸는 작업
    _nodeSpace_Str = '='*objChannels + '\n' + '\n'.join( [''.join(x) for x in _nodeSpace_bit] )
    fullSpace.append(_nodeSpace_Str)
    
    # 여기까지 마쳤을때 fullSpace element 내용 예시 (7키)
    # ========
    # 00000-00
    # -0000000
    # 000-0000
    # 00000-00

# 마지막 string 작업
fullStr = '\n'.join(fullSpace)
print(fullStr)