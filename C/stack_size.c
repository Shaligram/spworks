#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#define LARGE (2097152); /* 8MB/sizeof(int) */
int main(int argc, char **argv)
{
    int status = 0;
    int limit = LARGE;
    while(1)
    {
        limit--;
        int pid = fork();
        if(pid == 0)
        {
            /* Child would crash with a segfault if stack overflows */
            int arr[limit];
            arr[0] = limit;
            return arr[0];
        }
        /* Wait for this particular child to exit or crash. */
        waitpid(pid, &status, WUNTRACED);
        if(WIFEXITED(status))
        {
            /* Child exited normally and not because of a segfault. */
            printf("Estimated stack size is %d\n", limit * sizeof(int));
            break;
        }
    }
    return 0;
}
