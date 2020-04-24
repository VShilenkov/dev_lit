## Chapter 15. Language Requirements

### 15.1. Setting The Language Standard Directly

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
