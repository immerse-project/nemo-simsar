# Bundle up

Everything is ready to bundle up? Here is a short checklist:

!!! warning ""
    * [x] Your **experiment folder** is complete, clean and ready.
    * [x] **README.md** is ready in the experiment folder.
    * [x] **input.ini** is present and lists all necessary files.
    * [x] Local **git client** is installed (`git --version`)
    * [ ] You have access to a git remote server (maybe also to some group namespace)
    * [ ] ...

The next step depends on whether your local NEMO worktree/repository is already under git control or not, though it might be under subversion control :

<center>[(A) NEMO tree NOT under git control](#a-nemo-tree-not-under-git-control){: .md-button .md-button--primary }</center>



<center>or (Not ready yet!)<br>[(B) NEMO tree already under git control](#){: .md-button .md-button--primary }</center>

------



## (A) NEMO Tree **NOT** under git control

You are lucky! This is as easy as putting any existing directory under git control and pushing it to some remote repository.

**Global shell variables **

Examples below may use some shell variables. These variables are:

!!! help ""
    `$WORK`: Shell variable which holds the path to some scratch disk, where NEMO was checked out.

### (1) Initialize git

First, you have to put your configuration's folder (one level deeper than `CONFIG`/ or `cfgs/`). Let's assume we have a Configuration named "ORCA2_ICE"  we are going to share in the example below:

```bash
cd $WORK/NEMO/release-4.0/cfgs/ORCA2_ICE/
git init
```

Now, you'll find a new (hidden) golder, called `.git` in the configuration's folder.

### (2) Branching Off

The deafult branch name will be ***master***. If you want to use branches that explicitly matches the NEMO branches, you could create a new branch using the `-b` argument with the **`git checkout`** command:

```bash
git checkout -b release-4.0
```



### (3) Ignore Patterns

Surely, there are files you won't submit to a public repository, like backup files or snippets. You can use file name patterns in the `.gitignore` file to exclude them from beeing tracked. Just open an ASCII editor, e.g. *vi* and add your patterns (If you start  an entry with `**/` the pattern will work recursively). Patterns you'll need to exclude anyway, are:

* `BLD/`
* `WORK/`

The `.gitignore` file is stored in the root folder of the git repository, hence:

```bash
vi $WORK/NEMO/release-4.0/cfgs/ORCA2_ICE/.gitignore
```

-----

**EXAMPLE:**

In the example below, the *BLD/*, *WORK/* and *EXP00/* folders are going to be ignored while all files with suffixes *\*.bak*, *\*.tar* or *\*.swp* are excluded, too.

!!! tldr ".gitignore"
	```
	BLD
	WORK
	EXP00
	**/*.bak
	**/*.tar
	**/*.swp
	```

-----

After saving this file, the ignore patterns are immediately effective. **Don't forget** to add it to the commit stage:

```bash
git add .gitignore
```



### (4) README

#### Option-a: Single Experiment

If your' going to submit only one experiment folder, just copy the README.md file from your experiment into the configuration's folder before submitting. In the example below, the only experiment will be "REF":

```bash
# still in $WORK/NEMO/release-4.0/cfgs/ORCA2_ICE/
cp REF/README.md README.md
```



#### Option-b: Multiple Experiments

In the case you want to publish multiple experiments with your SImulation Package:

1. Make sure you have a **README for each experiment**
2. **Copy one of the README files into the configuration's folder** as you would for only one experiment 
3. **Modify the title** in the README
4. Add a list of your experiments** linked with each specific README.md file
5. Modify the **text of the purpose** accordingly

```bash
# still in $WORK/NEMO/release-4.0/cfgs/ORCA2_ICE/
cp REF/README.md README.md
vi README
```
!!! tldr "Example README.md for Simulation Package with multiple experiments"
    === "Original"

        ``` md
        # ORCA2_ICE-REF
        ___
    
        [Purpose](#purpose)  |  [Contact](#contact)  |  [License](#license)  |  [Configuration](#configuration) | [Input Files](#input-files)  |  [Diagnostics](#diagnostics)  | [Installation](#installation)
    
        ____
    
        ## Purpose
        
        Reference experiment with ORCA2 and Sea Ice
        ```
    
    === "Modified"
    
        ``` md
        # ORCA2_ICE-*
        ___
    
        [Experiments](#experiments) |  [Purpose](#purpose)  |  [Contact](#contact)  |  [License](#license)  |  [Configuration](#configuration) | [Input Files](#input-files)  |  [Diagnostics](#diagnostics)  | [Installation](#installation)
    
        ____
    
        ## Experiments
    
        * [REF](REF/README.md)
        * [SENS1](SENS1/README.md)
        * [SENS2](SENS2/README.md)
    
        ## Purpose
    	Series of simple experiments with ORCA2 and Sea Ice.
    	
        ```



### (5) Add Files

Now is the time, to add some files and folders to track them with git (= files and folders which are going to be submitted to the remote repository). Please, consider adding those files **separately** using **`git add <file/folder>`** instead of using the bunch command `git add .` (adding a folder however will add it recursively). 

For example , `REF/` is the experiment we want to share:

```bash
git add README.md
git add MY_SRC
git add REF
git add cpp_ORCA2_ICE.fcm
```



### (6) Commit

You can check which files will be tracked with **`git status`**:

```bash
git status
```

If you're happy with the result, commit them, e.g.:

```bash
git commit -m "Initial commit for experiment ORCA2_ICE-REF"
```

If you omit the *-m* option, the default editor will open and you'll have to type your commit message therein. After saving the temporary MESSAGE file and closing the editor git will proceed with finalizing the commit.

### (7) Push to remote

This step is part of the **publishing process**. Please follow the link or click on the buttons below:

<center>[Publish: General Remarks](publish_general.html){: .md-button .md-button--primary }</center>

<center>[Publish with GIT](publish_git.html){: .md-button .md-button--primary }</center>



-----

## (B) NEMO tree already under git control

Not ready yet. Coming soon...
