from __future__ import print_function

# Designed by Chui-hui Chiu for BIC-LSU project.
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Lesser General Public License as 
#published by the Free Software Foundation, or (at your option) any 
#later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, 
#see <http://www.gnu.org/licenses/>.

import re
import json
import argparse

def parseBrowserBlock(
    path_type, 
    prefix, 
    suffix, 
    variable_sequence):

    form_skeleton = {}

    if str(path_type) in ["both", "directory"]:
        form_skeleton["path_type"] = str(path_type)
    else:
        raise Exception(
            "not supported path type in parseBrowserBlock")
    form_skeleton["prefix"] = str(prefix)
    form_skeleton["suffix"] = str(suffix)
    form_skeleton["input_type"] = "browser"
    form_skeleton["id_sequence"] = variable_sequence
    variable_string = \
        "<BIC " + str(variable_sequence) + " LSU>"
    variable_sequence += 1

    return form_skeleton, variable_string, variable_sequence

# end of parseBrowserBlock

def parseTextBlock(
    prefix, 
    default, 
    suffix, 
    variable_sequence):

    form_skeleton = {}

    form_skeleton["prefix"] = str(prefix)
    form_skeleton["default"] = str(default)
    form_skeleton["suffix"] = str(suffix)
    form_skeleton["input_type"] = "text"
    form_skeleton["id_sequence"] = variable_sequence
    variable_string = \
        "<BIC " + str(variable_sequence) + " LSU>"
    variable_sequence += 1

    return form_skeleton, variable_string, variable_sequence

# end of parseTextBlock

def parseInputBlock(block_string, variable_sequence):

    block_segments = block_string.split(',')

    #print("blo seg: " + str(block_segments))

    if block_segments[1] == "text":

        form_skeleton, variable_string, variable_sequence = \
            parseTextBlock(
                block_segments[2], block_segments[3], 
                block_segments[4], variable_sequence)

    elif block_segments[1] == "file_browser":

        form_skeleton, variable_string, variable_sequence = \
            parseBrowserBlock(
                block_segments[2], block_segments[3], 
                block_segments[4], variable_sequence)

    return form_skeleton, variable_string, variable_sequence

# end of parseInputBlock

def parseVarListBlock(block_string, variable_sequence):

    #print("block: " + str(block_string))

    form_skeleton = {}

    # consume "var_list" column
    index_start_of_prefix = block_string.find(',') + 1   

    index_end_of_prefix = \
        block_string[index_start_of_prefix:].find(',')
    form_skeleton["prefix"] = \
        str(block_string[index_start_of_prefix:index_start_of_prefix + index_end_of_prefix])

    index_end_of_suffix = \
        block_string[index_end_of_prefix+1:].find(',')
    form_skeleton["suffix"] = \
        str(block_string[index_end_of_prefix+1:index_end_of_suffix])

    form_skeleton["list_type"] = "variable"

    match_left = re.compile(r"<BIC")
    match_right = re.compile(r"LSU>")

    index_temp_start = index_end_of_suffix + 1
    match = match_left.search(block_string[index_temp_start:])

    if not match:
        raise Exception(
                "cannot match \"<BIC\".  \
                Syntax error in parseVarListBlock!")
    #print("matched: " + block_string\
    #    [index_temp_start+match.start():\
    #    index_temp_start+match.end()])

    index_temp_start = index_temp_start + match.end() + 1
    index_block_start = index_temp_start
    #print("block start: " + block_string[index_block_start:])

    match = match_right.search(block_string[index_block_start:])

    if not match:
        raise Exception("syntax error in parseVarListBlock!")

    index_block_end = index_block_start + match.start() - 1

    #print("one block: " + block_string\
    #    [index_block_start:index_block_end])

    form_skeleton_input, variable_string, variable_sequence = \
        parseInputBlock(block_string\
            [index_block_start:index_block_end], variable_sequence)

    form_skeleton["input_template"] = form_skeleton_input

    return form_skeleton, variable_string, variable_sequence

# end of parseVarListBlock

def parseListBlock(block_string, variable_sequence):

    #print("block: " + str(block_string))

    form_skeleton = {}

    # consume "list" column
    index_start_of_prefix = block_string.find(',') + 1   

    index_end_of_prefix = \
        block_string[index_start_of_prefix:].find(',')    
    form_skeleton["prefix"] = \
        str(block_string[index_start_of_prefix:index_end_of_prefix])

    index_end_of_suffix = \
        block_string[index_end_of_prefix+1:].find(',')
    form_skeleton["suffix"] = \
        str(block_string[index_end_of_prefix+1:index_end_of_suffix])

    form_skeleton["list_type"] = "fixed"

    input_list = []
    variable_list_string = ""

    match_left = re.compile(r"<BIC")
    match_right = re.compile(r"LSU>")

    index_temp_start = index_end_of_suffix + 1
    match = match_left.search(block_string[index_temp_start:])

    while match:

	#print("matched: " + block_string\
        #    [index_temp_start+match.start():\
        #    index_temp_start+match.end()])
        index_temp_start = index_temp_start + match.end() + 1
        index_block_start = index_temp_start
        #print("block start: " + block_string[index_block_start:])
        match = match_right.search(block_string[index_block_start:])

        if not match:
            raise Exception("syntax error in parseListBlock!")

        index_block_end = index_block_start + match.start() - 1

        #print("one block: " + block_string\
        #    [index_block_start:index_block_end])
        
        form_skeleton_input, variable_string, variable_sequence = \
            parseInputBlock(
                block_string[index_block_start:index_block_end], 
                variable_sequence)
        variable_list_string += " " + variable_string

        input_list.append(form_skeleton_input)

        #print("continue to find ',' at " + \
        #    block_string[index_block_start + match.end():])
        index_temp_start = \
            block_string[index_block_start + match.end():].find(',')

        if index_temp_start == -1:
            # finish
            break
        else:
            # parse next input block
            index_temp_start = \
                index_block_start + match.end() + 1 + \
                index_temp_start
        
        #print("find next input at: " + \
        #    block_string[index_temp_start:])

        match = match_left.search(block_string[index_temp_start:])

    form_skeleton["input_list"] = input_list

    return form_skeleton, variable_list_string, variable_sequence

