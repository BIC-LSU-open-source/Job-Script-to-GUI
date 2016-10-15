# Job-Script-to-GUI
A set of directive rules and parsers for converting a job batch script into some graphical user interface and retrieving the user input back into the script.

## Supported Directives

**BIC-LSU Input Block**<br />
\<BIC input,text,\<prefix>,\<default>,\<suffix> LSU><br />
\<BIC input,file_brwoser,\<allowed path type>,\<prefix>,\<suffix> Lsu><br />
"allowed path type" can be "both" or "directory".

**BIC-LSU List Block**<br />
\<BIC list,\<prefix>,\<suffix>,\<BIC-LSU input block 1>,...,\<BIC-LSU input block N> LSU>

**BIC-LSU Variable-length List Block**<br />
\<BIC var_list,\<prefix>,\<suffix>,\<BIC-LSU input block template> LSU><br />
"BIC-LSU input block template" can be any one of the "BIC-LSU Input Block".

## Program Usage

1. Run **BICLSU_job_script_to_GUI_skeleton** on the job batch script tagged with directives to generate a coverted script and a skeleton for creating a GUI.  The converted script and the skeleton maintain the mapping of each pair of the variable in the converted script and the variables in the skeleton using an identical sequence number. 
2. Run **BICLSU_GUI_to_final_job_script** to map the inputs collected from the GUI back into the converted script to generate a submittable job batch script.

### BICLSU_job_script_to_GUI_skeleton Usage

BICLSU_job_script_to_GUI_skeleton \<tagged job script path>

#### Format of \<tagged job script path>

```
preceeding regular statements

#PBS -o <BIC input,file_browser,directory,Output Directory: , LSU>
var_A=<BIC input,text,Parallelism: ,4,Thread(s) LSU>
cat <BIC input,file_browser,both,Document to Display: , LSU>
cp <BIC var_list,Files to Copy: ,,<BIC input,file_browser,both,Source File, LSU> LSU> -t $HOME

proceeding regular statements
```

#### Program Output

A JSON string in the following format.
```
{
    "gui skeleton":<GUI skeleton>,
    "converted script":<converted script>
}
```

The format of \<GUI skeleton>
```
[
    {
        "path_type": "directory", 
        "prefix": "Output Directory: ", 
        "suffix": "", 
        "sequence": 0, 
        "input_type": "browser"
    }, 
    {
        "default": "4", 
        "input_type": "text", 
        "prefix": "Parallelism: ", 
        "suffix": "Thread(s)", 
        "sequence": 1
    }, 
    {
        "path_type": "both", 
        "prefix": "Document to Display: ", 
        "suffix": "", 
        "sequence": 2, 
        "input_type": "browser"
    }, 
    {
        "prefix": "Files to Copy: ", 
        "input_template": 
        {
            "path_type": "both", 
            "prefix": "Source File", 
            "suffix": "", 
            "sequence": 3, 
            "input_type": "browser"
        }, 
        "suffix": "", 
        "list_type": "variable"
    }
]
```

The format of \<converted script>
```
preceeding regular statements\n
#PBS -o <BIC 0 LSU>\n
var_A=<BIC 1 LSU>\n
cat <BIC 2 LSU>\n
cp <BIC 3 LSU> -t $HOME\n
proceeding regular statements\n
```

### BICLSU_GUI_to_final_job_script Usage

BICLSU_GUI_to_final_job_script \<converted script path> \<input from GUI path>

#### Format of \<input from GUI path>

```
[
    {
        "value": "/home/user/output_dir",
        "sequence": 0
    }, 
    {
        "value": "2",
        "sequence": 1
    },
    {
        "value": "/home/user/document_file",
        "sequence": 2
    },
    {
        "value": "/home/user/result/source_file1",
        "sequence": 3,
        "sub_sequence": 0
    },
    {
        "value": "/home/user/result/source_file2",
        "sequence": 3,
        "sub_sequence": 1
    }
]
```

#### Program Output

The submittable version of the tagged job batch script.
```
preceeding regular statements

#PBS -o /home/user/output_dir
var_A=2
cat /home/user/document_file
cp /home/user/result/source_file1 /home/user/result/source_file2 -t $HOME

proceeding regular statements
```

## Use Cases

### BIC-LSU Project

1. The experienced user of an application tags an existing job batch script using the directives.
2. The BIC-LSU system automatically parses the tagged script with the **BICLSU_job_script_to_GUI_skeleton** and generates web page GUI.
3. The BIC-LSU system automatically generates the submittable job batch script with the **BICLSU_GUI_to_final_job_script** and input from the GUI and then submits the job.  The experienced user can instantly monitor the whole process and correct any errors.
4. The BIC-LSU preserves the converted script for subsequent GUI generation and job submission.
