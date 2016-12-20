int x = 10;
void main(void) {
    int pid;
    pid = fork();
    printf("COMMON%d\n", x);
    if (pid == 0) {
        ++x;
        printf("CHILD %d\n", x);
    } else if (pid > 0) {
        printf("PARENT %d\n", x);
    } else {
        printf("failed to fork\n");
    }
    printf("COMMON %d\n", x);
}
