import os
#报告存放位置

def latest_report(filepath):
    # report_dir = r'C:\Users\Yuexl\Documents\GitHub\SeleniumLesson\trunk\unittestlihh\testreport'
    report_dir = filepath
    #返回指定的文件夹中的文件列表
    lists = os.listdir(report_dir)
    #按时间顺序对文件排序
    lists.sort(key=lambda fn:os.path.getatime(report_dir+'\\'))
    print(lists)
    print("latest report is:"+lists[-1])

    #输出最新报告路径
    file = os.path.join(report_dir,lists[-1])
    print(file)