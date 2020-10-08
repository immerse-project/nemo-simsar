# Example Nemo session

During this session we will create a new configuration **ORCA2-ICE** which will be then published/shared in a (private) git repository with nemo-simsar.

## (1) Install NEMO

This step installs NEMO from scratch and creates the new configuration if both do not exist yet.

### + Clone / Checkout NEMO repo

If you're going to run your experiments within the NEMO repository tree, make sure, you're not working within your `$HOME` directory. You may want to use a 'scratch disk' instead (e.g. `$WORK`) which can also store large input and output files.

```bash
cd $WORK
svn co https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/releases/release-4.0 NEMO-release-4.0
```

### + New ARCH

For simplicity we us a new ARCH file which would run the model in a serial mode (instead of a parallel mode):

**`arch-linux_gfortran_serial.fcm`:**

```
%NCDF_HOME           /usr
%HDF5_HOME           /usr
%XIOS_HOME           
%OASIS_HOME          

%NCDF_INC            -I%NCDF_HOME/include -I%HDF5_HOME/include/hdf5/serial
%NCDF_LIB            -L%NCDF_HOME/lib/x86_64-linux-gnu -lnetcdff -lnetcdf
%XIOS_INC            
%XIOS_LIB            

%OASIS_INC           
%OASIS_LIB           

%CPP                 cpp -Dkey_nosignedzero 
%FC                  /usr/bin/gfortran -c -cpp 
%FCFLAGS             -fdefault-real-8 -O3 -funroll-all-loops -fcray-pointer -ffree-line-length-none
%FFLAGS              %FCFLAGS
#%LD                  /usr/bin/gfortran -Wl,-rpath=$HOME/INSTALL/lib:/usr/lib
%LD                  /usr/bin/gfortran
%LDFLAGS             
%FPPFLAGS            -P -C -traditional
%AR                  ar
%ARFLAGS             rs
%MK                  make
%USER_INC            %XIOS_INC %OASIS_INC %NCDF_INC
%USER_LIB            %XIOS_LIB %OASIS_LIB %NCDF_LIB

%CC                  cc
%CFLAGS              -O0
```

### + Create new ORCA2_ICE configuration

The next commands will create the new configuration "ORCA2_ICE" based on the existing reference configuration ORCA2_ICE_PISCES" (which originally also uses the NST component). The model components are reduced to OCE and ICE and all CPP keys that'd require MPI (parallel computing) are removed, too.

```bash
cd NEMO-release-4.0
./makenemo -m linux_gfortran_serial -r ORCA2_ICE_PISCES -n ORCA2_ICE -j 0
./makenemo -m linux_gfortran_serial -r ORCA2_ICE -j 0 -d OCE,ICE
./makenemo -m linux_gfortran_serial -r ORCA2_ICE -j 0 del_key 'key_top key_iomput key_mpp_mpi'
```

Now, there is also a new file `cfgs/work_cfgs.txt` listing the user configurations and their model components:

```
ORCA2_ICE  OCE TOP ICE NST
```

and the cpp file `cpp_ORCA2_ICE.fcm` only contains now the macro key for the sea ice model:

```
bld::tool::fppkeys   key_si3
```

### + MY_SRC

We will just copy a file from the original source tree in order to simulate the existence of a user-modified file in `MY_SRC/`:

```
cd cfgs/ORCA2_ICE/MY_SRC
cp src/OCE/SBC/sbcblk.F90 cfgs/ORCA2_ICE/MY_SRC/.
```

### + COMPILATION

Still in `NEMO-release-4.0/` folder:

```
./makenemo -m linux_gfortran_serial -r ORCA2_ICE
```

### + Experiment REF

```
cp -R EXP00 REF
```



## (2) Install nemo-simsar

```
cd $HOME
git clone https://
export PATH=$HOME/nemo-simsar/bin:$PATH
```



## (3) Prepare Software Package

### + List input files in `input.def`

```
cd $WORK/NEMO-release-4.0/cfgs/ORCA2_ICE/RE
vi input.def
```

**`REF/input.def`:**

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

ORCA_R2_zps_domcfg.nc, \
                       SHA256=736500c34b2f5959070d961ca64a0649895cfa27101368eff90edb7f90c5097f\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
data_1m_salinity_nomask.nc, \
                       SHA256=b3f60e3507bbea3466834a363f366b45ef8aec19495ae0975ea3dcbbbfc70aa2\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
geothermal_heating.nc, \
                       SHA256=a72baf9af15e53bce87a53148ed8fddf8d9948449f5c04da5d84526edf39ccc3\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
eddy_viscosity_3D.nc, \
                       SHA256=a3083b470710a32bb83678632904f3b3d09f96d47110440dfac7d6ddc978c269\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
mixing_power_pyc.nc, \
                       SHA256=4c1d530408921c6418e91a0c4f2451420407e0a3ac9176d7cf2125b417f1233f\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
mixing_power_cri.nc, \
                       SHA256=13d3c239277f39a7bf2f082deb4b5507b467c03120ceed15e6e79fc2e2c2d84b\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
mixing_power_bot.nc, \
                       SHA256=c2485f028fe8d7978d924737d2c2eb2f61cb780ab906ac8ceecd18e8b6e9b343\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
runoff_core_monthly.nc, \
                       SHA256=e5f3b92205561d78731b9253caf302ddf82d98cd3eabe46ab0cf152be6d74ffb\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
resto.nc, \
                       SHA256=b3ac69284d46276497928a55a69c167cdb579443f85383186c442c4e235ee032\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
data_1m_potential_temperature_nomask.nc, \
                       SHA256=302179020c3c8c1ca02d8f749206f13eca522a9de8704a1a148f5e1eddcc70b8\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
u_10.15JUNE2009_fill.nc, \
                       SHA256=a226c422488b78fdcccb31c64219787510cb383dc9bd9f27a3fef3cc2052a171\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
weights_core_orca2_bicubic_noc.nc, \
                       SHA256=9bbdbbdf773307e08b7372712123a2cefdd9f2ea1928d61aae3f27a10cb065b2\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
weights_core_orca2_bilinear_noc.nc, \
                       SHA256=20c7e0af58792b9401b9a47dc5f3c9a5726f44d0454f2d6fe01ccaa5e3af725e\
                       DOI=10.5281/zenodo.3767939 \
                       https://doi.org/10.5281/zenodo.3767939, \
                       https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
v_10.15JUNE2009_fill.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
t_10.15JUNE2009_fill.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
q_10.15JUNE2009_fill.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
ncar_rad.15JUNE2009_fill.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
ncar_precip.15JUNE2009_fill.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
slp.15JUNE2009_fill.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
sss_data.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
chlorophyll.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
decay_scale_cri.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1
decay_scale_bot.nc, , https://zenodo.org/record/3767939/files/ORCA2_ICE_v4.2.tar?download=1

```

