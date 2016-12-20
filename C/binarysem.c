#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <semaphore.h>
#define LIMIT 1000

    sem_t sem1,sem2;
void* function1(void *p)
{
    int expected = *(int *)p;

    while(expected < LIMIT) {
        
        sem_wait(&sem1);{
            printf("Even %d\n", expected);
            expected += 2;
        }
        sem_post(&sem2);
    }
    exit(0);
}

void* function2(void *p)
{
    int expected = *(int *)p;

    while(expected < LIMIT) {
        sem_wait(&sem2); {
            printf("Odd  %d\n", expected);
            expected += 2;
        }
        sem_post(&sem1);
    }
    exit(0);
}

int main(int argc, char *argv[])
{
    pthread_t thread1, thread2;
    int counter = 0;
    int expected_0 = 0, expected_1 = 1;
    sem_init(&sem1, 0, 1);
    sem_init(&sem2, 0, 0);

    pthread_create(&thread1, NULL, function1, (void *)&expected_0);
    pthread_create(&thread2, NULL, function2, (void *)&expected_1);
  


    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    return 0;
}
