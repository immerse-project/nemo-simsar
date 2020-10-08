# How to refer to Input Data

Beside the **run-time parameters** (namelists) and the **program code** of the model, the **input data** files are the third essential component for the reproducibility of a simulation.

It is therefore indispensable that the origin and the history of the input data is well documented and that each file can be referenced unequivocally. This can be achieved by:

* **version control**
* a **persistent data handler** per file
* a **check-sum**



## Data Version Control

The simplest way of version-controlling a data file is using a different file name for each version. But this approach may cause trouble and confusion for automation processes (scripts) and users with different file naming conventions. A much more robust, though resource-intensive way would be a *svn* or *git-lfs* system. 

Whatever system it is, that you prefer, it should sustain an easy and persistent way of accessing the exact data file that is needed for a specific simulation. 



## Persistent Data Handler

Document Object Identifiers (DOI) are used for a long time now and are a very effective way of referencing documents. Something similar can be used for data files as well. You can use either a DOI or any other form of persistent handler.



## Data Files or Data Sets?

It's your choice whether you want to publish each file separately or as a  data set combining the different files. The latter is much easier and less time consuming. But the former can be used in a more flexible way such as re-using it for different experiments without dealing with unnecessary files in the same collection.



## Example: Publish with GitHub and zenodo

Both GitHub and zenodo provide free service for publicly available data. Furthermore, they can be combined.

### Alternative 1: one-time upload

Data sets that will not change or will not be further developed, can be simply uploaded to zenodo without a repository link.

???+ example "Step 1: Login to zenodo"
    You can either use your GitHub account, your OrcID or you sign up for a zenodo account. Just visit [zenodo.org/login](https://zenodo.org/login) and follow the instructions there.

??? example "Step 2: Create a new data set"
    Create a new data set using the "New Upload button" on the [Upload](https://zenodo.org/deposit) page (see the top menu of the zenodo page).

??? example "Step 3: Fill in the data set details"
    ...

### Alternative 2: version controlled repository

If you want to document the development of a data file or provide additional files, like a script for creation or testing, upload your files to a git repository first, then create a fixed tag for a certain revision (release) and then upload and link this version at zenodo:

???+ example "Step 1:New Git-LFS project on github"
    go to github.org and create a new data project, e.g. with the following sub-folders:
    

    * **data/**
    * **docs/**
    * **util/**
    
    Don't forget adding a README(.md,.rst,.txt) and a LICENSE file.

??? example "Step 2: git-lfs"
    Clone the git project onto your local host, enable git-lfs by adding a filter (don't forget to run git-lfs install on this host once), add the files, commit and push to the remote repo. For example:
    
    ``` bash
    git clone https://github.org/namespace/data-project.git
    cd data-project
    mkdir data docs util
    git-lfs install        # only once on a host
    git lfs track "*.nc"   # e.g. for NetCDF files
    git add .gitattributes
    cp /path/to/data/data.nc data/.
    git add data/data.nc
    git commit -m "adding data.nc"
    git push origin master
    ```
    
???+ example "Step 3: Login to zenodo"
    You can either use your GitHub account, your OrcID or you sign up for a zenodo account. Just visit [zenodo.org/login](https://zenodo.org/login) and follow the instructions there.

??? example "Step 4: Create a new data set"
    Create a new data set using the "New Upload button" on the [Upload](https://zenodo.org/deposit) page (see the top menu of the zenodo page).

??? example "Step 5: Fill in the data set details"
    ...

