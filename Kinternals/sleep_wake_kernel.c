#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/sched.h>
#include <linux/kthread.h>

#define DBG_FN_ENTRY()  \
    do { \
        printk(KERN_INFO "Inside function [ %s ]\n", \
                __FUNCTION__); \
    } while(0)

struct task_struct *sleeping_task = NULL;
int k = 0;
int func(void *s)
{
    int i;

    for(i=0;i<20;i++) {
        printk("[%d][%s]\n", i, (char *)s);
        if(sleeping_task)
            wake_up_process(sleeping_task);
        if(i==10) {
            sleeping_task = current;
            set_current_state(TASK_INTERRUPTIBLE);
            schedule();
        }
    }
    return 0;
}

int init_module(void)
{
    DBG_FN_ENTRY();

    kthread_create(func, (void *)"first", 0);
    kthread_create(func, (void *)"second", 0);

    return 0;
}

void cleanup_module(void)
{
    DBG_FN_ENTRY();
}
