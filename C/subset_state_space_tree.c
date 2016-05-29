/*Binary tree traversal:*/

#include <stdio.h>
#include <malloc.h>
struct node
{
    struct node *left;
    int data;
    int sum;
    int valid;
    struct node *right;
};
#define SUM_TOTAL 16
/* Prototypes for funtions needed in printPaths() */
void printPathsRecur(struct node* node, int path[], int pathLen);
void printArray(int ints[], int len);

/*Given a binary tree, print out all of its root-to-leaf
 *  paths, one per line. Uses a recursive helper to do the work.*/
void printPaths(struct node* node) 
{
    int path[1000];
    printPathsRecur(node, path, 0);
}


int a[]= { 1,12,23,14,5,6,7,18,9,10};
int sum;
void main()
{
    void insert(struct node **,int, int, int);
    void inorder(struct node *);

    struct node *ptr;
    int no,i,num;

    ptr = NULL;

    printf("\nProgram for Tree Traversal\n");
    printf("Enter the number of nodes to add to the tree.<BR>\n");

    insert(&ptr, 0, 0, 0);
    for(i=0;i<sizeof(a)/sizeof(int);i++)
    {
        sum+=a[i];
        insert(&ptr, a[i], sum, 0);
    }

    /*getch();*/
    printf("\nINORDER TRAVERSAL\n");
    /*inorder(ptr);*/
    printf("\n");
    printf("\nSubset are \n");
    printPaths(ptr);

}

void insert(struct node **p,int data, int sum, int valid)
{
    int i=0;

    if((*p)==NULL)
    {
        printf("Leaf node created with (%d,%d)\n", data,sum);
        (*p)=malloc(sizeof(struct node));
        (*p)->left = NULL;
        (*p)->right = NULL;
        (*p)->data = data;
        (*p)->sum = sum;
        (*p)->valid = valid;
        return;
    }
    else if((*p)->data==data)
            {
                /*If duplicate numbers are present, then don't add in the tree */
                return;
            }
    else
    {
        if(((*p)->sum + data) > SUM_TOTAL) /* Base condition */
            return;

        printf("---> Directed to left link.\n");
        insert(&((*p)->left), data, (*p)->sum+data,1);

        printf("---> Directed to right link.\n");
        insert(&((*p)->right),data, (*p)->sum,0);
    }
    return;
}

void inorder(struct node *p)
{
    if(p!=NULL)
    {
        inorder(p->left);
        printf("\nData :%d",p->data);
        inorder(p->right);
    }
    else
        return;
}
/* Recursive helper function -- given a node, and an array containing
 *  the path from the root node up to but not including this node,
 *   print out all the root-leaf paths.*/
void printPathsRecur(struct node* node, int path[], int pathLen) 
{
    if (node==NULL) 
        return;

    /* append this node to the path array */
    if(node->valid) {
    path[pathLen] = node->data;
    pathLen++;
    }

    /* it's a leaf, so print the path that led to here  */
    if (node->left==NULL && node->right==NULL) 
    {
        printArray(path, pathLen);
    }
    else
    {
        /* otherwise try both subtrees */
        printPathsRecur(node->left, path, pathLen);
        printPathsRecur(node->right, path, pathLen);
    }
}


/* UTILITY FUNCTIONS */
/* Utility that prints out an array on a line. */
void printArray(int ints[], int len) 
{
    int i;
    int sum=0;
    for (i=0; i<len; i++) 
    {
        sum+=ints[i];
    }
    if(sum==SUM_TOTAL)
    {
        for (i=0; i<len; i++) 
        {
            printf("%d ", ints[i]);
        }
    printf("\n");
    }
} 
