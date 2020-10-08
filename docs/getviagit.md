# Get Simulation Package via GIT

Getting a Simulation Package with git is as easy as pushing it to a remote git server, in particular if your NEMO root installation is under Subversion (no interference between svn and git).

## (A) NEMO root **NOT** under git control

If your NEMO installation **is not under git control**, you can clone a configuration using the URL specified on the repository's web page:

Go into the **configurations directory** in your local NEMO installation (`CONFIG/` for NEMO version 3, `cfgs/` for version 4) and clone this project (see the "Clone" link or button on the git webinterface to get the URL).



-----

**EXAMPLE:** 

In this example, NEMO (version 4) has been installed on a separate scratch-disk (`$WORK`) and the simulation repository was hosted on github under the namespace "mscheinert":

```
cd $WORK/NEMO-release-4.0/cfgs
git clone https://github.com/mscheinert/ORCA2_ICE.git
cat ORCA2_ICE/exp_cfg.txt >> ./work_cfgs.txt
```

Instead of the default branch you can also specify it when cloning (e.g. `release-4.0` if it exists):

```
git clone -b release-4.0 https://github.com/mscheinert/ORCA2_ICE.git
```

This wil create a new configuration folder, which can be used as a reference case for **makenemo -r**. Make sure, you add this configuration to the local registry file `cfg.txt` (NEMO version 3) or `work_cfgs.txt` (NEMO version 4) before invoking **makenemo**.

-----



!!! warning "Name Collision"
	In the case you have already a configuration with the **same name**, you can specify a new name for the clone you are pulling from remote. Just add another argument with the new name:

    ```
    git clone -b release-4.0 https://github.com/mscheinert/ORCA2_ICE.git ORCA2_ICE__release4
    ```





## (B) NEMOGCM already under git control

If your **NEMOGCM installation is already under git control** you cannot clone a different repository into the existing working copy. Instead, you can use **git subtree** to inject files from another remote repository into a particular sub-folder of your existing working tree.

Within NEMO root directory:

```
cd $WORK/NEMO-release-4.0
git remote add -f remote_ORCA2_ICE-mscheinert https://github.com/mscheinert/ORCA2_ICE.git   # add remote
git subtree add --prefix cfgs/ORCA2_ICE remote_ORCA2_ICE-scheinert release-4.0 --squash     # donwload master branch into sub-folder
cat cfgs/ORCA2_ICE/exp_cfg.txt >> cfgs/work_cfgs.txt
```

> In this case, you keep the information from where you have downloaded the reference configuration (see `git remote -v`).

Or even shorter, without keeping remote source information (not recommended):

```
cd $WORK/NEMO-release-4.0
git subtree add --prefix cfgs/ORCA2_ICE-REF git@github.com:immerse-project/ORCA2_ICE-REF.git release-4.0 --squash
cat cfgs/ORCA2_ICE-REF/exp_cfg.txt >> cfgs/work_cfgs.txt
```

#### Other revisions

The revision that will be installed, is the most recent one from the **master** branch. If you're seeking another branch/revision of this configuration (e.g. an older one), you can browse available branches/tags via the web-interface or list alternative branches on the command line and swap available branches/tags easily with `checkout`:

```
cd ORCA2_ICE-REF
git branches -r
git checkout otherBranch
```

Note: *origin/HEAD* in the output listing is not a branch in its own but points to the default branch (master branch in most cases).