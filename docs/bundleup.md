# Bundle up




## WARNING!

This recipe is highly preliminary and should be used with causion. It was originally developed for a NEMO repository under git control. 

**Please, backup your files and commit all necessary changes BEFORE you invoke any of the commands below!**


## Environment

```bash
# in NEMOGCM repository/worktree
OWD=`pwd`
CONFIG=ORCA025.L46.LIM2vp.CFCSF6.JRA.XIOS2
EXP=cycle1
EXP+=(cycle2 cycle3 cycle4 cycle5 cycle6)
REPOROOT=$(git rev-parse --show-toplevel)
# Within EXP folder:  
#  APWD=$(pwd -P);APWD=(${APWD//\// }); EXP=${APWD[@]: -1}; CONFIG=${APWD[@]: -2:1}
CURBRANCH=$(git symbolic-ref HEAD  | sed -e 's,.*/\(.*\),\1,')
#CURBRANCH=${CURBRANCH%-*}    # Remove possible host-suffix from branch name
DSTMP=$(mktemp -d)
```


### 1. Prepare for Export

```bash
cd CONFIG/${CONFIG}
for zEXP in ${EXP[@]}; do
    [ ! -f $zEXP/README.md ] && mkreadme $zEXP
done
cd ../..
git add .
git commit -m "adding README.md"

for zEXP in ${EXP[@]}; do

    git subtree split --prefix=CONFIG/${CONFIG} -b split
    WTSPLIT=${DSTMP}/split
    git worktree add ${WTSPLIT} split
    cd ${DSTMP}/split
```



### 2. List unwanted folders

remove unwanted folders (all folders except for MY_SRC, the default EXP00 and the actual experiment folder):

```bash
    # variable p is an array, If you want to check the content, you can do that using:
    #  echo ${p[@]}
    p=(EXP00 MY_SRC)
    p+=($zEXP)
    #zopt=();for zp in ${p[@]}; do zopt+=("-not -path \*${zp}\*"); done
    zopt=();for zp in ${p[@]}; do zopt+=("-not -path ${zp}"); done
    luwf=($(eval "find * -maxdepth 0 -type d ${zopt[@]}"))
```



### 3. Delete unwanted folders

> Example from [stackoverflow](https://stackoverflow.com/a/32886427): To remove `DIRECTORY_NAME` completely (also from history)
>
> ```
> git filter-branch --index-filter 'git rm -rf --cached --ignore-unmatch DIRECTORY_NAME/' --prune-empty --tag-name-filter cat -- --all
> git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
>
> # Ensure all old refs are fully removed
> rm -Rf .git/logs .git/refs/original
>
> # Perform a garbage collection to remove commits with no refs
> git gc --prune=all --aggressive
> ```
>
> 

Using a loop over list of unwanted folders (based on the solution above):

```bash
    for uwf in ${luwf[@]}; do
        git filter-branch \
            --index-filter "git rm -rf --cached --quiet --ignore-unmatch ${uwf}/" \
            --prune-empty \
            --tag-name-filter cat -- \
            --all

        git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d

        # Ensure all old refs are fully removed
        rm -Rf .git/logs .git/refs/original

        # Perform a garbage collection to remove commits with no refs
        git gc --prune=all --aggressive

    done

```



> ### 4.( Inport DRAKKARshare)
>
> :warning: URL for DRAKKARshare/Template will change! will be moved to git.geomar.de.
>
> ```bash
> git remote add DStemplate git@gitlab.com:DRAKKARshare/Template.git
> git fetch DStemplate
> git merge --allow-unrelated-histories remotes/DStemplate/master
> ```



### 5. Replace EXP00 with actual experiment setup

```bash
    rm -rf EXP00
    mv $zEXP EXP00
    cp EXP00/README.md .

   #vi README.md

    # Modify as needed

    git add .
    git commit -m "update for export"
```



### 6. clone or create new CONF-CASE Project

-----

![ngit](https://img.shields.io/badge/gitlab%5fversion-%3e10.5-green.svg)

```bash
    GS=git.geomar.de
    GN=NEMO/EXP
    GT=(git@ :)

    git clone ${GT[0]}${GS}${GT[1]}${GN}/${CONFIG}-${zEXP}.git ${DSTMP}/$CONFIG-$zEXP
    [[ ! -d ${DSTMP}/$CONFIG-$zEXP ]] && git init ${DSTMP}/$CONFIG-$zEXP

    git push ${DSTMP}/$CONFIG-$zEXP split:${CURBRANCH}-split
    cd ${DSTMP}/$CONFIG-$zEXP
    git checkout -b $CURBRANCH
    git merge ${CURBRANCH}-split

    git push --set-upstream ${GT[0]}${GS}${GT[1]}${GN}/${CONFIG}-${zEXP}.git $CURBRANCH

    git branch -D ${CURBRANCH}-split
    cd -
    
```

-----

Obsolete:

> 
>
> ![ngit](img/uses-ngit-red.svg)
>
> ```
> GP=$(ngit sp $CONFIG-$EXP 2>/dev/null | sed -n 's/.*git : \(.*\)/\1/p;' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g;s/[\x01-\x1F\x7F]\(B//g")
> # as private project : [[ -z ${GP} ]] && NGITVIS=private ngit cp NEMO/EXP/$CONFIG-$EXP
> # as internal project:
> [[ -z ${GP} ]] && ngit cp NEMO/EXP/$CONFIG-$EXP
>
> GP=$(ngit sp $CONFIG-$EXP 2>/dev/null | sed -n 's/.*git : \(.*\)/\1/p;' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g;s/[\x01-\x1F\x7F]\(B//g")
> if [[ -n ${GP} ]]; then
> 	git clone ${GP} ${DSTMP}/$CONFIG-$EXP
> 	git push ${DSTMP}/$CONFIG-$EXP split:$CURBRANCH
> 	cd ${DSTMP}/$CONFIG-$EXP
> 	git push -u origin $CURBRANCH
> 	
> fi
>                                                
> ```
>



### 7. Clean up

```bash
    cd $OWD
    rm -r $WTSPLIT
    git worktree prune
    git branch -D split

    
done

```


