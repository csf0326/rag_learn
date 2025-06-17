import lazyllm
from lazyllm import bind
# # 文档加载
documents = lazyllm.Document(dataset_path="/home/mnt/zhuchaoshuai/data_kb")

prompt = 'You will act as an AI question-answering assistant and complete a dialogue task. \
          In this task, you need to provide your answers based on the given context and questions.'
with lazyllm.pipeline() as ppl:
    ppl.retriever = lazyllm.Retriever(doc=documents, group_name="CoarseChunk", similarity="bm25_chinese", topk=3)
    ppl.formatter = (lambda nodes, query: {"query": query, "context_str": "".join([node.get_content() for node in nodes])}) | bind(query=ppl.input)
    ppl.llm = lazyllm.OnlineChatModule().prompt(lazyllm.ChatPrompter(instruction=prompt, extra_keys=['context_str']))

lazyllm.WebModule(ppl, port=23466).start().wait()

