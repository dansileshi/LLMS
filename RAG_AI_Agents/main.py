from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from pdf import UK_engine


load_dotenv()

population_df = pd.read_csv(os.path.join('data','Worldpopulation2023.csv'))

#print(population_df.head())

population_query_engine = PandasQueryEngine(df=population_df, 
                                            verbose=True,
                                            instruction_str = instruction_str
                                            )
population_query_engine.update_prompts({"pandas_prompt": new_prompt})
population_query_engine.query("what is the population of the united kingdom")

tools = [
    note_engine,
    QueryEngineTool(
        query_engine = population_query_engine,
        metadata = ToolMetadata(
            name = "population_data",
            description = "this gives infaotmion at the world population and demographics",
        ),
    ),

    QueryEngineTool(
        query_engine = UK_engine,
        metadata = ToolMetadata(
            name = "UK_data",
            description = "this gives infaotmion at the UK",
        ),
    ),
]


llm = OpenAI(model = "gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm = llm, verbose =True, context = context)

while ( prompt := input("Enter a prompt (q to quit): ")) != "q":    
    result = agent.query(prompt)
    print(result)

       