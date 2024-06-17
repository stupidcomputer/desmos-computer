payload = """
ticker 1 : main
# Main memory structure
# This should be filled in with an override
id testing : B = []
# Operations on memory
: q(l, v, i)=ifval(l, i, [1...length(l)], v)
: setlistval(index, v) = B -> q(B, v, index)
: incx(index, v) = setlistval(index, B[index] + v)
: ifval(l, index, c, v) = {c = index : v, l[c]}

# Operations
: oadd(x, y) = x + y
: osub(x, y) = x - y
: odiv(x, y) = x / y
: omul(x, y) = x * y

# Instruction implementation
: ijmp(a, b, c) = ip -> a, jumped -> 1
: iadd(a, b, t_o) = setlistval(t_o, oadd(B[a], B[b]))
: isub(a, b, t_o) = setlistval(t_o, osub(B[a], B[b]))
: idiv(a, b, t_o) = setlistval(t_o, odiv(B[a], B[b]))
: imul(a, b, t_o) = setlistval(t_o, omul(B[a], B[b]))

: icmp(a, b, z) = { \\
    B[a] = B[b] : equals -> 1 , \\
    B[a] > B[b] : greater -> 1 , \\
    B[a] < B[b] : less -> 1 \\
  }
: irst(a, b, c) = equals -> 0, greater -> 0, less -> 0
: ield(addr, b) = setlistval(addr, equals)
: igld(addr, b) = setlistval(addr, greater)
: illd(addr, b) = setlistval(addr, less)


: ibe(addr, b, c) = {equals = 1 : ijmp(addr, 0, 0), jumped -> 1}
: ibne(addr, b, c) = {equals = 0 : ijmp(addr, 0, 0), jumped -> 1}
: ibg(addr, b, c) = {greater = 1 : ijmp(addr, 0, 0), jumped -> 1}
: ibl(addr, b, c) = {less = 1 : ijmp(addr, 0, 0), jumped -> 1}

: isto(v, addr) = setlistval(addr, v)
: imov(from, target) = setlistval(target, B[from])

# registers
# instruction pointer
: ip = 1

# is the result of icmp equal?
: equals = 0

# ditto for greater than
: greater = 0

# ditto for less than
: less = 0

# instruction loading areas
: inst = 0

# next three values after the instruction
: paramone = 0
: paramtwo = 0
: paramthree = 0

# main execution flows
: load(addr) = jumped -> 0, inst -> B[addr], \\
    paramone -> B[addr + 1], \\
    paramtwo -> B[addr + 2], \\
    paramthree -> B[addr + 3]
: exec = { \\
    inst = sto  : isto(paramone, paramtwo), \\
    inst = mov  : imov(paramone, paramtwo), \\
    inst = add  : iadd(paramone, paramtwo, paramthree), \\
    inst = cmp  : icmp(paramone, paramtwo, paramthree), \\
    inst = eld  : ield(paramone, paramtwo), \\
    inst = gld  : igld(paramone, paramtwo), \\
    inst = lld  : illd(paramone, paramtwo), \\
    inst = jmp  : ijmp(paramone, paramtwo, paramthree), \\
    inst = be   : ibe(paramone, paramtwo, paramthree), \\
    inst = bne  : ibne(paramone, paramtwo, paramthree), \\
    inst = bg   : ibg(paramone, paramtwo, paramthree), \\
    inst = bl   : ibl(paramone, paramtwo, paramthree), \\
    inst = sub  : isub(paramone, paramtwo, paramthree), \\
    inst = mul  : imul(paramone, paramtwo, paramthree), \\
    inst = div  : idiv(paramone, paramtwo, paramthree) \\
}
: incip = {jumped = 0 : ip -> ip + instwidth[inst] + 1}

# execution occurs here
: execution = 0
: jumped = 0

: loop = {execution = 0 : execution -> 1, execution = 1 : execution -> 2, execution = 2 : execution -> 0}
: loopaction = {execution = 0 : load(ip), execution = 1 : exec, execution = 2 : incip}
: main = loopaction, loop

: sto = 1
: mov = 17
: add = 2
: cmp = 3
: eld = 4
: gld = 5
: lld = 6
: jmp = 7
: be = 8
: bne = 9
: bg = 10
: bl = 11
: sub = 12
: mul = 13
: div = 14
: rst = 15

: instwidth = [2,3,2,1,1,1,1,1,1,1,3,3,3,3,0,2,2]
"""
