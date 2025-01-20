import logging
import os.path
import pdb
import sys
sys.path.insert(1, '/Users/epohl/projects/dynamic_assignment/src/')
sys.path.insert(1, '/Users/epohl/projects/dynamic_assignment/')

def remove_logging(line):
    # key assumptions are not safe here
    line = line.replace('logger.info("', "")
    line = line.rstrip(" ")
    if line[-2:] == '")':
        line = line[:-2]
    return line

def process_code(c, x, fname):
    with open("output.md", "wt") as md_file_handle:
        code_lines = c.split("\n")
        output_now = False
        output_code = []
        in_note = False
        note_line_no =0
        with open(x, "rt") as output_file_handle:
            md_file_handle.write(f"# Usage Walkthrough Markdown created by usage-vacuum from {fname}\n\n")
            for line in output_file_handle:
                if "<string>" in line and "<module>" in line:
                    line_num = line[
                               line.index("<string>")+8+1:
                               line.index("<module>")-1
                               ]

                    code_line = code_lines[int(line_num)-1].rstrip("\n")
                    if code_line.lstrip().startswith("logger.info"):
                        if output_now and len(output_code) > 0:
                            md_file_handle.write('\n```python\n')
                            for output_code_line in output_code:
                                md_file_handle.write(output_code_line + "\n")
                            md_file_handle.write('```\n')
                            output_code = []
                        if not in_note:
                            in_note = True
                            md_file_handle.write("> [!NOTE]\n")
                            note_line_no = 1
                        else:
                            note_line_no += 1
                        if note_line_no == 1:
                            prefix = "> "
                        else:
                            prefix = ""
                        md_file_handle.write(prefix + remove_logging(code_line)+'</br>')
                    elif output_now:
                        in_note = False
                        output_code.append(code_line)
                    elif "__main__" in code_line:
                        output_now = True
                        in_note = False
                else:
                    if "Return" in line:
                        output_now = False
                        in_note = False
                    if output_now:
                        if in_note:
                            md_file_handle.write("\n")
                            in_note = False
                        md_file_handle.write('\n```python\n')
                        for output_code_line in output_code:
                            md_file_handle.write(output_code_line+"\n")
                        md_file_handle.write('```\n')
                        md_file_handle.write(line.replace("(Pdb) ", "").rstrip("\n")+"\n")
                        output_code = []
            if len(output_code) > 0:
                md_file_handle.write("'''\\")
                for output_code_line in output_code:
                    md_file_handle.write(output_code_line+"\\")
                md_file_handle.write("'''\\")


if __name__ == '__main__':
    logging.info("in main")
    root = 'dynamic_assignment'
    source_path = r"C:\Users\epohl\projects\dynamic_assignment\src\demo_write_configs.py"
    fpath_list = source_path.split('\\')
    fpath = '.'.join(fpath_list[fpath_list.index(root):])
    print("hello", fpath)
    # get code
    with open(source_path, 'r') as f:
        code = '\n'.join([line.rstrip("\n") for line in f])
    print("hello", code)
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
    process_code(code, "output.txt", fpath)
