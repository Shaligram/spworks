#define _GNU_SOURCE
#include <assert.h>
#include <unistd.h>

int main(void) {
    /* Get the first address beyond the end of the heap. */
    void *b = sbrk(0);
    int *p = (int *)b;

    /* Below statement generated SEGFAULT */
     /* Segfault because it is outside of the heap. */
/*    *p=1;*/


    /* Move it 2 ints forward */
    brk(p + 2);

    /* Use the ints. */
    *p = 1;
    *(p + 1) = 2;
    assert(*p == 1);
    assert(*(p + 1) == 2);
    /* Deallocate back. */
    brk(b);

    return 0;
}
