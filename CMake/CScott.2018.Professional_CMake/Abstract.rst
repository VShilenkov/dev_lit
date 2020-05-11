.. include:: ../../docs/include/cmake.roles.txt

#########################################################
[Craig Scott](2018) Professional CMake: A Practical Guide
#########################################################

.. contents:: Table of Contents
    :backlinks: top

************************
15.Language Requirements
************************

15.1. Setting The Language Standard Directly
============================================

Target properties:

- :cmake:prop_tgt:`CXX_STANDARD`
    - inits with variable :cmake:variable:`CMAKE_CXX_STANDARD`
- :cmake:prop_tgt:`C_STANDARD`
    - inits with variable :cmake:variable:`CMAKE_C_STANDARD`
- :cmake:prop_tgt:`CUDA_STANDARD`
    - init with variable :cmake:variable:`CMAKE_CUDA_STANDARD`


.. code-block:: cmake
    :linenos:
    :caption: Setting standard for target
    :name: code_15_1_listing_0

    # target properties

    set_property(TARGET c_tgt
        PROPERTY
            # C_STANDARD: 90, 99, 11
            C_STANDARD          11
            # C_STANDARD_REQUIRED: On/Off
            # Default: Off
            C_STANDARD_REQUIRED On
            # C_EXTENSIONS: On/Off
            # Default: On
            C_EXTENSIONS        Off
    )

    set_property(TARGET cxx_tgt
        PROPERTY
            # CXX_STANDARD: 98, 11, 14, 17, 20
            CXX_STANDARD 11
            # CXX_STANDARD_REQUIRED: On/Off
            # Default: Off
            CXX_STANDARD_REQUIRED On
            # CXX_EXTENSIONS: On/Off
            # Default: On
            CXX_EXTENSIONS        Off
    )

- :inline_cmake:`<LANG>_STANDARD_REQUIRED` is :inline_cmake:`Off` dy default
- :inline_cmake:`<LANG>_EXTENSIONS` may be ignored if
  :inline_cmake:`<LANG>_STANDARD` is not set
- :inline_cmake:`<LANG>_STANDARD` specifies a minimum standard, not necessarily
  an exact requirement (higher version may be chosen)
- Properties cannot be :inline_cmake:`INTERFACE`

.. important::
    Projects should set all three properties/variables rather than just some of them

.. code-block:: cmake
    :linenos:
    :caption: Setting standard for all the targets
    :name: code_15_1_listing_1

    # Require C++11 and disable extensions for all targets
    set(CMAKE_CXX_STANDARD          11)
    set(CMAKE_CXX_STANDARD_REQUIRED On)
    set(CMAKE_CXX_EXTENSIONS        Off)


15.2. Setting The Language Standard By Feature Requirements
===========================================================

:cmake:manual:`cmake-compile-features.7`

- :cmake:prop_tgt:`COMPILE_FEATURES`
- :cmake:prop_tgt:`INTERFACE_COMPILE_FEATURES`
- :cmake:command:`target_compile_features`
- Each feature must be one of the features supported by the underlying compiler
    - :cmake:prop_gbl:`CMAKE_C_KNOWN_FEATURES`
    - :cmake:prop_gbl:`CMAKE_CXX_KNOWN_FEATURES`
    - :cmake:prop_gbl:`CMAKE_CUDA_KNOWN_FEATURES`
    - :cmake:variable:`CMAKE_C_COMPILE_FEATURES`
    - :cmake:variable:`CMAKE_CXX_COMPILE_FEATURES`
    - :cmake:variable:`CMAKE_CUDA_COMPILE_FEATURES`
- meta-features: :inline_cmake:`<lang>_std_<value>`
    - :inline_cmake:`cxx_std_98`
    - :inline_cmake:`cxx_std_11`
    - :inline_cmake:`cxx_std_14`
    - :inline_cmake:`cxx_std_17`
    - :inline_cmake:`cxx_std_20`
    - :inline_cmake:`c_std_90`
    - :inline_cmake:`c_std_99`
    - :inline_cmake:`c_std_11`
- In situations where a target has both its :inline_cmake:`<LANG>_STANDARD`
  property set and compile features specified, CMake will enforce the stronger
  standard requirement.

15.2.1. Detection And Use Of Optional Language Features
-------------------------------------------------------

- :cmake:manual:`cmake-generator-expressions.7` -
  :inline_cmake:`$<COMPILE_FEATURES:features>`

.. code-block:: cmake
    :linenos:
    :caption: Provide override keyword support for library
    :name: code_15_2_1_listing_0

    add_library(foo ...)
    # Make override a feature requirement only if available
    target_compile_features(foo
        PUBLIC
            $<$<COMPILE_FEATURES:cxx_override>:cxx_override>
    )

    # Define the foo_OVERRIDE symbol so it provides the
    # override keyword if available or empty otherwise
    target_compile_definitions(foo
        PUBLIC
            $<$<COMPILE_FEATURES:cxx_override>:-Dfoo_OVERRIDE=override>
            $<$<NOT:$<COMPILE_FEATURES:cxx_override>>:-Dfoo_OVERRIDE>
    )

