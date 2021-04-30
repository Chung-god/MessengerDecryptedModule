import hashlib

def mix1(A, B):
    result = ''
    for i in range(0, min(len(A),len(B))):
        result = result + A[i*2:(i*2+2)] + B[i]
    result = result + A[i*2+3:] + B[i+1:]
    return result

def mix2(A, B):
    result=''
    for i in range(0, min(len(A), len(B))):
        result = result + A[i*1:(i*1+1)] + B[i]
    result = result + A[i+1:] + B[i+1:]
    return result

def mix3(A, B):
    result = B + A
    return result

def userDB_key(android_id):
    
    ustring1 = "754s8UlVo8[4X(2<D:y%!lf,Zl0obZoN"
    ustring2 = "xJ*v*:x|68ZZ'w!}TjI%!lf<w3tsVU\\v"
    ustring3 = "_;F*hJ2_7e4s8UlV<Ey5!L6\$V*R|`Nx~x[zXH2|6(zO'7!f68Zj'w!]FqL9NB`z"

    resultA = mix1(hashlib.sha256(android_id.encode()).hexdigest(), ustring1)
    resultB = mix2(hashlib.sha256(resultA.encode()).hexdigest(), ustring2)
    resultC = mix1(hashlib.sha256(resultB.encode()).hexdigest(), ustring3)
    userkey = hashlib.sha256(resultC.encode()).hexdigest()
    
    return userkey

def talkDB_key(useridx):

    tstring1 = "8slUV47U'j!8]Z6w!%f:,yDl8sl5V47U"
    tstring2 = "!%fj<IDlN9`qz<FBXz2x|[~H|RNVx*$`"
    tstring3 = "Vsl3vtwU'J!(fz6'h*2;_F_J!56J\yJLXD28<[o('Z!8}Z6wboolN0ZZ*vxJ|.x:"

    resultD = mix2(hashlib.sha256(useridx.encode()).hexdigest(), tstring1)
    resultE = mix2(hashlib.sha256(resultD.encode()).hexdigest(), tstring2)
    resultF = mix3(hashlib.sha256(resultE.encode()).hexdigest(), tstring3)
    talkkey = hashlib.sha256(resultF.encode()).hexdigest()
    
    return talkkey

    
if __name__ == '__main__':
    android_id = '4f77d977f3f1c488'
    useridx = "2169372"

    userkey = userDB_key(android_id)
    talkkey = talkDB_key(useridx)
    print(userkey)
    print(talkkey)