#!/usr/bin/env python3

import argparse
import json
import os
import re

from luaparser import ast, astnodes

parser = argparse.ArgumentParser(description="")

parser.add_argument("--import-path",
                    action="store",
                    nargs=1,
                    default="./export_grf",
                    type=str,
                    help="import path")

args = parser.parse_args()

def main(args:dict):
    skill_dict: dict = {}

    ###############################################################################################
    filename: str = "skillnamelist.lua"
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    regex_skill = re.compile(r"^SKILL_INFO_LIST\[SKID\.([^]]+)\].SkillName = \"(.*)\"")
    for line in lines:
        line: str = line.rstrip().replace("¥","")
        matches = regex_skill.match(line)
        if matches is not None:
            skill_id = matches[1]
            skill_name = matches[2]

            skill_dict[skill_id] = {
                "name" : skill_name
            }

    ###############################################################################################
    filename: str = "skillinfolist.20231209.lua"
    lua_data: str = ""
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lua_data = fp.read()

    tree = ast.parse(lua_data)
    #print(ast.to_pretty_str(tree))

    for skill_assign in tree.body.body:
        if isinstance(skill_assign, astnodes.Assign):
            skill_id: str = None
            skill_name: str = None
            skill_max_lv: int = 0
            skill_type: str = None
            sp_amount: dict[int] = {}
            attack_range: dict[int] = {}
            need_skill_list: list[dict] = []

            for data in skill_assign.values[0].fields:
                #print(ast.to_pretty_str(data)) # trace code

                if isinstance(data.key, astnodes.Number):
                    skill_id: str = data.value.s
                else:
                    if data.key.id == "SkillName":
                        skill_name = data.value.s
                    elif data.key.id == "MaxLv":
                        skill_max_lv = data.value.n
                    elif data.key.id == "Type":
                        skill_type = data.value.s
                    #elif data.key.id == "bSeperateLv":
                    #    skill_seperate_lv = ""
                    elif data.key.id == "_NeedSkillList":
                        for idx in range(len(data.value.fields)):
                            need_skill_list.append({
                                "skill_id": data.value.fields[idx].value.fields[0].value.idx.id,
                                "need_lv": data.value.fields[idx].value.fields[1].value.n
                            })
                    elif data.key.id == "SpAmount":
                        for idx in range(len(data.value.fields)):
                            sp_amount[idx] = data.value.fields[idx].value.n
                    elif data.key.id == "AttackRange":
                        for idx in range(len(data.value.fields)):
                            attack_range[idx] = data.value.fields[idx].value.n

            #print(skill_id, skill_name, skill_max_lv, skill_type, sp_amount, attack_range) # trace code

            skill_dict[skill_id] = {
                "name": skill_name,
                "max_lv": skill_max_lv,
                "type": skill_type,
                "sp_amount": sp_amount,
                "attack_range": attack_range,
                "need_skill_list": need_skill_list
            }

    with open(os.path.abspath("./skill_data.json"), "w", encoding="utf-8") as fp:
        fp.write(json.dumps(skill_dict, sort_keys=True,ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main(args)