.. code-block:: c++
    :linenos:
    :caption: Usage example
    :name: code_15_2_1_listing_1

    class MyClass : public Base
    {
    public:
        void func() foo_OVERRIDE;
    };

- :cmake:module:`WriteCompilerDetectionHeader`
    - :inline_cmake:`write_compiler_detection_header()`

15.3. Recommended Practices
===========================

- Do not set compiler and linker flags directly
- Set standard
    - for overall project with variables
        - :inline_cmake:`CMAKE_<LANG>_STANDARD`
        - :inline_cmake:`CMAKE_<LANG>_STANDARD_REQUIRED`
        - :inline_cmake:`CMAKE_<LANG>_EXTENSIONS`
            - set them after the first :cmake:command:`project`
            - set them all together
            - omitting :inline_cmake:`CMAKE_<LANG>_STANDARD_REQUIRED` or
              :inline_cmake:`CMAKE_<LANG>_EXTENSIONS` can often lead to
              unexpected behavior
    - for specific target with properties:
        - :inline_cmake:`<LANG>_STANDARD`
        - :inline_cmake:`<LANG>_STANDARD_REQUIRED`
        - :inline_cmake:`<LANG>_EXTENSIONS`
    - for specific target with compile features
        - :inline_cmake:`<lang>_std_<value>`
- Compile features should be used only in special cases where user knows what
  they do

- :cmake:module:`WriteCompilerDetectionHeader` can be used to detect and
  provide implementation for compile features

    - better to use in cases when moving to new standard

****************
16. Target Types
****************

16.1. Executables
=================

:cmake:command:`add_executable`

.. code-block:: cmake
    :linenos:
    :caption: Three forms of ``add_executable()`` command
    :name: code_16_1_listing_0

    add_executable(targetName
        [WIN32] [MACOSX_BUNDLE] [EXCLUDE_FROM_ALL]
        source1 [source2 ...]
    )
    add_executable(targetName IMPORTED [GLOBAL])
    add_executable(aliasName ALIAS targetName)

:inline_cmake:`IMPORTED` form

- create a CMake target for an existing executable
- cannot be installed
- properties to be set:
    - :cmake:prop_tgt:`IMPORTED_LOCATION`
    - :cmake:prop_tgt:`IMPORTED_LOCATION_\<CONFIG\>`
- :inline_cmake:`GLOBAL` makes the target visible everywhere
- regular executable targets built by the project are always global

:inline_cmake:`ALIAS` form

- creates another name for a specific target
- does not create new build target
- cannot point to alias
- cannot point to imported non-global targets
- cannot be installed
- cannot be exported
- cannot be used as the operand of :cmake:command:`set_property`,
  :cmake:command:`set_target_properties`,
  :cmake:command:`target_link_libraries` etc.

16.2. Libraries
===============

:cmake:command:`add_library`

.. code-block:: cmake
    :linenos:
    :caption: Expanded basic form ``add_library()`` command
    :name: code_16_2_listing_0

    add_library(targetName [STATIC | SHARED | MODULE | OBJECT]
        [EXCLUDE_FROM_ALL]
        source1 [source2 ...]
    )

OBJECT
------

- :cmake:release:`3.12 <`
    - cannot be linked
        - no use with :cmake:command:`target_link_libraries`
        - don’t provide transitive dependencies to the targets they are added
          to as objects/sources
        - header search paths, compiler defines, etc. have to be manually
          carried across
    - should be used as a source of other target
        -  generator expression :inline_cmake:`$<TARGET_OBJECTS:objLib>`
- :cmake:release:`3.12 >`
    - can be used with :cmake:command:`target_link_libraries`
        - as a target to link with
        - as a target that links with some other targets
    - usage requirements propagates
    - object files added only to direct target (no propagation)

IMPORTED
--------

- used by config files
- used by Find-* modules
- don't define a library to be built
- provides a reference for external library
- if library type is defined - should be provided, otherwise
  :inline_cmake:`UNKNOWN` type used
- properties have to be set:
    - non :inline_cmake:`OBJECT` libraries:
        - :cmake:prop_tgt:`IMPORTED_LOCATION`
        - :cmake:prop_tgt:`IMPORTED_LOCATION_\<CONFIG\>`
        - Windows: :cmake:prop_tgt:`IMPORTED_IMPLIB`
        - Windows: :cmake:prop_tgt:`IMPORTED_IMPLIB_\<CONFIG\>`
    - :inline_cmake:`OBJECT` libraries:
        - :cmake:prop_tgt:`IMPORTED_OBJECTS`
        - :cmake:prop_tgt:`IMPORTED_OBJECTS_\<CONFIG\>`
