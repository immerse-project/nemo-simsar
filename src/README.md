# SIMSAR Package
This project is part of the IMMERSE Project funded by the EC.

*Document your NEMO ocean model simulations and share them with others using git remote repositories.* 
____

## Purpose

This software is intended for NEMO framework with a NEMO simulation to share. 

SIMSAR Package is an interactive script to create a README file (Markdown format) to give an overview of the simulation's settings and providing instructions on how to include it in your own NEMO framework.

More information available at : [https://immerse-ocean.eu/nemo-simsar/](https://immerse-ocean.eu/nemo-simsar/)


## Terms of Use

**By downloading this package and using the code you agree to the following conditions.**

The code in this project is based on the [NEMO](http://www.nemo-ocean.eu) software (Copyright (c) Centre National de la Recherche Scientifique CNRS).

The original code as well as the contribution to this code in this project are licensed under the conditions of [CeCILL](http://www.cecill.info). 

The person stated under '*Contact*' above is the owner of the intellectual property rights of these contributions and **must be informed afore** publishing and **must be cited** in every published work that is based completely or partially on the modifications and additional code provided by this configuration.

Usage is at one's own risk. 

## Installing

*Since this version is still in its testing phase, this package is published on [test.pypi.org](https://test.pypi.org/). When this package is finalised it will be published on [pypi.org](pypi.org) *


```
pip install -i https://test.pypi.org/simple/ tsimsar
```

## Requirements

Assuming you're working on a *nix like system you have to meet the following pre-requisits before running a tool or following a recipe from this project:

- A working **NEMO framework** (see [nemo-ocean.eu](nemo-ocean.eu){: target=_blank})

- A **NEMO** simulation to share (=configuration + experiment details)

- **git** client is installed and working

- access to a remote **git server**

- Python3 including these standard libraries: `os`, `re`, `subprocess`, `pathlib`, `textwrap`

- The following additional **Python3 packages** must be installed (e.g. with `pip` or `conda` or through your favorite package manager):

    - [svn](https://pypi.org/project/svn/) (pypi{: target=_blank} | [anaconda:main](https://anaconda.org/main/svn){: target=_blank})
    - [wget](https://pypi.org/project/wget/) (pypi{: target=_blank}| [anaconda:main](https://anaconda.org/main/wget){: target=_blank})
    - [GitPython](https://pypi.org/project/GitPython/) (pypi{: target=_blank} | [anaconda:main](https://anaconda.org/main/gitpython){: target=_blank})
    - [Jinja2](https://pypi.org/project/Jinja2/) (pypi{: target=_blank} | [anaconda:main](https://anaconda.org/main/jinja2){: target=_blank})
    - [pycurl](https://pypi.org/project/pycurl/) (pypi{: target=_blank} | [anaconda:main](https://anaconda.org/main/pycurl){: target=_blank})
    - [netcdf4](https://pypi.org/project/netCDF4/)(pypi{: target=_blank} | [anaconda:main](https://anaconda.org/main/netcdf4){: target=_blank})

!!! example "EXAMPLE: Install required Python3 packages"

```
  === "pip"

      pip3 install svn wget GitPython Jinja2 pycurl netCDF4
      
  === "conda"
      Using the [conda-forge channel](https://conda-forge.org/):
      
      conda install --channel conda-forge python=3 svn wget gitpython jinja2 pycurl netcdf4
```

## Usage

>**Important**

>The script should be called within a configuration, e.g. AMM12, ORCA_ICE etc..
>The configuration should also include input.ini


To import and call the package:
```
PYTHON

import tsimsar
tsimsar.make_readme()
```

After importing the SIMSAR Package, please read the [User Guide](https://immerse-ocean.eu/nemo-simsar/introduction.html) for further instructions how to use SIMSAR since it does not only consist of one single program but is a collection of recipes with a few tools to assist the user. The [Introduction](https://immerse-ocean.eu/nemo-simsar/introduction.html) tells you about the background and how to use SIMSAR. The [Getting Started](https://immerse-ocean.eu/nemo-simsar/gettingstarted.html) section provides step-by-step instructions.

## Contributing

Please use the collaboration tools provided for the GitHub project [IMMERSE-project/nemo-simsar](https://github.com/immerse-project/nemo-simsar).

## Versioning

V4

## Authors

[Markus Scheinert](mscheinert@geomar.de)
[Lucienne Micallef](lmicallef@geomar.de)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details