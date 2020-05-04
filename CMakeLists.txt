cmake_minimum_required(VERSION 3.12)
project(development-literature
    VERSION      0.0.1
    DESCRIPTION  "Collection of read books abstracts and exercises"
    HOMEPAGE_URL "https://github.com/VShilenkov/dev_lit"
    LANGUAGES    NONE
)

find_package(CMakeFramework REQUIRED)

add_subdirectory(docs)