- other :inline_cmake:`IMPORTED_` properties CMake set's automatically
- defines as a directory scope target
- :inline_cmake:`GLOBAL` makes target scope global
- can be declared without :inline_cmake:`GLOBAL` and then promoted to global
  scope


.. code-block:: cmake
    :linenos:
    :caption: Windows-specific example of imported library
    :name: code_16_2_listing_1

    add_library(myWindowsLib SHARED IMPORTED)
    set_target_properties(myWindowsLib PROPERTIES
        IMPORTED_LOCATION /some/path/bin/foo.dll
        IMPORTED_IMPLIB   /some/path/lib/foo.lib
    )

.. code-block:: cmake
    :linenos:
    :caption: Imported library of unknown type
    :name: code_16_2_listing_2

    # Assume FOO_LIB holds the location of the library but its type is unknown
    add_library(mysteryLib UNKNOWN IMPORTED)
    set_target_properties(mysteryLib PROPERTIES
        IMPORTED_LOCATION ${FOO_LIB}
    )

.. code-block:: cmake
    :linenos:
    :caption: Imported object library, Windows example
    :name: code_16_2_listing_3

    add_library(myObjLib OBJECT IMPORTED)
    set_target_properties(myObjLib PROPERTIES
    IMPORTED_OBJECTS /some/path/obj1.obj    # These .obj files would be .o
                     /some/path/obj2.obj    # on most other platforms
    )

    # Regular executable target using imported object library.
    # Platform differences are already handled by myObjLib.
    add_executable(myExe $<TARGET_SOURCES:myObjLib>)

INTERFACE
---------

.. code-block:: cmake
    :caption: Interface library form
    :name: code_16_2_listing_4

    add_library(targetName INTERFACE [IMPORTED [GLOBAL]])

- do not represent a physical library
- serves to collect usage requirements and dependencies
- :inline_cmake:`target_*()` commands can be used with
  :inline_cmake:`INTERFACE` mode to define usage requirements
- :cmake:command:`set_property` and :cmake:command:`set_target_properties`
  can be utilized to set :inline_cmake:`INTERFACE_*` properties
- examples
    - header-only libraries
    - combination a set of libraries in a one meta target

.. code-block:: cmake
    :linenos:
    :caption: Header-only library usage
    :name: code_16_2_listing_5

    add_library(myHeaderOnlyToolkit INTERFACE)
    target_include_directories(myHeaderOnlyToolkit
        INTERFACE /some/path/include
    )

    target_compile_definitions(myHeaderOnlyToolkit
        INTERFACE COOL_FEATURE=1
                  $<$<COMPILE_FEATURES:cxx_std_11>:HAVE_CXX11>
    )

    add_executable(myApp ...)
    target_link_libraries(myApp PRIVATE myHeaderOnlyToolkit)

.. code-block:: cmake
    :linenos:
    :caption: Convenience interface library
    :name: code_16_2_listing_6

    # Regular library targets
    add_library(algo_fast ...)
    add_library(algo_accurate ...)
    add_library(algo_beta ...)

    # Convenience interface library
    add_library(algo_all INTERFACE)
    target_link_libraries(algo_all
        INTERFACE
            algo_fast
            algo_accurate
            $<$<BOOL:${ENABLE_ALGO_BETA}>:algo_beta>
    )

    # Other targets link to the interface library
    # instead of each of the real libraries
    add_executable(myApp ...)
    target_link_libraries(myApp PRIVATE algo_all)

INTERFACE IMPORTED
^^^^^^^^^^^^^^^^^^

- INTERFACE library is exported or installed for use outside of the project
- directory scope
- prohibited to set :cmake:prop_tgt:`IMPORTED_LOCATION`

.. list-table:: INTERFACE/IMPORTED summary
   :header-rows: 1

   * - Keywords
     - Visibility
     - ``IMPORTED_LOCATION``
     - Set Interface Properties
     - Installable
   * - ``INTERFACE``
     - Global
     - Prohibited
     - Any method
     - Yes
   * - ``IMPORTED``
     - Local
     - Required
     - :cmake:command:`set_property`
       :cmake:command:`set_target_properties`
       :cmake:release:`3.11 >` :inline_cmake:`target_*()`
     - No
   * - ``IMPORTED GLOBAL``
     - Global
     - Required
     - `-`
     - `-`
   * - ``INTERFACE IMPORTED``
     - Local
     - Prohibited
     - `-`
     - `-`
   * - ``INTERFACE IMPORTED GLOBAL``
     - Global
     - Prohibited
     - `-`
     - `-`

ALIAS
-----

.. code-block:: cmake
    :caption: Alias library
    :name: code_16_2_listing_7

    add_library(aliasName ALIAS otherTarget)

