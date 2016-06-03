#include <stdio.h>

 
typedef struct structa_tag
{
    char    c;
    short int  s;
} structa_t;

 
typedef struct structb_tag
{
    short int  s;
    char    c;
    int     i;
} structb_t;

 
typedef struct structc_tag
{
    char    c;
    double   d;
    int      s;
} structc_t;

 
typedef struct structd_tag
{
    double   d;
    int      s;
    char    c;
} structd_t;

#pragma pack(push,2)
typedef struct struct_pada_tag
{
    char    c;
    short int  s;
} struct_pada_t;

 
typedef struct struct_padb_tag
{
    short int  s;
    char    c;
    int     i;
} struct_padb_t;

 
typedef struct struct_padc_tag
{
    char    c;
    double   d;
    int      s;
} struct_padc_t;

 
typedef struct struct_padd_tag
{
    double   d;
    int      s;
    char    c;
} struct_padd_t;
#pragma pack(pop)

int main()
{
    printf("sizeof(structa_t) = %ld\n", sizeof(structa_t));
    printf("sizeof(structb_t) = %ld\n", sizeof(structb_t));
    printf("sizeof(structc_t) = %ld\n", sizeof(structc_t));
    printf("sizeof(structd_t) = %ld\n", sizeof(structd_t));

    printf("Padding disabled\n"); 
    printf("sizeof(struct_pada_t) = %ld\n", sizeof(struct_pada_t));
    printf("sizeof(struct_padb_t) = %ld\n", sizeof(struct_padb_t));
    printf("sizeof(struct_padc_t) = %ld\n", sizeof(struct_padc_t));
    printf("sizeof(struct_padd_t) = %ld\n", sizeof(struct_padd_t));
    return 0;
}
