#include <stdlib.h>

int main()
{
    int *p = malloc(4);
    free(p);
    return p[0];
}
