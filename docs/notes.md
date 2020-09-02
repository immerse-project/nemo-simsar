# Hidden Notes

!!! note

!!! warning

!!! info

!!! success

!!! question
    * Which license?
    * test github pages under immerse?

!!! fail

!!! danger

!!! bug

:fontawesome-solid-external-link-alt:

:smile:

* :material-account-circle: – `.icons/material/account-circle.svg`
* :fontawesome-regular-laugh-wink: – `.icons/fontawesome/regular/laugh-wink.svg`
* :octicons-octoface-16: – `.icons/octicons/octoface-16.svg`




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


:octicons-mark-github-16:
    
=== "GitHub"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "GitLab"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```
    
=== "other"
    Some other Git Host.
