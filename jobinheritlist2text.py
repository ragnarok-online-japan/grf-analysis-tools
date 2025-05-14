#!/usr/bin/env python3.13

import argparse
import os

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

def main(args:dict):
    job_dict: dict = {}

    ###############################################################################################

    filename: str = "jobinheritlist.lua"
    lua_data: str = ""
    with open(os.path.abspath("{:}/{:}".format(args.import_path, filename)), "r", encoding="utf-8") as fp:
        lua_data = fp.read()

    tree = ast.parse(lua_data)

    for job_field in tree.body.body[0].values[0].fields:
        if isinstance(job_field, astnodes.Field):
            name: str = job_field.key.id
            id_num: str = job_field.value.n

            job_dict[name] = {
                "name": name,
                "id_num": id_num,
            }

    ###############################################################################################

    filename = "jobs.jsonl"
    print("export :", filename)
    records = []
    utf8_fields = {"name"}
    for _, value in job_dict.items():
        value = value.copy()
        for field in utf8_fields:
            if field in value:
                if value[field] is None:
                     value[field] = ""
                elif not isinstance(value[field], str):
                     value[field] = str(value[field])
        records.append(value)
    df = pl.from_dicts(records)
    df.write_ndjson(filename)

if __name__ == "__main__":
    main(args)
