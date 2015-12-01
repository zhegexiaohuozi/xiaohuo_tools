#!/usr/bin/python
# -*-coding:utf8-*-
# author xiaohuo [et.tw@163.com]
from optparse import OptionParser
import re, os, sys, time, datetime, shutil

sys.path.append(os.path.dirname(__file__))
reload(sys)
sys.setdefaultencoding('utf8')


def merge_log_by_time(input_file_list, out_file):
    u'''
    要被合并的不同的日志文件建议以不同后缀结尾，方便识别merge后的日志这一行是来自于哪个文件，如www.log.www1, www.log.www2
    合并后的日志会加上来自于哪个文件信息，例如：
        www1:[2015-11-23] [15-11-23 15:13:16.044] xxxxxxxxxxxxxxxxxxxxxxxxxx
        www2:[2015-11-25] [15-11-25 15:13:16.044] xxxxxxxxxxxxxxxxxxxxxxxxxx
        www2:[2015-11-26] [15-11-26 15:13:16.044] xxxxxxxxxxxxxxxxxxxxxxxxxx
    :param input_file_list:
    :param out_file:
    :return:
    '''
    once_max_size = 10485760  # 10M
    fds = [open(x, "r") for x in input_file_list]
    f_tmp_lines = [[] for x in xrange(0, len(fds))]
    out = open(out_file, "w")
    for i in xrange(0, len(fds)):
        f_tmp_lines[i] = fds[i].readlines(once_max_size)
    while not reduce(lambda z, y: z & y, [len(m) == 0 for m in f_tmp_lines]):
        out_lines = []
        f_tmp_lines = [pre_deal_log_lines(t_l) for t_l in f_tmp_lines]
        for j in xrange(0, len(f_tmp_lines)):
            tmp_f_name = input_file_list[j]
            for ll in f_tmp_lines[j]:
                out_lines.append(tmp_f_name[tmp_f_name.rfind('.') + 1:] + ":" + ll)
        out_lines = sorted(out_lines, key=get_sort_key)
        out.writelines(out_lines)
        for xi in xrange(0, len(fds)):
            f_tmp_lines[xi] = fds[xi].readlines(once_max_size)
    out.flush()
    out.close()
    try:
        for fd in fds:
            fd.close()
        for f in input_file_list:
            os.remove(f)
    except Exception as e:
        pass
    print "merge files done!"


def pre_deal_log_lines(lines):
    result = []
    tmp_line = ''
    for i in xrange(0, len(lines)):
        l = lines[i]
        time = get_time_by_row(l)
        if time is not None:
            result.append(tmp_line)
            tmp_line = l
        else:
            tmp_line = tmp_line + l
    result.append(tmp_line)
    return result


def render_fixed_len_host(host):
    fixed_len = 15
    if len(host) < fixed_len:
        host += ''.join(['_' for i in xrange(fixed_len - len(host))])
    return host


def get_time_by_row(row):
    date_r = re.compile(r'20\d{2}-[0-1]\d-[0-3]\d')
    time_r = re.compile(r'[0-2]\d:[0-5]\d:[0-5]\d')
    date_str = date_r.search(row, 0, 50).group() if date_r.search(row, 0, 50) is not None else None
    time_str = time_r.search(row, 0, 50).group() if time_r.search(row, 0, 50) is not None else None
    if date_str is None or time_str is None or row.startswith('  ') or row.startswith('\t'):
        return None
    return datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M:%S")


def get_sort_key(row):
    return datetime.datetime.now() if get_time_by_row(row) is None else get_time_by_row(row)


if __name__ == '__main__':
    usage = "python %prog [options] arg, use -h to get help info"
    parser = OptionParser(usage=usage, version='%prog 1.0')
    parser.add_option("-l", "--log_list", type="string", dest="log_list", help=u"需要进行合并的log列表多个文件路径用‘,’分隔")
    parser.add_option("-o", "--output", type="string", dest="output", help=u"指定输入合并后的日志路径")
    (options, args) = parser.parse_args()
    if not options.log_list or not options.output:
        print parser.get_usage()
    else:
        merge_log_by_time(options.log_list.split(','), options.output)