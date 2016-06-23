/**
 * @file cmnutil.h
 * @author Jiahui Xie
 *
 * @section LICENSE
 *
 * Copyright © 2016 Jiahui Xie
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
 * WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * @section DESCRIPTION
 *
 * Common utility header defines various macros used for feature testing
 * and error checking.
 */

#ifndef CMNUTIL_H
#define CMNUTIL_H

/*
                       +-------------------------------+
                       |Compiler/Libc Test Conditionals|
                       +-------------------------------+
*/
#include <features.h>
/*
 * For gcc, c99 is fully supported since 4.3, so a test is performed
 * in the following.
 *
 * To avoid erroneous stop of compilation behavior from llvm-clang,
 * an extra macro is tested as well due to the fact that clang also
 * defines __GNUC__ if invoked with "-std=gnu99" flag.
 *
 * A similar test can be performed for clang, but the technique is
 * not known for the author(jiahui) of this software so it is left out,
 * but as long as you are not using some ancient versions you should be fine.
 *
 * Reference
 * https://gcc.gnu.org/c99status.html
 */
#if !defined(__clang__) && defined(__GNUC__)
#if 4 > __GNUC__
#error "<" __FILE__ "> GCC Version Test -- [ FAIL ]"
#error "This software requires gcc to be at least 4.3"
#elif 4 == __GNUC__ && 3 > __GNUC_MINOR__
#error "<" __FILE__ "> GCC Version Test -- [ FAIL ]"
#error "This software requires gcc to be at least 4.3"
#endif
#endif

/* secure_getenv first appeared in glibc 2.17 */
#if defined(__GLIBC__)
#if 2 > __GLIBC__
#error "<" __FILE__ "> GLIBC Version Test -- [ FAIL ]"
#error "This software requires the glibc to be at least 2.17"
#elif 2 == __GLIBC__ && 17 > __GLIBC_MINOR__
#error "<" __FILE__ "> GLIBC Version Test -- [ FAIL ]"
#error "This software requires the glibc to be at least 2.17"
#endif
#endif


/*
                             +-------------------+
                             |Feature Test Macros|
                             +-------------------+
*/
#define _POSIX_C_SOURCE 200809L


/*
                                +--------------+
                                |Utility Macros|
                                +--------------+
*/
#include <errno.h>  /* errno */
#include <stdio.h>  /* fprintf() */
#include <stdlib.h> /* abort() */
#include <string.h> /* strerror() */

/* ANSI Color Escape Sequences */
#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_KHAKI   "\x1b[1;33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_PURPLE  "\x1b[1;35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_BOLD    "\x1b[1m"
#define ANSI_COLOR_RESET   "\x1b[0m"

#define CMNUTIL_ERRABRT(expr) \
        do { \
                int status__ = 0; \
                if (0 != (status__ = (expr))) { \
                        fprintf(stderr, \
                                "[%s] on line [%d] within function [%s]" \
                                "in file [%s]: %s\n", \
                                #expr, __LINE__, __func__, \
                                __FILE__, strerror(status__)); \
                        abort(); \
                } \
        } while (0)


#define CMNUTIL_ERRNOABRT(experr, expr) \
        do { \
                if ((experr) == (expr)) { \
                        fprintf(stderr, \
                                "[%s] on line [%d] within function [%s]" \
                                "in file [%s]: %s\n", \
                                #expr, __LINE__, __func__, \
                                __FILE__, strerror(errno)); \
                        abort(); \
                } \
        } while (0)

#define CMNUTIL_STREACH(iterator_, ...) \
        for (char **iterator_ = (char *[]){__VA_ARGS__, NULL}; \
             *iterator_; \
             ++iterator_)

#define CMNUTIL_ZFREE(ptr) \
        do { \
                free(ptr); \
                ptr = NULL; \
        } while (0)

/*
                            +-----------------------+
                            |Enumeration Definitions|
                            +-----------------------+
*/

#endif /* CMNUTIL_H */
