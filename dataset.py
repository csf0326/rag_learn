import os
from datasets import load_dataset

dataset = load_dataset('cmrc2018')  # 加载数据集
# dataset = load_dataset('cmrc2018', cache_dir='path/to/datasets') # 指定下载路径
# print(dataset)

def create_KB(dataset):
    '''基于测试集中的context字段创建一个知识库，每10条数据为一个txt，最后不足10条的也为一个txt'''
    Context = []
    for i in dataset:
        Context.append(i['context'])
    Context = list(set(Context))  # 去重后获得256个语料

    # 计算需要的文件数
    chunk_size = 10
    total_files = (len(Context) + chunk_size - 1) // chunk_size  # 向上取整

    # 创建文件夹data_kb保存知识库语料
    os.makedirs("data_kb", exist_ok=True) 

    # 按 10 条数据一组写入多个文件
    for i in range(total_files):
        chunk = Context[i * chunk_size : (i + 1) * chunk_size]  # 获取当前 10 条数据
        file_name = f"./data_kb/part_{i+1}.txt"  # 生成文件名
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))  # 以换行符分隔写入文件
            
# 调用create_KB()创建知识库
create_KB(dataset['test'])
# 展示其中一个txt文件中的内容
with open('data_kb/part_1.txt') as f:
    print(f.read())