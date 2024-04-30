/*
 * Sample program to demonstrate buffer overflow attack.
 */
#include <stdio.h>

char *gets(char*);

void return_input (void) {
       char array[8];
       gets(array);
       printf("%s\n", array);
}

int main() {
       return_input();
       return 0;
}

