# input.def

The `input.def` file is an additional file that is not part of the original NEMO framework. It lists all the input data files needed for a specific simulation, each with 

* their file names as expected by NEMO (hard coded or by namelist parameter)
* one or multiple remote sources (file name may differ from the NEMO name)
* a SHA256 checksum (optional)
* a reference, like a publication or the data file's DOI/POI (optional)

The format of the file is simple: 

* One record (line) per file
* A record may consist of multiple continuing lines (use `\` and a line break at the end of a line to continue in the next line instead of a simple line break)
* Lines that start with a '`#`' are completely treated as comments (may be preceded with blanks; continuing lines ('\\') must start with a hash character as well)
* Each record consists of three or more comma separated columns:
  1. The file name as expected by NEMO
  2. A SHA256 checksum (preceded with '`sha256=`') and/or a Reference Text
  3. at least one source URL
  4. (optional) additional URLs, if available (also comma separated)

See the example/template file `docs/input.def`:

```
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

