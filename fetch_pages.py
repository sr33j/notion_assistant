
## Pull documents with Notion api

import requests
from dotenv import load_dotenv
import os
import csv

from notion_client import Client
load_dotenv()

from embed import get_embeddings_from_page
from time import time

# Assuming you have NOTION_API_KEY in your environment variables
notion_api_key = os.getenv('NOTION_API_KEY')

# # Load environment variables
# page_id = parent_page_ids['Tasks']
api_key = os.getenv("NOTION_API_KEY")

# Initialize the client
notion = Client(auth=api_key)


def fetch_all_page_ids():
    url = 'https://api.notion.com/v1/search'
    headers = {
        'Authorization': f'Bearer {notion_api_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    data = {
        "filter": {
            "value": "page",
            "property": "object"
        },
        "sort": {
            "direction": "ascending",
            "timestamp": "last_edited_time"
        }
    }
    page_ids = []
    has_more = True
    start_cursor = None

    while has_more:
        if start_cursor:
            data['start_cursor'] = start_cursor
        
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()

        # Extracting the page IDs from the response
        page_ids.extend([result['id'] for result in response_json.get('results', []) if result['object'] == 'page'])
        
        # Check if there are more pages to fetch
        has_more = response_json.get('has_more', False)
        start_cursor = response_json.get('next_cursor', None)

    return page_ids

# Function to get plain text from rich text
def get_plain_text_from_rich_text(rich_text):
    return "".join(t["plain_text"] for t in rich_text)

# Function to get media source text
def get_media_source_text(block):
    block_type = block.get(block["type"])
    source = None
    caption = ""

    if block_type.get("external"):
        source = block_type["external"]["url"]
    elif block_type.get("file"):
        source = block_type["file"]["url"]
    elif block_type.get("url"):
        source = block_type["url"]
    else:
        source = "[Missing case for media block types]: " + block["type"]

    if block_type.get("caption"):
        caption = get_plain_text_from_rich_text(block_type["caption"])
        return f"{caption}: {source}"

    return source

# Function to get text from any block type
def get_text_from_block(block):
    text = ""
    block_type = block.get(block["type"])

    if block_type.get("rich_text"):
        text = get_plain_text_from_rich_text(block_type["rich_text"])
    else:
        match block["type"]:
            case "unsupported":
                text = "[Unsupported block type]"
            case "bookmark":
                text = block["bookmark"]["url"]
            case "child_database":
                text = block["child_database"]["title"]
            case "child_page":
                text = block["child_page"]["title"]
                # text += "\n" + get_text_from_page(block["id"])
            case "embed" | "video" | "file" | "image" | "pdf":
                text = get_media_source_text(block)
            case "equation":
                text = block["equation"]["expression"]
            case "link_preview":
                text = block["link_preview"]["url"]
            case "synced_block":
                text = ("This block is synced with a block with the following ID: " +
                        block["synced_block"]["synced_from"][block["synced_block"]["synced_from"]["type"]]
                        if block["synced_block"].get("synced_from") else
                        "Source sync block that another blocked is synced with.")
            case "table":
                text = "Table width: " + str(block["table"]["table_width"])
            case "table_of_contents":
                text = "ToC color: " + block["table_of_contents"]["color"]
            case "breadcrumb" | "column_list" | "divider":
                text = "No text available"
            case _:
                # text = "[Needs case added]"
                text = ""

    return f"{text}"

# Function to retrieve block children
def retrieve_block_children(id):
    print("Retrieving blocks (async)...")
    blocks = []

    # Paginate through all blocks in the page
    block_children = notion.blocks.children.list(block_id=id)
    while block_children:
        blocks.extend(block_children["results"])
        if block_children.get("has_more"):
            start_cursor = block_children.get("next_cursor")
            block_children = notion.blocks.children.list(block_id=id, start_cursor=start_cursor)
        else:
            break

    return blocks

# Function to print block text
def get_text_from_page(page_id):
    print("Displaying blocks:")
    blocks = retrieve_block_children(page_id)
    full_text = ""
    for block in blocks:
        text = get_text_from_block(block)
        full_text += text + "\n"
    return full_text
        

# Main function
def main():
    START = time()
    page_ids = fetch_all_page_ids()
    data = []
    count = 0
    for page_id in page_ids:
        print("PAGES EMBEDDED:", count, "out of ", len(page_ids))
        page_text = get_text_from_page(page_id)
        embeddings = get_embeddings_from_page(page_text)
        data.extend(embeddings)
        count += 1
    print(time()-START, "seconds to finish embedding")
    
    # Writing to the CSV file
    csv_file = 'notion_embeddings.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['Embedding', 'Page Text'])
        
        # Write the data
        for embedding, page_text in data:
            # Convert the embedding to a string if it's not already one
            embedding_str = ','.join(map(str, embedding)) if isinstance(embedding, (list, tuple)) else str(embedding)
            writer.writerow([embedding_str, page_text])
    
    print(time()-START, "seconds to finish writing")


# Execute the main function
if __name__ == "__main__":
    main()
