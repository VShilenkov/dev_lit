#########################################################
CMake Code Lexer Test
#########################################################

.. code-block:: cmake_code

    #[[ block test ]] # end line comment

    #[=[ multi equal signs test  ]=] # end line comment

    #[==[
        multiline test
        # end line comment
    ]==] # end line comment

    # end line comment
    break()
    CMAKE_MINIMUM_REQUIRED()
    continue()
    my_macro()

    my_fuckingfunction(BLABLA text1
        [==[
            huy wam wsem
            folders
            fdsfdsf
            dssds
        ]==]
        #[=[
            multiline
        comment ]=]
        HUYABLA text2

        $<BOOL:string>
        $<AND:conditions>
        $<OR:conditions>
        $<NOT:condition>

        $<STREQUAL:string1,string2>
            $<STREQUAL:$<UPPER_CASE:${foo}>,"BAR"> # "1" if ${foo} is any of "BAR", "Bar", "bar", ...


                ${var_${var}_${var}}_${var}
        $ENV{blabla}
        $ENV{${var}}
        $CACHE{piski}
        $CACHE{piski_${var}_$ENV{piu}}

        $<BOOL:string>
        HUYABLA text2

        "aaa"
        able
        ""
        hyabla
        "aaa"

        "This is a quoted argument containing multiple lines."

        "two
        lines"

        "This is always one argument even though it contains a ; character.
        Both \\-escape sequences and ${variable} references are evaluated.
        The text does not end on an escaped double-quote like \".
        It does end in an unescaped double quote.
        "

        $<EQUAL:value1,value2>
        $<IN_LIST:string,list>
        $<VERSION_LESS:v1,v2>
        $<VERSION_GREATER:v1,v2>
        $<VERSION_EQUAL:v1,v2>
        $<VERSION_LESS_EQUAL:v1,v2>
        $<VERSION_GREATER_EQUAL:v1,v2>
        $<TARGET_EXISTS:target>
        $<CONFIG:cfg>
        $<PLATFORM_ID:platform_ids>
        $<C_COMPILER_ID:compiler_ids>
        $<CXX_COMPILER_ID:compiler_ids>
        $<CUDA_COMPILER_ID:compiler_ids>
        $<OBJC_COMPILER_ID:compiler_ids>
        $<OBJCXX_COMPILER_ID:compiler_ids>
        $<Fortran_COMPILER_ID:compiler_ids>
        $<C_COMPILER_VERSION:version>
        $<CXX_COMPILER_VERSION:version>
        $<CUDA_COMPILER_VERSION:version>
        $<OBJC_COMPILER_VERSION:version>
        $<OBJCXX_COMPILER_VERSION:version>
        $<Fortran_COMPILER_VERSION:version>
        $<TARGET_POLICY:policy>
        $<COMPILE_FEATURES:features>
        $<COMPILE_LANG_AND_ID:language,compiler_ids>

        $<$<CONFIG:Debug>:DEBUG_MODE>
        $<$<CONFIG:Debug>:DEBUG_MODE>

        $<$<COMPILE_LANG_AND_ID:CXX,AppleClang,Clang>:COMPILING_CXX_WITH_CLANG>

            PRIVATE $<$<COMPILE_LANG_AND_ID:CXX,AppleClang,Clang>:COMPILING_CXX_WITH_CLANG>
                        $<$<COMPILE_LANG_AND_ID:CXX,Intel>:COMPILING_CXX_WITH_INTEL>
                        $<$<COMPILE_LANG_AND_ID:C,Clang>:COMPILING_C_WITH_CLANG>

        $<COMPILE_LANGUAGE:languages>

        PRIVATE $<$<COMPILE_LANGUAGE:CXX>:-fno-exceptions>

        PRIVATE $<$<COMPILE_LANGUAGE:CXX>:COMPILING_CXX>
                $<$<COMPILE_LANGUAGE:CUDA>:COMPILING_CUDA>
        PRIVATE $<$<COMPILE_LANGUAGE:CXX,CUDA>:"/opt/foo/headers">

        /usr/include/$<CXX_COMPILER_ID>/

        $<$<VERSION_LESS:$<CXX_COMPILER_VERSION>,4.2.0>:OLD_COMPILER>

        -I$<JOIN:$<TARGET_PROPERTY:INCLUDE_DIRECTORIES>, -I>

        $<$<BOOL:${prop}>:-I$<JOIN:${prop}, -I>>

        COMMAND ${CMAKE_COMMAND} -E echo $<TARGET_PROPERTY:foo,CUSTOM_KEYS>

        COMMAND ${CMAKE_COMMAND} -E
                echo $<TARGET_GENEX_EVAL:foo,$<TARGET_PROPERTY:foo,CUSTOM_KEYS>>
    )

