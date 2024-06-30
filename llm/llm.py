from langchain_community.utilities.sql_database import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import re

def callDatabase():
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    db_info = db.get_table_info()
    db_table_name = db.get_table_names()
    return db, db_info, db_table_name

def makeTemplate():
    template = """
    당신은 10년차 데이터베이스 전문가 입니다. 여러 데이터를 가지고 있으며 사용자는 한 개 혹은 여러 개의 데이터를 조합하여 사용하고 싶어합니다.
    사용자는 데이터사이언티스이며 데이터를 제공받아 새로운 인사이트를 도출하려고 합니다. 테이블명에 주의하여 사용자에게 알맞은 정보를 제공해주세요.
    아래 조건에 맞춰 적절한 답변을 해주세요.
    1. 쿼리가 나오는 이유를 100자 이상 200자 이하로 설명해주세요.
    2. 사용자 질문에 알맞는 쿼리를 제공해주세요.
    
    #대화내용
    {chat_history}
    ----
    사용자: {question}
    엑셀전문가:"""
    prompt = PromptTemplate.from_template(template)
    return prompt

def callLLM():
    API_KEY = "(입력)"
    API_BASE = "(입력)"
    
    llm = ChatOpenAI(
        model="gpt-4o",
        openai_api_key = API_KEY,
        openai_api_base = API_BASE,
    )
    
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    conversation = ConversationChain(
        llm = llm,
        prompt = prompt,
        memory = memory,
        input_key = "question"
    )
    return memory, conversation

def findSQL(answer):
    pattern = r"sql\n(.*?);"
    match = re.search(pattern, answer, re.DOTALL)
    
    if match:
        sql_query = match.group(1)
        return sql_query
    else:
        return -1
        
db, db_info, db_table_name = callDatabase()
prompt = makeTemplate()
prompt.partial(chat_history="쿼리 작성 방법에 대해 알려주세요.")
memory, conversation = callLLM()
input_question = input()
answer = conversation.predict(question = "데이터베이스 정보는 다음과 같습니다. " +
                              db_info + " 테이블명은 다음과 같습니다. " + str(db_table_name) + 
                              " 해당 데이터베이스를 바탕으로 사용자의 질문은 다음과 같습니다. " + input_question)

sql_query = findSQL(answer)

# 결과 출력
print("***설명\n" + answer)
print("***쿼리문\n" + sql_query)
print("***실행 결과\n")
if sql_query != -1:
    print(db.run(sql_query))
else:
    print("No SQL query found.")
    
# print(memory.buffer)
