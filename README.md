---
typora-root-url: .
---

# nemo-simsar

Document your NEMO ocean model simulations and share them with others using git remote repositories

This project is part of the EC funded **IMMERSE** project ([immerse-ocean.eu](http://immerse-ocean.eu/))

## 1. Description

Ocean model simulations that are based on the NEMO ocean modelling framework ([nemo-ocean.eu](https://www.nemo-ocean.eu)) consists of several components:

* The source code provided by NEMO and by the user (FORTRAN code)
* Build settings (model components, compiler options)
* Runtime parameters (FORTRAN and XML namelists)
* Input data fIles (e.g. grid, bathymetry, boundary conditions, initialisation)

While the first two components define a certain "**configuration**", the latter two  provide the details for a specific **experiment** with the said configuration. Both together define a **simulation**.

<img src="docs/img/simsar_SimulationPackage.png" alt="simsar_SimulationPackage"  />

The recipes and the tools in this project allows users to create a package containing all the necessary information in order to share it with other users intending to reproduce the simulation or to start from this simulation with their own settings.  See also the documentation in the `doc/` folder for more details.

![simsar_ProcedureOverview](/docs/img/simsar_ProcedureOverview.png)



#### Features

* Interactive script in order to create a README file (Markdown format) giving an overview of the simulation's settings and providing instructions how to include it in your own NEMO framework.
* Recipe to extract and upload a configuration from inside the NEMO framework into a remote git repository

## 2. Requirements

The user has to meet the following pre-requisits before running a tool or following a recipe from this project:

* A working NEMO framework (see [nemo-ocean.eu](https://www.nemo-ocean.eu)) 
* A NEMO configuration + experiment details (=simulation) to share
* A definition list (`input.def`) containing names and remote sources of the citable, version-controlled input data files. See `doc/inputfiles.md` for details
* **git** client is installed and working
* access to a remote **git server**
* **Python3** including these standard libraries: 
  * os
  * re
  * subprocess
  * pathlib
  * textwrap
* The following additional **Python3 packages** must be installed (e.g. with `pip` or `conda` or  through your favorite package manager):
  * svn ([pip](https://pypi.org/project/svn/))
  * wget ([pip](https://pypi.org/project/wget/))
  * GitPython ([pip](https://pypi.org/project/GitPython/))
  * Jinja2 ([pip](https://pypi.org/project/Jinja2/))
  * pycurl ([pip](https://pypi.org/project/pycurl/))
* A local copy of this git project.

#### Terms of Use & License Agreement

Before using this software, the user must agree to the license given by the [LICENSE](LICENSE) file in the project's repository. This software can be used free of charge. 

## 3. Download & Installation

First make sure that the required Python3 packages are installed on your local machine. If you're using **pip** for example, you can run the following command:

```
pip3 install svn wget GitPython Jinja2 pycurl 
```

Then change to the directory where you want to keep your local copy of this project and clone it:

```bash
git clone git@github.com:immerse-project/nemo-simsar.git
```



#### Updates

Go into your local copy of the nemo-simsar repository and run `git fetch` and review any changes before merging manually.

```
git fetch
```

Or, if you're inclined to merge any changes immediately into your local repository, just run a `git pull`:

```
git pull
```





## 4. Usage

*`Short notes on how to start/use the program and the command syntax (if necessary)`*

The most important tool is the **mkReadme** script. Make sure, the full path to `nemo-simsar/bin` is part of your `$PATH` environment variable:

```bash
# Bash-like:
export PATH=/path/to/nemo-simsar/bin:${PATH}

# or csh:
setenv PATH /path/to/nemo-simsar/bin:${PATH}
```

Before you can run the mkReadme tool, make sure, that the following information is available:

> * The **NEMO code repository**, **branch identifier** and **revision number** the simulation's code is based on
> * An `input.def` file listing file names of the input files used by NEMO and their remote sources as well as references (see the **`input.def` template** in the `doc/` folder)
> * 

Then go into your configuration's folder and run `mkReadme`

```bash
mkReadme
```

***NOTE***: If the `nemo-simsar/bin` is not part of your `$PATH` variable, run the script using the full path, something like:

```
/home/myname/nemo-simsar/bin/mkReadme
```

The script does not accept any arguments yet (May change in the future).

#### Example

*`Provide one ore more examples`*

```bash
# Example 1:

cd $HOME/NEMO/release-4.0/cfg/CrazyWhirl
mkReadme

```



#### Testing

Currently, there is no testing implemented.



## 5. Documentation

See the files in the `doc/` sub-folder of this project.



## 6. Support

There is only a limited support during the introduction phase of this package. Please, use the issue reporting on GitHub.



