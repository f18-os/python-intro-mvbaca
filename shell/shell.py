#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()

while 1:
    command = input("$")

    if command == "exit":
        break

    args = command.split(" ")
    if len(args) is not 3 and len(args) is not 4:
        if command == "":
            pass
        else:
            os.write(2, ("%s" % "Error: invalid input\n").encode())

    else:
        
        rc = os.fork()
        
        if rc == 0:
             
            if len(args) is 3 and args[1] == "<":
                args2 = [args[0],"../"+args[2]]
                for dir in re.split(":" , os.environ['PATH']):
                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args2, os.environ)
                        print("")
                    except FileNotFoundError:
                        pass
                    
            else:
                if args[2] == ">":
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

                if args[2] == "|":
                    r,w = os.pipe()
                    os.set_inheritable(r, True)
                    os.set_inheritable(w, True)
                    rc2 = os.fork()
                    if rc2 == 0:
                        os.close(1)
                        os.dup2(w,1)
                        os.close(w)
                        os.close(r)
                        args2 = [args[0], "../"+args[1]]
                        for dir in re.split(":", os.environ['PATH']):
                            program = "%s/%s" % (dir,args[0])
                            try:
                                os.execve(program, args2, os.environ)

                            except FileNotFoundError:
                                pass
                    else:
                        os.waitpid(rc2,0)
                        os.close(0)
                        os.dup2(r,0)
                        os.close(r)
                        os.close(w)
                        args3 = [args[3]]
                        for dir in re.split(":", os.environ['PATH']):
                            program = "%s/%s" % (dir, args[3])
                            try:
                                os.execve(program, args3, os.environ)

                            except FileNotFoundError:
                                pass
                    sys.exit(1)
