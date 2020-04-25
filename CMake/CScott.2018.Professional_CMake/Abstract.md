## Table of contents

- [15.1.](#chapter_15.1) Setting The Language Standard Directly
- [15.2.](#chapter_15.2) Setting The Language Standard By Feature Requirements 

## Chapter 15. Language Requirements

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

- **TGTPPT**: `COMPILE_FEATURES`
- **TGTPPT**: `INTERFACE_COMPILE_FEATURES`
- **command**: `target_compile_features()`
