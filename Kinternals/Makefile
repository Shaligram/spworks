obj-m += sleep_wake_kernel.o spinlock.o kernel_wait.o
all:
	 make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:  
	  make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

