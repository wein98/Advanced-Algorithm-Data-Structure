stringx = "aab$aabaabcaxaabaabcy"
n = len(stringx)
zArr = [0]*n
zArr[0] = n     # set first zArr to length of string

L = 0
R = 0

for i in range(1,n):
    if i < R:
        k = i-L

        # case 2 - where zArr[k] is < remaining
        if zArr[k] < R-i+1:
            zArr[i] = zArr[k]

        # case 2b - where zArr[k] is >= remaining
        else:
            while R < n and stringx[R] == stringx[R-i]:
                R += 1

            zArr[i] = R-i
            L = i
            R -= 1
    
    # case 1
    else:
        L = i
        R = i
        while R < n and stringx[R] == stringx[R-i]:
            R +=1
        
        zArr[i] = R-i
        R -= 1

print(zArr)