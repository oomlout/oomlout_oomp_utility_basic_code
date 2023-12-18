import os
import yaml
import glob

folder_configuration = "configuration"
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
file_configuration = os.path.join(folder_configuration, "configuration.yaml")
#check if exists
if not os.path.exists(file_configuration):
    print(f"no configuration.yaml found in {folder_configuration} using default")
    file_configuration = os.path.join(folder_configuration, "configuration_default.yaml")

folder_navigation = "navigation"

#import configuration
configuration = {}
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)


def main(**kwargs):
    folder = kwargs.get("folder", f"{os.path.dirname(__file__)}/parts")
    folder = folder.replace("\\","/")
    
    kwargs["configuration"] = configuration
    print(f"running utility for: {folder}")
    create_recursive(**kwargs)

def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    for item in os.listdir(folder):
        directory_absolute = os.path.join(folder, item)
        directory_absolute = directory_absolute.replace("\\","/")
        if os.path.isdir(directory_absolute):
            #if base.yaml exists in the folder and working.yaml does not make a copy of base and call it working.yaml
            if os.path.exists(os.path.join(directory_absolute, "base.yaml")) and not os.path.exists(os.path.join(directory_absolute, "working.yaml")):
                #copy base.yaml to working.yaml
                import shutil
                shutil.copyfile(os.path.join(directory_absolute, "base.yaml"), os.path.join(directory_absolute, "working.yaml"))
            #if working.yaml exists in the folder
            if os.path.exists(os.path.join(directory_absolute, "working.yaml")):
                kwargs["directory_absolute"] = directory_absolute
                create(**kwargs)

def create(**kwargs):
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())    
    kwargs["directory_absolute"] = directory_absolute    
    generate(**kwargs)
    

def generate(**kwargs):    
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())
    folder = kwargs.get("folder", os.getcwd())
    yaml_file = os.path.join(directory_absolute, "working.yaml")
    kwargs["yaml_file"] = yaml_file
    #load the yaml file
    details = {}
    with open(yaml_file, 'r') as stream:
        try:
            details = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)
    
    if details != {}:        
        print(f"    generating basic code for {directory_absolute}")
        kwargs["details"] = details
    
        kwargs = add_id(**kwargs)
        kwargs = add_name(**kwargs)
        kwargs = add_md5(**kwargs)
        kwargs = add_oomp_moji(**kwargs)

        details = kwargs.get("details", {})
        #save updated details to working,yaml
        with open(yaml_file, 'w') as outfile:
            yaml.dump(details, outfile, default_flow_style=False)

    else:
        print(f"no yaml file found in {directory_absolute}")    

def add_id(**kwargs):
    details = kwargs.get("details", {})
    id = details.get("id", None)
    clas = details.get("classification", None)
    id_no_class = id.replace(f"{clas}_","")        
    details["id_no_class"] = id_no_class
    typ = details.get("type",None)
    id_no_type = id_no_class.replace(f"{typ}_","")        
    details["id_no_type"] = id_no_type
    siz = details.get("size",None)
    id_no_size = id_no_type.replace(f"{siz}_","")
    details["id_no_size"] = id_no_size
    col = details.get("color",None)    
    id_no_color = id_no_size.replace(f"{col}_","")
    details["id_no_color"] = id_no_color

    details["oomp_key"] = f'oomp_{id}'
    details["github_link"] = f"https://github.com/oomlout/oomlout_oomp_part_src/tree/main/parts/{id}" 
    
    #add the directory
    details["directory"] = f'parts/{id}'   

    return kwargs

def add_md5(**kwargs):
    details = kwargs.get("details", {})
    #add a md5 hash of the id as a keyed item to kwargs
    import hashlib
    id = details.get("id", None)
    details["md5"] = hashlib.md5(id.encode()).hexdigest()
    #trim md5 to 6 and add it as md5_6
    details["md5_5"] = details["md5"][0:5]
    details["md5_5_upper"] = details["md5"][0:5].upper()
    md5_6 = details["md5"][0:6]
    details["md5_6"] = md5_6
    details["md5_6_upper"] = details["md5_6"].upper()

    md5_6_alpha = hex_to_base36(details["md5_6"])
    details["md5_6_alpha"] = md5_6_alpha
    details["md5_6_alpha_upper"] = details["md5_6_alpha"].upper()
    
    details["md5_10"] = details["md5"][0:10]
    details["md5_10_upper"] = details["md5_10"].upper()

    return kwargs



def add_name(**kwargs):
    details = kwargs.get("details", {})
    #add name, the name is the id with proper capitalization and _ replaced with ' '
    id = details.get("id", None)
    details["name"] = id.replace("_", " ").title()
    id_no_class = details.get("id_no_class", None)
    name_no_class = id_no_class.replace("_", " ").title()
    details["name_no_class"] = name_no_class
    id_no_type = details.get("id_no_type", None)
    name_no_type = id_no_type.replace("_", " ").title()
    details["name_no_type"] = name_no_type
    id_no_size = details.get("id_no_size", None)
    name_no_size = id_no_size.replace("_", " ").title()
    details["name_no_size"] = name_no_size
    id_no_color = details.get("id_no_color", None)
    name_no_color = id_no_color.replace("_", " ").title()
    details["name_no_color"] = name_no_color
    return kwargs

def add_oomp_moji(**kwargs):
    details = kwargs.get("details", {})
    md5_6 = details.get("md5_6", None)
    # impotoomp_word from this files directory even if that isn't the cwd
    import sys
    sys.path.append(os.path.dirname(__file__))
    import oomp_word
    oomp_word_value = oomp_word.get_oomp_word(md5_6, style="string")
    details["oomp_word"] = oomp_word_value
    details["oomp_word_list"] = oomp_word.get_oomp_word(md5_6, style="list")
    details["oomp_word_emoji"] = oomp_word.get_oomp_word(md5_6, style="emoji")
    details["oomp_word_emoji_list"] = oomp_word.get_oomp_word(md5_6, style="emoji_list")

    return kwargs

###### helpers

def hex_to_base36(hex_value):
    # Convert the hex value to an integer
    decimal_value = int(hex_value, 16)

    # Encode the integer as base36
    base36_value = ''
    while decimal_value > 0:
        decimal_value, remainder = divmod(decimal_value, 36)
        base36_digit = '0123456789abcdefghijklmnopqrstuvwxyz'[remainder]
        base36_value = base36_digit + base36_value

    return base36_value









if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    #folder = "C:/gh/oomlout_oobb_version_4/things"
    folder = "C:/gh/oomlout_oomp_current_version"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    main(**kwargs)

