from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import json
import ast
import click

load_dotenv(verbose=True, override=True)
del load_dotenv

@click.command()
@click.option("--num-iterations", '-i', default=1, help="Number of iterations to run")
def main(num_iterations: int):
    graph = Neo4jGraph(
        url="bolt://localhost:7687", 
        username="neo4j", 
        password="pleaseletmein"
    )

    try:
        chain = GraphCypherQAChain.from_llm(ChatOpenAI(temperature=0), graph=graph, verbose=True)
    except Exception as e:
        raise  ValueError(f"Failed to initialize chain: {e}")
    
    for _ in range(num_iterations):
        try:
            graph.refresh_schema()
        except Exception as e:
            print(f"Failed to refresh schema: {e}")
            continue
        
        try:
            synth_prompt = "Imagin a random dish. Describe the ingredients used, the cooking process, the taste of each ingredient, and the overall flavor of the dish."
            synth_llm = OpenAI(temperature=0.7, verbose=True)
            synth_result = synth_llm.predict(synth_prompt)
            print(synth_result)
        except Exception as e:
            print(f"Failed to synthesize prompt: {e}")
            continue
        
        try:
            preprocess_instruction = f"List all the relational information that can be gleaned from the given text:\n{synth_result}"
            preprocess_llm = OpenAI(temperature=0.7, verbose=True)
            preprocess_result = preprocess_llm.predict(preprocess_instruction)
            print(preprocess_result)
        except Exception as e:
            print(f"Failed to preprocess prompt: {e}")
            continue
        
        try:
            knowledge_graph_parsing_instruction = f"Divide and list all the information that can be gleaned from the given data into units suitable for storage in a graph database:\n{preprocess_result}"
            kg_llm = OpenAI(temperature=0.7, verbose=True)
            kg_result = kg_llm.predict(knowledge_graph_parsing_instruction)
            print(kg_result)
        except Exception as e:
            print(f"Failed to parse prompt: {e}")
            continue

        try:
            kg_meta_node_labels = chain.run(f"Summarize the node labels")
            # kg_meta_edge_labels = chain.run(f"Summarize the edge labels")
            print(kg_meta_node_labels)
            # print(kg_meta_edge_labels)
        except Exception as e:
            print(f"Failed to summarize prompt: {e}")
            continue
        
        try:
            graph_data_update_prompt = f"""
Node labels:\n{kg_meta_node_labels}\n
Instruction:\nSave the contents into the database (output format: Neo4j Query)\n
Contents:\n{kg_result}
"""
            # chain.run(f"Save the contents into the database:\n{kg_result}")
            chain.run(graph_data_update_prompt)
        except Exception as e:
            print(f"Failed to update graph: {e}")
        
        try:
            # test
            graph_data_update_prompt = f"""
Node labels:\n{kg_meta_node_labels}\n
Instruction:\nSave the contents into the database (output format: Neo4j Query)\n
Contents:\n{preprocess_result}
"""
            chain.run(graph_data_update_prompt)
        except Exception as e:
            print(f"Failed to update graph: {e}")


if __name__ == "__main__":
    main()