import streamlit as st
import PyPDF2
import plotly.graph_objects as go
import numpy as np
import re
import pandas as pd
import bs4
import requests
import spacy
from spacy import displacy
import re
import xlrd
import csv
import PyPDF2
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher
from spacy.tokens import Span
from string import punctuation

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk import tokenize
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize, pos_tag

from collections import Counter
import math

import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable not set.")

openai.api_key = api_key

pd.set_option('display.max_colwidth', 200)
st.set_page_config(layout="wide", page_title="ER info")


candidate_sentences = []

def clean_lines(i):
    clean_line = i.replace("\n", "")
    clean_line = clean_line.replace(" -", "")
    clean_line = clean_line.lstrip()
    
    return clean_line

def read_pdf_lines(file, page_number):
    reader = PyPDF2.PdfReader(file)
    page = reader.pages[page_number]
    text = page.extract_text()
    if text:
        lines = re.split('[.!?]', text)
        print(f"Page {page_number + 1}:")   
        
        lines = interpret_command_with_chatgpt(lines)

        i = 0
        for line in lines:
            i+=1
            new_line = clean_lines(line)
            candidate_sentences.append(new_line)

def interpret_command_with_chatgpt(sentences):
    try:
        prompt_text = f"""I have extracted text from a PDF document which includes some sentences that seem incoherent or appear to be part of the header, page number, page title, or image descriptions. 
        This is a list of sentences {sentences} from the document. Please review each sentence and remove any that do not form a coherent part of the main text. 
        Return only the coherent and relevant sentences, as bullet points (-)
        """        
        # Call to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )

        cleaned_text = response['choices'][0]['message']['content'].strip()
        cleaned_sentences = []
        for line in cleaned_text.split('\n'):
            if line.startswith('- '):  # Check if the line is a main bullet point
                cleaned_sentences.append(line[2:].strip())
        return cleaned_sentences
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_entities(sent):
    nlp = spacy.load("en_core_web_sm")
    ent1 = ""
    ent2 = ""

    prv_tok_dep = ""    # Dependency tag of the previous token in the sentence
    prv_tok_text = ""   # Previous token in the sentence

    prefix = ""
    modifier = ""

    adjectives = []  
    adverbs = []
    numbers = []  

    for tok in nlp(sent):
        if tok.dep_ != "punct":
            # Handling compound nouns
            if tok.dep_ == "compound":
                prefix = tok.text if not prefix else prefix + " " + tok.text

            if tok.dep_.endswith("mod"):  # Includes 'amod' (adjectival modifier)
                modifier = tok.text if not modifier else modifier + " " + tok.text

            if tok.pos_ == "ADV":
                adverbs.append(tok.text)
                
            if tok.pos_ == 'NUM':
                numbers.append(tok.text)

            if "subj" in tok.dep_:
                ent1 = f"{modifier} {prefix} {tok.text}".strip()
                adjectives.append(modifier)
                prefix, modifier = "", ""

            if "obj" in tok.dep_:
                ent2 = f"{modifier} {prefix} {tok.text}".strip()
                prefix, modifier = "", ""

        # Update the previous token variables
        prv_tok_dep, prv_tok_text = tok.dep_, tok.text

    return {
        'Entity1': ent1,
        'Entity2': ent2,
        'Adjectives': adjectives,
        'Adverbs': adverbs,
        'Numbers': numbers
    }
    
def get_relation(sent):
    doc = nlp(sent)

    matcher = Matcher(nlp.vocab)

    pattern = [
        {'DEP': 'ROOT'},  
        {'DEP': 'prep', 'OP': "?"},
        {'DEP': 'agent', 'OP': "?"}, 
        {'POS': 'ADJ', 'OP': "?"}, 
        {'POS': 'ADV', 'OP': "*"},  
        {'DEP': 'amod', 'OP': "?"}, 
        {'DEP': 'acl', 'OP': "?"},  
        {'DEP': 'attr', 'OP': "?"}
    ]

    matcher.add("matching_1", [pattern])

    matches = matcher(doc)
    
    if matches:
        k = len(matches) - 1
        span = doc[matches[k][1]:matches[k][2]]
        return span.text
    else:
        return "No relation found"

