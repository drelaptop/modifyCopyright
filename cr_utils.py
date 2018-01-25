#!/usr/bin/python
# coding=utf-8

import os
import re

# get Copyright prefix
def get_copyright_prefix(single_line, pattern_content):
    """
    get Copyright prefix

    @param single_line: single line, might be Copyright line
    @param pattern_content: pattern the main content
    @return: string before Copyright, "", "", " * "
    @rtype: string
    """
    copyright_prefix = ""
    search_ret = re.search(pattern_content, single_line)

    if search_ret != None:
        position = search_ret.span()
        copyright_prefix = single_line[0:position[0]]

    return copyright_prefix

# reuse and custom from https://github.com/jingjingpiggy/copyright
def go_through_all_files(dir_path, file_types_need, file_folders_except):
    """
    Go throught all files under dir_path, filter file type and folder

    @param dir_path: relative or absolute directory path
    @return: all eligible files
    @rtype: list
    """
    def filter_file(file_name):
        suffix_pattern = re.compile(file_types_need)
        ret = suffix_pattern.match(file_name.split('.')[-1])
        if not ret:
            return None
        else:
            return ret

    # return true if find it, other false
    def filter_folder(path):
        for single_filter in file_folders_except:
            ret = re.search(single_filter, path)
            if ret:
                return True
        return False

    files_list = []
    for root, dirs, files in os.walk(dir_path):
        if filter_folder(root):
            continue
        for file_name in files:
            if filter_file(file_name):
                files_list.append(os.path.join(root,file_name))

    return files_list

def get_first_comment_block_length(line_list, up_flag, right_flag):
    """
    get first Copyright comment block length in source, which style like:
    /***
    ...Copyright..
    ***/
    @param line_list: all lines of a source file
    @param up_flag: find comment flag, such as r'\/\*'
    @param up_flag: find comment flag, such as r'\*\/'
    @return: length of first Copyright comment lines, 0 if not find
    @rtype: int
    """
    is_get_comment_up_line = False
    is_get_comment_down_line = False
    cc_comment_num = 0
    for cc_line in line_list:
        cc_comment_num = cc_comment_num + 1
        up_ret = re.search(up_flag, cc_line)
        if up_ret and cc_comment_num < 3:
            is_get_comment_up_line = True
        if is_get_comment_up_line:
            down_ret = re.search(right_flag, cc_line)
            if down_ret:
                is_get_comment_down_line = True
                break
    # 
    if cc_comment_num > 1:
        for i in range(0, cc_comment_num - 1):
            if line_list[i].find("Copyright") >= 0:
                return cc_comment_num
    return 0