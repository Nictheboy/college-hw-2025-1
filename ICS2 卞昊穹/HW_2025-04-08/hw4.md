# Homework 4

## Question 1

My program:

```c
int main() {
    int *p = 0;
    return *p;
}
```

The program crashed:

```bash
$ ./null 
Segmentation fault (core dumped)
```

## Question 2

GDB output:

```bash
$ gdb null
GNU gdb (Ubuntu 15.1-1ubuntu2) 15.1
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "aarch64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from null...
(gdb) r
Starting program: /home/nictheboy/Desktop/college/ICS2 卞昊穹/HW_2025-04-08/null 

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.ubuntu.com>
Enable debuginfod for this session? (y or [n]) 
Debuginfod has been disabled.
To make this setting permanent, add 'set debuginfod enabled off' to .gdbinit.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/aarch64-linux-gnu/libthread_db.so.1".

Program received signal SIGSEGV, Segmentation fault.
0x0000aaaaaaaa07b4 in main () at null.c:3
3           return *p;
(gdb) 
```

## Question 3

Valgrind output:

```bash
$ sudo valgrind --leak-check=yes ./null 
==22985== Memcheck, a memory error detector
==22985== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==22985== Using Valgrind-3.23.0 and LibVEX; rerun with -h for copyright info
==22985== Command: ./null
==22985== 
==22985== Invalid read of size 4
==22985==    at 0x1087B4: main (null.c:3)
==22985==  Address 0x0 is not stack'd, malloc'd or (recently) free'd
==22985== 
==22985== 
==22985== Process terminating with default action of signal 11 (SIGSEGV)
==22985==  Access not within mapped region at address 0x0
==22985==    at 0x1087B4: main (null.c:3)
==22985==  If you believe this happened as a result of a stack
==22985==  overflow in your program's main thread (unlikely but
==22985==  possible), you can try to increase the size of the
==22985==  main thread stack using the --main-stacksize= flag.
==22985==  The main thread stack size used in this run was 8388608.
==22985== 
==22985== HEAP SUMMARY:
==22985==     in use at exit: 0 bytes in 0 blocks
==22985==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==22985== 
==22985== All heap blocks were freed -- no leaks are possible
==22985== 
==22985== For lists of detected and suppressed errors, rerun with: -s
==22985== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault
```

It means memory 0x0 which is NULL is accessed.

## Question 4

There's a memory leak.

I cannot use GDB to find the leak.

Valgrind can:

```c
#include <stdlib.h>

int main() {
    malloc(1);
    return 0;
}
```

```bash
$ gcc leak.c -o leak -g
$ sudo valgrind --leak-check=yes ./leak 
==24683== Memcheck, a memory error detector
==24683== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==24683== Using Valgrind-3.23.0 and LibVEX; rerun with -h for copyright info
==24683== Command: ./leak
==24683== 
==24683== 
==24683== HEAP SUMMARY:
==24683==     in use at exit: 1 bytes in 1 blocks
==24683==   total heap usage: 1 allocs, 0 frees, 1 bytes allocated
==24683== 
==24683== 1 bytes in 1 blocks are definitely lost in loss record 1 of 1
==24683==    at 0x488547C: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==24683==    by 0x1087F7: main (leak.c:4)
==24683== 
==24683== LEAK SUMMARY:
==24683==    definitely lost: 1 bytes in 1 blocks
==24683==    indirectly lost: 0 bytes in 0 blocks
==24683==      possibly lost: 0 bytes in 0 blocks
==24683==    still reachable: 0 bytes in 0 blocks
==24683==         suppressed: 0 bytes in 0 blocks
==24683== 
==24683== For lists of detected and suppressed errors, rerun with: -s
==24683== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## Question 5

```c
int array[100];

int main() {
    return array[100];
}
```

It works but is not correct.

```bash
$ gcc overflow.c -o overflow -g
$ ./overflow
$ sudo valgrind --leak-check=yes ./overflow 
==25169== Memcheck, a memory error detector
==25169== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==25169== Using Valgrind-3.23.0 and LibVEX; rerun with -h for copyright info
==25169== Command: ./overflow
==25169== 
==25169== 
==25169== HEAP SUMMARY:
==25169==     in use at exit: 0 bytes in 0 blocks
==25169==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==25169== 
==25169== All heap blocks were freed -- no leaks are possible
==25169== 
==25169== For lists of detected and suppressed errors, rerun with: -s
==25169== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

## Question 6

It works, but it's not correct:

```c
#include <stdlib.h>

int main()
{
    int *p = malloc(4);
    free(p);
    return p[0];
}
```

```bash
$ gcc free.c -o free
$ ./free 
$ sudo valgrind --leak-check=yes ./free 
==25361== Memcheck, a memory error detector
==25361== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==25361== Using Valgrind-3.23.0 and LibVEX; rerun with -h for copyright info
==25361== Command: ./free
==25361== 
==25361== Invalid read of size 4
==25361==    at 0x108848: main (in /home/nictheboy/Desktop/college/ICS2 卞昊穹/HW_2025-04-08/free)
==25361==  Address 0x4a7e040 is 0 bytes inside a block of size 4 free'd
==25361==    at 0x4888518: free (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==25361==    by 0x108843: main (in /home/nictheboy/Desktop/college/ICS2 卞昊穹/HW_2025-04-08/free)
==25361==  Block was alloc'd at
==25361==    at 0x488547C: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==25361==    by 0x108837: main (in /home/nictheboy/Desktop/college/ICS2 卞昊穹/HW_2025-04-08/free)
==25361== 
==25361== 
==25361== HEAP SUMMARY:
==25361==     in use at exit: 0 bytes in 0 blocks
==25361==   total heap usage: 1 allocs, 1 frees, 4 bytes allocated
==25361== 
==25361== All heap blocks were freed -- no leaks are possible
==25361== 
==25361== For lists of detected and suppressed errors, rerun with: -s
==25361== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## Question 7

It crashed. I do not need tool to find this problem.

```c
#include <stdlib.h>

int main() {
    int *p = malloc(8);
    free(p + 4);
    return 0;
}
```

```bash
$ gcc free2.c -o free2
free2.c: In function ‘main’:
free2.c:5:5: warning: ‘free’ called on pointer ‘p’ with nonzero offset 16 [-Wfree-nonheap-object]
    5 |     free(p + 4);
      |     ^~~~~~~~~~~
free2.c:4:14: note: returned from ‘malloc’
    4 |     int *p = malloc(8);
      |              ^~~~~~~~~
$ ./free2 
free(): invalid pointer
Aborted (core dumped)
```

