# Job-Script-to-GUI
A set of directive rules and parsers for converting a job batch script into some graphical user interface and retrieving the user input back into the script.

## Supported Directives

**BIC-LSU Input Block**<br />
\<BIC input,text,\<prefix>,\<default>,\<suffix> LSU><br />
\<BIC input,file_brwoser,\<allowed path type>,\<prefix>,\<suffix> LSU><br />
"allowed path type" can be "all" or "directory".

**BIC-LSU List Block**<br />
\<BIC list,\<prefix>,\<suffix>,\<BIC-LSU input block 1>,...,\<BIC-LSU input block N> LSU>

**BIC-LSU Variable-length List Block**<br />
\<BIC var_list,\<prefix>,\<suffix>,\<BIC-LSU input block template> LSU><br />
"BIC-LSU input block template" can be any one of the "BIC-LSU Input Block".

## Program Usage

1. Run **BICLSU_JobScript_to_GUISkeleton.py** on the job batch script tagged with directives to generate a coverted script and a skeleton for creating a GUI.  The converted script and the skeleton maintain the mapping of each pair of the variable in the converted script and the variables in the skeleton using one unique sequence number. 
2. Run **BICLSU_GUIInput_to_JobScript.py** to map the inputs collected from the GUI back into the converted script to generate a submittable job batch script.

### BICLSU_JobScript_to_GUISkeleton.py Usage

BICLSU_JobScript_to_GUISkeleton.py \<tagged job script path>

#### Format of \<tagged job script path>

```
preceeding regular statements

#PBS -o <BIC input,file_browser,directory,Output Directory: , LSU>
var_A=<BIC input,text,Parallelism: ,4,Thread(s) LSU>
cat <BIC input,file_browser,all,Document to Display: , LSU>
cp <BIC var_list,Files to Copy: ,,<BIC input,file_browser,all,Source File, LSU> LSU> -t $HOME

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
        "component_type": "input",
        "path_type": "directory", 
        "prefix": "Output Directory: ", 
        "suffix": "", 
        "sequence": 0, 
        "input_type": "browser"
    }, 
    {
        "component_type": "input",
        "default": "4", 
        "input_type": "text", 
        "prefix": "Parallelism: ", 
        "suffix": "Thread(s)", 
        "sequence": 1
    }, 
    {
        "component_type": "input",
        "path_type": "all", 
        "prefix": "Document to Display: ", 
        "suffix": "", 
        "sequence": 2, 
        "input_type": "browser"
    }, 
    {
        "component_type": "var_list",
        "prefix": "Files to Copy: ", 
        "input_template": 
        {
            "component_type": "input",
            "path_type": "all", 
            "prefix": "Source File", 
            "suffix": "", 
            "sequence": 3, 
            "input_type": "browser"
        }, 
        "suffix": ""
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

### BICLSU_GUIInput_to_JobScript.py Usage

BICLSU_GUIInput_to_JobScript.py \<converted script path> \<input from GUI path>

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
2. The BIC-LSU system automatically parses the tagged script with the **BICLSU_JobScript_to_GUISkeleton.py** and generates web page GUI.
3. The BIC-LSU system automatically generates the submittable job batch script with the **BICLSU_GUIInput_to_JobScript.py** and input from the GUI and then submits the job.  The experienced user can instantly monitor the whole process and correct any errors.
4. The BIC-LSU preserves the skeleton and converted script for subsequent GUI generation and job submission.
