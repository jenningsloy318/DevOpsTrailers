# AWK

- formatting with `printf`
    - add string to a column

    ```sh
    $ echo MaCo-MMT/mmt-srv-utility | awk -F "/" '{printf "maco-%s\n", $2}'
    maco-mmt-srv-utility
    ```
    - format string with alignment and width

    ```sh
    awk '{ printf "%-10s %s\n", $1, $2 }' mail-list
    ```
    > \- (Minus): The minus sign, used before the width modifier (see later on in this list), says to left-justify the argument within its specified width. Normally, the argument is printed right-justified in the specified width. Thus:
- sum the column

    ```sh
    awk -F '|' '$1 ~ /smiths/ {sum += $3} END {print sum}' inputfilename
    ```
    or

    ```sh
    awk -F '|' '$1 == "smiths" {sum += $3} END {print sum}' inputfilename
    ```
- count the column

    ```sh
    awk -F '|' '$1 ~ /smiths/ {count += 1} END {print count}' inputfilename
    ```
    or

    ```sh
    awk -F '|' '$1 ~ /smiths/ {count += 1} END {print count}' inputfilename
    ```