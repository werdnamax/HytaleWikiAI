import re
import json
from cleaner import genSemantics

genSemantics()

with open('data/semantics/cleaned_content.json', 'r') as f:
    content = json.load(f)

max_chunk_size = 2048
overlap = 512

i = 0
def Rcharsplit(text, patterns = ['\n\n', '\n', ' ', '']):
    if len(text) <= max_chunk_size:
        return [text]
    
    if not patterns:
        return [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    
    res = []
    pattern = patterns[0]

    splits = text.split(pattern)
    current_chunk = ''

    for split in splits:

        if len(current_chunk) + len(split) + len(pattern) <= max_chunk_size:
            if current_chunk:
                res.append(current_chunk)

            if len(split) > max_chunk_size:
                res.extend(Rcharsplit(split, patterns[1:]))
            else:
                current_chunk = split
        else:
            current_chunk += (pattern if current_chunk else '') + split
        
    if current_chunk:
        res.append(current_chunk)

    return res
        

        
def genChunks():
    links = []
    for item in content:
        block = {
            "text": Rcharsplit(item['content']),
            "source": item['url'],
            "title": item['url'].split('/')[-1].replace('_', ' ')
        }
        links.append(block)
    
    with open('data/chunks/chunks.json', 'w') as f:
        json.dump(links, f, indent=4)
    
genChunks()