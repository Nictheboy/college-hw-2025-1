#include <stdlib.h>

int main() {
    int *p = malloc(8);
    free(p + 4);
    return 0;
}
