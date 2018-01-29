#!/usr/bin/python
# coding=utf-8

import os
import re
import time
import io
import sys
import chardet
import codecs
import cr_utils

reload(sys)
sys.setdefaultencoding('utf-8')

# set the dir you want to modify Copyright
cocos2dx_dir = '/Users/laptop/2d-x'
# add file folder filter, absolute path for now
cc_filter_folders = [
    r'^/Users/laptop/2d-x/cocos/scripting/js-bindings/auto',
    r'^/Users/laptop/2d-x/cocos/scripting/lua-bindings/auto',
    r'^/Users/laptop/2d-x/web',# sub modual
    r'^/Users/laptop/2d-x/external',## sub modual and third party
    r'^/Users/laptop/2d-x/tools/bindings-generator',# sub modual
    r'^/Users/laptop/2d-x/tools/cocos2d-console',# sub modual
    r'^/Users/laptop/2d-x/cocos/editor-support/spine', #not belong to cocos
    r'^/Users/laptop/2d-x/tests/cpp-tests/Classes/SpineTest',#not belong to cocos
    r'^/Users/laptop/2d-x/tools/simulator/libsimulator/lib/protobuf-lite/google',#not belong to cocos
    r'^/Users/laptop/2d-x/tests/cpp-tests/Classes/Box2DTestBed',#not belong to cocos
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

comment_up_edge = "r'\/\*'"
comment_down_edge =  "r'\*\/'"

cocos_file_list = cr_utils.go_through_all_files(cocos2dx_dir, cc_file_types, cc_filter_folders)
cocos_modify_record = ["Cocos2d-x Copyright Modify..."]

def is_changed_finish(cc_lines):
    """
    return true if we can "Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd." in lines
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
    if cr_utils.get_first_comment_block_length(cc_lines, comment_up_edge, comment_down_edge) <= 0:
        file_template = open(cc_all_copyright_content, "r")
        template_lines = file_template.readlines()
        file_template.close()
        return (template_lines + cc_lines)
    return []

def add_single_line(cc_lines):
    """
    Copyright (c) 2012 cocos2d-x.org
        
    ->
    Copyright (c) 2012 cocos2d-x.org
    Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.

    """
    cc_comment_len = cr_utils.get_first_comment_block_length(cc_lines, comment_up_edge, comment_down_edge)
    cc_count = 0
    cc_lines_ret = []
    is_changed = False
    is_cc = is_cocos_comment(cc_lines)
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
    if is_cc and is_changed:
        return cc_lines_ret
    else:
        return []

def add_after_last_cy(cc_lines):
    """
    * Copyright (c) 2012 cocos2d-x.org
    * http://www.cocos2d-x.org
    *
    * Copyright 2012 Yannick Loriot. All rights reserved.
    * http://yannickloriot.com
    * 
    * Permission is hereby granted,
    ->
    * Copyright (c) 2012 cocos2d-x.org
    * http://www.cocos2d-x.org
    *
    * Copyright 2012 Yannick Loriot. All rights reserved.
    * http://yannickloriot.com
    * 
    * Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
    * 
    * Permission is hereby granted,
    """
    is_cc = is_cocos_comment(cc_lines)
    cr_length = cr_utils.get_first_comment_block_length(cc_lines, comment_up_edge, comment_down_edge)
    line_num = 0
    cc_lines_ret = []
    is_changed = False
    for cc_line in cc_lines:
        line_num = line_num + 1
        if line_num > cr_length:
            break
        find_ret = cc_line.find("Permission is hereby granted")
        if find_ret >= 0:
            cc_prefix = cc_line[0:find_ret]
            cc_lines_ret.append(cc_prefix + cc_replace_xm_2017)
            cc_lines_ret.append(cc_prefix + "\n")
            is_changed = True
        cc_lines_ret.append(cc_line)
    if is_cc and is_changed:
        return cc_lines_ret
    else:
        return []

# judge the comment block is in a cocos2d-x self's source file
def is_cocos_comment(lines):
    cc_comment_len = cr_utils.get_first_comment_block_length(cc_lines, comment_up_edge, comment_down_edge)
    # use to prevent to change the third party source file
    exist_cocos_flag = False
    exist_chukong_flag = False
    if cc_comment_len <= 0:
        return False
    lin_num = 0
    for cc_line in cc_lines:
        lin_num = lin_num + 1
        find_cc = cc_line.find("cocos2d-x")
        if find_cc >= 0:
            exist_cocos_flag = True
        find_ck = cc_line.find("Chukong")
        if find_ck >= 0:
            exist_chukong_flag = True
        if lin_num >= cc_comment_len:
            break
    return (exist_chukong_flag or exist_cocos_flag)

# old files have encode utf-8-sig
def cocos_get_encode(filename):
    bytes = min(32, os.path.getsize(filename))
    fo = open(filename, 'rb')
    raw = fo.read(bytes)
    encoding = ""
    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        encoding = result['encoding']
    fo.close()
    # it might be a  mistake when judge a encode type
    if encoding == 'ascii':
        encoding = 'utf-8'
    return encoding

def cocos_lines2utf8(lines):
    lines_ret = []
    for line in lines:
        lines_ret.append(line.decode('utf-8'))
    return lines_ret

# travel all files, modify needed
for ccfile in cocos_file_list:

    cc_encode = cocos_get_encode(ccfile)
    file_opened = io.open(ccfile, "r+", encoding=cc_encode)
    # lines of the source file
    print file_opened.name
    cc_lines = file_opened.readlines()
    # source lines, after modified
    cc_lines_after = []
    # record log for every one file
    single_log = ""
    is_need_rewrite = False

    while True:
        if is_changed_finish(cc_lines):
            single_log = "\nDone Before - "
            break
        cc_lines_after = add_total_cr_if_needed(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nTemplate Add- "
            is_need_rewrite = True
            break
        cc_lines_after = modify_and_add_line(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nModified OK - "
            is_need_rewrite = True
            break
        # Single Add must behand other modified
        cc_lines_after = add_single_line(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nSingle Add  - "
            is_need_rewrite = True
            break
        cc_lines_after = add_after_last_cy(cc_lines)
        if len(cc_lines_after) > 0:
            single_log = "\nAdd In Last - "
            is_need_rewrite = True
            break
        single_log = "\nNeed Review - "
        break
    if cc_encode:
        encode_log = 'File Type(' + cc_encode + ') '
    else:
        encode_log = 'File Type(error) ' 
    
    single_log = single_log + encode_log + file_opened.name
    print single_log
    cocos_modify_record.append(single_log)

    if is_need_rewrite:
        # empty old file, add write lines after modify
        file_opened.seek(0, 0)
        file_opened.truncate()
        cc_lines_after = cocos_lines2utf8(cc_lines_after)
        file_opened.writelines(cc_lines_after)
    # close file
    file_opened.close()

# write log
file_log = open(cc_log_file, "w+")
file_log.writelines(cocos_modify_record)
file_log.close()

print "\n Modify records have been write to file: " + cc_log_file