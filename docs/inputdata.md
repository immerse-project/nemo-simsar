# How to refer to Input Data

Beside the **run-time parameters** (namelists) and the **program code** of the model, the **input data** files are the third essential component for the reproducibility of a simulation.

It is therefore indispensable that the origin and the history of the input data is well documented and that each file can be referenced unequivocally. This can be achieved by:

* **version control**
* a **persistent data handler** per file
* a **check-sum**



## Data Version Control

The simplest way of version-controlling a data file is using a different file name for each version. But this approach may cause trouble and confusion for automation processes (scripts) and users with different file naming conventions. A much more robust though resource-intensive way would be a svn or git-lfs system. 

Whatever system it is, that you prefer, it should sustain an easy and persistent way of accessing the exact data file that is needed for a specific simulation. 



## Persistent Data Handler

Document Object Identifiers (DOI) are used for a long time now and are a very effective way of referencing documents. Something similar can be used for data files as well. You can use either a DOI or any other form of persistent handler.



## Data Files or Data Sets?

It's your choice whether you want to publish each file separately of as a  data set combining the different files. The latter is much easier and less time consuming.



## Example: Publish with GitHub and zenodo

Both GitHub and zenodo provide free service for publicly available data. 

### Alternative 1: one-time upload

Data sets that will not change or will not be further developed, can be simply uploaded to zenodo without a repository link.

???+ example "1. Login to zenodo"
    You can either use your GitHub account, your OrcID or you sign up for a zenodo account. Just visit [zenodo.org/login](https://zenodo.org/login) and follow the instructions there.

??? example "2. Create a new data set"
    Create a new data set using the "New Upload button" on the [Upload](https://zenodo.org/deposit) page (see the top menu of the zenodo page).

??? example "3. Fill in the data set details"

#### 1. Login to zenodo

You can either use your GitHub account, your OrcID or you sign up for a zenodo account. Just visi[t zenodo.org/login](https://zenodo.org/login) and follow the instructions there.

