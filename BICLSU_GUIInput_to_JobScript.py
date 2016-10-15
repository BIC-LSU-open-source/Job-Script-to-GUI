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

def generateSubmittableScript(
    converted_script, 
    gui_input):

    #print("conv: " + str(converted_script))
    #print("g in: " + str(gui_input))

    submittable_script = ""

    index_temp_start = 0
    current_sequence = -1
    current_sub_sequence = -1
    # all sequence numbers must be in increasing order
    for one_var in gui_input:

        #if new sequence
        #    if old accumulated_string
        #        substitute old place holder w/ old accumulated_string
        #    search for place holder
        #    generate prefix
        #    if no sub sequence
        #        substitute place holder w/ value
        #    else
        #        assign value to accumulated_string
        #else
        #    append value to accumulated_string

        sequence = one_var["sequence"]

        if not sequence == current_sequence:
            # new sequence
            current_sequence = sequence
            
            if current_sub_sequence >= 0:
                # there is old accumulated string

                submittable_script += accumulated_values
                current_sub_sequence = -1

            match_holder = re.compile(r"<BIC \d+ LSU>")
            match = \
                match_holder.search(converted_script[index_temp_start:])

            index_holder_start = \
                index_temp_start + match.start()

            # generate prefix
            submittable_script += \
                converted_script[index_temp_start:index_holder_start]
            index_temp_start = \
                index_temp_start + match.end()

            try:
                sub_sequence = one_var["sub_sequence"]

            except KeyError:
                # without sub sequence
                submittable_script += one_var["value"]

            else:
                # with sub sequence
                accumulated_values = one_var["value"]
                current_sub_sequence = sub_sequence

        else:
            # old sequence
            accumulated_values += one_var["value"]
            current_sub_sequence += 1

        #print("script: " + submittable_script)
        
    #if old accumulated_string
    #    substitute old place holder w/ old accumulated_string
    if current_sub_sequence >= 0:
        submittable_script += accumulated_values

    #submittable_script += " "

    #generate suffix
    submittable_script += \
        converted_script[index_temp_start:]

    return submittable_script

# end of function generateSubmittableScript

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('converted_script_file_path')
    parser.add_argument('gui_input_file_path')
    args = parser.parse_args()

    with open(args.converted_script_file_path, 'r') as script_file:
        converted_script = script_file.read()

    with open(args.gui_input_file_path, 'r') as script_file:
        gui_input_json = script_file.read()
    gui_input = json.loads(gui_input_json)

    submittable_script = \
        generateSubmittableScript(converted_script, gui_input)

    print(str(submittable_script))

# end of __main__

#preceeding regular statements\n#PBS -o <BIC 0 LSU>\nvar_A=<BIC 1 LSU>\ncat <BIC 2 LSU>\ncp <BIC 3 LSU> -t $HOME\nproceeding regular statements\n

#[{"value": "/home/user/output_dir", "sequence": 0}, {"value": "2", "sequence": 1}, {"value": "/home/user/document_file", "sequence": 2}, {"value": "/home/user/result/source_file1", "sequence": 3, "sub_sequence": 0}, {"value": "/home/user/result/source_file2", "sequence": 3, "sub_sequence": 1}]
