"""
General drawing methods for graphs using Bokeh.
"""
import math
from random import sample
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet,
                          ColumnDataSource)
from bokeh.palettes import Category20


class BokehGraph:
    def __init__(self, graph, cc, connected):
        self.graph = graph
        self.cc = cc
        self.connected = connected

    def draw(self):
        graph = self.graph
        cc = self.cc

        N = len( graph.vertices )
        n = len( cc )

        if self.connected == False:
            graph_colors = sample(Category20[20], N)
        else:
            colors_dict = {}
            colors = list(sample(Category20[20], n))
            for arr in cc:
                color = colors.pop()
                for num in arr:
                    colors_dict[num] = color
            graph_colors = []
            for i in range(N):
                graph_colors.append(colors_dict[i])
                
            print(f"\nConnected Components: {cc}")

        node_indices = list(graph.vertices.keys())

        plot = figure(title="Bokeh Graph", x_range=(-12,12), y_range=(-12,12),
                      tools="", toolbar_location=None)

        graph_renderer = GraphRenderer()
        
        graph_renderer.node_renderer.data_source.add(node_indices, 'index')
        graph_renderer.node_renderer.data_source.add(graph_colors, 'color')
        graph_renderer.node_renderer.glyph = Circle(radius=0.4, fill_color="color")

        edge_start = []
        edge_end = []

        for vertex_id in node_indices:
            for v in graph.vertices[vertex_id].edges:
                edge_start.append(vertex_id)
                edge_end.append(v)

        graph_renderer.edge_renderer.data_source.data = dict(
            start=edge_start,
            end=edge_end)

        ### start of layout code
        x = []
        y = []
        for vertex_id in node_indices:
            vertex = graph.vertices[vertex_id]
            x.append(vertex.x)
            y.append(vertex.y)

        graph_layout = dict(zip(node_indices, zip(x, y)))
        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot.renderers.append(graph_renderer)

        labelSource = ColumnDataSource(data=dict(x=x, y=y, names=[vertex_id for vertex_id in graph.vertices]))
        labels = LabelSet(x='x', y='y', text='names', level='glyph',
                     text_align='center', text_baseline='middle', source=labelSource, render_mode='canvas')


        plot.add_layout(labels)

        output_file('graph.html')
        show(plot)