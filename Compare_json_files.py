import json
import jsondiff
import csv
from tabulate import tabulate

lst = []

def character_set(resp1, policy_config1, key, key_r1):
    character_set = resp1[key_r1]
    for keyx in character_set.keys():
        character_set_metachar = resp1[key_r1][keyx]
        for keyy in character_set_metachar:
            var1 = policy_config1[key][key_r1][keyx][keyy]
            #print(var1)
            character_set = {}
            character_set[keyy] = var1
            resp1[key_r1] = character_set
    return resp1


def module(resp1, policy_config1, key, key_r1):
    module = resp1[key_r1]
    for keyx in module.keys():
        var1 = policy_config1[key][key_r1][keyx]
        module = {}
        module[keyx] = var1
        resp1[key_r1] = module
    return resp1

def identify1(resp1, policy_config1, key):
    for key_r1 in resp1.keys():
        if key_r1 == "character_set":
            character_set(resp1, policy_config1, key, key_r1)

        if key_r1 == "violation" or key_r1 == "evasion_setting" or key_r1 == "signature":
            module(resp1, policy_config1, key, key_r1)
        else:
            pass
    return resp1

def identify2(resp2, policy_config2, key):
    for key_r1 in resp2.keys():
        if key_r1 == "character_set":
            character_set = resp2[key_r1]
            for keyx in character_set.keys():
                character_set_metachar = resp2[key_r1][keyx]
                for keyy in character_set_metachar:
                    var1 = policy_config2[key][key_r1][keyx][keyy]
                    character_set = {}
                    character_set[keyy] = var1
                    resp2[key_r1] = character_set
    return resp2



def compare_policies(policy_config1, policy_config2, lst):
    NA = "Not configured"
    keys = policy_config1.keys() | policy_config2.keys()
    #print(keys)
    for key in keys:
        lst_rec = []
        try:
            if policy_config1[key] != policy_config2[key] or policy_config2[key] != policy_config1[key]:

                lst_rec.clear()
                lst_rec.append(key)
                val1 = policy_config1[key]
                val2 = policy_config2[key]
                resp1 = jsondiff.diff(val1, val2)
                resp2 = jsondiff.diff(val2, val1)

                #print(resp1)
                #print(resp2)

                identify1(resp1, policy_config1, key)
                identify2(resp2, policy_config2, key)

                lst_rec.append(resp1)
                lst_rec.append(resp2)
                lst.append(lst_rec)

        except KeyError:
            if key not in policy_config1:
                lst_rec.clear()
                val2 = f"{key}:{NA}"
                val1 = f"{key}:{policy_config1[key]}"
                lst_rec.append(val1)
                lst_rec.append(val2)
                lst.append(lst_rec)
            if key not in policy_config2:
                lst_rec.clear()
                val2 = f"{key}:{NA}"
                val1 = f"{key}:{policy_config2[key]}"
                lst_rec.append(val1)
                lst_rec.append(val2)
                lst.append(lst_rec)
    return lst


def table(policy_config1, policy_config2, lst):
    compare_policies(policy_config1, policy_config2, lst)
    output = tabulate(lst, headers=["       ", f"POLICY 1", f"POLICY 2"], tablefmt='fancy_grid')
    print(output)
    file = open("differences.txt", "w", encoding="utf-8")
    file.write(output)
    file.close()

    with open("diferences.csv", 'w', newline='') as csvfile:
        headers = [' ' ,'Policy 1', 'Policy 2']
        writer = csv.DictWriter(csvfile, fieldnames= headers)
        writer.writeheader()
        writer.writerow(lst)

    print("Done")

if __name__ == "__main__":
    try:
        print("Coxmparing policies ...")
        with open("test1.json", "r") as json_file1:
            policy_config1 = json.load(json_file1)
            policy_config1 = policy_config1["policy"]
        with open("test2.json", "r") as json_file2:
            policy_config2 = json.load(json_file2)
            policy_config2 = policy_config2["policy"]

        table(policy_config1, policy_config2, lst)
    except NameError as e:
        print(e)
