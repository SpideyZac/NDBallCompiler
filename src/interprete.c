#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LEN 256

struct Token {
    char token[50];
};

int main(int argc, char *argv[])
{
    FILE* fp;
    int lines;
    char buffer[MAX_LEN];
    int counter = 0;

    fp = fopen(argv[1], "r");
    if (fp == NULL) {
      perror("Failed: ");
      return 1;
    } while (fgets(buffer, MAX_LEN, fp)) {
        lines++;
    } fclose(fp); fp = fopen(argv[1], "r"); char *text[lines]; while (fgets(buffer, MAX_LEN, fp)) {
        buffer[strcspn(buffer, "\n")] = 0;
        text[counter] = buffer;
        counter++;
    }

    fclose(fp);
    free(fp);

    return 0;
}