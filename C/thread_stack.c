#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <limits.h>
void *thread(void *arg) {
    char *ret;
    int a=0xdead;
    printf("thread() entered with argument '%s'\n", (char *)arg);
    if ((ret = (char*) malloc(20)) == NULL) {
        perror("malloc() error");
        exit(2);
    }
    strcpy(ret, "This is a test");
    pthread_exit((void*)&a);
}

int main(void)
{
    pthread_attr_t attr;
    int              rc;

    pthread_t thid;
    void *ret;

    void  *mystack;
    size_t mystacksize = 2 * PTHREAD_STACK_MIN;

    if (pthread_attr_init(&attr) == -1) {
        exit(1);
    }

    /* Get a big enough stack and align it on 4K boundary. */
    mystack = malloc(PTHREAD_STACK_MIN * 3);
    if (mystack != NULL) {
        printf("Using PTHREAD_STACK_MIN to align stackaddr %x.\n", mystack);
        mystack = (void *)((((long)mystack + (PTHREAD_STACK_MIN - 1)) /
                    PTHREAD_STACK_MIN) * PTHREAD_STACK_MIN);
    } else {
        exit(2);
    }

    printf("Setting stackaddr to %x\n", mystack);
    printf("Setting stacksize to %x\n", mystacksize);
    rc = pthread_attr_setstack(&attr, mystack, mystacksize);
    if (rc != 0) {
        printf("pthread_attr_setstack returned: %d\n", rc);
        exit(3);
    } else {
        printf("Set stackaddr to %x\n", mystack);
        printf("Set stacksize to %x\n", mystacksize);
    }


    if (pthread_create(&thid, &attr, thread, "thread 1") != 0) {
        exit(1);
    }

    if (pthread_join(thid, &ret) != 0) {
        exit(3);
    }

    printf("thread exited with '%s'\n", ret);
    rc = pthread_attr_destroy(&attr);
    if (rc != 0) {
        exit(5);
    }

    exit(0);
}
