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

