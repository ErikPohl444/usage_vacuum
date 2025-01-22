import logging
import pdb
import sys
import argparse
sys.path.insert(1, '/Users/epohl/projects/dynamic_assignment/src/')
sys.path.insert(1, '/Users/epohl/projects/dynamic_assignment/')


def remove_logging(logging_line):
    # key assumptions are not safe here
    logging_line = logging_line.replace('logger.info("', "").rstrip(" ")
    if logging_line[-2:] == '")':
        logging_line = logging_line[:-2]
    return logging_line


def flush_output_buffer(file_handle, output_buffer):
    file_handle.write('\n```python\n')
    for output_code_line in output_buffer:
        file_handle.write(output_code_line + "\n")
    file_handle.write('```\n')
    return []


def is_code_line(line):
    if "<string>" in line and "<module>" in line:
        return line[
               line.index("<string>")+8+1:
               line.index("<module>")-1
               ]
    else:
        return None


def convert_transcript_to_markdown(
        demo_usage_code_text,
        demo_usage_transcript_file_name,
        source_module_name,
        markdown_output_file_name
):
    demo_code_lines = demo_usage_code_text.split("\n")
    with open(markdown_output_file_name, "wt") as markdown_file_handle:
        output_now = False
        output_code_buffer = []
        within_logging_block = False
        logging_block_line_count = 0
        with open(demo_usage_transcript_file_name, "rt") as transcript_file_handle:
            markdown_file_handle.write(
                f"# Usage Walkthrough Markdown created by usage-vacuum from {source_module_name}\n\n"
            )
            for transcript_line in transcript_file_handle:
                if line_num := is_code_line(transcript_line):
                    code_line = demo_code_lines[int(line_num)-1].rstrip("\n")
                    if code_line.lstrip().startswith("logger.info"):
                        if output_now and len(output_code_buffer) > 0:
                            output_code_buffer = flush_output_buffer(markdown_file_handle, output_code_buffer)
                        if not within_logging_block:
                            within_logging_block = True
                            markdown_file_handle.write("> [!NOTE]\n")
                            logging_block_line_count = 1
                        else:
                            logging_block_line_count += 1
                        if logging_block_line_count == 1:
                            prefix = "> "
                        else:
                            prefix = ""
                        markdown_file_handle.write(prefix + remove_logging(code_line)+'</br>')
                    elif output_now:
                        within_logging_block = False
                        output_code_buffer.append(code_line)
                    elif "__main__" in code_line:
                        output_now = True
                        within_logging_block = False
                else:
                    if "Return" in transcript_line:
                        output_now = False
                        within_logging_block = False
                    if output_now:
                        if within_logging_block:
                            markdown_file_handle.write("\n")
                            within_logging_block = False
                        output_code_buffer = flush_output_buffer(markdown_file_handle, output_code_buffer)
                        markdown_file_handle.write(transcript_line.replace("(Pdb) ", "").rstrip("\n")+"\n")
            if len(output_code_buffer) > 0:
                flush_output_buffer(markdown_file_handle, output_code_buffer)


def get_dot_notation(demo_usage_file_path, application_name):
    demo_usage_file_path_list = demo_usage_file_path.split('\\')
    return '.'.join(
        demo_usage_file_path_list[demo_usage_file_path_list.index(application_name):]
    )


def set_args(arg_metadata):
    parser = argparse.ArgumentParser(
        description="Transform a demo usage script into markdown"
    )
    for arg in arg_metadata:
        parser.add_argument(arg[0], help=arg[1])
    return parser.parse_args()


if __name__ == '__main__':
    logging.info("in main")

    # get args for CLI usage
    args_metadata = [
        ("demo_usage_file_path", "Path of the demo usage file and its path"),
        ("applicationname", "Application name which is being demoed"),
        ("markdown_file_path", "Markdown file name and path")
    ]
    args = set_args(args_metadata)

    # define core variables based on args
    application_name = args.applicationname
    demo_usage_file_path = args.demo_usage_file_path
    application_path_dot_notation = get_dot_notation(demo_usage_file_path, application_name)
    markdown_output_file = args.markdown_file_path

    # create number of debug line iterations file name
    debug_line_iterations_file_name = "./tmp/test.txt"
    demo_transcript_file_name = "./tmp/output.txt"

    # get code
    with open(demo_usage_file_path, 'r') as f:
        demo_walkthrough_code = '\n'.join(
            [line.rstrip("\n") for line in f]
        )

    # create stdin for code lines number of ns for pdb to iterate and direct stdin to that file
    with open(debug_line_iterations_file_name, "wt") as test_file_handle:
        # 100 was added here because I encountered a loop which made the program run longer than the line length
        # why 100
        # why not run until pdb is over?
        test_file_handle.write("n\n" * demo_walkthrough_code.count("\n") * 100)

    with open(debug_line_iterations_file_name, "rt") as demo_line_iterations_file_handle:
        sys.stdin = demo_line_iterations_file_handle

        # direct stdout to a file
        with open(demo_transcript_file_name, "wt") as demo_transcript_file_handle:
            remember_stdout = sys.stdout
            sys.stdout = demo_transcript_file_handle

            # run pdb, capturing stdout for pdb using stdin
            pdb.run(demo_walkthrough_code)

            # redirect stdout back to true stdout
            sys.stdout = remember_stdout

    # process the output file to pretty it up
    convert_transcript_to_markdown(
        demo_walkthrough_code,
        demo_transcript_file_name,
        application_path_dot_notation,
        markdown_output_file
    )