- read-only way to refer to another library
- does not create build target
- cannot be installed
- cannot be defined as an alias for another alias
- :cmake:release:`3.11 <` cannot be created for imported targets
- :cmake:release:`3.11 >` could be created for imported global targets
- used to create qualified library name with namespace

.. code-block:: cmake
    :linenos:
    :caption: Namespace for the target
    :name: code_16_2_listing_8

    # Any sort of real library (SHARED, STATIC, MODULE
    # or possibly OBJECT)
    add_library(myRealThings SHARED src1.cpp ...)
    add_library(otherThings STATIC srcA.cpp ...)

    # Aliases to the above with special names
    add_library(BagOfBeans::myRealThings ALIAS myRealThings)
    add_library(BagOfBeans::otherThings ALIAS otherThings)

.. code-block:: cmake
    :linenos:
    :caption: Using namespaced name from a package
    :name: code_16_2_listing_9

    # Pull in imported targets from an installed package.
    find_package(BagOfBeans REQUIRED)

    # Define an executable that links to the imported
    # library from the installed package
    add_executable(eatLunch main.cpp ...)
    target_link_libraries(eatLunch
        PRIVATE
            BagOfBeans::myRealThings
    )

.. code-block:: cmake
    :linenos:
    :caption: Using namespaced name directly from package's project
    :name: code_16_2_listing_10

    # Add BagOfBeans directly to this project, making
    # all of its targets directly available
    add_subdirectory(BagOfBeans)

    # Same definition of linking relationship still works
    add_executable(eatLunch main.cpp ...)
    target_link_libraries(eatLunch
        PRIVATE
            BagOfBeans::myRealThings
    )

.. important::
    Another important aspect of names having a double-colon (::) is that CMake
    will always treat them as the name of an alias or imported target.
    Any attempt to use such a name for a different target type will result in an error.


.. code-block:: cmake
    :linenos:
    :caption: Typos in bare name and in namespaced name
    :name: code_16_2_listing_11

    add_executable(main main.cpp)
    add_library(bar STATIC ...)
    add_library(foo::bar ALIAS bar)

    # Typo in name being linked to, CMake will assume a
    # library called "bart" will be provided by the
    # system at link time and won't issue an error.
    target_link_libraries(main PRIVATE bart)

    # Typo in name being linked to, CMake flags an error
    # at generation time because a namespaced name must
    # be a CMake target.
    target_link_libraries(main PRIVATE foo::bart)


16.3. Promoting Imported Targets
================================

- Can be made ``GLOBAL`` when created
- Client code may have no control on creation
- :cmake:prop_tgt:`IMPORTED_GLOBAL` can be used
- no way back to cancel global visibility
- promotion possible in the same visibility scope as creation
    - :cmake:command:`include` and :cmake:command:`find_package` doesn't
      introduce new directory scope
- may be aliased

.. code-block:: cmake
    :linenos:
    :caption: Imported target global scope promotion
    :name: code_16_3_listing_0

    # Imported library created with local visibility.
    # This could be in an external file brought in
    # by an include() call rather than in the same
    # file as the lines further below.
    add_library(builtElsewhere STATIC IMPORTED)
    set_target_properties(builtElsewhere PROPERTIES
        IMPORTED_LOCATION /path/to/libSomething.a
    )

    # Promote the imported target to global visibility
    set_target_properties(builtElsewhere PROPERTIES
        IMPORTED_GLOBAL TRUE
    )

16.4. Recommended Practices
===========================

- :cmake:release:`3.0` each target carries all the necessary information in
  its own properties
- interface libraries
    - header only libraries
    - collection of resources
- imported targets
    - Find modules
    - config files

Imported targets

- :cmake:release:`3.0 <` CMake modules provides set of variables
- :cmake:release:`3.0 >` CMake modules provides imported targets
    - external tools
    - external libraries
    - usage requirements handled by CMake
    - abstracting platform differences
    - abstracting option-dependent tool selection


- static libraries vs object libraries
    - :cmake:release:`3.12 <` Object libraries: no linking possible
    - Object libraries: non trivial propagation of properties
    - Static libraries: better support from old versions

- Aliasing targets with namespace for non project private targets
    - allows to use such target in same source tree
    - allows to use it as imported ones
    - allows renaming original library and stay compatible with consuming
      projects
    - allows to split library and use interface and alias

.. code-block:: cmake
    :caption: Old version of library
    :name: code_16_4_listing_0

    add_library(deepCompute SHARED ...)

.. code-block:: cmake
    :linenos:
    :caption: Splitting the library
    :name: code_16_4_listing_1

    # Now the library has been split in two, so define
    # an interface library with the old name to effectively
    # forward on the link dependency to the new libraries
    add_library(computeAlgoA SHARED ...)
    add_library(computeAlgoB SHARED ...)
    add_library(deepCompute INTERFACE)
    target_link_libraries(deepCompute
        INTERFACE
            computeAlgoA
            computeAlgoB
    )

