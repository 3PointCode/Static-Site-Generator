def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []

    for block in blocks:
        if block == "":
            continue
        
        clean_blocks.append(block.strip())

    return clean_blocks 