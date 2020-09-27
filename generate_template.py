""""
@author: William Richard
@email: oantawilliam@gmail.com
"""
class TemplateTree(object):
    """
    A general node, which is used for building the entire tree structure based
    on the provided template data.
    """
    def __init__(self, id, parent=None):
        self.id = id
        self.parent = parent
        self.contents = []
        self.children = []
        self.children_ids = []
        self.all_nodes = {}

    def __repr__(self):
        return self.id

    """
    Adding parent to a node.
    """
    def add_parent(self, parent):
        try:
            assert isinstance(parent, TemplateTree)
            self.parent = parent
        except AssertionError as error:
            print(error)
            print("The added child is not a TemplateTree type.")
            exit(1)

    """
    Adding a word to a node.
    """
    def add_word(self, content):
        try:
            assert isinstance(content, str)
            self.contents.append(content)
        except AssertionError as error:
            print(error)
            print("The added content is not a string type.")
            exit(1)

    """
    Adding a child to a node.
    """
    def add_child(self, node):
        try:
            assert isinstance(node, TemplateTree)
            self.children.append(node)
            self.children_ids.append(node.id)
        except AssertionError as error:
            print(error)
            print("The added child is not a TemplateTree type.")
            exit(1)

class TemplateTreeBuilder(object):

    """
    Builder is used for generating the TemplateTree from the template data.
    """

    def __init__(self):
        self.tree = None
        self.GROUP_ID = "group_id"
        self.CONTENT = "content"
        self.CHILDREN = "children"
        self.ROOT_INDEX = 0

    """Sets root node of the tree. """
    def set_root_node(self, root_group):
        root_id = root_group[self.GROUP_ID]
        self.tree = TemplateTree(root_id)

        # Add node to root node for easy future retrieval
        self.tree.all_nodes[root_id] = self.tree

        if self.CONTENT in root_group:
            self.tree.contents.append(root_group[self.CONTENT])

    """Adds a child to a node."""
    def add_child(self, parent, child):
        if child.id not in parent.children_ids:
            parent.add_child(child)
        return parent

    """Retrieves previous node if same id, else creates a new node. """
    def get_current_node(self, current_group_id, previous_node, current_parent):
        if current_group_id == previous_node.id:
            # If node already created, we update contents.
            current_node = previous_node
        else:
            current_node = TemplateTree(current_group_id, current_parent)
            # Add node to root node for easy future retrieval

        return current_node

    """Updates current node content or children."""
    def update_node(self, current_node, current_group, current_parent):

        # Update contents
        if self.CONTENT in current_group:
            current_node.contents.append(current_group[self.CONTENT])
            self.add_child(current_parent, current_node)

        # Update children
        elif self.CHILDREN in current_group:
            self.add_child(current_parent, current_node)
            current_parent = current_node

        return current_node, current_parent

    """Core method that builds the entire tree from template data."""
    def build_tree(self, template_data):

        # Set root of the tree
        self.set_root_node(template_data[self.ROOT_INDEX])

        # Construct the remaining nodes
        current_parent = self.tree
        previous_node = self.tree

        for index in range(self.ROOT_INDEX + 1, len(template_data)):

            # Get current item in template
            current_group = template_data[index]
            current_group_id = current_group[self.GROUP_ID]

            # Get current node
            current_node = self.get_current_node(current_group_id, previous_node, current_parent)

            # Update current node
            current_node, current_parent = self.update_node(current_node, current_group, current_parent)

            # Add node to root node for easy future retrieval
            self.tree.all_nodes[current_group_id] = current_node

            previous_node = current_node

        return self.tree

class TemplateGenerator(object):
    """Generats a sentence or word template from the built TemplateTree."""
    def __init__(self, id, tree):
        # Id given for starting position.
        self.id = id
        self.tree = tree
        # Threshold used for choosing random item.
        self.THRESHOLD = 0.5
        self.DOT = "."

    """Main method that is called for generating the template."""
    def generate_template(self):

        # Get starting node
        starting_node = self.tree.all_nodes[self.id]
        generated_text = self.process_node(starting_node)

        return generated_text.strip() + self.DOT

    """Recursive method used to parse and construct the sentence."""
    def process_node(self, node):

        import random

        text = ""
        # When only content exists
        if node.contents and not node.children:
            text += " " + random.choice(node.contents)

        # When only children exists
        elif node.children and not node.contents:
            for child_node in node.children:
                text += self.process_node(child_node)

        # When children and contents exist
        elif node.contents and node.children:

            if random.random() < self.THRESHOLD:
                text += " " + random.choice(node.contents)
            else:
                for child_node in node.children:
                    text += self.process_node(child_node)

        return text

def generate_template(group_id, template_data):

    # Build tree.
    builder = TemplateTreeBuilder()
    tree = builder.build_tree(template_data)

    # Generate sequence from tree.
    generator = TemplateGenerator(group_id, tree)
    text = generator.generate_template()

    return text

if __name__ == '__main__':
    template_data = [
        {
            "group_id": 154,
            "children": [234, 124, 36]
        },
        {
            "group_id": 234,
            "content": "I"
        },
        {
            "group_id": 234,
            "content": "You"
        },
        {
            "group_id": 234,
            "content": "We"
        },
        {
            "group_id": 124,
            "content": "like to"
        },
        {
            "group_id": 124,
            "content": "sometimes"
        },
        {
            "group_id": 36,
            "content": "jog"
        },
        {
            "group_id": 36,
            "children": [46, 242]
        },
        {
            "group_id": 46,
            "content": "eat"
        },
        {
            "group_id": 242,
            "content": "sandwiches"
        },
        {
            "group_id": 242,
            "content": "eggs"
        }
    ]

    group_id = 154

    text = generate_template(group_id, template_data)
    print(text)




