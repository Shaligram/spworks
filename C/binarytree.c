
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <pthread.h>
struct link
{
    struct link *left;
    struct link *right;
};
struct item
{
    struct link link;
    int data;
};

pthread_mutex_t lock;
void callback_fn(struct item *p);
void (*cb_fn)(struct item *p) = &callback_fn;
void insert(struct item **,int);
void *inorder(void *arg);

static int sum =0, occurence = 0, last_data=0;
void main()
{
    struct item *ptr;
    int no,i,num;
    pthread_t th_id;

    ptr = NULL;
    if(pthread_mutex_init(&lock, NULL)!=0)
    {
        printf("Mutex lock init failed\n");
        exit(1);
    }


    printf("\nProgram for Tree Traversal\n");
    printf("Enter the number of items to add to the tree.\n");
    scanf("%d",&no);

    printf("\nEnter the item\n");
    for(i=0;i<no;i++)
    {
        scanf("%d",&num);
        insert(&ptr,num);
    }

    /*getch();*/
    pthread_create(&th_id, NULL, &inorder, ptr);
    printf("\nINORDER TRAVERSAL\n");
    pthread_join(th_id,NULL);
    printf("\nData :%d| sum %d occurence %d\n", last_data, sum, occurence);
    pthread_mutex_destroy(&lock);
    
    getchar();
}

void insert(struct item **p,int num)
{
    if((*p)==NULL)
    {
     /*   printf("Leaf item created.\n");*/
        (*p)=malloc(sizeof(struct item));
        (*p)->link.left = NULL;
        (*p)->link.right = NULL;
        (*p)->data = num;
        return;
    }
    else
    {
        if(num<(*p)->data)
        {
          /*Directed to left link*/
            insert((struct item **)&((*p)->link.left),num);
        }
        else
        {
            /*Directed to right link*/
            insert((struct item **)&((*p)->link.right),num);
        }
    }
    return;
}

void *inorder(void *arg)
{
    struct item *p = (struct item *) arg;

    if(p!=NULL)
    {
        inorder(p->link.left);
        (*cb_fn)(p);
        inorder(p->link.right);
    }
    else
        return;
}

void callback_fn(struct item *p)
{
    static int flag =0;
    if(p!=NULL)
    {
        pthread_mutex_lock(&lock);
        /* set the flag for the first entry in the tree. this variable Initializes the value of first data*/
        if(flag==0)
        {
            last_data = p->data;
            flag =1;
            /* update sum and occurrence */
            sum = p->data;
            occurence =1;
        }
        else if(p->data!=last_data)
        {
            /* New data so, reset the occurence counter and print it */
            printf("\nData :%d| sum %d occurence %d\n", last_data, sum, occurence);
            sum = p->data;
            occurence =1;
            last_data = p->data;
        } 
        else
        {
            sum += p->data;
            occurence +=1;
        }

        pthread_mutex_unlock(&lock);
    }


}
