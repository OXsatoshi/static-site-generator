from textnode import TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
  
    result = []
    for node in old_nodes:
        number_of_delimiter = len([ch for ch in node.text if ch == delimiter])
        if number_of_delimiter %2 != 0:
            raise Exception("delimiter doesnt mutch")
        node_text_list = node.text.split(delimiter)
        i = 0
        while i < len(node_text_list):
            if i %2 == 0:
                result.append(TextNode(node_text_list[i],node.text_type))
            else:
                result.append(TextNode(node_text_list[i],text_type))
            i+=1
    return result