# end of parseListBlock

def parseBlock(block_string, variable_sequence):

    index = block_string.find(',')
    type = block_string[:index]

    if type == "input":

        form_skeleton, variable_string, variable_sequence = \
            parseInputBlock(block_string, variable_sequence)

    elif type == "list":

        form_skeleton, variable_string, variable_sequence = \
            parseListBlock(block_string, variable_sequence)

    elif type == "var_list":

        form_skeleton, variable_string, variable_sequence = \
            parseVarListBlock(block_string, variable_sequence)

    return form_skeleton, variable_string, variable_sequence

# end of parseInputBlock

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('tagged_script_file_path')
    args = parser.parse_args()

    with open(args.tagged_script_file_path, 'r') as script_file:
        script = script_file.read()

    # The job batch script must be tagged with the following
    # directive blocks.
    #
    # BIC-LSU Input Block:
    # <BIC input,text,<prefix>,<default>,<suffix> LSU>
    # <BIC input,file_brwoser,<allowed path type>,<prefix>,<suffix> Lsu>
    # allowed path type: "both" or "directory"
    # BIC-LSU List Block:
    # <BIC list,<prefix>,<suffix>,<BIC-LSU input block 1>,...,<BIC-LSU input block N> LSU>
    # BIC-LSU Variable List Block:
    # <BIC var_list,<prefix>,<suffix>,<BIC-LSU input block template> LSU>
    #
    # Example:
    #script = '''
    #    no_of_processor=<BIC input,text,Length:,,inch LSU>
    #    dependencies=<BIC list,All dependencies,,<BIC input,text,math,, LSU>,<BIC input,text,io,, LSU> LSU>
    #    genome_libraries=<BIC var_list,Genome Libraries,,<BIC input,file_browser,both,Library, LSU> LSU>
    #    output=<BIC input,file_browser,directory,, LSU>
    #'''

    # converted_script stores the original tagged script with BIC-LSU
    # directive blocks replaced with simple variable names. Identical
    # variable names are used in the GUI for collecting user inputs. 
    # Mapping the user inputs back into the converted_script
    # generates a valid job batch script with user provided
    # parameters.
    converted_script = ""

    form_skeleton_overall = []

    variable_sequence = 0

    print("tagged script: " + str(script))

    index_total_end = len(script)

    match_left = re.compile(r"<BIC")
    match_right = re.compile(r"LSU>")
    match_left_or_right = re.compile(r"(<BIC)|(LSU>)")

    match = match_left.search(script)
    index_temp_start = 0
    index_convert_start = 0

    while match:

        left_bracket = 1
        index_block_start = \
            index_temp_start + match.end() + 1
            # one prepending space
        converted_script += \
            script[index_convert_start:\
            index_temp_start + match.start()]
        #matched = \
        #    script[index_temp_start + match.start(): \
        #        index_temp_start + match.end()]
        #print("matched: " + str(matched))
        #print("block start: " + script[index_block_start:])

        index_temp_start = index_block_start
        match = \
            match_left_or_right.search(script[index_block_start:])
        while match:

            matched = \
                script[index_temp_start + match.start(): \
                    index_temp_start + match.end()]
        #    print("matched: " + str(matched))

            if matched == "<BIC":
                left_bracket += 1
            elif matched == "LSU>":
                left_bracket -= 1

            index_temp_start = index_temp_start + match.end()
        #    print("continue at: " + script[index_temp_start:])

            if left_bracket == 0:
                index_block_end = \
                    index_temp_start - len(matched) - 1 
                    # one appending space
        #        print("block end: " + str(index_block_end))
                break

            match = \
                match_left_or_right.search(script[index_temp_start:])

        if not left_bracket == 0:
            raise Exception("syntax error!")

        # form_skeleton describes the skeleton of the GUI
        form_skeleton, variable_string, variable_sequence = \
            parseBlock(
                script[index_block_start:index_block_end], 
                variable_sequence)
        converted_script += variable_string
        #print("new block: " + str(form_skeleton))
        form_skeleton_overall.append(form_skeleton)

        index_temp_start = index_block_end + 5
        index_convert_start = index_temp_start

        match = match_left.search(script[index_temp_start:])
        #print("find next block: " + script[index_temp_start:])

    converted_script += script[index_convert_start:]

    return_value = {}
    return_value["gui skeleton"] = form_skeleton_overall
    return_value["converted script"] = converted_script

    print(str(json.dumps(return_value)))
