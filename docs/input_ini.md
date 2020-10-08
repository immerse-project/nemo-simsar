# The `input.ini` File

The `input.ini` file is an additional file that is not part of the original NEMO framework. It lists all the input data files needed for a specific simulation, each with 

* their ***file names*** as expected by NEMO (hard coded or by namelist parameter)
* one or multiple ***remote sources*** (file name may differ from the NEMO name)
* a  ***checksum*** (optional, e.g. SHA256)
* a ***reference***, like a publication or the data file's DOI/POI (optional)

!!! info
    `input.ini` is read by the **mkReadme** python script.

## File Format

The file is a simple ASCII text file (*INI* format) with:

* each section representing one input file
* each section contains at least one key (`URL`):
    1. The section name represents the file name as expected by NEMO (hard coded or set by namelist parameter)
    2. At least one source URL
    3. A checksum 
    4. An indicator for the type of the checksum (sha or md5)
    5. (optional) additional URLs, if available (also comma separated)
* lines that start with a '`#` or `;`' are treated as comments.
* lines might be indented

## Example

See the example/template file `docs/input.ini`:

!!! example "Example `input.inni`"
    ```ini
    # NEMO-simsar input file registry
    #
    # Each NEMO input file has one entry: The SECTION name in square brackets is the 
    # file name NEMO expects (hard coded or by namelist parameter).
    # Each section has several key=value pairs:
    #
    #       [NemoFileName.nc]
    #               URL = https://
    #               Reference = Author, A. (YEAR)
    #               DOI = <doi:reference-id, not the url>
    #               CheckSum = <HASH:sha1|sha224|sha256|sha384|sha512|md5>
    #               CheckSumType = [SHA|MD5| ] 
    #               Comment = Some additional notes or comments on the data set
    #

    [coordinates.nc]
        URL = https://data.myserver.org/ORCA025/coordinates__3.6.0_ORCA025_v1.0.1.nc
        Reference = 
        DOI = 10.5281/zenodo.3767939
        CheckSum = 288b021a8595efeee8de7c4fb665d3037bd356a72ca13e591bb81acc5c3ceeb5
        CheckSumType = sha
        Comment =

    [data_1m_salinity_nomask.nc]
        URL = https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
        Reference = 
        DOI = 10.5281/zenodo.3767939
        CheckSum = b3f60e3507bbea3466834a363f366b45ef8aec19495ae0975ea3dcbbbfc70aa2
        CheckSumType = sha
        Comment =

    ```



