#include<stdio.h>
#include <string.h>
inline void* _al_malloc(size_t size, size_t alignment)
{
    size_t a = alignment - 1;
    size_t word_length = sizeof(void*);
    void* raw = malloc(word_length + size + a);
    if (!raw)
    {
        return 0;
    }
    void* ptr = (void*)(((size_t)(raw) + (word_length + a)) & ~a);
    void* ptr1 = (void*)(raw + word_length + a);
    *((void**)ptr - 1) = raw;
    /*printf("ram %d %d %d %d \n", (unsigned int ) raw, (unsigned int ) ptr1, (unsigned int )ptr, (unsigned int) ptr-1);*/
    printf("\nram %p %p %p %p \n",  raw,  ptr1, ptr,  ptr-1);
    return ptr;
}
/**
 *  * Free allocated memory
 *   */
inline void _al_free(void * ptr)
{
    if (!ptr)
    {
        return;
    }
    void* raw = *((void**)ptr - 1);
    free(raw);
}

main()
{
    int i=0;
    void *p1,*p2,*p3;
    for(i=0;i<10;i++)
    {
    p1=_al_malloc(4, 16);
    printf("%d \n", (unsigned int ) p1);
    }
}
