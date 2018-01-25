#!/usr/bin/python

import os
import re
import time

# set the dir you want to modify Copyright
cocos2dx_dir = '/Users/laptop/2d-x'
# cocos2dx_dir = 'F:\cocos2d-x-3.16\cmake'
# add file folder filter, absolute path for now
cc_filter_folders = [r'^/Users/laptop/2d-x/external',r'^/Users/laptop/2d-x/tools']
# file types, need to be modify
cc_file_types = r'^h$|^c$|^cc$|^cpp$|^java$|^json$|^txt$|^py$|^am$|^sh$|^mk$|^Makefile$|^xml$|^README$'

# log file name
cc_log_file = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + ".log"
# the total Copyright which need replace, use this to get prefix
cc_pattern_all_content = r'Copyright.{0,20} Chukong Technologies Inc.\n$'
# old Copyright part, will replace to cc_replace_ck_2016
cc_pattern_need_replace = r'-[0-5,7-9]{0,4} Chukong Technologies Inc.\n$'
# new Copyright part, replace cc_pattern_need_replace
cc_replace_ck_2016 = "-2016 Chukong Technologies Inc.\n"
# external line Copyright of Xiamen Yaji Software, it need a prefix
cc_replace_xm_2017 = "Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.\n"
# TODO: the Copyright info to add, when can't find Copyright info
cc_copyright_new_header= ""

# get Copyright prefix
def get_copyright_prefix(single_line):
    """
    get Copyright prefix

    @param single_line: single line, might be Copyright line
    @return: string before Copyright, "", "", " * " or others
    @rtype: string
    """
    copyright_prefix = ""
    search_ret = re.search(cc_pattern_all_content, single_line)

    if search_ret != None:
        position = search_ret.span()
        copyright_prefix = single_line[0:position[0]]

    return copyright_prefix

# reuse and custom from https://github.com/jingjingpiggy/copyright
def go_through_all_files(dir_path):
    """
    Go throught all files under dir_path, filter file type and folder

    @param dir_path: relative or absolute directory path
    @return: all eligible files
    @rtype: list
    """
    def filter_file(f):
        suffix_pattern = re.compile(cc_file_types)
        r = suffix_pattern.match(f.split('.')[-1])
        if not r:
            return None
        else:
            return r

    # return true if find it, other false
    def filter_folder(path):
        for cc_single_filter in cc_filter_folders:
            r = re.search(cc_single_filter, path)
            if r:
                return True
        return False

    files_set = set()
    for root, dirs, files in os.walk(dir_path):
        if filter_folder(root):
            continue
        for filespath in files:
            if filter_file(filespath):
                files_set.add(os.path.join(root,filespath))

    return files_set

cocos_file_set = go_through_all_files(cocos2dx_dir)
cocos_modify_record = ["modify cocos Copyright"]
# travel all files, modify needed
for ccfile in cocos_file_set:
    file_opened = open(ccfile, "r+")
    # lines of the source file
    cc_lines = file_opened.readlines()
    # lines after modify Copyright
    cc_lines_after = []
    for cc_line in cc_lines:
        s_ret = re.search(cc_pattern_need_replace, cc_line)
        if not s_ret:
            # not change the line
            cc_lines_after.append(cc_line)
        else:
            # modify Chukong Copyright
            cc_line_new = re.sub(cc_pattern_need_replace, cc_replace_ck_2016, cc_line)
            cc_lines_after.append(cc_line_new)
            # add external line, Copyright of Xiamen Yaji Software
            cc_line_ext = get_copyright_prefix(cc_line) + cc_replace_xm_2017
            cc_lines_after.append(cc_line_ext)

            single_log = "\nCopyright modified: " + file_opened.name
            print single_log
            cocos_modify_record.append(single_log)
        
    # empty old file, add write lines after modify
    file_opened.seek(0, 0)
    file_opened.truncate()
    file_opened.writelines(cc_lines_after)
    # close file
    file_opened.close()
    # write log
    file_log = open(cc_log_file, "w+")
    file_log.writelines(cocos_modify_record)
    file_log.close()
