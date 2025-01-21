import logging
import pdb
import sys
import argparse
sys.path.insert(1, '/Users/epohl/projects/dynamic_assignment/src/')
sys.path.insert(1, '/Users/epohl/projects/dynamic_assignment/')


def remove_logging(line):
    # key assumptions are not safe here
    line = line.replace('logger.info("', "").rstrip(" ")
    if line[-2:] == '")':
        line = line[:-2]
    return line


def process_code(
        code_text,
        demo_usage_walkthrough_file_name,
        source_module_name,
        markdown_output_file_name
):
    with open(markdown_output_file_name, "wt") as md_file_handle:
        code_lines = code_text.split("\n")
        output_now = False
        output_code = []
        in_note = False
        note_line_no = 0
        with open(demo_usage_walkthrough_file_name, "rt") as output_file_handle:
            md_file_handle.write(
                f"# Usage Walkthrough Markdown created by usage-vacuum from {source_module_name}\n\n"
            )
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
    parser = argparse.ArgumentParser(
        description="Transform a demo usage script into markdown"
    )
    parser.add_argument(
        "filename",
        help="Path of the demo usage file"
    )
    parser.add_argument(
        "applicationname",
        help="Application name which is being demoed"
    )
    parser.add_argument(
        "markdown_file_path",
        help="Markdown file name and path"
    )
    args = parser.parse_args()
    root = args.applicationname
    source_path = args.filename
    fpath_list = source_path.split('\\')
    fpath = '.'.join(fpath_list[fpath_list.index(root):])
    markdown_output_file = args.markdown_file_path
    # get code
    with open(source_path, 'r') as f:
        code = '\n'.join([line.rstrip("\n") for line in f])
    # create stdin for code lines number of ns for pdb to iterate and direct stdin to that file
    with open("./tmp/test.txt", "wt") as test_file_handle:
        # 100 was added here because I encountered a loop which made the program run longer than the line length
        # why 100
        # why not run until pdb is over?
        for x in range(code.count("\n")*100):
            test_file_handle.write("n\n")
    fin = open("./tmp/test.txt", "rt")
    sys.stdin = fin

    # direct stdout to a file
    fout = open("./tmp/output.txt", "wt")
    save_out = sys.stdout
    sys.stdout = fout

    # run pdb, capturing stdout for pdb using stdin
    pdb.run(code)

    # redirect stdout back to true stdout
    sys.stdout = save_out
    fout.close()
    fin.close()

    # process the output file to pretty it up
    process_code(
        code,
        "../output.txt",
        fpath,
        markdown_output_file
    )