****************
17. Custom Tasks
****************

17.1. Custom Targets
====================

- :cmake:command:`add_custom_target`
- target always considered out of date -> always rerun
- anything that depends on custom target will be always rerun
- keyword :cmake:inline:keyword:`COMMAND` can be omitted for the first command
    - recommended to use for each command
- any target name of executable type will be replaced to the location of
  executable

    - for other target type use generator expression
      :inline_cmake:`$<TARGET_FILE:target_name>`

- executable target used as a command will be added to dependencies of custom
  target

    - same for generator expression or arguments of a command

- dependencies on any other target should be added with
  :cmake:command:`add_dependencies`
- dependencies on any file should be added with :cmake:inline:keyword:`DEPENDS`
  keyword

    - useful if a file is generated before
        - target that produces this file will be added to dependencies
    - use only full paths
    - :cmake:inline:keyword:`DEPENDS` keyword should not be use for adding
      dependencies on targets
- only order of commands is forced
    - any other assumptions can't be made
        - each command could run in one shell
        - each command could run in its own shell
        - each command could run without shell environment at all
- symbols escaping in commands should be done with
  :cmake:inline:keyword:`VERBATIM` option

    - no further escaping by the platform
- working directory by default is :cmake:variable:`CMAKE_CURRENT_BINARY_DIR`
    - can be changed with :cmake:inline:keyword:`WORKING_DIRECTORY` option
        - relative path is treated relative to
          :cmake:variable:`CMAKE_CURRENT_BINARY_DIR`
- :cmake:inline:keyword:`BYPRODUCTS` lists all files which will be produced by
  this target

    - for :cmake:generator:`Ninja` required if another target depends on
      produced files
    - for all generators files listed in :cmake:inline:keyword:`BYPRODUCTS`
      will have :cmake:prop_sf:`GENERATED` set to
      :cmake:inline:literal:unquoted:`True`

        - ensure correctly handling of dependent targets on these files
- :cmake:inline:keyword:`COMMENT` option provides way to print a message before
  target will be executed
- :cmake:release:`3.2 >` :cmake:inline:keyword:`USES_TERMINAL` instructs CMake
  to give the command direct access to the terminal, if possible
- :cmake:inline:keyword:`SOURCES` allows to list files that target requires for
  some reasons

    - all of them will be checked if exists
    - used with IDE type generators to show those files in IDE

17.2. Adding Build Steps To An Existing Target
==============================================

- :cmake:command:`add_custom_command` with :cmake:inline:keyword:`TARGET`
  keyword
- attaches the commands to an existing target
- :cmake:inline:keyword:`PRE_BUILD`
    - :cmake:generator:`Visual Studio 7` and above
        - commands should be run before any other rules for the specified
          target
    - all other generators treat as a :cmake:inline:keyword:`PRE_LINK` stage
- :cmake:inline:keyword:`PRE_LINK`
    - The commands will be run after sources are compiled, but before they are
      linked
    - Static libraries: before archive tool run
    - Custom targets: not supported
- :cmake:inline:keyword:`POST_BUILD`
    - commands will be run after all other rules for the specified target

.. code-block:: cmake
    :linenos:
    :caption: Multiple command calls
    :name: code_17_2_listing_0

    add_executable(myExe main.cpp)
    add_custom_command(TARGET myExe POST_BUILD
        COMMAND script1 $<TARGET_FILE:myExe>
    )

    # Additional command which will run after the above from a different directory
    add_custom_command(TARGET myExe POST_BUILD
        COMMAND             writeHash $<TARGET_FILE:myExe>
        BYPRODUCTS          ${CMAKE_BINARY_DIR}/verify/myExe.md5
        WORKING_DIRECTORY   ${CMAKE_BINARY_DIR}/verify
    )

17.3. Commands That Generate Files
==================================

- :cmake:command:`add_custom_command` with :cmake:inline:keyword:`OUTPUT`
  keyword
- commands treated as a recipe for generating output files
- relative paths are relative to the current binary directory
- no files will be built bu itself
    - must be a target which:
        - in the same directory scope
        - depends on some of the files that :cmake:command:`add_custom_command`
          generates
        - CMake will create a dependency automatically

.. code-block:: cmake
    :linenos:
    :caption: Using :cmake:inline:keyword:`OUTPUT` form of :cmake:command:`add_custom_command`
    :name: code_17_3_listing_0

    add_executable(myExe main.cpp)

    # Output file with relative path, generated in the build directory
    add_custom_command(OUTPUT myExe.md5
        COMMAND writeHash $<TARGET_FILE:myExe>
    )

    # Absolute path needed for DEPENDS, otherwise relative to source directory
    add_custom_target(computeHash
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/myExe.md5
    )

