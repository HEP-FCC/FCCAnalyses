/* 
 * panic.c --
 *
 *	Source code for the "panic" library procedure for Tcl;
 *	individual applications will probably override this with
 *	an application-specific panic procedure.
 *
 * Copyright (c) 1988-1993 The Regents of the University of California.
 * Copyright (c) 1994 Sun Microsystems, Inc.
 *
 * See the file "license.terms" for information on usage and redistribution
 * of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 *
 * RCS: @(#) $Id: panic.c,v 1.1 2008-06-04 13:58:02 demin Exp $
 */

#include <stdio.h>
#ifdef NO_STDLIB_H
#   include "../compat/stdlib.h"
#else
#   include <stdlib.h>
#endif

#define panic panicDummy
#include "tcl.h"
#undef panic

# undef TCL_STORAGE_CLASS
# define TCL_STORAGE_CLASS DLLEXPORT

EXTERN void		panic _ANSI_ARGS_((char *format, char *arg1,
			    char *arg2, char *arg3, char *arg4, char *arg5,
			    char *arg6, char *arg7, char *arg8));

/*
 * The panicProc variable contains a pointer to an application
 * specific panic procedure.
 */

void (*panicProc) _ANSI_ARGS_(TCL_VARARGS(char *,format)) = NULL;

/*
 *----------------------------------------------------------------------
 *
 * Tcl_SetPanicProc --
 *
 *	Replace the default panic behavior with the specified functiion.
 *
 * Results:
 *	None.
 *
 * Side effects:
 *	Sets the panicProc variable.
 *
 *----------------------------------------------------------------------
 */

void
Tcl_SetPanicProc(proc)
    void (*proc) _ANSI_ARGS_(TCL_VARARGS(char *,format));
{
    panicProc = proc;
}

/*
 *----------------------------------------------------------------------
 *
 * panic --
 *
 *	Print an error message and kill the process.
 *
 * Results:
 *	None.
 *
 * Side effects:
 *	The process dies, entering the debugger if possible.
 *
 *----------------------------------------------------------------------
 */

	/* VARARGS ARGSUSED */
void
panic(format, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)
    char *format;		/* Format string, suitable for passing to
				 * fprintf. */
    char *arg1, *arg2, *arg3;	/* Additional arguments (variable in number)
				 * to pass to fprintf. */
    char *arg4, *arg5, *arg6, *arg7, *arg8;
{
    if (panicProc != NULL) {
	(void) (*panicProc)(format, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8);
    } else {
	(void) fprintf(stderr, format, arg1, arg2, arg3, arg4, arg5, arg6,
		arg7, arg8);
	(void) fprintf(stderr, "\n");
	(void) fflush(stderr);
	abort();
    }
}
