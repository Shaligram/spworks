#include <pthread.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <ctype.h>


typedef struct thread_info
{
    pthread_t id;
    int thread_num;
    char *input_arg;
}t_info_t;


void *thread_start(void *arg)
{
    char *p;
    char *upper_arg;
    t_info_t *t_info = (t_info_t *) arg;

    printf("stack  %p  %d name %s\n", &p, t_info->thread_num, t_info->input_arg);

    upper_arg = strdup(t_info->input_arg);
    p = upper_arg;
    while(*p!='\0')
    {
        *p=toupper(*p);
        p++;
    }
    return upper_arg;
}

main(int argc, char *argv[])
{
    int num_threads, i;
    pthread_attr_t attr;
    t_info_t *info;

    void *res;

    
    num_threads = argc-1;

    pthread_attr_init(&attr);

    pthread_attr_setstacksize(&attr, 0x10);
    info  = calloc(num_threads, sizeof(t_info_t));

    printf("Nuk of thread %d\n", num_threads);
    for(i=0;i<num_threads;i++)
    {
    info[i].thread_num = i+1;
    info[i].input_arg = argv[i+1];
    pthread_create(&(info[i].id), &attr,&thread_start, &info[i]);
    }
sleep(3);

    pthread_attr_destroy(&attr);

    for(i=0;i<num_threads;i++) {
    pthread_join((info[i].id), &res);
    printf("Join thread id %d for thread name %s\n", info[i].thread_num, (char*)res);
    free(res);
    }
    free(info);

}

