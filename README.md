# Job-Script-to-GUI
A set of directive rules and a parser for converting a job batch script into some graphical user interface.

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

## Program Input

A job batch script file tagged with directives.

```
preceeding regular statements

#PBS -o <BIC input,file_browser,directory,Output Directory: , LSU>
var_A=<BIC input,text,Parallelism: ,4,Thread(s) LSU>
cat <BIC input,file_browser,both,Document to Display: , LSU>
cp <BIC var_list,Files to Copy: ,,<BIC input,file_browser,both,Source File, LSU> LSU> -t $HOME

proceeding regular statements
```

## Program Output

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
        "id_sequence": 0, 
        "input_type": "browser"
    }, 
    {
        "default": "4", 
        "input_type": "text", 
        "prefix": "Parallelism: ", 
        "suffix": "Thread(s)", 
        "id_sequence": 1
    }, 
    {
        "path_type": "both", 
        "prefix": "Document to Display: ", 
        "suffix": "", 
        "id_sequence": 2, 
        "input_type": "browser"
    }, 
    {
        "prefix": "Files to Copy: ", 
        "input_template": 
        {
            "path_type": "both", 
            "prefix": "Source File", 
            "suffix": "", 
            "id_sequence": 3, 
            "input_type": "browser"
        }, 
        "suffix": "", 
        "list_type": "variable"
    }
]
```

The format of \<converted script>
```
"preceeding regular statements\n
#PBS -o <BIC 0 LSU>\n
var_A=<BIC 1 LSU>\n
cat <BIC 2 LSU>\n
cp <BIC 3 LSU> -t $HOME\n
proceeding regular statements\n"
```
