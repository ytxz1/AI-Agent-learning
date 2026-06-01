"""练习 2：对比不同切分参数。

练习目标：
理解 chunk_size 和 chunk_overlap 如何影响切分结果。

答案写在文件后面：
chunk_size 越小，切出来的文本块越多；
chunk_overlap 越大，相邻文本块重复内容越多，上下文更连续，但冗余也更多。
"""

print("练习 2 答案：")
print("1. 在 config.py 中把 CHUNK_SIZE 改成 100，运行 python 02_text_splitter.py。")
print("2. 再把 CHUNK_SIZE 改成 300，重新运行。")
print("3. 对比结果：100 更碎，300 更完整；overlap 越大，上下文越不容易断。")

