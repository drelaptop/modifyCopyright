#!/usr/bin/python
# coding=utf-8

import os
import re
import time

import cr_utils

# set the dir you want to modify Copyright
cocos2dx_dir = '/Users/laptop/2d-x/tests'
# add file folder filter, absolute path for now
cc_filter_folders = [
    r'^/Users/laptop/2d-x/external',
    r'^/Users/laptop/2d-x/tools',
    r'^/Users/laptop/2d-x/cocos',
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
cc_copyright_new_header= "Copyright Template.txt"


cocos_file_list = cr_utils.go_through_all_files(cocos2dx_dir, cc_file_types, cc_filter_folders)
cocos_modify_record = ["Cocos2d-x Copyright Modify..."]
# travel all files, modify needed
for ccfile in cocos_file_list:
    is_file_modified = False
    file_opened = open(ccfile, "r+")
    # lines of the source file
    cc_lines = file_opened.readlines()
    # lines after modify Copyright
    cc_lines_after = []
    # might improve
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
            cc_line_ext = cr_utils.get_copyright_prefix(cc_line, cc_pattern_all_content) + cc_replace_xm_2017
            cc_lines_after.append(cc_line_ext)
            is_file_modified = True
    # after deal a file
    single_log = ""
    if is_file_modified:
        single_log = "\nModified OK : " + file_opened.name
    else:
        # judge is need to add
        is_file_need_add = False
        if cr_utils.get_first_comment_block_length(cc_lines, r'\/\*', r'\*\/') <= 0:
            is_file_need_add = True
        # do add Copyright from template
        if not is_file_need_add:
            is_done_before = False
            for cc_line in cc_lines:
                ret = cc_line.find(cc_replace_xm_2017)
                if ret >= 0:
                    is_done_before = True
                    break
            if is_done_before:
                single_log = "\nDone Before : " + file_opened.name
            else:
                single_log = "\nNeed Review : " + file_opened.name
                # deal files only need add a single line
                cc_comment_len = cr_utils.get_first_comment_block_length(cc_lines, r'\/\*', r'\*\/')
                cc_count = 0
                cc_lines_temp = []
                is_add_single_line = False
                for cc_line in cc_lines:
                    cc_lines_temp.append(cc_line)
                    cc_count = cc_count + 1
                    # len(cc_lines[cc_count]) < 4, for content maybe " * \n"
                    if cc_count < cc_comment_len and cc_lines[cc_count-1].find("Copyright") >= 0 and len(cc_lines[cc_count]) < 4:
                        # add external line, Copyright of Xiamen Yaji Software
                        cc_line_ext = cr_utils.get_copyright_prefix(cc_line, cc_pattern_all_content) + cc_replace_xm_2017
                        cc_lines_temp.append(cc_line_ext)
                        is_add_single_line = True
                if is_add_single_line:
                    cc_lines_after = cc_lines_temp
                    single_log = "\nSingle Add  : " + file_opened.name
                else:
                    single_log = "\nNeed Review : " + file_opened.name


        else:
            single_log = "\nTemplate Add: " + file_opened.name
            file_template = open(cc_copyright_new_header, "r")
            template_lines = file_template.readlines()
            file_template.close()
            cc_lines_after = template_lines + cc_lines
            pass
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
