#include <stdio.h>
#include <stdbool.h>	/* true and false */
#include <string.h>	/* strncmp() */

char *gets(char *str);

void next_tag(char *str)
{
    strncpy(str, "START", 8);
}

int main(int argc, char *argv[])
{
    int valid = false;
    char str1[8];
    char str2[8];

    next_tag(str1);
    gets(str2);
    if (strncmp(str1, str2, 8) == 0)
	valid = true; 
    printf("buffer1: str1(%s), str2(%s), valid(%d)\n", str1, str2, valid);
}

