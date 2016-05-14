#include<stdlib.h>
#include<stdio.h>

typedef struct list {
    int a;
    struct list *next;
}mylist;

mylist *head;
main()
{
    int i;

    head=NULL;
    for(i=0;i<10;i++)
    {
        createlist(&head, i);
    }
        printf("====== \n");
        display(head);
        printf("Reversing====== \n");
        reversel(&head, head);
        display(head);
        /*reversed(head);*/
}
display(mylist *head)
{
    while(head!=NULL)
    {
        printf("Added =%d %p\n",head->a, head);
        head =head->next;
    }
}

createlist(mylist **head, int a)
{
    mylist *temp,*prev;
    if(*head==NULL)
    {
        temp=(mylist *)calloc(1,sizeof(mylist));
        temp->a=a;
        temp->next=NULL;
        *head=temp;
        printf("Added =%d %p\n",a, temp);
    }
    else
    {
        prev =*head;
        while(prev->next!=NULL){
        prev=prev->next;
        }
        temp =(mylist *)calloc(1,sizeof(mylist));
        temp->a=a;
        temp->next=NULL;
        prev->next=temp;
        printf("Added =%d %p\n",a,temp);
    }

}
reversed(mylist *head)
{
    if(head==NULL){
        return;
    }
    reversed(head->next);
    printf("\nValue %d %p", head->a, head);
}

reversel(mylist **head, mylist *tmp)
{
    mylist *prev;
    if(tmp->next==NULL)
    {
        *head=tmp;
        return;
    }
    
    reversel(head, tmp->next);
    prev= tmp->next;
    prev->next = tmp;
    tmp->next=NULL;
}

deleteitem()
{
}
search()
{
}
