#! /bin/bash

FROM=$1
TO=$2

#for kind in MC DATA; do
for kind in DATA; do
#for kind in MC; do
    f=${FROM}_${kind}
    t=${TO}_${kind}

    if [ ! -d "$f" ]; then
        echo "Error: $f does not exist"
        continue
    fi

    if [ -d "$t" ]; then
        echo "Error: $t already exist"
        continue
    fi

    echo "Cloning $f to $t"
    cp -r $f $t

    pushd $t &> /dev/null

    echo "Substituing $FROM to $TO in all files..."
    find . \( -type l -o -type f \) |
        while read filename
        do
            if [ -L $filename ]; then
                target=`readlink $filename`
                ln -sf ${target//$FROM/$TO} $filename
            fi

            mv $filename ${filename//$FROM/$TO}
        done

    popd &> /dev/null
    echo "Done"
done
