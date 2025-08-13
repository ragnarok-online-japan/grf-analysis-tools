#!/usr/bin/env python3.13

import argparse
import os

import yaml
from luaparser import ast, astnodes
import polars as pl

parser = argparse.ArgumentParser(description="")

parser.add_argument("--import-path",
                    action="store",
                    nargs=1,
                    default="./export_grf",
                    type=str,
                    help="import path")

args = parser.parse_args()

def main(args: argparse.Namespace):
    skill_dict: dict = {}

    ###############################################################################################

    filename: str = "skillinfolist.lua"
    lua_data: str = ""
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lua_data = fp.read()

    tree = ast.parse(lua_data)

    for skill_field in tree.body.body[0].values[0].fields: # type: ignore
        if isinstance(skill_field, astnodes.Field):
            skill_id: str = skill_field.key.idx.id # type: ignore
            skill_name: str|None = None
            skill_max_lv: int = 0
            skill_type: str|None = None
            skill_seperate_lv: bool = False
            sp_amount: dict = {}
            attack_range: dict = {}
            need_skill_list: list = []

            for data in skill_field.value.fields: # type: ignore
                #print(ast.to_pretty_str(data)) # trace code

                if isinstance(data.key, astnodes.Name) == False:
                    continue

                if data.key.id == "SkillName":
                    skill_name = data.value.s
                elif data.key.id == "MaxLv":
                    skill_max_lv = data.value.n
                elif data.key.id == "Type":
                    skill_type = data.value.s
                elif data.key.id == "bSeperateLv":
                    if isinstance(data.value, astnodes.TrueExpr):
                        skill_seperate_lv = True
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

            #print(skill_id, skill_name, skill_max_lv, skill_type, skill_seperate_lv, sp_amount, attack_range) # trace code

            skill_dict[skill_id] = {
                "name": skill_name,
                "max_lv": skill_max_lv,
                "type": skill_type,
                "seperate_lv": skill_seperate_lv,
                "sp_amount": sp_amount,
                "attack_range": attack_range,
                "need_skill_list": need_skill_list
            }

    ###############################################################################################

    filename: str = "skillid.lua"
    lua_data: str = ""
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lua_data = fp.read()

    tree = ast.parse(lua_data)

    for skill_field in tree.body.body[0].values[0].fields: # type: ignore
        if isinstance(skill_field, astnodes.Field):
            skill_id: str = skill_field.key.id # type: ignore
            skill_id_num: int = skill_field.value.n # type: ignore

            if skill_id not in skill_dict:
                skill_dict[skill_id] = {}

            skill_dict[skill_id]["id_num"] = skill_id_num

    ###############################################################################################

    filename = "skill.yaml"
    print("export :", filename)
    records = []
    utf8_fields = {"id", "name", "type", "sp_amount", "attack_range", "need_skill_list"}
    for key, value in skill_dict.items():
        value = value.copy()
        value["id"] = key
        for field in utf8_fields:
            if field in value:
                if value[field] is None:
                     value[field] = ""
                elif not isinstance(value[field], str):
                     value[field] = str(value[field])
        records.append(value)

    with open(os.path.abspath(filename), "w", encoding="utf-8") as fp:
        yaml.dump(records, fp, encoding='utf8', allow_unicode=True)

if __name__ == "__main__":
    main(args)