:ref:`code_17_3_listing_0`: no hashing happen until
:cmake:inline:target:`computeHash` target wouldn't be called explicitly

Source file generation
----------------------

.. code-block:: cmake
    :linenos:
    :caption: Generate sources
    :name: code_17_3_listing_1

    add_executable(generator generator.cpp)

    add_custom_command(OUTPUT onTheFly.cpp
        COMMAND generator
    )

    add_executable(myExe ${CMAKE_CURRENT_BINARY_DIR}/onTheFly.cpp)

- :cmake:inline:target:`myExe` target requires :code:`onTheFly.cpp` file
- CMake recognizes that this file is generated by custom command
- custom command uses executable :code:`generator` which is a target itself
- CMake replaces name of the target :cmake:inline:target:`generator` with a
  binary it produces
- custom command depends on the :code:`generator` binary
- CMake knows how to create that binary with a target
- CMake created dependency on the target :cmake:inline:target:`generator`

Possible limitations for such kind of dependency:

1. :code:`onTheFly.cpp` doesn't exist
2. build target :cmake:inline:target:`myExe`
    - target :cmake:inline:target:`generator` brought up to date
    - custom command executed -> :code:`onTheFly.cpp` generated
    - target :cmake:inline:target:`myExe` is built
3. modify file :code:`generator.cpp`
4. build target :cmake:inline:target:`myExe`
    - :code:`generator.cpp` changed
        - target :cmake:inline:target:`generator` brought up to date
    - :code:`onTheFly.cpp` exists
        - custom command **NOT** executed
    - :code:`onTheFly.cpp` exists up to date
        - :cmake:inline:target:`myExe` is **NOT** rebuilt

To avoid this situation an explicit dependency has to be specified with keyword
:cmake:inline:keyword:`DEPENDS`

DEPENDS
^^^^^^^

- can be files or targets
- recommended to list all targets and files in :cmake:inline:keyword:`DEPENDS`
  argument
- files that are required by a custom command but haven't appear in arguments
  should also be listed in :cmake:inline:keyword:`DEPENDS` argument

MAIN_DEPENDENCY
^^^^^^^^^^^^^^^

- mostly the same effect as :cmake:inline:keyword:`DEPENDS`
- IDE generators mey apply some additional logic
- custom command becomes replacement for the default build rule

.. code-block:: cmake
    :linenos:
    :caption: replace default build rule for file
    :name: code_17_3_listing_2

    add_custom_command(OUTPUT transformed.cpp
        COMMAND transform
                ${CMAKE_CURRENT_SOURCE_DIR}/original.cpp
                transformed.cpp
        MAIN_DEPENDENCY ${CMAKE_CURRENT_SOURCE_DIR}/original.cpp
    )

    add_executable(original    original.cpp)
    add_executable(transformed transformed.cpp)

- no shared objects will be created for target :cmake:inline:target:`original`
    - default rule for :code:`original.cpp` replaced by custom command
        - :code:`transformed.cpp` will be generated instead object file
- linker error for target :cmake:inline:target:`original`

can be solved using keyword :cmake:inline:keyword:`DEPENDS` instead of
:cmake:inline:keyword:`MAIN_DEPENDENCY`

IMPLICIT_DEPENDS
^^^^^^^^^^^^^^^^

- supported only by Makefile generators
    - due to limit number of supported generators should be avoided
- invokes a C or C++ scanner to determine dependencies of the listed files
- discovered dependencies added to the custom command dependency list

DEPFILE
^^^^^^^

- supported only by :cmake:generator:`Ninja`
    - due to limit number of supported generators should be avoided
    - emit error for any other generator
- provides a Ninja-specific :code:`.d` dependency file

APPEND
^^^^^^

- with :cmake:inline:keyword:`OUTPUT` form
    - the first :cmake:inline:keyword:`OUTPUT` file listed must be the same
      for the first and subsequent calls to :cmake:command:`add_custom_command`
    - only :cmake:inline:keyword:`COMMAND` and :cmake:inline:keyword:`DEPENDS`
      can be used for the subsequent calls
- with :cmake:inline:keyword:`TARGET` form
    - no :cmake:inline:keyword:`APPEND` keyword required for subsequent calls
      for the same target
    - :cmake:inline:keyword:`COMMENT` and
      :cmake:inline:keyword:`WORKING_DIRECTORY` can be used for subsequent
      calls

17.4. Configure Time Tasks
==========================

On configure time custom task mey be required:

- obtain information to be used during configuration
- writing or touching files which need to be updated any time CMake is re-run
- generation of :code:`CMakeLists.txt` or other files which need to be included
  or processed as part of the current configure step

----------

- :cmake:command:`execute_process`
- :cmake:inline:keyword:`COMMAND` section specifies tasks
- :cmake:inline:keyword:`WORKING_DIRECTORY` specifies where those task will run
- no intermediate shell environment
    - no io redirection
    - environment variables not supported
