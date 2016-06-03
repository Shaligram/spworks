#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

#define LIMIT 100

int global =0;
void* function1(void *p)
{
    int expected = *(int *)p;

    while(expected < LIMIT) {
        if(global==0) {
            printf("%d\n", expected);
            expected += 2;
            global=1;
        };
    }
    exit(0);
}

void* function2(void *p)
{
    int expected = *(int *)p;

    while(expected < LIMIT) {
        if(global==1) {
            printf("%d\n", expected);
            expected += 2;
            global=0;
        };
    }
    exit(0);
}

int main(int argc, char *argv[])
{
    pthread_t thread1, thread2;
    int counter = 0;
    int expected_0 = 0, expected_1 = 1;

    pthread_create(&thread1, NULL, function1, (void *)&expected_0);
    pthread_create(&thread2, NULL, function2, (void *)&expected_1);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    return 0;
}
