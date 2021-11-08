AWK
---


1. formatting with `printf`
    - add string to a column
    ```
    $ echo MaCo-MMT/mmt-srv-utility | awk -F "/" '{printf "maco-%s\n", $2}'
    maco-mmt-srv-utility
    ```
    - format string with alignment and width
    ```
    awk '{ printf "%-10s %s\n", $1, $2 }' mail-list
    ```
    > - - (Minus): The minus sign, used before the width modifier (see later on in this list), says to left-justify the argument within its specified width. Normally, the argument is printed right-justified in the specified width. Thus:
2. sum the column
    ```
    awk -F '|' '$1 ~ /smiths/ {sum += $3} END {print sum}' inputfilename
    ```
    or 
    ```
    awk -F '|' '$1 == "smiths" {sum += $3} END {print sum}' inputfilename
    ```
3. count the column
    ```
    awk -F '|' '$1 ~ /smiths/ {count += 1} END {print count}' inputfilename
    ```
    or 
    ```
    awk -F '|' '$1 ~ /smiths/ {count += 1} END {print count}' inputfilename
    ```