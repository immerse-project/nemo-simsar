# Getting Started

!!! note
    The working environment structure can differ significantly between different users. Hence there is no "one-click & go" solution for publishing a simulation package. SIMSAR follows rather a "recipe" guided approach and provides the user with batch scripts or other tools where feasible.

Assuming the path to your copy of the NEMO repository is `NEMO/release-4.0` in your `$HOME` directory, let's go into the respective experiment folder of the simulation you want to publish (e.g. experiment `MyExp1` under configuration `My_Config`):

```bash
cd ~/NEMO/release-4.0/cfgs/My_Config/MyEXP1
```

From this directory go through the steps below:

## Step-1: List input data files
First, we need a list of the **required input data files** for your simulation together with some detailed meta-data, like sources, references and check-sums. SIMSAR expects this list in a special file, the **`input.def`** file. If this file does not exists yet, please create it. You'll find more information about the file format and how to create it in the "**Citable Input Data**" section of this guide. Just click on these buttons for further details:

* [How to refer to Input Data](){: .md-button}
* [The "input.def" file](){: .md-button  .md-button--primary}

!!! Success "Check"
    Now you should have an `input.def` file in your experiment folder that looks similar to the example below. 
    ```ini
    #--------------------------------------------------------------------------------------
    # NEMO Input File Definition
    #
    # <NEMO-FileName>, <'DOI|Reference SHA256=xxxx...'>, <URI>[,<URI>[,...]]
    #
    #    Each 'Reference' can also contain a SHA256-hash for verifying the file. This entry
    #    is separated with spaces and has the preceding key-word SHA256= without any blanks
    #
    #    You can use hash character (#) to comment the rest of the line out
    #    Long lines can be split by backslashes (\); trailing comments (#) are allowed.
    #
    #--------------------------------------------------------------------------------------
    # <NEMO-FileName>,  <'DOI|Reference SHA256=xxxx...'>,  <URI>[,<URI>[,...]]

    coordinates.nc,                SHA256=288b021a8595efeee8de7c4fb665d3037bd356a72ca13e591bb81acc5c3ceeb5 ,\
                                   https://data.myserver.org/ORCA025/coordinates__3.6.0_ORCA025_v1.0.1.nc
    
    reshape_jra55_orca025_bilin.nc, SHA256=645de13bb1cbe652c1c2fa3913523d42adf4ec04fd3f55f20766a43abbd00e50 ,\
                                    git@git.myserver.org:ORCA025/reshape_jra.git/reshape_jra_bilin__v1.0.1.nc
    
    reshape_jra55_orca025_bicub.nc, SHA256=91edfbc233a48d6aaa266d7aca71665f420da9957d3d124e9864e91e0012e10f ,\
                                    git@git.myserver.org:ORCA025/reshape_jra.git/reshape_jra_bicub__v1.0.1.nc
    ```

!!! Danger "Important"
	Make sure, that the sources in this list (the URLs) are publicly accessible (or grant permissions respectively).





## Step-2: Create a Simulation Package

A Simulation Package consists of 

* the **code** (reference to the NEMO revision + the user code modifications), 
* the **build settings** and 
* the **runtime environment** (namelists + input files). 

The package can be optionally extended with output data or figures for evaluation (or a reference to them) and testing/analysis routines.

<!--//<img src="img/simsar_SimulationPackage.png" alt="simsar_SimulationPackage" style="zoom:67%;" />//-->

In order to create the simulation package, you'll need to go through these three sub-steps:

1. *Get some of the meta-information ready that we cannot detect automatically*  
   [Preparation](){: .md-button  .md-button--primary style="margin:10px;" }  


2. *Create a README file that summarizes the characteristics of the simulation (involves automatic detection as well as an interactive user dialog)*  
   [Create a README (mkReadme)](){: .md-button  .md-button--primary style="margin:10px;" }  


3. *Create a separate local git repository containing a clean copy of the relevant files for the simulation package that can be easily reviewed before submission to a remote respoitory*  
   [Bundle up](){: .md-button  .md-button--primary style="margin:10px;" }








!!! Success "Check"
    Now you should have a clean simulation repository in a separate directory looking similar to this:

    ```bash
    tree /tmp/My_Config-MyExp1
    
    /tmp/My_Config-MyExp1/
      |-MY_SRC/
        |-sbcblk.F90
      |-MyExp1/
          |-iodef.xml
          |-input.def
          |-namelist_cfg
          |-namelist_ice_cfg
          |-namelist_ice_ref
          |-namelist_ref
      |-cpp_MyConfig.fcm
      |-README.md
      |-ref_cfgs.input
    ```



## Step-3: Publish
### Via Git

Allows others to contribute to the development of a simulation (if desired).

- [publish via git](){: .md-button  .md-button--primary}

!!! tip
    Maybe you want to indicate a persistent handler (e.g. DOI) in the README file. In this case, try to get a preliminary identifier from the service provider, modify the README accordingly, then commit to the remote repository and finally register this commit with the handler provider.

### + Add Static Webpage (optional)

Can be also used with the "unsupported configuration" switch `makenemo -u` to import this simulation into NEMO.

* [add static webpage](){: .md-button .md-button--primary}



### + Persistent Handler (optional)

If the simulation you've just published is used for some (printed) publication or if you want colleagues to be able to cite your simulation correctly (e.g. because they are using the model output from your run), you should link the repository (and/or the static pages) to some kind of persistant handler, like a DOI. 

* [Get a DOI](){: .md-button .md-button--primary }