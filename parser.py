import networkx
import obonet
import os

def load_data(data_folder):
    graph = obonet.read_obo(os.path.join(data_folder, 'go.obo'))

    IGNORE_FIELDS = ['is_a'] # captured in parent field already

    for node in graph.nodes(data=True):
        parents = list(graph.predecessors(node[0]))
        children = list(graph.successors(node[0]))
        ancestors = list(networkx.ancestors(graph, node[0]))
        descendants = list(networkx.descendants(graph, node[0]))

        n = {
            '_id': node[0],
            'parents': parents, # predecessors/successors mean the opposite in networkx
            'children': children,
            'ancestors': ancestors, # networkx ancestors/descendants are opposite as well
            'descendants': descendants,
            'num_parents': len(parents),
            'num_children': len(children),
            'num_ancestors': len(ancestors),
            'num_descendants': len(descendants),
            **{k: v for k, v in node[1].items() if k not in IGNORE_FIELDS} # unpack fields like name, def, comment, synonym, xref, etc.
        }

        yield n
