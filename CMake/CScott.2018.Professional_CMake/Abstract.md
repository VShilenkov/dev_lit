## Table of contents

- [15.]((#chapter_15)) Language Requirements
    - [15.1.](#chapter_15.1) Setting The Language Standard Directly
    - [15.2.](#chapter_15.2) Setting The Language Standard By Feature Requirements 
        - [15.2.1.](#chapter_15.2.1) Detection And Use Of Optional Language Features
    - [15.3.](#chapter_15.3) Recommended Practices

## <a name="chapter_15"></a> Chapter 15. Language Requirements

### <a name="chapter_15.1"></a> 15.1. Setting The Language Standard Directly

- **TGTPPT**: `<LANG>_STANDARD`
    - init with **VAR**: `CMAKE_<LANG>_STANDARD`

- **TGTPPT**: `<LANG>_STANDARD_REQUIRED` 
    - init with **VAR**: `CMAKE_<LANG>_STANDARD_REQUIRED`

- **TGTPPT**: `<LANG>_EXTENSIONS` 
    - init with **VAR**: `CMAKE_<LANG>_EXTENSIONS`


```cmake
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
```

- `<LANG>_STANDARD_REQUIRED` is Off dy default
- `<LANG>_EXTENSIONS` may be ignored if `<LANG>_STANDARD` is not set
- `<LANG>_STANDARD` specifies a minimum standard, not necessarily an exact requirement (higher version may be choosen)
- Properties cannot be `INTERFACE`

> ( ! ) Projects should set all three properties/variables rather than just some of them

```cmake
# Require C++11 and disable extensions for all targets
set(CMAKE_CXX_STANDARD          11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS        OFF)
```

### <a name="chapter_15.2"></a> 15.2. Setting The Language Standard By Feature Requirements

[cmake-compile-features(7)](https://cmake.org/cmake/help/latest/manual/cmake-compile-features.7.html)

- **TGTPPT**: [COMPILE_FEATURES](https://cmake.org/cmake/help/latest/prop_tgt/COMPILE_FEATURES.html#prop_tgt:COMPILE_FEATURES)
- **TGTPPT**: [INTERFACE_COMPILE_FEATURES](https://cmake.org/cmake/help/latest/prop_tgt/INTERFACE_COMPILE_FEATURES.html#prop_tgt:INTERFACE_COMPILE_FEATURES)
- **COMMAND**: [target_compile_features()](https://cmake.org/cmake/help/latest/command/target_compile_features.html#command:target_compile_features)
- Each feature must be one of the features supported by the underlying compiler.
    - **GBLPPT**: [CMAKE_C_KNOWN_FEATURES](https://cmake.org/cmake/help/latest/prop_gbl/CMAKE_C_KNOWN_FEATURES.html#prop_gbl:CMAKE_C_KNOWN_FEATURES)
    - **GBLPPT**: [CMAKE_CXX_KNOWN_FEATURES](https://cmake.org/cmake/help/latest/prop_gbl/CMAKE_CXX_KNOWN_FEATURES.html#prop_gbl:CMAKE_CXX_KNOWN_FEATURES)
    - **VAR**: [CMAKE_C_COMPILE_FEATURES](https://cmake.org/cmake/help/latest/variable/CMAKE_C_COMPILE_FEATURES.html#variable:CMAKE_C_COMPILE_FEATURES)
    - **VAR**: [CMAKE_CXX_COMPILE_FEATURES](https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_COMPILE_FEATURES.html#variable:CMAKE_CXX_COMPILE_FEATURES)
- meta-features: `<lang>_std_<value>` 
    - `cxx_std_98`
    - `cxx_std_11`
    - `cxx_std_14`
    - `cxx_std_17`
    - `cxx_std_20`
    - `c_std_90`
    - `c_std_99`
    - `c_std_11`
- In situations where a target has both its `<LANG>_STANDARD` property set and compile features specified, CMake will
enforce the stronger standard requirement.

#### <a name="chapter_15.2.1"></a> 15.2.1. Detection And Use Of Optional Language Features

- **GENEXP**: `$<COMPILE_FEATURES:>`

```cmake
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
```

```c++
class MyClass : public Base
{
public:
    void func() foo_OVERRIDE;
};
```

- **MODULE**: [WriteCompilerDetectionHeader](https://cmake.org/cmake/help/latest/module/WriteCompilerDetectionHeader.html)
    - **COMMAND**: `write_compiler_detection_header()`

## <a name="chapter_15.3"></a> 15.3. Recommended Practices

- Do not set compiler and linker flags directly
- Set standard 
    - for overall project with variables 
        - **VAR**:`CMAKE_<LANG>_STANDARD`
        - **VAR**:`CMAKE_<LANG>_STANDARD_REQUIRED` 
        - **VAR**:`CMAKE_<LANG>_EXTENSIONS`
            - set them after the first **COMMAND**: project()
            - set them all together
            - Omitting `CMAKE_<LANG>_STANDARD_REQUIRED` or `CMAKE_<LANG>_EXTENSIONS` can often lead to unexpected behavior
    - for specific target with properties:
        - **TGTPPT**: `<LANG>_STANDARD`
        - **TGTPPT**: `<LANG>_STANDARD_REQUIRED`
        - **TGTPPT**: `<LANG>_EXTENSIONS`
    - for specific target with compile features
        - `<lang>_std_<value>`
