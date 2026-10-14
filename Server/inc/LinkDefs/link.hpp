
#ifndef __inc_linkdefs_link
#define __inc_linkdefs_link

    #ifdef _WIN32
        #include <LinkDefs/link_win.hpp>
        #ifdef LINK_SRCS
            #include <LinkDefs/srcs/win.CPP>
        #endif
    #endif

    #ifdef __unix
        #include <LinkDefs/link_lin.hpp>
        #ifdef LINK_SRCS
            #include <LinkDefs/srcs/lin.CPP>
        #endif
    #endif

    class ClientLink {
            
    };

#endif