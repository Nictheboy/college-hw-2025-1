#include <stdio.h>
#include <unistd.h>
#include <signal.h>

void handler(int sig) {}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <seconds>\n", argv[0]);
        return 1;
    }
    int sec;
    sscanf(argv[1], "%d", &sec);
    signal(SIGINT, handler);
    int remain = sleep(sec);
    printf("Slept for %d of %dsecs.\n", sec - remain, sec);
    return 0;
}
