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

.. role:: inline_cmake(code)
    :language: cmake
    :class: cmake-inline

- :inline_cmake:`<LANG>_STANDARD_REQUIRED` is :inline_cmake:`Off` dy default
- :inline_cmake:`<LANG>_EXTENSIONS` may be ignored if :inline_cmake:`<LANG>_STANDARD` is not set
- :inline_cmake:`<LANG>_STANDARD` specifies a minimum standard, not necessarily an exact requirement (higher version may be choosen)
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
- Each feature must be one of the features supported by the underlying compiler.
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
- In situations where a target has both its :inline_cmake:`<LANG>_STANDARD` property set and compile features specified, CMake will enforce the stronger standard requirement.

15.2.1. Detection And Use Of Optional Language Features
-------------------------------------------------------

- :cmake:manual:`cmake-generator-expressions.7` - :inline_cmake:`$<COMPILE_FEATURES:features>`

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
            - set them after the first :cmake:command:`project()`
            - set them all together
            - omitting :inline_cmake:`CMAKE_<LANG>_STANDARD_REQUIRED` or :inline_cmake:`CMAKE_<LANG>_EXTENSIONS` can often lead to unexpected behavior
    - for specific target with properties:
        - :inline_cmake:`<LANG>_STANDARD`
        - :inline_cmake:`<LANG>_STANDARD_REQUIRED`
        - :inline_cmake:`<LANG>_EXTENSIONS`
    - for specific target with compile features
        - :inline_cmake:`<lang>_std_<value>`
- Compile features should be used only in special cases where user knows what they do
- :cmake:module:`WriteCompilerDetectionHeader` can be used to detect and provide implementation for compile features
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
- cannot be used as the operand of :cmake:command:`set_property`, :cmake:command:`set_target_properties`, :cmake:command:`target_link_libraries` etc.

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

- :cmake:release:`< 3.12`
    - cannot be linked
        - no use with :cmake:command:`target_link_libraries`
        - don’t provide transitive dependencies to the targets they are added to as objects/sources
        - header search paths, compiler defines, etc. have to be manually carried across
    - should be used as a source of other target
        -  generator expression :inline_cmake:`$<TARGET_OBJECTS:objLib>`
- :cmake:release:`> 3.12`
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
- if library type is defined - should be provided, otherwise :inline_cmake:`UNKNOWN` type used
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
- can be declared without :inline_cmake:`GLOBAL` and then promoted to global scope


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
- :inline_cmake:`target_*()` commands can be used with :inline_cmake:`INTERFACE` mode to define usage requirements
- :cmake:command:`set_property` and :cmake:command:`set_target_properties` can be utilized to set :inline_cmake:`INTERFACE_*` properties
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
       :cmake:release:`> 3.11` :inline_cmake:`target_*()`
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
- :cmake:release:`< 3.11` cannot be created for imported targets
- :cmake:release:`> 3.11` could be created for imported global targets
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
    - :cmake:command:`include` and :cmake:command:`find_package` doesn't introduce new directory scope
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

- :cmake:release:`3.0` each target carries all the necessary information in its own properties
- interface libraries
    - header only libraries
    - collection of resources
- imported targets
    - Find modules
    - config files

Imported targets

- :cmake:release:`<3.0` CMake modules provides set of variables
- :cmake:release:`>3.0` CMake modules provides imported targets
    - external tools
    - external libraries
    - usage requirements handled by CMake
    - abstracting platform differences
    - abstracting option-dependent tool selection


- static libraries vs object libraries
    - :cmake:release:`<3.12` Object libraries: no linking possible
    - Object libraries: non trivial propagation of properties
    - Static libraries: better support from old versions

- Aliasing targets with namespace for non project private targets
    - allows to use such target in same source tree
    - allows to use it as imported ones
    - allows renaming original library and stay compatible with consuming projects
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