- for multiple :cmake:inline:keyword:`COMMAND` sections
    - executed in order listed
    - output from previous command piped to input of the next one
    - output of the *last* command is sent to the output of CMake
    - error of *each* command is sent to the error stream of CMake
- :cmake:inline:keyword:`OUTPUT_VARIABLE` captures the output of the last
  command to variable
- :cmake:inline:keyword:`ERROR_VARIABLE` captures the error stream of each
  command
- :cmake:inline:keyword:`OUTPUT_STRIP_TRAILING_WHITESPACE` removes trailing
  whitespaces from output variable

    - RECOMMENDED
- :cmake:inline:keyword:`ERROR_STRIP_TRAILING_WHITESPACE` removes trailing
  whitespaces from error variable

    - RECOMMENDED
- using same variable name for the error and output will lead to merge  these
  two streams
- :cmake:inline:keyword:`OUTPUT_FILE` allows to redirect output of the last
  command to a file

    - :cmake:inline:keyword:`OUTPUT_STRIP_TRAILING_WHITESPACE` has no effect on
      file
- :cmake:inline:keyword:`ERROR_FILE` allows to redirect errors of each command
  to a file

     - :cmake:inline:keyword:`ERROR_STRIP_TRAILING_WHITESPACE` has no effect on
       file
- :cmake:inline:keyword:`INPUT_FILE` can be used to provide file with input to
  the first command
- same stream cannot be captured to the file and to a variable
    - possible to send one stream to a variable and another to the file
- :cmake:inline:keyword:`OUTPUT_QUIET` to discard output of the last command
- :cmake:inline:keyword:`ERROR_QUIET` to discard error stream of all commands
- :cmake:inline:keyword:`RESULT_VARIABLE` to check the return code or error
  string message of the last command being run

.. code-block:: cmake
    :linenos:
    :caption: checking for the success of a call to :cmake:inline:command:`execute_process()`
    :name: code_17_4_listing_0

    execute_process(
        COMMAND         runSomeScript
        RESULT_VARIABLE result
    )

    if(result)
        message(FATAL_ERROR "runSomeScript failed: ${result}")
    endif()


- :cmake:release:`3.10 >` :cmake:inline:keyword:`RESULTS_VARIABLE` stores the
  result of each command in a list

- :cmake:inline:keyword:`TIMEOUT` leads to termination with timeout error for
  the sequence of commands if they take time longer then was set in option

    - CMake will not halt with error
    - Timeout error will be stored in :cmake:inline:keyword:`RESULT_VARIABLE`

- if project enables C and C++ languages in first run all commands in
  :cmake:command:`execute_process` will have :cmake:variable:env:`CC` and
  :cmake:variable:env:`CXX` environment variables explicitly set to C and C++
  compilers of the main build

    - in subsequent runs of CMake these variables will not be set
    - commands should not use environment variables :cmake:variable:env:`CC`
      and :cmake:variable:env:`CXX`
    - to not set environment variables to the value of main build compilers in
      a first run :cmake:inline:variable:`CMAKE_GENERATOR_NO_COMPILER_ENV` can
      be set to :cmake:inline:literal:unquoted:`True`. (undocumented variable)


17.5. Platform Independent Commands
===================================

:cmake:manual:`cmake.1 run-a-command-line-tool`

.. code-block:: Bash
    :caption: Command line tool mode
    :name: code_17_5_listing_0

    cmake -E cmd [args...]


.. code-block:: cmake
    :caption: Removing directory in two ways
    :name: code_17_5_listing_1

    set(discardDir "${CMAKE_CURRENT_BINARY_DIR}/private")

    # Naive platform specific implementation (not robust)
    if(WIN32)
        add_custom_target(myCleanup
            COMMAND rmdir /S /Q "${discardDir}"
        )
    elseif(UNIX)
        add_custom_target(myCleanup
            COMMAND rm -rf "${discardDir}"
        )
    else()
        message(FATAL_ERROR "Unsupported platform")
    endif()

    # Platform independent equivalent
    add_custom_target(myCleanup
        COMMAND "${CMAKE_COMMAND}" -E remove_directory "${discardDir}"
    )

.. warning::
    :cmake:inline:command:`if-else` testing **target** platform not **host**

- :cmake:variable:`CMAKE_COMMAND` holds the full path to ``cmake`` executable
    - same ``cmake`` version for all the custom commands
    - same that was invoked for the main build
    - remains the same for the generation step

- :cmake:inline:keyword:`COMMENT` in :cmake:command:`add_custom_target` and
  :cmake:command:`add_custom_command` not always reliable

    - command line tool ``-E echo`` can be used instead


