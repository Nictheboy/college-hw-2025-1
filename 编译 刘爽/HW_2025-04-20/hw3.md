# Homework 3

## 1. 下列文法对整型常数和实型常数施用乘法运算符生成表达式：当两个整型数相乘时，结果仍为整型数；否则结果为实型数。注：用 type表示类型属性

```
E→E*T|T

T→num.num | num
```

(1) 给出确定每个子表达式结果类型的属性文法。

答：

```
E1→E2*T {
    if (E2.type == INTEGER && T.type == INTEGER)
        E1.type = INTEGER;
    else
        E1.type = REAL;
}
E→T {
    E.type = T.type;
}
T→num1.num2 {
    T.type = REAL;
}
T→num {
    T.type = INTEGER;
}
```

其中 floor(x) 是向下取整函数。

(2) 扩充（1）的属性文法，加入将表达式翻译成后缀形式的语义。

```
E1→E2*T {
    if (E2.type == INTEGER && T.type == INTEGER)
        E1.type = INTEGER;
    else
        E1.type = REAL;
    E1.postfix = E2.postfix || T.value || *
}
E→T {
    E.type = T.type;
    E.postfix = T.value;
}
T→num1.num2 {
    T.type = REAL;
    T.value = VALUE(num1.num2);
}
T→num {
    T.type = INTEGER;
    T.value = VALUE(num);
}
```

其中 || 表示串的拼接。

## 2. 下列文法由开始符号S产生一个二进制数，令综合属性val给出该数的十进制值，例如对于给定的二进制数101.101，S.val=5.625

```
S→L.L|L
L→LB|B
B→0|1
```

设计求S.val的属性文法。其中已知B的综合属性bval 给出由B产生的二进位的结果值，可以自行定义其他计算中需要用到的属性值。

```
S→L1.L2 { S.val = L1.val + L2.val / pow(2, floor(log(2, L2.val)) + 1); }
S→L { S.val = L.val; }
L1→L2B { L1.val = L2.val * 2 + B.bval; }
L→B { L.val = B.bval; }
```

## 3. 下列文法生成变量的类型说明

L→id L
L→, id L | :T
T→integer | real
构造一个翻译模式，把每个标识符的类型存入符号表（提示：存入符号表操作通过addtype(id.entry, L.type)来实现, L是产生id的非终结符）。

```
L1→id L2 {
    L1.type = L2.type;
    addtype(id.entry, L2.type);
}
L1→, id L2 {
    L1.type = L2.type;
    addtype(id.entry, L2.type);
}
L→:T { L.type = T.type; }
T→integer { T.type = INTEGER; }
T→real { T.type = REAL; }
```

## 4. 给出下列表达式的逆波兰（后缀式）表示

 (1) (A or B) and (C or not D and not E) or F
 (2) -a+b*c^(c-d/e)-(-c+d)
 (3) if a+b*(c+d/e)==0 then s:=a^(3+e) else s:=b^a^d

```
(1) A B or C D not E not and or and F or
(2) a -' b c c d e / - ^ * + c -' d + -
(3) a b c d e / + * + 0 == s a 3 e + ^ := s b a d ^ ^ := IF
```

其中 -' 是一元 - 运算符，即相反数运算符

## 5. 请将下列表达式分别表示成三元式，间接三元式和四元式序列

-(a+b)*c^(a*d+e)-(a+b-c)

三元式

| idx | operator | oprand1 | oprand2 |
| --- | -------- | ------- | ------- |
|(1) |+ |a |b|
|(2) |* |a |d|
|(3) |+ |(2)| e|
|(4) |^ |c |(3)|
|(5) |* |(1)| (4)|
|(6) |- |(5)||
|(7) |+ |a |b|
|(8) |- |(7)| c|
|(9) |- |(6) |(8)|

间接三元式

| idx | operator | oprand1 | oprand2 |
| --- | -------- | ------- | ------- |
|(1) |+ |a |b|
|(2) |* |a |d|
|(3) |+ |(2)| e|
|(4) |^ |c |(3)|
|(5) |* |(1)| (4)|
|(6) |- |(5)||
|(7) |+ |a |b|
|(8) |- |(7)| c|
|(9) |- |(6) |(8)|

| order | idx |
| ----- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |
| 6 | 6 |
| 7 | 7 |
| 8 | 8 |
| 9 | 9 |

四元式

| idx | operator | oprand1 | oprand2 | result |
| --- | -------- | ------- | ------- | ------ |
|(1) |+ |a |b| t1 |
|(2) |* |a |d| t2 |
|(3) |+ |t2| e| t3 |
|(4) |^ |c |t3| t4 |
|(5) |* |t1|t4| t5 |
|(6) |- |t5|| t6 |
|(7) |+ |a |b| t7 |
|(8) |- |t7| c| t8 |
|(9) |- |t6 |t8| t9 |
