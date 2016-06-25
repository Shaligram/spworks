#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/semaphore.h>
#include <linux/kthread.h>  // for threads
#include <linux/sched.h>  // for task_struct
#include <linux/time.h>
#include <linux/timer.h>
#include <linux/spinlock.h>
#include <linux/spinlock_types.h>
#include <linux/delay.h>
static struct task_struct *thread1,*thread2;
static DEFINE_SPINLOCK(my_lock);

int thread_fn1(void * data) {

    unsigned long j0,j1;
    int delay = 60*HZ;
    j0 = jiffies;
    j1 = j0 + delay;
    spin_lock(&my_lock);
    while (time_before(jiffies, j1))
          schedule();
    spin_unlock(&my_lock);
    return 0;
}

int  thread_fn2(void *data) {
    int ret=0;
    msleep(100);
    ret=spin_trylock(&my_lock);
    if(!ret) {
         printk(KERN_INFO "Unable to hold lock");
          return 0;
    } else {
        printk(KERN_INFO "Lock acquired");
        spin_unlock(&my_lock);
        return 0;
    }
}



int thread_init (void) {
     
     char name[8]="thread1";
      char name1[8]="thread2";
       thread1 = kthread_create(thread_fn1,NULL,name);
        if((thread1))
              {
                    wake_up_process(thread1);
                      }
         
         thread2 = kthread_create(thread_fn2,NULL,name1);
          
          if((thread2))
                {
                      wake_up_process(thread2);
                        }
           return 0;
}



void thread_cleanup(void) {
     int ret;
      ret = kthread_stop(thread1);
       if(!ret)
             printk(KERN_INFO "Thread stopped");

}
MODULE_LICENSE("GPL"); 
module_init(thread_init);
module_exit(thread_cleanup);