.. code-block:: cmake
    :caption: Echoing
    :name: code_17_5_listing_2

    set(discardDir "${CMAKE_CURRENT_BINARY_DIR}/private")
    add_custom_target(myCleanup
        COMMAND "${CMAKE_COMMAND}" -E echo "Removing ${discardDir}"
        COMMAND "${CMAKE_COMMAND}" -E remove_directory "${discardDir}"
        COMMAND "${CMAKE_COMMAND}" -E echo "Recreating ${discardDir}"
        COMMAND "${CMAKE_COMMAND}" -E make_directory "${discardDir}"
    )

Scripting engine
----------------

:cmake:manual:`cmake.1 run-a-script`

.. code-block:: Bash
    :caption: Script mode
    :name: code_15_5_listing_3

    cmake [options] -P filename

- no configure or generate steps
- ``CMakeCache.txt`` not updated
- script file is essentially processed as just a set of commands rather than as
  a project

    - no project related commands supported

- supports ``-D`` option to pass variables and their values

.. code-block:: Bash
    :caption: Passing variables in a script mode
    :name: code_15_5_listing_4

    cmake -DOPTION_A=1 -DOPTION_B=foo -P myCustomScript.cmake

17.6. Combining The Different Approaches
========================================

.. code-block:: cmake
    :linenos:
    :caption: ``CMakeLists.txt``
    :name: code_15_6_listing_0

    cmake_minimum_required(VERSION 3.0)
    project(Example)

    # Define an executable which generates various files in a
    # directory passed as a command line argument
    add_executable(generateFiles generateFiles.cpp)

    # Create a custom target which invokes the above executable
    # after creating an empty output directory for it to populate,
    # then invoke a script to archive that directory's contents
    # and print the MD5 checksum of that archive
    set(outDir "foo")
    add_custom_target(archiver
        COMMAND "${CMAKE_COMMAND}" -E echo "Archiving generated files"
        COMMAND "${CMAKE_COMMAND}" -E remove_directory "${outDir}"
        COMMAND "${CMAKE_COMMAND}" -E make_directory "${outDir}"
        COMMAND "generateFiles" "${outDir}"
        COMMAND "${CMAKE_COMMAND}" "-DTAR_DIR=${outDir}"
                                 -P "${CMAKE_CURRENT_SOURCE_DIR}/archiver.cmake"
    )

.. code-block:: cmake
    :linenos:
    :caption: ``archiver.cmake``
    :name: code_15_6_listing_1

    cmake_minimum_required(VERSION 3.0)

    if(NOT TAR_DIR)
        message(FATAL_ERROR "TAR_DIR must be set")
    endif()

    # Create an archive of the directory
    set(archive archive.tar)
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar cf ${archive} "${TAR_DIR}"
        RESULT_VARIABLE result
    )

    if(result)
        message(FATAL_ERROR "Archiving ${TAR_DIR} failed: ${result}")
    endif()

    # Compute MD5 checksum of the archive
    execute_process(COMMAND ${CMAKE_COMMAND} -E md5sum ${archive}
        OUTPUT_VARIABLE md5output
        RESULT_VARIABLE result
    )

    if(result)
        message(FATAL_ERROR "Unable to compute md5 of archive: ${result}")
    endif()

    # Extract just the checksum from the output
        string(REGEX MATCH "^ *[^ ]*" md5sum "${md5output}")
    message("Archive MD5 checksum: ${md5sum}")

17.7. Recommended Practices
===========================

- for custom tasks prefer to use build time commands
  :cmake:command:`add_custom_command` and :cmake:command:`add_custom_target`
  instead of configure time command :cmake:command:`execute_process`

    - keep configure time as short as possible
        - configure step maybe reinvoked any time due to changes to files

- use CMake's command line tool mode :inline_cmake:`-E <cmd>`
  everywhere possible instead of platform specific commands

- use CMake's scripting mode :inline_cmake:`-P <filename>`
  instead of any other scripting platform dependent languages

    - reduce complexity of a project
    - less dependencies
    - platform independence

- try to avoid for :cmake:command:`add_custom_command`
  :cmake:command:`add_custom_target`

    - better to use :inline_cmake:`${CMAKE_COMMAND} -E echo "message"` instead
      of :cmake:inline:keyword:`COMMENT`
    - :cmake:inline:keyword:`PRE_BUILD`
    - generator specific :cmake:inline:keyword:`IMPLICIT_DEPENDS`
      :cmake:inline:keyword:`DEPFILE`
    - :cmake:inline:keyword:`MAIN_DEPENDENCY` when it is not an intention to
      replace default build rule

- all files created by :cmake:command:`add_custom_command` should be listed in
  :cmake:inline:keyword:`OUTPUT`

- explicitly list all the required files in :cmake:inline:keyword:`DEPENDS`

- use absolute paths in :cmake:inline:keyword:`DEPENDS`

- test the result of :cmake:command:`execute_process` with :cmake:command:`if`
  and :cmake:inline:keyword:`RESULT_VARIABLE`



