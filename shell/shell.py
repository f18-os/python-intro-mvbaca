#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()

while 1:
    command = input("\t>>>")

    args = command.split(" ")
    if len(args) is not 3 and len(args) is not 4:
        os.write(2, ("%s" % "\nError: invalid input\n").encode())

    else:
        
        rc = os.fork()
        
        if rc == 0:
             
            if len(args) is 3 and args[1] == "<":
                args2 = [args[0],"../"+args[2]]
                for dir in re.split(":" , os.environ['PATH']):
                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args2, os.environ)
                        
                    except FileNotFoundError:
                        pass
            elif len(args) is 4 and args[2] == ">":
                args2 = [args[0],"../"+args[1]]
                os.close(1)
                sys.stdout = open("../"+args[3], "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir, args[0])
                    try:
                         os.execve(program, args2, os.environ)
                         
                    except FileNotFoundError:
                         pass
                
    if command == "quit":
        break
    
