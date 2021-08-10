cat $1 | awk '{ total1 += $2 ; avg1=total1/NR ; var1=var1+(($2 - avg1)^2 / (NR )); total2 += $3 ; avg2=total2/NR ; var2=var2+(($3 - avg2)^2 / (NR )); total3 += $4 ; avg3=total3/NR ; var3=var3+(($4 - avg3)^2 / (NR )); total4 += $5 ; avg4=total4/NR ; var4=var4+(($5 - avg4)^2 / (NR )); } END { print NR, total1/NR, avg1, var1, avg2, var2, avg3, var3, avg4, var4 }'

