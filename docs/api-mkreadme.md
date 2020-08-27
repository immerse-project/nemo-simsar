# `mkReadme`

::: mk_readme.clsmkReadme.MakeReadme
    handler: python
    rendering:
      show_root_heading: false
      show_source: true

      
: : : my_package.my_module.MyClass
    handler: python
    selection:
      members:
        - method_a
        - method_b
    rendering:
      show_root_heading: false
      show_source: false

: : : my_package.my_module.MyClass
    handler: python
    rendering:
      show_root_heading: false
      show_source: false

: : : MY_PACKAGE.your_module
    handler: python
    rendering:
      show_root_heading: false
      show_source: false
