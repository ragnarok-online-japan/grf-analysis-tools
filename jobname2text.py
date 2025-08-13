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
    job_dict: dict = {}

    ###############################################################################################

    filename: str = "pcjobname.lua"
    lua_data: str = ""
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lua_data = fp.read()

    tree = ast.parse(lua_data)

    for job_field in tree.body.body[0].values[0].fields: # type: ignore
        if isinstance(job_field, astnodes.Field):
            id: str = job_field.key.idx.id # type: ignore
            name: str = job_field.value.s # type: ignore
            job_dict[id] = {
                "id": id,
                "name": name,
            }

    ###############################################################################################


    filename: str = "jobinheritlist.lua"
    lua_data: str = ""
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lua_data = fp.read()

    tree = ast.parse(lua_data)

    for job_field in tree.body.body[0].values[0].fields: # type: ignore
        if isinstance(job_field, astnodes.Field):
            name: str = job_field.key.id # type: ignore
            id_num: str = job_field.value.n # type: ignore

            if name in job_dict:
                job_dict[name]["id_num"] = id_num

    ###############################################################################################

    filename = "jobname.yaml"
    print("export :", filename)
    records = []
    utf8_fields = {"id", "name"}
    for _, value in job_dict.items():
        value = value.copy()
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
