#!/usr/bin/python
# coding=utf-8

import os
import re
import time

import cr_utils

# set the dir you want to modify Copyright
cocos2dx_dir = '/Users/laptop/2d-x'
# add file folder filter, absolute path for now
cc_filter_folders = [
    r'^/Users/laptop/2d-x/cocos/scripting/js-bindings/auto',
    r'^/Users/laptop/2d-x/cocos/scripting/lua-bindings/auto',
    r'^/Users/laptop/2d-x/web'
    ]
# file types, need to be modify
cc_file_types = r'^h$|^mm$|^c$|^hpp$|^cpp$|^java$|^js$'
# TODO: "py/lua" files need another deal

# log file name
cc_log_file = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + ".log"
# the total Copyright which need replace, use this to get prefix
cc_pattern_all_content = r'Copyright.{0,50}$'
# old Copyright part, will replace to cc_replace_ck_2016
cc_pattern_need_replace = r'-[0-5,7-9]{0,4} Chukong Technologies Inc.\n$'
# new Copyright part, replace cc_pattern_need_replace
cc_replace_ck_2016 = "-2016 Chukong Technologies Inc.\n"
# external line Copyright of Xiamen Yaji Software, it need a prefix
cc_replace_xm_2017 = "Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.\n"
# the Copyright info to add, when can't find Copyright info
cc_all_copyright_content= "cr_template.txt"


cocos_file_list = cr_utils.go_through_all_files(cocos2dx_dir, cc_file_types, cc_filter_folders)
cocos_modify_record = ["Cocos2d-x Copyright Modify..."]

def is_changed_finish(cc_lines):
    """
    return true if we can find cc_replace_xm_2017 in lines
    """
    is_done_before = False
    # can improve, reduce the range
    for cc_line in cc_lines:
        ret = cc_line.find(cc_replace_xm_2017)
        if ret >= 0:
            is_done_before = True
            break
    return is_done_before

def modify_and_add_line(cc_lines):
    """
    Copyright (c) 2013-2017 Chukong Technologies Inc.
    ->
    Copyright (c) 2013-2016 Chukong Technologies Inc.
    Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
    """
    is_changed = False
    cc_lines_ret = []
     # might improve
    for cc_line in cc_lines:
        s_ret = re.search(cc_pattern_need_replace, cc_line)
        if not s_ret:
            # not change the line
            cc_lines_ret.append(cc_line)
        else:
            # modify Chukong Copyright
            cc_line_new = re.sub(cc_pattern_need_replace, cc_replace_ck_2016, cc_line)
            cc_lines_ret.append(cc_line_new)
            # add external line, Copyright of Xiamen Yaji Software
            cc_line_ext = cr_utils.get_copyright_prefix(cc_line, cc_pattern_all_content) + cc_replace_xm_2017
            cc_lines_ret.append(cc_line_ext)
            is_changed = True
    if is_changed:
        return cc_lines_ret
    else:
        return []

def add_total_cr_if_needed(cc_lines):
    """
    No Copyright
    ->
    add all Copyright content in file cc_all_copyright_content
    """
    if cr_utils.get_first_comment_block_length(cc_lines, "r'\/\*'", "r'\*\/'") <= 0:
        file_template = open(cc_all_copyright_content, "r")
        template_lines = file_template.readlines()
        file_template.close()
        return (template_lines + cc_lines)
    return []

def add_single_line(cc_lines):
    cc_comment_len = cr_utils.get_first_comment_block_length(cc_lines, "r'\/\*'", "r'\*\/'")
    cc_count = 0
    cc_lines_ret = []
    is_changed = False
    if cc_comment_len <= 0:
        return []
    for cc_line in cc_lines:
        cc_lines_ret.append(cc_line)
        cc_count = cc_count + 1
        # len(cc_lines[cc_count]) < 4, for content maybe " * \n"
        if cc_count < cc_comment_len and cc_lines[cc_count-1].find("Copyright") >= 0 and len(cc_lines[cc_count]) < 4:
            # add external line, Copyright of Xiamen Yaji Software
            cc_line_ext = cr_utils.get_copyright_prefix(cc_line, cc_pattern_all_content) + cc_replace_xm_2017
            cc_lines_ret.append(cc_line_ext)
            is_changed = True
    if is_changed:
        return cc_lines_ret
    else:
        return []

# travel all files, modify needed
for ccfile in cocos_file_list:

    file_opened = open(ccfile, "r+")
    # lines of the source file
    cc_lines = file_opened.readlines()
    # source lines, after modified
    cc_lines_after = []
    # record log for every one file
    single_log = ""
    is_need_rewrite = False

    while True:
        if is_changed_finish(cc_lines):
            single_log = "\nDone Before : "
            break
        cc_lines_after = add_total_cr_if_needed(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nTemplate Add: "
            is_need_rewrite = True
            break
        cc_lines_after = modify_and_add_line(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nModified OK : "
            is_need_rewrite = True
            break
        # Single Add must behand other modified
        cc_lines_after = add_single_line(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nSingle Add  : "
            is_need_rewrite = True
            break
        single_log = "\nNeed Review : "
        break

    single_log = single_log + file_opened.name
    print single_log
    cocos_modify_record.append(single_log)

    if is_need_rewrite:
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

print "\n Modify records have been write to file: " + cc_log_file