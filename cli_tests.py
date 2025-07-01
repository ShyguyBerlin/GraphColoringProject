#!/usr/bin/python

from solvers.solvers import get_generic_solvers
from sys import argv
from tools.testing_tools import *
import asyncio


def print_help():
    print(f"""     Use: {argv[0]} OPTIONS FILES\n
        Options:
        --test-name -n <name> : Set a specific test name which will be printed to the results
        --timeout -t <time> : Sets a timeout for the test, give time in miliseconds
        --repetitions -r <number> : Repeat the test n times, averaging results and counteracting randomness on small datasets
        --parser -p <format> : Sets the format the parser should use to read the file
        --definition-file -d : Assume files given to be in Test definition format, refer to README to learn about the format. 
        --solver -s <array of sorters> : Set which sorters the test should run, defaults to all of them
        --output -o <path> : Output to specified path
          
        --multiprocessing -mp : Enables Multiprocessing

    When using definition files, the parameters set through arguments overwrite their counterparts in the definition files.""")

async def main():
    use_def_files=False
    test_name=None
    timeout=None
    repetitions=None
    parser=None
    output_path=None
    timeout_ms=None
    use_multiprocessing=False

    solvers=None
    files=[]

    if len(argv)<=1:
        print_help()
        exit()
    #solve_graph(nx.erdos_renyi_graph(200,0.2),wigdersons_first)

    i=1
    while i<len(argv):
        match(argv[i]):
            case "--test-name" | "-n":
                if len(argv) > i+1:
                    test_name=argv[i+1]
                    i+=1
                else:
                    print("Incorrect amount/layout of arguments")
                    exit(1)
            case "--timeout" | "-t":
                if len(argv) > i+1:
                    timeout=int(argv[i+1])
                    i+=1
                else:
                    print("Incorrect amount/layout of arguments")
                    exit(1)
            case "--repetitions" | "-r":
                if len(argv) > i+1:
                    repetitions=int(argv[i+1])
                    i+=1
                else:
                    print("Incorrect amount/layout of arguments")
                    exit(1)
            case "--parser" | "-p":
                if len(argv) > i+1:
                    parser=argv[i+1]
                    i+=1
                else:
                    print("Incorrect amount/layout of arguments")
                    exit(1)
            case "--definition-file" | "-d":
                use_def_files=True
            case "--solver" | "-s":
                if len(argv) > i+1:
                    solvers=argv[i+1].split(",")
                    i+=1
                else:
                    print("Incorrect amount/layout of arguments")
                    exit(1)
            case "--output" | "-o":
                if len(argv) > i+1:
                    output_path=argv[i+1]
                    i+=1
                else:
                    print("Incorrect amount/layout of arguments")
                    exit(1)
            case "--multiprocessing" | "-mp":
                use_multiprocessing=True
            case x:
                if parser==None and not use_def_files:
                    print("You need to specify a parser/format to run a test on a data containing file.")
                    exit(1)
                files.append((x,x,parser))
        i+=1
    #print(use_def_files,test_name,timeout,parser,output_path,files)
    # Set default values for arguments not given:
    if not use_def_files:
        if test_name==None:
            test_name="Test"
        if timeout==None:
            timeout=10000
        if solvers==None:
            solvers=get_generic_solvers().keys()
        if repetitions==None:
            repetitions=1

    if len(files)==0:
        print("No files to run tests on given!")
        exit(1)

    print("Preparing test input...")
    csv=""
    if not use_def_files:
        input = Test_input(test_name,timeout,files,solvers,repetitions)
        timeout_ms = timeout/1000
        try:
            test_result = await asyncio.wait_for(run_test(input,use_multiprocessing), timeout=timeout_ms)
            csv = format_test_as_csv(test_result)
        except asyncio.TimeoutError:
            print("run_test() timed out")
    else:
        tests:list[Test_input]=[]
        for _,i,_ in files:
            test=get_test_from_file(i)

            if test_name!=None:
                test.test_name=test
            if timeout!=None:
                test.timeout=timeout
            if repetitions!=None:
                test.repetitions=repetitions
            if solvers!=None:
                test.solvers=solvers
            tests.append(test)

        results:list[Test_result]=[]
        for test in tests:
            timeout_ms = timeout/1000
            try:
                test_result = await asyncio.wait_for(run_test(test,use_multiprocessing), timeout=timeout_ms)
                results.append(test_result)
            except asyncio.TimeoutError:
                print("run_test() timed out")
        csv = format_tests_as_csv(results)
    if output_path==None:
        print(csv)
    else:
        with open(output_path,"w") as f:
            f.write(csv)

if __name__=="__main__":
    asyncio.run(main())
