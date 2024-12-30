import pdb
import sys
import markdown as md
sys.path.insert(1, '/Users/epohl/projects/setsy/src/')
sys.path.insert(1, '/Users/epohl/projects/setsy/')


def process_code(c, x, md):
    with open("output.md", "wt") as md_file_handle:
        code_lines = c.split("\n")
        output_now = False
        output_code = []
        with open(x, "rt") as output_file_handle:
            for line in output_file_handle:
                if "<string>" in line and "<module>" in line:
                    line_num = line[
                               line.index("<string>")+8+1:
                               line.index("<module>")-1
                               ]
                    code_line = code_lines[int(line_num)-1].rstrip("\n")
                    if output_now:
                        output_code.append(code_line)
                    if "__main__" in code_line:
                        output_now = True
                else:
                    if "Return" in line:
                        output_now = False
                    if output_now:
                        md_file_handle.write('```\n')
                        for output_code_line in output_code:
                            md_file_handle.write(output_code_line+"\n")
                        md_file_handle.write('```\n')
                        md_file_handle.write(line.replace("(Pdb) ","").rstrip("\n")+"\n")
                        output_code =[]
            if len(output_code) > 0:
                md_file_handle.write("'''\\")
                for output_code_line in output_code:
                    md_file_handle.write(output_code_line+"\\")
                md_file_handle.write("'''\\")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get code
    with open("c:\\users\\epohl\\projects\\setsy\\src\\demo_usage.py", 'r') as f:
        code = '\n'.join([line.rstrip("\n") for line in f])

    # create stdin for code lines number of ns for pdb to iterate and direct stdin to that file
    with open("test.txt", "wt") as test_file_handle:
        for x in range(code.count("\n")):
            test_file_handle.write("n\n")
    fin = open("test.txt", "rt")
    sys.stdin = fin

    # direct stdout to a file
    fout = open("output.txt", "wt")
    save_out = sys.stdout
    sys.stdout = fout

    # run pdb, capturing stdout for pdb using stdin
    pdb.run(code)

    # redirect stdout back to true stdout
    sys.stdout = save_out
    fout.close()
    fin.close()

    # process the output file to pretty it up
    process_code(code, "output.txt", "output.md")