def process_entity_relations(entity_pairs_with_attrs, relations):
    # Clean up empty entities and the corresponding relations
    cleaned_pairs = []
    cleaned_relations = []
    for pair, rel in zip(entity_pairs_with_attrs, relations):
        if pair['Entity1'] and pair['Entity2']:  # Ensure no empty entities
            cleaned_pairs.append(pair)
            cleaned_relations.append(rel)

    # Prepare data for the knowledge graph
    er_info = []
    for pair, rel in zip(cleaned_pairs, cleaned_relations):
        er_dict = {
            "entity1": pair['Entity1'],
            "entity2": pair['Entity2'],
            "relation": rel,
            "adjectives_entity1": pair['Adjectives'],
            "adverbs": pair['Adverbs'],  # Assuming adverbs relate to the action/link
            "numbers": pair['Numbers']
        }

        # Use NLTK to determine the grammatical number of entities
        first_ent = nltk.pos_tag([pair['Entity1'].split()[-1]])  # Get last word of entity1 for tagging
        second_ent = nltk.pos_tag([pair['Entity2'].split()[-1]])  # Get last word of entity2 for tagging

        # Classifying the relation type based on the grammatical number
        if first_ent[0][1].startswith("NN") and second_ent[0][1].startswith("NN"):
            er_dict["relation type"] = "one-one"
        elif first_ent[0][1].startswith("NN") and second_ent[0][1].startswith("NNS"):
            er_dict["relation type"] = "one-many"
        elif first_ent[0][1].startswith("NNS") and second_ent[0][1].startswith("NN"):
            er_dict["relation type"] = "many-one"
        elif first_ent[0][1].startswith("NNS") and second_ent[0][1].startswith("NNS"):
            er_dict["relation type"] = "many-many"
        else:
            er_dict["relation type"] = "undefined"

        er_info.append(er_dict)

    return er_info

def generate_file_content(er_info):
    content = "SNO, Entity1, Entity2, Relation, Relation Type\n"
    for i in range(len(er_info)):
        content += f"{i+1}, {er_info[i]['entity1']}, {er_info[i]['entity2']}, {er_info[i]['relation']}, {er_info[i]['relation type']}\n"
    return content

def draw_network_graph(kg_df):
    G = nx.from_pandas_edgelist(kg_df, "source", "target",
                                edge_attr=True, create_using=nx.MultiDiGraph())

    plt.figure(figsize=(20,20))
    pos = nx.spring_layout(G)  
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=2000)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=10)
    nx.draw_networkx_labels(G, pos)
    edge_labels = {(u, v): f"{d['edge']} | Adj: {', '.join(d['adjectives'])} | Adv: {', '.join(d['adverbs'])} | Num: {', '.join(d['numbers'])}"
                    for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')  # Turn off the axis
    return plt

# Streamlit app
def main():
    st.title("PDF Reader and Knowledge Graph Visualizer")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        
        reader = PyPDF2.PdfReader(uploaded_file)
        number_of_pages = len(reader.pages)

        page_number = st.number_input("Select a Page", min_value=1, max_value=number_of_pages, value=1)
        
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        if col3.button('Generate Knowledge Graph'):
            my_msg = st.empty()
            my_msg.info("Reading File and Processing Text 🧐")
            read_pdf_lines(uploaded_file, page_number-1)
            entity_pairs = []
            my_msg.info("Finding entity pairs")
            for i in candidate_sentences:
                entity_pairs.append(get_entities(i))
            my_msg.info("Finding relations")    
            relations = [get_relation(i) for i in candidate_sentences]
            my_msg.info("Finding entity relations")
            er_info = process_entity_relations(entity_pairs, relations)

            col_1, col_2, col_3, col_4, col_5 = st.columns([1,1,1,1,1])
            if col_3.button('Download E-R Info'):
                file_content = generate_file_content(er_info)
                col_3.download_button(
                    label="Download Data as CSV",
                    data=file_content,
                    file_name='entity_relation_info.csv',
                    mime='text/csv',
                )
                
            ep = entity_pairs.copy()
            source = [item['Entity1'] for item in ep if item['Entity1'] and item['Entity2']]
            target = [item['Entity2'] for item in ep if item['Entity1'] and item['Entity2']]
            filtered_relations = [relations[i] for i in range(len(ep)) if ep[i]['Entity1'] and ep[i]['Entity2']]
            adjectives = [item.get('Adjectives', []) for item in ep if item['Entity1'] and item['Entity2']]
            adverbs = [item.get('Adverbs', []) for item in ep if item['Entity1'] and item['Entity2']]
            numbers = [item.get('Numbers', []) for item in ep if item['Entity1'] and item['Entity2']]

            kg_df = pd.DataFrame({
                'source': source,
                'target': target,
                'edge': filtered_relations,
                'adjectives': adjectives,
                'adverbs': adverbs,
                'numbers': numbers,
            })
            my_msg.success("Done ✅ ")
            plt = draw_network_graph(kg_df)
            st.pyplot(plt)
            plt.clf()
            

if __name__ == "__main__":
    main()
