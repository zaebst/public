#include "EXTERN.h"
#include "perl.h"
#include "XSUB.h"

#include "ppport.h"
#include <sys/types.h>
#include <grp.h>
#include <unistd.h>
#include <stdio.h>

/*
  SysRet automatically converts system return codes to perl return codes.
  If RETVAL is -1, the SysRet type returns undef 
  If RETVAL is  0, the SysRet type returns the idomatic "0 but true"
*/
typedef int SysRet;

MODULE=Process::Initgroups         PACKAGE=Process::Initgroups
PROTOTYPES:DISABLE


SysRet
initgroups(user,group)
        const char * user;
        Gid_t group;
    PREINIT:
        struct passwd * pw;
        struct group * grp = NULL;

    CODE:
        pw = getpwnam(user);
        grp = getgrgid(group);
        if (! (pw && pw->pw_name && pw->pw_name[0] && pw->pw_dir && pw->pw_dir[0] && pw->pw_passwd && pw->pw_gid ) ) { 
            RETVAL = -1;
        }
        else if (grp == NULL)
        {   
            RETVAL = -1;
        }   
        else {
            RETVAL = initgroups(pw->pw_name, group);
        }
    OUTPUT:
            RETVAL

